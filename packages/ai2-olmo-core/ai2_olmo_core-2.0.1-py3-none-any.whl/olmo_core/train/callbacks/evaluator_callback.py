import logging
import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, List, Optional

import torch
import torch.distributed as dist
from torch.utils.data import DataLoader, DistributedSampler

from olmo_core.data import (
    NumpyDatasetConfig,
    NumpyPaddedFSLDataset,
    TextDataLoaderBase,
    TokenizerConfig,
)
from olmo_core.data.utils import get_labels
from olmo_core.distributed.utils import get_rank, get_world_size, is_distributed
from olmo_core.eval import Evaluator
from olmo_core.eval.lm_evaluator import LMEvaluator
from olmo_core.exceptions import OLMoConfigurationError
from olmo_core.nn.lm_head import LMOutputWithLoss
from olmo_core.utils import (
    cuda_sync_debug_mode,
    format_float,
    get_default_device,
    move_to_device,
)

from ..common import Duration
from ..train_module import EvalBatchSizeUnit, EvalBatchSpec, TransformerTrainModule
from .callback import Callback, CallbackConfig

if TYPE_CHECKING:
    from olmo_eval import HFTokenizer

    from ..trainer import Trainer

log = logging.getLogger(__name__)


@dataclass
class EvaluatorCallback(Callback):
    """
    Runs in-loop evaluations for a :class:`~olmo_core.train.train_module.TransformerTrainModule`
    periodically during training.
    """

    evaluators: List[Evaluator] = field(default_factory=list)
    """
    The evaluators to run.
    """

    eval_interval: int = 1000
    """
    The interval (in steps) with which to run the evaluators.
    """

    eval_duration: Duration = field(default_factory=lambda: Duration.epochs(1))
    """
    The duration to run each evaluator for.
    """

    log_interval: int = 5
    """
    How often to log eval progress to the console during an eval loop.
    """

    def post_attach(self):
        if not isinstance(self.trainer.train_module, TransformerTrainModule):
            raise OLMoConfigurationError(
                f"'{self.__class__.__name__}' only suports the '{TransformerTrainModule.__name__}' train module"
            )

    def post_step(self):
        if self.step <= 1 or self.step % self.eval_interval != 0:
            return

        # Put model in eval train mode.
        # TODO: make sure grads will be zeroed at this point
        #  self.trainer.optim.zero_grad(set_to_none=True)
        #  self.trainer.model.eval()
        dp_world_size = get_world_size(self.trainer.dp_process_group)

        evaluator_times = []
        evaluator_names = []
        evaluator_bs = []

        for evaluator in self.evaluators:
            log.info(f"Running {evaluator.name} evals...")
            start_time = time.monotonic()
            evaluator.reset_metrics()
            eval_step = 0
            eval_tokens = 0
            for batch in evaluator:
                eval_step += 1
                eval_tokens += batch["input_ids"].numel() * dp_world_size

                batch = move_to_device(batch, get_default_device())
                with torch.no_grad():
                    # Run forward pass, get logits and un-reduced CE loss.
                    labels = get_labels(batch)
                    output = self.trainer.train_module.eval_batch(batch, labels=labels)
                    assert isinstance(output, LMOutputWithLoss)
                    logits, ce_loss, _ = output

                    # NOTE: might have host-device syncs here but that's okay.
                    with cuda_sync_debug_mode(0):
                        evaluator.update_metrics(batch, ce_loss, logits)

                if eval_step % self.trainer.cancel_check_interval == 0:
                    self.trainer.check_if_canceled()

                if self.trainer.is_canceled:
                    self._log_progress(evaluator, eval_step)
                    return
                elif self.eval_duration.due(step=eval_step, tokens=eval_tokens, epoch=1):
                    self._log_progress(evaluator, eval_step)
                    break
                elif eval_step % self.log_interval == 0 or eval_step == evaluator.total_batches:
                    self._log_progress(evaluator, eval_step)

            # NOTE: going to have a host-device sync here but that's okay. It's only once
            # per evaluator.
            metrics_str = []
            evaluation_names = []
            with cuda_sync_debug_mode(0):
                metrics = evaluator.compute_metrics()
                for name, value in metrics.items():
                    evaluation_names.append(name)
                    metrics_str.append(f"    {name}={format_float(value.item())}")
                    self.trainer.record_metric(f"eval/{evaluator.name}/{name}", value)

            evaluator_times.append(time.monotonic() - start_time)
            evaluator_names.append(evaluation_names)
            evaluator_bs.append(evaluator.total_batches)

            log.info(
                f"Finished {evaluator.name} evals in {time.monotonic() - start_time:.1f} seconds. Metrics:\n"
                + "\n".join(metrics_str)
            )

        # Sort by evaluator_times in ascending order
        sorted_evaluators = sorted(
            zip(evaluator_names, evaluator_bs, evaluator_times), key=lambda x: x[2]
        )

        # Record evaluation speed
        log.info("Evaluation speed:")
        max_time_width = max(len(f"{t:.1f}") for t in evaluator_times)
        max_batch_width = max(len(str(bs)) for bs in evaluator_bs)
        for names, bs, t in sorted_evaluators:
            name = names[0]  # only use the name of the first metric for each downstream task
            log.info(
                f"    {t:>{max_time_width}.1f} sec ({bs:>{max_batch_width}} batches): {name} (+ variants)"
            )
        total_time = sum(evaluator_times)
        total_bs = sum(int(bs) if bs is not None else 0 for bs in evaluator_bs)
        log.info(f"    Total evaluation time: {total_time:.1f} seconds ({total_bs} batches)")

        self.trainer.record_metric("throughput/in-loop eval time (s)", total_time)
        self.trainer.record_metric("throughput/in-loop eval batches", total_bs)

    def _log_progress(self, evaluator: Evaluator, eval_step: int):
        if evaluator.total_batches is not None:
            log.info(f"[eval={evaluator.name},step={eval_step}/{evaluator.total_batches}]")
        else:
            log.info(f"[eval={evaluator.name},step={eval_step}]")


