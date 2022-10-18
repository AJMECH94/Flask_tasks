from flask import Flask, request, render_template
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy


config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}


app = Flask(__name__)
app.config['SECRET_KEY'] = 'e550fec4dbc38d360d226ca689004f4e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config.from_mapping(config)
cache = Cache(app)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"


@app.route('/set')
@cache.cached(timeout=500)
def set():
    return '<h1>Cache has benn set</h1>'



@app.route('/', methods=['GET', 'POST'])
@cache.cached(timeout=500)
def user():
    if request.method == 'POST':
        print(request.data)
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

    return render_template('index.html')



@app.route('/getuser')
def get():
    key = cache.get('user')
    print(key)
    return f'<h1>set value is {key}</h1>'


if __name__ == "__main__":
    app.run(debug=True)