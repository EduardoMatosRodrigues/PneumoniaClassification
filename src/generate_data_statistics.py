import hydra
import json
import numpy
from joblib import Parallel, delayed
from omegaconf import DictConfig
from tqdm import tqdm
from utils import set_up_config
from dataset import Dataset


@hydra.main(config_path="../config", config_name='main', version_base="1.3")
def generate_data_statistics(config: DictConfig):
    set_up_config(config)
    dataset = Dataset(config)
    processed_training_dataset_pixel_arrays = dataset.get_pixel_arrays("processed", "training")
    normalized_sum_of_image_pixel_values = Parallel(n_jobs=config.number_of_cpu_cores_for_multiprocessing)(
        delayed(dataset.get_normalized_sum_of_image_pixel_values)(processed_dicom_image)
        for processed_dicom_image in tqdm(
            processed_training_dataset_pixel_arrays, desc="Calculating the normalized sum of image pixel values"))
    normalized_squared_sum_of_image_pixel_values = Parallel(n_jobs=config.number_of_cpu_cores_for_multiprocessing)(
        delayed(dataset.get_normalized_squared_sum_of_image_pixel_values)(processed_dicom_image)
        for processed_dicom_image in tqdm(
            processed_training_dataset_pixel_arrays, desc="Calculating the normalized squared sum of image pixel values"))
    statistics = dict(image_pixel_values=dict(
        mean=sum(normalized_sum_of_image_pixel_values) / dataset.get_size("processed", "training"),
        std=numpy.sqrt(sum(normalized_squared_sum_of_image_pixel_values) / dataset.get_size("processed", "training")
                       - (sum(normalized_sum_of_image_pixel_values) / dataset.get_size("processed", "training")) ** 2)))
    with open(config.data.statistics.path, 'w', encoding='utf-8') as file:
        json.dump(statistics, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    generate_data_statistics()
