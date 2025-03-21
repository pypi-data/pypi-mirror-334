import os
from google.cloud import aiplatform
from constellaxion.services.gcp.model_map import model_map

# def download_model(hf_path: str, model_dir: str):
#     """Downloads a Hugging Face model and tokenizer."""
#     print("Downloading model...")
#     model = AutoModelForSequenceClassification.from_pretrained(hf_path)
#     tokenizer = AutoTokenizer.from_pretrained(hf_path)

#     os.makedirs(model_dir, exist_ok=True)
#     model.save_pretrained(model_dir)
#     tokenizer.save_pretrained(model_dir)
#     print(f"Model saved to {model_dir}/")


# def upload_to_gcs(model_dir: str, bucket_name: str, gcs_path: str):
#     """Uploads the model to Google Cloud Storage."""
#     print(f"Uploading model to {gcs_path}...")
#     storage_client = storage.Client()
#     bucket = storage_client.bucket(bucket_name)

#     uploader = GCSUploadHandler(model_dir, gcs_path)
#     uploader.upload_directory(model_dir)
#     print(f"Uploaded model to {gcs_path}")


def create_model_from_custom_container(model_name: str, image_uri: str, env_vars: dict):
    print("Creating model from custom container...")

    # Define the container and model
    model = aiplatform.Model.upload(
        display_name=model_name,
        serving_container_image_uri=image_uri,
        serving_container_ports=[8080],  # Port your container exposes
        # Optional, adjust if your container provides health checks
        serving_container_health_route="/health",
        # Optional, adjust if your container provides a prediction endpoint
        serving_container_predict_route="/predict",
        serving_container_environment_variables=env_vars
    )
    print(f"Model created successfully: {model.resource_name}")
    return model

# Deploy the model to an endpoint


def deploy_model_to_endpoint(model,
                             model_id: str,
                             machine_type: str,
                             accelerator_type: str,
                             accelerator_count: int,
                             replica_count: int,
                             service_account: str
                             ):

    # Check if the endpoint exists, create it if not
    endpoints = aiplatform.Endpoint.list(
        filter=f'display_name="{model_id}"')
    if endpoints:
        endpoint = endpoints[0]  # Use the first matching endpoint
        print(f"Using existing endpoint: {endpoint.display_name}")
    else:
        # Create a new endpoint
        endpoint = aiplatform.Endpoint.create(
            display_name=model_id)
        print(f"Created new endpoint: {endpoint.display_name}")

    # Deploy the model to the endpoint
    deployed_model = model.deploy(
        endpoint=endpoint,
        deployed_model_display_name=model_id,
        traffic_split={"0": 100},  # Route all traffic to this model
        accelerator_type=accelerator_type,
        accelerator_count=accelerator_count,
        machine_type=machine_type,
        min_replica_count=replica_count,
        max_replica_count=replica_count,
        service_account=service_account,
    )

    print(f"Model deployed to endpoint: {endpoint.resource_name}")
    return endpoint.resource_name


def run_deploy_job(config):
    project_id = config['deploy']['project_id']
    base_model = config['model']['base_model']
    location = config['deploy']['location']
    bucket_name = config['deploy']['bucket_name']
    model_id = config['model']['model_id']
    service_account = config['deploy']['service_account']
    infra_config = model_map[base_model]["gcp_infra"]
    image_uri = model_map[base_model]["images"]["serve"]
    machine_type = infra_config['machine_type']
    accelerator_type = infra_config['accelerator_type']
    accelerator_count = infra_config['accelerator_count']
    replica_count = infra_config['replica_count']
    env_vars = {
        "MODEL_NAME": base_model
    }
    # Initialize the Vertex AI SDK
    aiplatform.init(project=project_id, location=location)
    # # Download the model
    # download_model(hf_path, model_path)
    # # Upload the model to GCS
    # upload_to_gcs(model_path, bucket_name, model_path)
    # Register a model
    model = create_model_from_custom_container(base_model, image_uri, env_vars)
    # Deploy model to endpoint
    endpoint_path = deploy_model_to_endpoint(model, model_id,
                                             machine_type, accelerator_type, accelerator_count, replica_count, service_account)
    return endpoint_path
