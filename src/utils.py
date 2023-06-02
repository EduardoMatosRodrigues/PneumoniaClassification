from hydra.utils import to_absolute_path
from omegaconf import OmegaConf


def set_up_config(config):

    def add_process_name_to_dir(config):
        config.model.checkpoints.dirpath = config.model.checkpoints.dirpath.replace("final", f"final/{config.process.name}")
        config.model.performance_metrics.dir = config.model.performance_metrics.dir.replace("final", f"final/{config.process.name}")
        config.model.prediction_results.dir = config.model.prediction_results.dir.replace("final", f"final/{config.process.name}")
        config.model.training_logs.dir = config.model.training_logs.dir.replace("final", f"final/{config.process.name}")

    def change_paths_to_absolute_path(config):
        for key, value in config.items():
            if "path" in key or "dir" in key:
                config[key] = to_absolute_path(config[key])
            elif OmegaConf.is_dict(value):
                change_paths_to_absolute_path(value)
 
    change_paths_to_absolute_path(config)
    add_process_name_to_dir(config)
