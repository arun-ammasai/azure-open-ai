import create_azure_open_ai_client as azure_open_ai_client

client = azure_open_ai_client.establish_azure_open_ai_client()

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": "I am going to Chennai, what should I see?",
        }
    ],
    max_tokens=4096,
    temperature=1.0,
    top_p=1.0,
    model=azure_open_ai_client.DEPLOYMENT
)

# Print the response
print(response.choices[0].message.content)