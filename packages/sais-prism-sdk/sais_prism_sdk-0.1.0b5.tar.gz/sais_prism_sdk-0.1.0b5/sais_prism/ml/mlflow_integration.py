from typing import Any, Dict, Optional
import os
import pytorch_lightning as pl
from pytorch_lightning.callbacks import Callback
from transformers import TrainerCallback
from ..core.config import ConfigManager


class MLflowManager(Callback, TrainerCallback):
    """MLflow integration manager that acts as both a PyTorch Lightning callback and Transformers callback"""

    def __init__(self, experiment_name: str, config: Any, mlflow) -> None:
        super().__init__()
        self.url = "http://mlflow.internal.sais.com.cn"
        self.experiment_name = experiment_name
        self.ml_config = config
        self.config = ConfigManager()
        self.mlflow = mlflow
        self.mlflow.set_tracking_uri(self.url)
        self.mlflow.set_experiment(experiment_name)
        self.system_tracing(self.ml_config.system_tracing)
        self.mlflow.autolog()

    # PyTorch Lightning callback methods - these have to match the PL interface
    def on_fit_start(self, trainer, pl_module):
        """Called when fit begins"""
        self.init_run()

    def on_train_batch_end(self, trainer, pl_module, outputs, batch, batch_idx):
        """Called when the train batch ends, log metrics if available"""
        if hasattr(outputs, "get") and isinstance(outputs, dict) and "loss" in outputs:
            self.log_metrics({"batch_loss": outputs["loss"].item() if hasattr(outputs["loss"], "item") else outputs["loss"]},
                             step=trainer.global_step)

    def on_validation_batch_end(self, trainer, pl_module, outputs, batch, batch_idx, dataloader_idx=0):
        """Called when the validation batch ends"""
        pass  # Implement if needed for validation metrics

    def on_train_epoch_end(self, trainer, pl_module):
        """Called when the train epoch ends"""
        metrics = trainer.callback_metrics
        self.log_metrics({k: v.item() if hasattr(v, 'item') else v
                          for k, v in metrics.items() if isinstance(v, (int, float))},
                         step=trainer.current_epoch)

    def on_fit_end(self, trainer, pl_module):
        """Called when fit ends"""
        if self.ml_config.artifacts:
            self.log_artifacts(self.ml_config.artifacts)
        self._ml_termination_()

    # Important: Add this method for PyTorch Lightning specifically
    def on_train_end(self, trainer, pl_module):
        """Called when training ends in PyTorch Lightning"""
        # Log final metrics if any
        metrics = trainer.callback_metrics
        if metrics:
            self.log_metrics({k: v.item() if hasattr(v, 'item') else v
                              for k, v in metrics.items() if isinstance(v, (int, float))})

    # Transformers TrainerCallback methods - these use the Transformers interface
    def on_log(self, args, state, control, logs=None, **kwargs):
        """Callback method to log metrics during training (Transformers)"""
        if state.is_world_process_zero and logs is not None:
            for k, v in logs.items():
                if isinstance(v, (int, float)):
                    self.log_metrics({k: v}, step=state.global_step)

    def on_train_begin(self, args, state, control, **kwargs):
        """Called when training begins (Transformers)"""
        self.init_run()

    # This version is only for Transformers
    def on_train_end(self, args=None, state=None, control=None, **kwargs):
        """Called when training ends (Transformers)"""
        if hasattr(self.ml_config, "artifacts"):
            self.log_artifacts(self.ml_config.artifacts)
        self._ml_termination_()

    # MLflow specific methods
    def init_run(self) -> None:
        """Initialize MLflow run with parameters, model info and artifacts"""
        if not self.mlflow.active_run():
            self.mlflow.start_run()

        params_dict = {}
        try:
            params_dict = self.config._convert_namespace_to_dict(
                self.ml_config.parameters)
        except (AttributeError, ValueError) as e:
            print(f"Warning: Could not convert parameters: {e}")

        self.log_params(params_dict)

        try:
            model_repo_dict = self.config._convert_namespace_to_dict(
                self.ml_config.model_repo)
            if model_repo_dict:
                self.log_model(model_repo_dict)
        except (AttributeError, ValueError) as e:
            print(f"Warning: Could not convert model repo: {e}")

        if hasattr(self.ml_config, "artifacts"):
            self.log_artifacts(self.ml_config.artifacts)

    def system_tracing(self, enabled: bool) -> None:
        """Enable or disable system metrics logging"""
        if enabled and hasattr(self.mlflow, "enable_system_metrics_logging"):
            self.mlflow.enable_system_metrics_logging()
            print("System Metrics is Enabled")
        else:
            print("System Metrics is Disabled")

    def log_model(self, params: Dict[str, Any]) -> None:
        """Log model information to MLflow"""
        if not params:
            return

        required_fields = {"model_uri", "name", "version"}
        if missing := required_fields - set(params.keys()):
            raise ValueError(f"Missing required fields: {missing}")

        if not self.mlflow.active_run():
            self.mlflow.start_run()

        model_uri = params["model_uri"].format(
            run_id=self.mlflow.active_run().info.run_id)

        self.mlflow.register_model(
            model_uri=model_uri,
            name=params["name"],
            tags={
                "version": params["version"],
                **(params.get("tag", {}) or {})
            }
        )

    def log_params(self, params: Dict[str, Any]) -> None:
        """Log parameters to MLflow"""
        if params and self.mlflow.active_run():
            self.mlflow.log_params(params)

    def log_metrics(self, metrics: Dict[str, float], step: int = 0) -> None:
        """Log metrics to MLflow with optional step number"""
        if metrics and self.mlflow.active_run():
            # Convert tensor values to Python scalars if needed
            cleaned_metrics = {}
            for k, v in metrics.items():
                if hasattr(v, 'item'):
                    cleaned_metrics[k] = v.item()
                else:
                    cleaned_metrics[k] = v
            self.mlflow.log_metrics(cleaned_metrics, step=step)

    def log_artifacts(self, artifacts: Dict[str, Any]) -> None:
        """Log artifacts to MLflow"""
        if artifacts and self.mlflow.active_run():
            if isinstance(artifacts, list):
                artifacts = {"artifacts": artifacts}
            for artifact in artifacts.values():
                if artifact:
                    self.mlflow.log_artifacts(artifact)

    def set_log_artifacts(self, obj_str: str) -> None:
        """Log a single artifact to MLflow"""
        if obj_str and self.mlflow.active_run():
            self.mlflow.log_artifacts(obj_str)

    def set_log_params(self, key: str, val: str) -> None:
        """Log a single parameter to MLflow"""
        if key and val and self.mlflow.active_run():
            self.mlflow.log_param(key, val)

    def _ml_termination_(self) -> None:
        """End the current MLflow run"""
        if self.mlflow.active_run():
            self.mlflow.end_run()


def initialize(experiment_name: str, config: Any, mlflow: Any) -> MLflowManager:
    """Initialize and return a new MLflowManager instance"""
    global client
    client = MLflowManager(experiment_name, config, mlflow)
    return client
