import create_azure_open_ai_client as azure_open_ai_client
client = azure_open_ai_client.establish_azure_open_ai_client()

deployment_name = "text-embedding-ada-002"
text_to_embed = ["what is the capital of France?"]


response = client.embeddings.create(
    input=text_to_embed,
    model=deployment_name  
)

if hasattr(response, 'data') and response.data:
    embedding_vector = response.data[0].embedding
    print("Embedding vector:", embedding_vector)
else:
    print("Error: Unable to extract embedding data from the response.")
