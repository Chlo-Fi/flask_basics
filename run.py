from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config.update(
    SECRET_KEY='topsecret',
    SQLALCHEMY_DATABASE_URI='postgresql://chloe:TopSecret!42@localhost/catalog_db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(app)

@app.route('/')
def homepage():
    return 'Welcome to the Home Page!'

# By typing in the web address/new/?greeting=howdy, this would return "the greeting is:howdy", otherwise its hello
@app.route('/new/')
def query_strings(greeting='hello'):
    query_val = request.args.get('greeting', greeting)
    return '<h1> the greeting is: {0} </h1>'.format(query_val)

# Passing Variables into URL
@app.route('/user')
@app.route('/user/<name>')
def no_query_strings(name='Guest'):
    return '<h1> hello there, {}! </h1>'.format(name)

# String
@app.route('/text/<string:name>')
def working_with_strings(name):
    return 'Here is a string:' + name

# int
@app.route('/numbers/<int:num>')
def working_with_ints(num):
    return 'The number you picked is:{}'.format(num)

# adding ints
@app.route('/add/<int:num1>/<int:num2>')
def adding_integers(num1, num2):
    return 'The sum is: {}'.format((num1 + num2))

# floats - NOTE: The numbers must be floats for this to work
@app.route('/product/<float:num1>/<float:num2>')
def product_two_numbers(num1, num2):
    return 'The product is: {}'.format((num1 * num2))

# Using Templates
@app.route('/temp')
def using_templates():
    return render_template('base.html')

# Jinja Templates
@app.route('/watch')
def top_movies():
    movie_list = ['autopsy of jane doe',
                  'neon demon',
                  'ghost in a shell',
                  'skull island',
                  'john wick 2',
                  'spiderman - homecoming']

    return render_template('movies.html',
                           movies=movie_list,
                           name="Harry")

# Jinja 2 - Tables
@app.route('/table')
def movies_plus():
    movies_dict = {'autopsy of jane doe': 02.14,
                   'neon demon': 3.20,
                   'ghost in a shell': 1.50,
                   'kong: skull island': 3.50,
                   'john wick 2': 2.52,
                   'spiderman - homecoming': 1.48}
    return render_template('table_data.html',
                           movies=movies_dict,
                           name='Sally')

# Filtering Data
@app.route('/filters')
@app.route('/filters/<username>')
def filter_data(username=None):
    movies_dict = {'autopsy of jane doe': 02.14,
                   'neon demon': 3.20,
                   'ghost in a shell': 1.50,
                   'kong: skull island': 3.50,
                   'john wick 2': 2.52,
                   'spiderman - homecoming': 1.48}

    return render_template('filter_data.html',
                           movies=movies_dict,
                           name=username,
                           film='a christmas carol')

# Working with Jinja Macros
@app.route('/macros')
def jinja_macros():
    movies_dict = {'autopsy of jane doe': 02.14,
                   'neon demon': 3.20,
                   'ghost in a shell': 1.50,
                   'kong: skull island': 3.50,
                   'john wick 2': 2.52,
                   'spiderman - homecoming': 1.48}

    return render_template('using_macros.html', movies=movies_dict)

# Working with Sessions
@app.route('/session')
def session_data():
    if 'name' not in session:
        session['name'] = 'harry'
        return render_template('session.html', session=session, name=session['name'])


# Creating Tables with PostGreSQL
class Publication(db.Model):
    __tablename__ = 'publication'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Publisher is {}'.format(self.name)

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

    # Relationship to Publication Table
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id):

        # Notice that book id & pub date are not included as they'll be updated automatically
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.book_format = book_format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return '{} by {}'.format(self.title, self.author)




if __name__ == "__main__":
    print('Trying to connect to database...')
    try:
        db.create_all()
        print('Succesfully Connected!')
    except Exception as error:
        print("Didn't work... Keep Trying")
    print("Running App")
    app.run(debug=True)