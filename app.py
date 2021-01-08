from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# config environment variables for the project and database
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
app.config.update(
    SECRET_KEY='topsecret',
    # SQLALCHEMY_DATABASE_URI='<database>://<user_id>:<password>@<server>/<database_name>',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:LasVegas2021$@localhost/catalog_db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(app)


# @app.route('/index')

@app.route('/')
def hello_world():
    return 'Hello World from Ana Tulea!'


# Request object with query strings #
@app.route('/new/')  # http://127.0.0.1:5000/new/?greeting=hola!
def query_string(greeting="hello"):
    query_val = request.args.get('greeting', greeting)
    return '<h1> the greeting is: {0} </h1>'.format(query_val)


# Request object withOUT  query strings #
@app.route('/user')  # http://127.0.0.1:5000/user  ----->  Hello there default!
@app.route('/user/<name>')  # http://127.0.0.1:5000/user/Ana ----->  Hello there Ana!
def no_query_string(name='default'):
    return '<h1> Hello there {}! </h1>'.format(name)


# STRINGS
@app.route('/text/<string:name>')
def working_with_strings(name):
    return '<h1> here is a string: ' + name + '</h1>'


# NUMBERS (if a different type of data other than int is sent , will return a 'NOT FOUND" ERROR
@app.route('/numbers/<int:num>')  # http://127.0.0.1:5000/numbers/3 -----> the number you picked is: 3
def working_with_numbers(num):
    return '<h1> the number you picked is: ' + str(num) + '</h1>'


# MORE NUMBERS
@app.route('/add/<int:num1>/<int:num2>')  # http://127.0.0.1:5000/add/2/45 ---> the sum is : 47
def adding_integers(num1, num2):
    return '<h1>the sum is : {}'.format(num1 + num2) + '</h1>'


# FLOATS
@app.route('/product/<float:num1>/<float:num2>')  # http://127.0.0.1:5000/product/3.2/3.4 ---> the product is: 10.88
def product_two_numbers(num1, num2):
    return '<h1> the product is: {}'.format(num1 * num2) + '</h1>'


# USING TEMPLATES
@app.route('/temp')
def using_templates():
    return render_template('hello.html')


# JINJA TEMPLATES
@app.route('/watch')
def top_movies():
    movie_list = ['autopsy of jane doe',
                  'neon demon',
                  'ghost in a shell',
                  'kong: skull island',
                  'john wick 2',
                  'spiderman - homecoming']

    return render_template('movies.html',
                           movies=movie_list,
                           name='Harry')


@app.route('/tables')
def movies_plus():
    movies_dict = {'autopsy of jane doe': 02.14,
                   'neon demon': 3.20,
                   'ghost in a shell': 1.50,
                   'kong: skull island': 3.50,
                   'john wick 2': 02.52,
                   'spiderman - homecoming': 1.48}

    return render_template('tables.html',
                           movies=movies_dict,
                           name='Sally')


@app.route('/filters')
def filter_data():
    movies_dict = {'autopsy of jane doe': 02.14,
                   'neon demon': 3.20,
                   'ghost in a shell': 1.50,
                   'kong: skull island': 3.50,
                   'john wick 2': 02.52,
                   'spiderman - homecoming': 1.48}

    return render_template('filter_data.html',
                           movies=movies_dict,
                           name=None,
                           film='a christmas carol')


# Macros -->https://jinja.palletsprojects.com/en/2.11.x/templates/#macros
@app.route('/macros')
def jinja_macros():
    movies_dict = {'autopsy of jane doe': 02.14,
                   'neon demon': 3.20,
                   'ghost in a shell': 1.50,
                   'kong: skull island': 3.50,
                   'john wick 2': 02.52,
                   'spiderman - homecoming': 1.48}

    return render_template('using_macros.html',
                           movies=movies_dict)


# --------> WORKING WITH DATABASES <------------ #

# create Publication table
class Publication(db.Model):
    __tablename__ = 'publication'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

    # String representation of instance
    def __repr__(self):
        return 'Publisher is {}'.format(self.name)


# create book table
class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())

    # Relationship
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id):
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = book_format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return '{} by {}'.format(self.title, self.author)


if __name__ == '__main__':
    db.create_all()  # creates all the tables only if they don't exist. If tables are created this is skipped.
    app.run(debug=True)
