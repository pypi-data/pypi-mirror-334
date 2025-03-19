import os

import openai

# Initialize the OpenAI client
client = openai.OpenAI(api_key=os.getenv("ARCADE_API_KEY"), base_url="https://api.arcade.dev/v1")


# Make a request to the OpenAI API with the tool
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "List my emails."},
    ],
    tools=["Google.ListEmails"],
    tool_choice="generate",
    user="sam",
)

# Process the response
message = response.choices[0].message.content

print(message)