@dataclass
class LMEvaluatorCallbackConfig(CallbackConfig):
    eval_dataset: NumpyDatasetConfig
    eval_interval: int = 1000
    eval_duration: Duration = field(default_factory=lambda: Duration.epochs(1))
    log_interval: int = 5
    enabled: bool = True

    def build(self, trainer: "Trainer") -> Optional[Callback]:
        if not self.enabled:
            return None

        batch_spec = trainer.train_module.eval_batch_spec
        if (
            batch_spec.max_sequence_length is not None
            and self.eval_dataset.effective_sequence_length > batch_spec.max_sequence_length
        ):
            raise OLMoConfigurationError(
                f"The maximum sequence length for the LM eval dataset ({self.eval_dataset.effective_sequence_length:,d} tokens) "
                f"is too long for the train module's maximum eval sequence length ({batch_spec.max_sequence_length:,d} tokens)"
            )

        global_eval_batch_size: int
        if batch_spec.batch_size_unit == EvalBatchSizeUnit.tokens:
            global_eval_batch_size = batch_spec.rank_batch_size * get_world_size(
                trainer.dp_process_group
            )
        elif batch_spec.batch_size_unit == EvalBatchSizeUnit.instances:
            global_eval_batch_size = (
                batch_spec.rank_batch_size
                * self.eval_dataset.effective_sequence_length
                * get_world_size(trainer.dp_process_group)
            )
        else:
            raise NotImplementedError(batch_spec.batch_size_unit)

        dataset = self.eval_dataset.build()
        if not isinstance(dataset, NumpyPaddedFSLDataset):
            raise OLMoConfigurationError(
                f"Expected a padded FSL dataset, got '{dataset.__class__.__name__}' instead"
            )

        if not isinstance(trainer.data_loader, TextDataLoaderBase):
            raise OLMoConfigurationError(
                f"Expected a text-based data loader, got '{dataset.__class__.__name__}' instead"
            )

        evaluator = LMEvaluator.from_numpy_dataset(
            dataset,
            name="lm",
            global_batch_size=global_eval_batch_size,
            collator=trainer.data_loader.collator,
            device=trainer.device,
            dp_process_group=trainer.dp_process_group,
        )
        return EvaluatorCallback(
            evaluators=[evaluator],
            eval_interval=self.eval_interval,
            log_interval=self.log_interval,
            eval_duration=self.eval_duration,
        )


