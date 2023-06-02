# Pneumonia classification

## Project structure
```bash
.
├── config                      
│    ├── main.yaml                       # Main configuration file
│    ├── data                            # Configurations for the data
│    │   ├── data1.yaml                  # First variation of parameters related to the data
│    │   └── data2.yaml                  # Second variation of parameters related to the data
│    └── model                           # Configurations for the model
│         ├── model1.yaml                # First variation of parameters related to the model
│         └── model2.yaml                # Second variation of parameters related to the model
├── data            
│    ├── processed                       # data after processing
│    ├── raw                             # raw data
│    ├── statistics                      # data statistics
│    └── raw.dvc                         # DVC file of data/raw
├── docs                                 # documentation for your project
├── dvc.yaml                             # DVC pipeline
├── .flake8                              # configuration for flake8 - a Python formatter tool
├── Makefile                             # store useful commands to set up the environment, run git flow commands and run Python scripts
├── models                               # store entire models, as well as model checkpoints and model training logs
├── notebooks                            # store notebooks
├── .pre-commit-config.yaml              # configurations for pre-commit
├── pyproject.toml                       # dependencies for poetry
├── README.md                            # describe your project
└── src                                  # store source code
     ├── __init__.py                     # make src a Python module 
     ├── dataset.py                      # module representing the dataset
     ├── figures.py                      # module representing the output figures
     ├── generate_data_statistics.py     # script to generate data statistics
     ├── generate_figure.py              # script to generate figures
     ├── model.py                        # module representing the model
     ├── process_data.py                 # script to process the raw data
     ├── pytorch_lightning_model.py      # module representing the PyTorch lightning model
     ├── test_model.py                   # script to test the model
     ├── train_model.py                  # script to train the model
     └── utils.py                        # module with useful functions used in some modules and scripts

```
