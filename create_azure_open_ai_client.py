import os
import yaml
from openai import AzureOpenAI



with open("open-ai-credentials.yml", "r") as file:
    config = yaml.safe_load(file)

AZURE_OPENAI_API_KEY = config["azure_openai"]["api_key"]
ENDPOINT = config["azure_openai"]["api_base"]
MODEL_NAME = config["azure_openai"]["model"]
DEPLOYMENT = config["azure_openai"]["deployment"]
API_VERSION = config["azure_openai"]["api_version"]


def establish_azure_open_ai_client():    
    client = AzureOpenAI(
        api_version=API_VERSION,
        azure_endpoint=ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        )
    return client