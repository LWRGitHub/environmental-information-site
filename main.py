from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for, flash
import os

load_dotenv()
yelp_api_key = os.getenv('yelp_api_key')

app = Flask(__name__)

def get_location():
    ''' Get's the user's ip addresses, then passes it to ip->location api and returns city corresponding to ip '''
    #checks if ip address is being forwarded. depends if running locally or deployed
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        response = requests.get("http://ip-api.com/json")
        js = response.json()

        city = js['city']
        lat = js['lat']
        lng = js['long']
        return lat, lng
        
    else:
        ip = request.environ['HTTP_X_FORWARDED_FOR']
        response = requests.get(f"http://ip-api.com/json/{ip}")
        js = response.json()

        city = js['city']
        lat = js['lat']
        lng = js['long']
        return lat, lng

@app.route('/')
def homepage():
    return "Hello, world!"

if __name__ == '__main__':
    app.run(debug=True)