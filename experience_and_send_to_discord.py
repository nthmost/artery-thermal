from datetime import datetime

from experience_generator import generate_experience
from experience_generator import send_to_discord

exp_text = generate_experience()
send_to_discord(exp_text)

print(exp_text)



