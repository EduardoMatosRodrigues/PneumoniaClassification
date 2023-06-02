import hydra
from joblib import Parallel, delayed
from omegaconf import DictConfig
from tqdm import tqdm
from utils import set_up_config
from dataset import Dataset


@hydra.main(config_path="../config", config_name='main', version_base="1.3")
def generate_processed_data(config: DictConfig):
    set_up_config(config)
    dataset = Dataset(config)
    for data_category in ["training", "validation", "test"]:
        dicom_image_names = dataset.get_dicom_image_names(data_category)
        Parallel(n_jobs=config.number_of_cpu_cores_for_multiprocessing)(delayed(
            dataset.generate_processed_dicom_image)(data_category, dicom_image_name) for dicom_image_name in tqdm(
            dicom_image_names, total=len(dicom_image_names),
            desc=f"Generating processed {data_category} data"))


if __name__ == "__main__":
    generate_processed_data()
