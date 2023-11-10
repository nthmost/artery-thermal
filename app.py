from flask import Flask, request, jsonify
import random
from experience_generator import MarkovGenerator

app = Flask(__name__)

# Initialize Markov Generator
party_db_path = "PARTY_DB.txt"
tescreal_db_path = "TESCREAL_DB.txt"
generator = MarkovGenerator(party_db_path, tescreal_db_path)

@app.route('/generate', methods=['GET'])
def generate():
    # Generate the experience
    # Example: Use your MarkovGenerator or any other logic here
    experience = generator.generate_experience()

    # Return the experience in the response
    return jsonify({"experience": experience})

if __name__ == '__main__':
    app.run(debug=True)

