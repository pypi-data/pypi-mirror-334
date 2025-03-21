import os
import tempfile
from copy import deepcopy
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Dict, Optional

import torch
import torch.distributed as dist

from ..config import Config
from ..data import DataLoaderBase
from ..exceptions import OLMoConfigurationError
from ..io import is_url
from ..utils import get_default_device
from .callbacks import Callback, CallbackConfig
from .checkpoint import CheckpointerConfig
from .common import Duration, LoadStrategy
from .train_module import TrainModule
from .trainer import Trainer


@dataclass
class TrainerConfig(Config):
    """
    A configuration class for easily building :class:`Trainer` instances.

    .. seealso::
        See the :class:`Trainer` documentation for a description of the fields.
    """

    save_folder: str

    work_dir: Optional[str] = None
    load_path: Optional[str] = None
    load_strategy: LoadStrategy = LoadStrategy.if_available
    checkpointer: CheckpointerConfig = field(default_factory=CheckpointerConfig)

    device: Optional[str] = None
    save_overwrite: bool = False
    max_duration: Duration = field(default_factory=lambda: Duration.epochs(1))
    cancel_check_interval: int = 25
    hard_stop: Optional[Duration] = None
    metrics_collect_interval: int = 5
    callbacks: Dict[str, Callback] = field(default_factory=dict)
    async_bookkeeping: Optional[bool] = None
    no_checkpoints: bool = False
    no_evals: bool = False

    def add_callback(self, name: str, callback: Callback):
        """
        Add another callback.
        """
        if name in self.callbacks:
            raise OLMoConfigurationError(f"A callback with name '{name}' already exists")
        self.callbacks[name] = callback

    def with_callback(self, name: str, callback: Callback) -> "TrainerConfig":
        """
        Return a new trainer config with an additional callback.

        :param name: A name to assign the callback. Must be unique.
        :param callback: The callback to add.
        """
        out = replace(self, callbacks=deepcopy(self.callbacks))
        out.add_callback(name, callback)
        return out

    def build(
        self,
        train_module: TrainModule,
        data_loader: DataLoaderBase,
        *,
        dp_process_group: Optional[dist.ProcessGroup] = None,
        checkpointer_pg: Optional[dist.ProcessGroup] = None,
    ) -> Trainer:
        """
        Build the corresponding trainer.

        :param train_module: The train module to fit.
        :param data_loader: The data loader to train on.
        :param dp_process_group: The data parallel process group. Defaults to
            :data:`olmo_core.train.train_module.TrainModule.dp_process_group`.
        """
        kwargs = self.as_dict(exclude_none=True, recurse=False)

        if dp_process_group is None:
            dp_process_group = train_module.dp_process_group

        device = kwargs.pop("device", None)

        work_dir = kwargs.pop("work_dir", None)
        if work_dir is None:
            if not is_url(self.save_folder):
                work_dir = self.save_folder
            else:
                work_dir = os.path.join(tempfile.gettempdir(), os.path.basename(self.save_folder))

        checkpointer_kwargs = {}
        if self.checkpointer.save_overwrite is None:
            checkpointer_kwargs["save_overwrite"] = self.save_overwrite
        if self.checkpointer.work_dir is None:
            checkpointer_kwargs["work_dir"] = work_dir
        checkpointer = kwargs.pop("checkpointer").build(
            process_group=checkpointer_pg, **checkpointer_kwargs
        )

        all_callbacks = kwargs.pop("callbacks")
        callbacks = {k: cb for k, cb in all_callbacks.items() if not isinstance(cb, CallbackConfig)}
        callback_configs = {
            k: cb for k, cb in all_callbacks.items() if isinstance(cb, CallbackConfig)
        }

        trainer = Trainer(
            train_module=train_module,
            data_loader=data_loader,
            checkpointer=checkpointer,
            work_dir=Path(work_dir),
            device=torch.device(device) if device is not None else get_default_device(),
            dp_process_group=dp_process_group,
            callbacks=callbacks,
            **kwargs,
        )

        for cb_name, cb_config in callback_configs.items():
            cb = cb_config.build(trainer)
            if cb is not None:
                trainer.add_callback(cb_name, cb)

        return trainer
