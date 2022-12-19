from flask import Flask , render_template, request, redirect, session, flash
from forms import UserForm
from flask_debugtoolbar import DebugToolbarExtension
from precious import MY_PRECIOUS
from models import connect_db, db, User
# import pdb;pdb.set_trace()
from sqlalchemy.exc import IntegrityError
import requests

#  What can I do with the returning JSON file i see? I just want to use it to make a simple list in which I hope to continue on with styling the app and making it work. 

app = Flask(__name__)
app.debug = True
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///capstone1"
app.config["SQLACHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLACLCHEMY_ECHO"] = True
app.config['SECRET_KEY'] = "rohan"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

debug = DebugToolbarExtension(app)



BASE_URL_API = 'https://the-one-api.dev/v2'
# include precious in api calls. The response format for all datasets is JSON
# header = {'Authorization': 'Bearer MY_PRECIOUS' }

# handeling the basic UI portion
@app.route('/')
def homepage():
    """Welcome page to the API"""
    return render_template('homepage.html')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_user = User.register(username, password)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('register.html', form=form)
        session['user_id'] = new_user.id
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect('/')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['user_id'] = user.id
            return redirect('/')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)

# Now we can use the API information. Seems to work server sided, issues on the front end.


@app.route('/books')
def show_all_books():
    """Return list of all books."""

    header = {
        'accept-encoding': 'gzip, deflate'
    }

    url = f'{BASE_URL_API}/book'
   
    response = requests.request("GET", url, headers=header)
    
    data = response.json()
    
    fello = data["docs"][0]["name"]
    # print('Im here')
    towers = data["docs"][1]["name"]
    king = data["docs"][2]["name"]
    books = {'fello': fello, 'towers': towers, 'king': king}
    print(books)
    return render_template('books.html')


@app.route('/movies', methods = ["GET"])
def all_movie_titles():
    """Return list of all movies titles"""

    # will need to use authorization token

    url = f'{BASE_URL_API}movie'
    headers = {'Authorization': f"Bearer {MY_PRECIOUS}"
    }
    response = requests.request("GET", url, headers=headers)

    data = response.json()
    # print(response.text)
    # Hobbit series
    unex_jour = data["docs"][2]['name']
    des_smog = data["docs"][3]['name']
    five_army = data["docs"][4]['name']

    # Original trilogy
    rings = data["docs"][6]['name']
    towers = data["docs"][5]['name']
    king = data["docs"][7]['name']

    hobbit = unex_jour, des_smog, five_army
    lotr = rings, towers, king

    all_movies = hobbit, lotr
    
    print (all_movies)

def lord_of_rings_series():
    """Return original series titles"""
    url = f'{BASE_URL_API}movie'
    headers = {'Authorization': f"Bearer {MY_PRECIOUS}"
    }
    response = requests.request("GET", url, headers=headers)
    # return render_template("movies.html")

@app.route('/characters', methods = ['GET'])
def show_all_characters():
    """return list of all movies"""

    url = f'{BASE_URL_API}character'
    headers = {'Authorization': f"Bearer {MY_PRECIOUS}"
    }

    response = requests.request("GET", url, headers=headers)

    # print(response.text)

    # resp = request.get(f'{BASE_URL_API}character', 
    #         header=header)

    return render_template('characters.html')















