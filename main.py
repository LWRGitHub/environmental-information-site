from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for, flash
import os
import requests

load_dotenv()
yelp_api_key = os.getenv('yelp_api_key')

app = Flask(__name__)

@app.route('/')
def homepage():
    return "Hello, world!"

@app.route('/search_store', methods=['GET', 'POST'])
def search_store():
    ''' Search for local stores '''
    if request.method == 'POST':
        location = ''
        #checks if ip address is being forwarded. depends if running locally or deployed
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            response = requests.get("http://ip-api.com/json")
            js = response.json()

            city = js['city']
            lat = js['lat']
            lng = js['lon']

            print(lat)
            print(lng)
            print(city)

        else:
            ip = request.environ['HTTP_X_FORWARDED_FOR']
            response = requests.get(f"http://ip-api.com/json/{ip}")
            js = response.json()

            city = js['city']
            lat = js['lat']
            lng = js['lon']

    return render_template('search_store.html')


if __name__ == '__main__':
    app.run(debug=True)