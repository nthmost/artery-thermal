import requests

from .spacy_markov import MarkovGenerator



WEBHOOK = "https://discord.com/api/webhooks/1168322131415793714/kJDfRvlfwgWOEv5WE1ZNw0b5FmLp4cGKKJBVSz9vjc6PUfvMMx_NZEX6GYCeoJ778vMf"

def send_to_discord(content):
    "Simple function to send text to Discord channel in NOISY/#experiences on our server."
    data = {
        "content": content,
        # You can add more fields if needed, like "username", "avatar_url", etc.
    }
    response = requests.post(WEBHOOK, json=data)
    if response.status_code != 204:
        print(f"Failed to send message to Discord. Status code: {response.status_code}")


def generate_and_send_to_discord(state_size=2):
    generator = MarkovGenerator(state_size)
    exp_text = generator.generate_experience()
    send_to_discord(exp_text)
    print(exp_text)


def main():
    import sys
    state_size = 2  # default value
    if len(sys.argv) > 1:
        try:
            state_size = int(sys.argv[1])
        except ValueError:
            print("Invalid state_size value. Using default (2).")
    generate_and_send_to_discord(state_size)

if __name__ == "__main__":
    main()



