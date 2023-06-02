import hydra
from joblib import Parallel, delayed
from omegaconf import DictConfig
from pathlib import Path
from tqdm import tqdm
from model import Model
from utils import set_up_config
from generate_figure import generate_model_performance_metrics_figure, generate_patient_figure


@hydra.main(config_path="../config", config_name="main", version_base="1.3")
def test_model(config: DictConfig):
    set_up_config(config)
    model = Model(config)
    Path(f"{config.model.performance_metrics.dir}/{config.process.name}").mkdir(parents=True, exist_ok=True)
    generate_model_performance_metrics_figure(config, model.get_accuracy_and_loss_of_each_epoch(), model.get_performance_metrics())
    test_dataset = model.get_torchvision_dataset("test")
    model_prediction_results = Parallel(n_jobs=config.number_of_cpu_cores_for_multiprocessing)(
        delayed(model.get_prediction_results)(
            config, model.load_pytorch_lightning(for_cam=True), test_dataset[index][0],
            test_dataset_sample[0].split("/")[-1].split(".")[0])
        for index, test_dataset_sample in tqdm(
            enumerate(test_dataset.samples), desc="Generating model prediction results", total=len(test_dataset.samples)))
    Path(f"{config.model.prediction_results.dir}/{config.process.name}").mkdir(parents=True, exist_ok=True)
    Parallel(n_jobs=config.number_of_cpu_cores_for_multiprocessing)(
        delayed(generate_patient_figure)(config, model_prediction_result)
        for model_prediction_result in tqdm(
            model_prediction_results, desc="Generating figures", total=len(model_prediction_results)))


if __name__ == "__main__":
    test_model()
