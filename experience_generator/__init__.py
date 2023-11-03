import requests

from .spacy_markov import MarkovGenerator

# these should be found in the root dir of this repo.
PARTYDB = "PARTY_DB.txt"
TESCREALDB = "TESCREAL_DB.txt"

# link to post experiences in Discord
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1168322131415793714/kJDfRvlfwgWOEv5WE1ZNw0b5FmLp4cGKKJBVSz9vjc6PUfvMMx_NZEX6GYCeoJ778vMf"


def send_to_discord(content):
    "Simple function to send text to Discord channel in NOISY/#experiences on our server."
    data = {
        "content": content,
        # You can add more fields if needed, like "username", "avatar_url", etc.
    }
    response = requests.post(DISCORD_WEBHOOK, json=data)
    if response.status_code != 204:
        print(f"Failed to send message to Discord. Status code: {response.status_code}")


def generate_and_send_to_discord(state_size=2, num_sentences=6):
    generator = MarkovGenerator(PARTYDB, TESCREALDB, state_size)
    exp_text = generator.generate_experience(num_sentences)
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



