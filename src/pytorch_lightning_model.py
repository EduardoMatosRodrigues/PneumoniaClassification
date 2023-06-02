import torch
import torchmetrics
import torchvision
from pytorch_lightning import LightningModule, Trainer


class PyTorchLightningModel(LightningModule):
    def __init__(self, weight=1):
        super().__init__()
        self.model = torchvision.models.resnet18()
        self.model.conv1 = torch.nn.Conv2d(1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
        self.model.fc = torch.nn.Linear(in_features=512, out_features=1)
        self._optimizer = torch.optim.Adam(self.model.parameters(), lr=1e-4)
        self._loss_function = torch.nn.BCEWithLogitsLoss(pos_weight=torch.tensor([weight]))
        self._training_accuracy = torchmetrics.Accuracy()
        self._validation_accuracy = torchmetrics.Accuracy()

    def forward(self, data):
        return self.model(data)

    def training_step(self, batch, batch_idx):
        x_ray, label = batch
        label = label.float()
        prediction = self(x_ray)[:, 0]
        loss = self._loss_function(prediction, label)
        self.log("Train Loss", loss)
        self.log("Step Train Acc", self._training_accuracy(torch.sigmoid(prediction), label.int()))
        return loss

    def training_epoch_end(self, outs):
        self.log("Train Acc", self._training_accuracy.compute())

    def validation_step(self, batch, batch_idx):
        x_ray, label = batch
        label = label.float()
        prediction = self(x_ray)[:, 0]
        loss = self._loss_function(prediction, label)
        self.log("Val Loss", loss)
        self.log("Step Val Acc", self._validation_accuracy(torch.sigmoid(prediction), label.int()))
        return loss

    def validation_epoch_end(self, outs):
        self.log("Val Acc", self._validation_accuracy.compute())

    def configure_optimizers(self):
        return [self._optimizer]


class PyTorchLightningModelForCAM(LightningModule):
    def __init__(self):
        super().__init__()
        self.model = torchvision.models.resnet18()
        self.model.conv1 = torch.nn.Conv2d(1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
        self.model.fc = torch.nn.Linear(in_features=512, out_features=1)
        self.feature_map = torch.nn.Sequential(*list(self.model.children())[:-2])

    def forward(self, data):
        feature_map = self.feature_map(data)
        avg_pool_output = torch.nn.functional.adaptive_avg_pool2d(input=feature_map, output_size=(1, 1))
        avg_pool_output_flattened = torch.flatten(avg_pool_output)
        pred = self.model.fc(avg_pool_output_flattened)
        return pred, feature_map
