import json
import random
import string
from abc import abstractmethod, ABC
from constellaxion.handlers.model import Model
from constellaxion.handlers.dataset import Dataset
from constellaxion.handlers.training import Training
from constellaxion.services.gcp.train_job import run_training_job
from constellaxion.services.gcp.serve_job import run_serving_job
from constellaxion.services.gcp.deploy_job import run_deploy_job
from constellaxion.services.gcp.prompt_model import send_prompt


class BaseCloudJob(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def run():
        pass

    @abstractmethod
    def create_config(model: Model, dataset: Dataset):
        pass


class GCPDeployJob(BaseCloudJob):
    def __init__(self):
        super().__init__()

    @staticmethod
    def run(config):
        run_training_job(config)

    @staticmethod
    def serve(config):
        """Serve GCP model """
        endpoint_path = run_serving_job(config)
        config['deploy']['endpoint_path'] = endpoint_path
        with open("job.json", "w") as f:
            json.dump(config, f, indent=4)

    @staticmethod
    def deploy(config):
        """Deploy GCP model"""
        endpoint_path = run_deploy_job(config)
        config['deploy']['endpoint_path'] = endpoint_path
        with open("job.json", "w") as f:
            json.dump(config, f, indent=4)

    @staticmethod
    def prompt(prompt, config):
        """Send prompt to model"""
        endpoint_path = config['deploy']['endpoint_path']
        location = config['deploy']['location']
        response = send_prompt(prompt, endpoint_path, location)
        return response

    @staticmethod
    def create_config(model: Model, project_id: str, location: str, service_account: str, dataset: Dataset, training: Training):
        """Create a JSON configuration file from model and dataset attributes."""
        bucket_name = f"constellaxion-{project_id}"
        job_config = {
            "model": {
                "model_id": model.id,
                "base_model": model.base_model,
            },
            "dataset": dataset.to_dict() if dataset else None,
            "training": training.to_dict() if training else None,
            "deploy": {
                "provider": "gcp",
                "project_id": project_id,
                "location": location,
                "bucket_name": bucket_name,
                "staging_dir": f"{model.id}/staging",
                "experiments_dir": f"{model.id}/experiments",
                "model_path": f"{model.id}/model",
                "service_account": service_account
            }
        }
        with open("job.json", "w") as f:
            json.dump(job_config, f, indent=4)


class AWSDeployJob(BaseCloudJob):
    def __init__(self, ):
        super().__init__()
        pass

    def run(self):
        pass

    def create_config(self, model: Model, dataset: Dataset):
        pass
