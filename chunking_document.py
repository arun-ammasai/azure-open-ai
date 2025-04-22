import yaml
from langchain.embeddings import AzureOpenAIEmbeddings

with open("open-ai-credentials.yml", "r") as file:
    config = yaml.safe_load(file)

client = AzureOpenAIEmbeddings(
        deployment="text-embedding-ada-002",
        model="text-embedding-ada-002",
        azure_endpoint=config['azure_endpoint'],
        openai_api_key=config['api_key'],
        chunk_size=1,
        validate_base_url=False)

# Example request to create embeddings
response = client.embeddings.create(input="Your text string goes here",  # Input text
deployment_id="text-embedding-3-large")  # Deployment ID for your embedding model)

# Print the response
print(response)