class DownstreamEvaluator(Evaluator):
    metric_type_to_label = {
        "f1": "F1 score",
        "acc": "accuracy",
        "len_norm": "length-normalized accuracy",
        "pmi_dc": "PMI-DC accuracy",
        "ce_loss": "CE loss",
        "bpb": "BPB",
        "soft": "soft loss",
        "soft_log": "log soft loss",
    }

    def __init__(
        self,
        *,
        name: str,
        task: str,
        batch_spec: EvalBatchSpec,
        tokenizer: "HFTokenizer",
        device: Optional[torch.device] = None,
        dp_process_group: Optional[dist.ProcessGroup] = None,
    ):
        from olmo_eval import ICLMetric, ICLMultiChoiceTaskDataset, build_task

        task_dataset: ICLMultiChoiceTaskDataset
        if batch_spec.fixed_sequence_length:
            assert batch_spec.max_sequence_length is not None
            task_dataset = build_task(
                task, tokenizer, model_ctx_len=batch_spec.max_sequence_length, fixed_ctx_len=True
            )
        elif batch_spec.max_sequence_length is not None:
            task_dataset = build_task(task, tokenizer, model_ctx_len=batch_spec.max_sequence_length)
        else:
            task_dataset = build_task(task, tokenizer)

        self.label = task
        self.task = task_dataset
        self.metric = ICLMetric(metric_type=self.task.metric_type).to(
            device or get_default_device()
        )
        sampler: Optional[DistributedSampler] = None
        if is_distributed():
            sampler = DistributedSampler(
                self.task,  # type: ignore
                drop_last=False,
                shuffle=False,
                num_replicas=get_world_size(dp_process_group),
                rank=get_rank(dp_process_group),
            )

        if (
            batch_spec.max_sequence_length is not None
            and self.task.max_sequence_length > batch_spec.max_sequence_length
        ):
            raise OLMoConfigurationError(
                f"The maximum sequence length for downstream eval task '{task}' ({self.task.max_sequence_length:,d} tokens) "
                f"is too long for the train module's maximum eval sequence length ({batch_spec.max_sequence_length:,d} tokens)"
            )

        rank_batch_size_instances: int
        if batch_spec.batch_size_unit == EvalBatchSizeUnit.instances:
            rank_batch_size_instances = batch_spec.rank_batch_size
        elif batch_spec.batch_size_unit == EvalBatchSizeUnit.tokens:
            if batch_spec.fixed_sequence_length:
                assert batch_spec.max_sequence_length is not None
                if batch_spec.rank_batch_size % batch_spec.max_sequence_length != 0:
                    raise OLMoConfigurationError(
                        f"The eval batch size ({batch_spec.rank_batch_size} tokens) must be divisible "
                        f"by the maximum eval sequence length ({batch_spec.max_sequence_length:,d} tokens)"
                    )
                rank_batch_size_instances = (
                    batch_spec.rank_batch_size // batch_spec.max_sequence_length
                )
            else:
                rank_batch_size_instances = (
                    batch_spec.rank_batch_size // self.task.max_sequence_length
                )
        else:
            raise NotImplementedError(batch_spec.batch_size_unit)

        log.info(
            f"Using per-rank batch size of {rank_batch_size_instances} instances "
            f"for downstream eval task '{task}' with max sequence length {self.task.max_sequence_length:,d} tokens"
        )

        data_loader = DataLoader(
            self.task,  # type: ignore
            batch_size=rank_batch_size_instances,
            collate_fn=self.task.collate_fn,
            drop_last=False,
            shuffle=False,
            num_workers=0,
            sampler=sampler,
        )

        super().__init__(name=name, batches=data_loader, device=device)

    def update_metrics(
        self, batch: Dict[str, Any], ce_loss: Optional[torch.Tensor], logits: Optional[torch.Tensor]
    ) -> None:
        del ce_loss
        self.metric.update(batch, logits)

    def compute_metrics(self) -> Dict[str, torch.Tensor]:
        metric_type_to_value = self.metric.compute()
        outputs = {}
        for metric_type, value in metric_type_to_value.items():
            key = f"{self.label} ({self.metric_type_to_label[metric_type]})"
            outputs[key] = value
        return outputs

    def reset_metrics(self) -> None:
        self.metric.reset()


@dataclass
class DownstreamEvaluatorCallbackConfig(CallbackConfig):
    tasks: List[str]
    tokenizer: TokenizerConfig
    eval_interval: int = 1000
    eval_duration: Duration = field(default_factory=lambda: Duration.epochs(1))
    log_interval: int = 5
    enabled: bool = True

    def build(self, trainer: "Trainer") -> Optional[Callback]:
        if not self.enabled:
            return None

        from olmo_eval import HFTokenizer

        if self.tokenizer.identifier is None:
            raise OLMoConfigurationError(
                "Tokenizer 'identifier' required to build a concrete tokenizer"
            )

        tokenizer = HFTokenizer(
            self.tokenizer.identifier,
            pad_token_id=self.tokenizer.pad_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
            bos_token_id=self.tokenizer.bos_token_id,
        )

        evaluators: List[Evaluator] = []
        for task in self.tasks:
            evaluators.append(
                DownstreamEvaluator(
                    name="downstream",
                    task=task,
                    batch_spec=trainer.train_module.eval_batch_spec,
                    tokenizer=tokenizer,
                    device=trainer.device,
                    dp_process_group=trainer.dp_process_group,
                )
            )

        return EvaluatorCallback(
            evaluators=evaluators,
            eval_interval=self.eval_interval,
            log_interval=self.log_interval,
            eval_duration=self.eval_duration,
        )
