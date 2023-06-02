import cv2
import numpy
import pandas
import pydicom
from os import listdir, walk
from pathlib import Path, PurePath
from tqdm import tqdm


class Dataset:

    def __init__(self, config):
        self._config = config

    def generate_processed_dicom_image(self, data_category, dicom_image_name):
        raw_dicom_image_pixel_array = \
            pydicom.read_file(f"{self._config.data.raw.training.dir}/{dicom_image_name}").pixel_array
        processed_dicom_image_pixel_array = \
            cv2.resize(raw_dicom_image_pixel_array / 255, (224, 224)).astype(numpy.float16)
        processed_dicom_image = \
            {"patient_id": dicom_image_name.split('.')[0], "pixel_array": processed_dicom_image_pixel_array}
        raw_training_labels = pandas.read_csv(f"{self._config.data.raw.training_labels.path}")
        training_labels = raw_training_labels.drop_duplicates('patientId')[['patientId', 'Target']].set_index('patientId')
        training_label = training_labels.loc[processed_dicom_image['patient_id'], 'Target']
        dicom_image_pixel_array_folder_path = f"{self._config.data.processed[data_category].dir}/{str(training_label)}"
        Path(dicom_image_pixel_array_folder_path).mkdir(parents=True, exist_ok=True)
        numpy.save(
            f"{dicom_image_pixel_array_folder_path}/{processed_dicom_image['patient_id']}",
            processed_dicom_image['pixel_array'])

    def get_dicom_image_names(self, data_category):
        all_dicom_image_names = listdir(f"{self._config.data.raw.training.dir}")[:self._config.data.size]
        dataset_size = len(all_dicom_image_names)
        if data_category == "test":
            return all_dicom_image_names[-round(dataset_size * self._config.data.raw.test.split_fraction):dataset_size]
        else:
            training_dataset_split = \
                1 - self._config.data.raw.test.split_fraction - self._config.data.raw.validation.split_fraction
            if data_category == "training":
                return all_dicom_image_names[:round(dataset_size * training_dataset_split)]
            elif data_category == "validation":
                return all_dicom_image_names[round(
                    dataset_size * training_dataset_split):round(dataset_size * (1 - self._config.data.raw.test.split_fraction))]
            else:
                raise Exception("Invalid data category")

    @staticmethod
    def get_normalized_squared_sum_of_image_pixel_values(image_pixel_array):
        return numpy.power(image_pixel_array, 2).sum() / image_pixel_array.size

    @staticmethod
    def get_normalized_sum_of_image_pixel_values(image_pixel_array):
        return numpy.sum(image_pixel_array) / image_pixel_array.size

    def get_pixel_arrays(self, dataset_type, data_category):
        progress_bar = tqdm(
            desc=f"Loading {dataset_type} {data_category} data",
            leave=False, total=self.get_size(dataset_type, data_category))
        pixel_arrays = []
        for dicom_image_dir_path, _, dicom_image_names in walk(Path(self._config.data[dataset_type][data_category].dir)):
            for dicom_image_name in dicom_image_names:
                pixel_arrays.append(numpy.load(PurePath(dicom_image_dir_path, dicom_image_name)))
                progress_bar.update()
        progress_bar.close()
        return pixel_arrays

    def get_size(self, dataset_type, data_category):
        return sum([len(files) for _, _, files in walk(Path(self._config.data[dataset_type][data_category].dir))])
