import hydra
import torch
from omegaconf import DictConfig, OmegaConf
from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.loggers import CSVLogger
from model import Model
from utils import set_up_config


@hydra.main(config_path="../config", config_name="main", version_base="1.3")
def train_model(config: DictConfig):
    set_up_config(config)
    model = Model(config)
    pytorch_lightning_trainer = Trainer(
        callbacks=ModelCheckpoint(**config.model.checkpoints),
        logger=CSVLogger(save_dir=config.model.training_logs.dir), **config.model.pytorch_lightning_trainer)
    pytorch_lightning_trainer.fit(
        model.get_pytorch_lightning(),
        torch.utils.data.DataLoader(model.get_torchvision_dataset("training"), **config.model.data_loader),
        torch.utils.data.DataLoader(model.get_torchvision_dataset("validation"), **config.model.data_loader))
    torch.save(model.get_pytorch_lightning().state_dict(), config.model.entire.path)


if __name__ == "__main__":
    train_model()
