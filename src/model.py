import json
import numpy
import pandas
import torch
import torchmetrics
import torchvision
import warnings
from torchvision import transforms
from tqdm import tqdm
from pytorch_lightning_model import PyTorchLightningModel, PyTorchLightningModelForCAM
warnings.filterwarnings("ignore")


class Model:

    def __init__(self, config):
        self._config = config

    def get_accuracy_and_loss_of_each_epoch(self):
        performance_metrics = pandas.read_csv(f"{self._config.model.training_logs.dir}/default/version_0/metrics.csv")
        relevant_steps = performance_metrics[performance_metrics['Val Loss'].notnull()]['step'].to_list()
        accuracy_and_loss_of_each_epoch = performance_metrics[
            performance_metrics['step'].isin(relevant_steps)].groupby(['step']).first().drop(
            columns=['Step Train Acc', 'Step Val Acc'])
        return accuracy_and_loss_of_each_epoch.set_index('epoch').rename(columns={
            "Train Loss": "Train loss", "Val Loss": "Validation loss",
            "Train Acc": "Train accuracy", "Val Acc": "Validation accuracy"})

    @staticmethod
    def get_prediction_results(config, model, original_image, patient_id):

        def get_class_activation_map_image():
            with torch.no_grad():
                prediction, features = model(original_image.unsqueeze(0))
            batch_size, number_of_channels, image_height, image_weight = features.shape
            features = features.reshape((number_of_channels, image_height * image_weight))
            model_weights = list(model.model.fc.parameters())[0]
            weight = model_weights[0].detach()
            raw_class_activation_map = torch.matmul(weight, features)
            standardized_map = raw_class_activation_map - torch.min(raw_class_activation_map)
            normalized_map = standardized_map / torch.max(standardized_map)
            reshaped_map = normalized_map.reshape(image_height, image_weight).cpu()
            return transforms.functional.resize(
                reshaped_map.unsqueeze(0), (original_image[0].shape[0], original_image[0].shape[1]))[0]

        def get_pneumonia_probability():
            with torch.no_grad():
                prediction, features = model(original_image.unsqueeze(0))
            return round(100 * float(torch.sigmoid(prediction)), 2)

        def get_patient_training_features():
            raw_training_features = pandas.read_csv(config.data.raw.training_labels.path)
            patient_training_features = \
                raw_training_features.drop_duplicates('patientId').drop('Target', axis=1).set_index('patientId')
            return patient_training_features.loc[patient_id].to_dict()

        return dict(
            cam_image=get_class_activation_map_image(), original_image=original_image,
            patient_id=patient_id, pneumonia_probability=get_pneumonia_probability(),
            patient_training_features=get_patient_training_features())

    @staticmethod
    def get_pytorch_lightning(for_cam=False):
        if for_cam:
            model = PyTorchLightningModelForCAM()
        else:
            model = PyTorchLightningModel()
        model.eval();
        return model

    def get_torchvision_dataset(self, data_category):
        with open(self._config.data.statistics.path, 'r', encoding='utf-8') as json_data:
            training_dataset_statistics = json.load(json_data)
        if data_category == "training":
            dataset_transforms = transforms.Compose([
                transforms.ToTensor(), transforms.Normalize(
                    training_dataset_statistics['image_pixel_values']['mean'],
                    training_dataset_statistics['image_pixel_values']['std']),
                transforms.RandomAffine(degrees=(-5, 5), translate=(0, 0.05), scale=(0.9, 1.1)),
                transforms.RandomResizedCrop((224, 224), scale=(0.35, 1))])
        elif data_category == "validation":
            dataset_transforms = transforms.Compose([
                transforms.ToTensor(), transforms.Normalize(
                    training_dataset_statistics['image_pixel_values']['mean'],
                    training_dataset_statistics['image_pixel_values']['std'])])
        elif data_category == "test":
            dataset_transforms = transforms.Compose([
                transforms.ToTensor(), transforms.Normalize(
                    training_dataset_statistics['image_pixel_values']['mean'],
                    training_dataset_statistics['image_pixel_values']['std'])])
        else:
            raise Exception("Invalid data category")
        return torchvision.datasets.DatasetFolder(
            root=self._config.data.processed[data_category].dir, extensions="npy",
            transform=dataset_transforms, loader=lambda x: numpy.load(x).astype(numpy.float32))

    def get_performance_metrics(self):

        def get_prediction(data):
            model_prediction = torch.sigmoid(pytorch_lightling_model(data)[0].cpu())
            return model_prediction

        pytorch_lightling_model = self.get_pytorch_lightning(for_cam=False)
        torch_device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        pytorch_lightling_model.to(torch_device);
        with torch.no_grad():
            model_predictions_and_labels = [
                (get_prediction(data.to(torch_device).float().unsqueeze(0)), label)
                for data, label in tqdm(
                    self.get_torchvision_dataset("test"), desc="Generating model predictions",
                    total=len(self.get_torchvision_dataset("test")))]
            model_predictions, model_labels = map(lambda x: torch.tensor(list(x)), zip(*model_predictions_and_labels))
        return dict(
            accuracy=torchmetrics.Accuracy()(model_predictions, model_labels),
            precision=torchmetrics.Precision()(model_predictions, model_labels),
            recall=torchmetrics.Recall()(model_predictions, model_labels),
            confusion_matrix=torchmetrics.ConfusionMatrix(num_classes=2)(model_predictions, model_labels))

    def load_pytorch_lightning(self, for_cam=False):
        if for_cam:
            model = PyTorchLightningModelForCAM()
            model.load_state_dict(torch.load(self._config.model.entire.path), strict=False)
        else:
            model = PyTorchLightningModel()
            model.load_state_dict(torch.load(self._config.model.entire.path))
        model.eval();
        return model
