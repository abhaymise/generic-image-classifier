# mlsaas-template

## Structure

```
ai-solution-service/
│
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions workflow for CI/CD
│
├── config/
│   └── config.yaml              # Configuration files
│
├── data/
│   └── raw/                     # Raw data
│   └── processed/               # Processed data
│
├── docs/
│   └── README.md                # Documentation files
│
├── models/
│   └── model.pkl                # Pre-trained models
│
├── notebooks/
│   └── exploration.ipynb        # Jupyter notebooks for exploration
│
├── scripts/
│   └── preprocess.py            # Data preprocessing scripts
│   └── train.py                 # Model training scripts
│   └── predict.py               # Prediction scripts
│
├── src/
│   ├── __init__.py              # Initialize the src module
│   ├── data_processing.py       # Data processing module
│   ├── model.py                 # Model definition and training module
│   ├── service.py               # FastAPI service module
│   └── utils.py                 # Utility functions
│
├── tests/
│   └── test_data_processing.py  # Unit tests for data processing
│   └── test_model.py            # Unit tests for model
│   └── test_service.py          # Unit tests for service
│
├── .gitignore                   # Git ignore file
├── Dockerfile                   # Dockerfile for containerization
├── docker-compose.yml           # Docker Compose file for multi-container setup
├── requirements.txt             # Python dependencies
├── setup.py                     # Setup script for packaging
└── README.md                    # Project README file

```

### Description of Directories and Files

- `config`: Configuration files (e.g., config.yaml for application settings, logging.yaml for logging configuration).
- `mlsaas`: Main source code dir for the application.
- `data`: Data handling modules (e.g., data_loader.py for loading and preprocessing data).
- `models`: Model definition and utility functions (e.g., model.py for model architecture, model_utils.py for helper functions).
- `docker`: Docker-related files for containerization.
  - Dockerfile: Instructions to build the Docker image.
  - docker-compose.yml: Configuration for Docker Compose.
- `scripts`: Shell scripts for common tasks (e.g., run_training.sh for running training, run_inference.sh for running inference).
  - `entrypoint.sh`: Entry point script for Docker container. 
- `notebooks`: Jupyter notebooks for exploration and experimentation (e.g., exploratory_data_analysis.ipynb for EDA).
- `docs`: Documentation files (e.g., architecture.md for system architecture, api_documentation.md for API documentation).
- `cd-ci`:  Actions workflows for CI/CD.
  - workflows
    - ci.yml: CI workflow for running tests and other checks.
```