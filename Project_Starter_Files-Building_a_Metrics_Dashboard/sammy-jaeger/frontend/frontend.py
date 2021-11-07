import os
import requests
from flask import Flask
app = Flask(__name__)

def get_counter(counter_endpoint):
    counter_response = requests.get(counter_endpoint)
    return counter_response.text

def increase_counter(counter_endpoint):
    counter_response = requests.post(counter_endpoint)
    return counter_response.text

@app.route('/')
def hello_world():
    counter_service = os.environ.get('COUNTER_ENDPOINT', default="https://localhost:5000")
    counter_endpoint = f'{counter_service}/api/counter'
    counter = get_counter(counter_endpoint)

    increase_counter(counter_endpoint)

    return f"""Hello, World!

You're visitor number {counter} in here!\n\n"""