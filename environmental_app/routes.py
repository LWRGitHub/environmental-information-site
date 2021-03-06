import flask_login
from environmental_app.forms import KickstarterForm
from flask_login.utils import login_required
from environmental_app.models import Kickstarter
from environmental_app import app, db, yelp_api
from flask import request, render_template, redirect, url_for, flash, Blueprint
from flask_googlemaps import Map
from flask_login import current_user
import requests
from environmental_app import db_sql


main = Blueprint("main", __name__)

@main.route('/')
def homepage():
    return render_template('home.html')

''' The code for the profile page '''
@main.route('/profile') #/<user_id>')
def profile(): #user_id):
    """Displays the user profile"""

    # profile_data = db.profile.find({})

    context = {
        "header_img": {
            'src':'https://wwww.environmental-info-site.com/img-name.jpg',
            'alt': "..."
        },
        'selfi': {
            'src':'https://wwww.environmental-info-site.com/img-name.jpg',
            'alt': "..."
        },
        'name': "Kickstart Name",
        'name_info': 'Environmentally friendly',
        'address': ["Address line 1", "Adress line 2"],
        'info': "Kickstart name is a new environment subgraoup that focuses on weekend community services for highway cleanup",
        'people_like_this': {
            'count': 37762, 
            'frind_count': 25,
            'img': [
                {
                    'src':'https://wwww.environmental-info-site.com/img-name.jpg',
                    'alt': "..."
                },
                {
                    'src':'https://wwww.environmental-info-site.com/img-name.jpg',
                    'alt': "..."
                },
                {
                    'src':'https://wwww.environmental-info-site.com/img-name.jpg',
                    'alt': "..."
                },
                {
                    'src':'https://wwww.environmental-info-site.com/img-name.jpg',
                    'alt': "..."
                },
                {
                    'src':'https://wwww.environmental-info-site.com/img-name.jpg',
                    'alt': "..."
                },
                {
                    'src':'https://wwww.environmental-info-site.com/img-name.jpg',
                    'alt': "..."
                }
            ]
        },
        'folowing': 37822,
        'friends_participated': 43,
        'url': 'https://www.kickstartgroup.com/',
        'phone': 5555555555,
        'away': True,
        'email': "email@website.com",
        'open_hr': {'open': 800, 'close': 1700},
        'industry': 'Industry',
        'photos': [
            {
                    'src':'/static/img/ph.png',
                    'alt': "..."
                },
                {
                    'src':'/static/img/ph.png',
                    'alt': "..."
                },
                {
                    'src':'/static/img/ph.png',
                    'alt': "..."
                },
                {
                    'src':'/static/img/ph.png',
                    'alt': "..."
                },
                {
                    'src':'/static/img/ph.png',
                    'alt': "..."
                },
                {
                    'src':'/static/img/ph.png',
                    'alt': "..."
                }
        ],
        'videos': {
            'video': {
                    'src':'https://wwww.environmental-info-site.com/img-name.jpg',
                    'alt': "..."
                },
            'info': 'what is most important to you when se...',
            'views': 88,
            'date_added': "Yesterday at 14:03", 
        },
        'pinned_post': [
            {
                'user_name': 'Ben Chan',
                'user_img': {
                    'src':'',
                    'alt': "..."
                },
                'date_added': 'Yesterday at 14:03', 
                'details': "Amazing group! I was able to learn so much from you guys! It's because of y'all that I was motivated to start my own kickstart in my local comunity! Can't wait to inspire more people to be green! :)",
                'img_vid': {
                    'is_img': True,
                    'src':'/static/img/ph.png',
                    'alt': "..."
                },
                'like_count': 40,
                'comment_count': 1,
                'share': 1,
                'views': 1,
            }
        ],
        'posts': [
            
            {
                'user_name': 'Aldrin Brillante',
                'user_img': {
                    'src':'https://wwww.environmental-info-site.com/img-name.jpg',
                    'alt': "..."
                },
                'date_added': "Yesterday at 14:03",
                'details': "Amazing group! I was able to learn so much from you guys! It's because of y'all that I was motivated to start my own kickstart in my local comunity! Can't wait to inspire more people to be green! :)",
                'img_vid': {
                    'src':'https://wwww.environmental-info-site.com/img-name.jpg',
                    'alt': "..."
                },
                'like_count': 40,
                'comment_count': 3,
                'views': 0,
            },
        ]
    }
    return render_template('profile.html', **context)



''' The code for the kickstarter routes + database is below '''
@main.route('/kickstarter')
def kick_list():
    """Displays the list of startups"""

    startups = Kickstarter.query.all()
    return render_template('startup_list.html', startups=startups ) 


@main.route('/create_startup', methods=['GET', 'POST'])
@login_required
def create_startup():
    form = KickstarterForm()
    if form.validate_on_submit():

        new_startup = Kickstarter(
            title = form.title.data,
            photo_url= form.photo_url.data,
            video_url=form.video_url.data,
            created_by = flask_login.current_user,
            end_date=form.end_date.data,
            money_goal=form.money_goal.data,
            description=form.description.data
        )
        db_sql.session.add(new_startup)
        db_sql.session.commit()

        return redirect(url_for('main.kick_list'))
    else:
        return render_template('create_startup.html', form=form)

@main.route('/startup/<startup_id>', methods=['GET', 'POST'])
@login_required
def details(startup_id):
    startup = Kickstarter.query.get(startup_id)
    return render_template('details.html', startup=startup)


@main.route('/search_store', methods=['GET', 'POST'])
def search_store():
    ''' Search for local stores '''
    # initializes an empty list that will store a list of dictionaries that contain the coordinates for the
    # markers parameter of business_map
    coordinates_list = []

    if request.method == 'POST':
        location = ''
        # obtains the user's current ip address
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            response = requests.get("http://ip-api.com/json")
            js = response.json()

            city = js['city']
            lat = js['lat']
            lng = js['lon']

        else:
            ip = request.environ['HTTP_X_FORWARDED_FOR']
            response = requests.get(f"http://ip-api.com/json/{ip}")
            js = response.json()

            city = js['city']
            lat = js['lat']
            lng = js['lon']
    
        store_name = request.form.get('store_name')

        # yelp api that provides a list of stores with the category vegan near the user's current latitude/longitude
        search_results = yelp_api.search_query(term = store_name, latitude = lat, longitude = lng, categories = "vegan")
        business_info = search_results['businesses']
        
        # stores pin image and all lat/lng of queried stores into a dictionary to be passed into the map and displayed on the page
        for coordinate in business_info:
            coordinates_dict = {}
            coordinates_dict['icon'] = "/static/img/leaf_pin.png"
            coordinates_dict['lat'] = coordinate['coordinates']['latitude']
            coordinates_dict['lng'] = coordinate['coordinates']['longitude']

            # appends dictionary entry into the list
            coordinates_list.append(coordinates_dict)

        # defines the parameters of the map that will be displayed on the web page
        business_map = Map(
            identifier = "test-map",
            style = "height:700px;width:700px;margin:0;",
            lat = lat,
            lng = lng,
            markers = coordinates_list
        )

        return render_template('display_store.html', business_info = business_info, business_map = business_map)

    else:
        return render_template('search_store.html')
