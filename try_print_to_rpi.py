import requests

# Replace this with your Raspberry Pi's IP address and the port number
url = "http://192.168.2.3:5000/print"

# Your text to print
text_to_print = "Hello, this is a test print."

# Preparing the data payload
data = {"text": text_to_print}

# Sending the POST request
response = requests.post(url, json=data)

# Checking the response
if response.status_code == 200:
    print("Print request successful.")
else:
    print(f"Print request failed. Status code: {response.status_code}, Message: {response.text}")

