from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for, flash
import os
app = Flask(__name__)

def get_location():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        response = requests.get("http://ip-api.com/json")
        js = response.json()
        location = js['city']
        return location
    else:
        ip = request.environ['HTTP_X_FORWARDED_FOR']
        response = requests.get(f"http://ip-api.com/json/{ip}")
        js = response.json()
        location = js['city']
        return location

@app.route('/')
def homepage():
    return "Hello, world!"

if __name__ == '__main__':
    app.run(debug=True)