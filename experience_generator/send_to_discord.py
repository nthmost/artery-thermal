import requests


WEBHOOK = "https://discord.com/api/webhooks/1168322131415793714/kJDfRvlfwgWOEv5WE1ZNw0b5FmLp4cGKKJBVSz9vjc6PUfvMMx_NZEX6GYCeoJ778vMf"



def send_to_discord(content):
    data = {
        "content": content,
        # You can add more fields if needed, like "username", "avatar_url", etc.
    }
    response = requests.post(WEBHOOK, json=data)
    if response.status_code != 204:
        print(f"Failed to send message to Discord. Status code: {response.status_code}")

# Your existing code...

# Wherever you generate the text in your script, call the send_to_discord function:
text_to_send = "This is the generated text."  # Replace with your generated text
send_to_discord(text_to_send)


