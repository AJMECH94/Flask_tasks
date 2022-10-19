from flask import Flask
from database.db import initialize_db
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from resources.errors import errors
from flask_mail import Mail, Message
from celery import Celery
from flask import Flask, request, render_template, session, flash, redirect, url_for, jsonify
import redis

app = Flask(__name__)
api = Api(app, errors=errors)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'pawarajinkya97@gmail.com'
app.config['MAIL_PASSWORD'] = 'uswwjvjpqnhshycr'
app.config['MAIL_DEFAULT_SENDER'] = 'pawarajinkya97@gmail.com'
app.config['SECRET_KEY'] = 't1NP63m4wnBg6nyHYKfmc2TpCOGI4nss'
app.config['SESSION_TYPE'] = 'memcached'
# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/0'
redis = redis.Redis(host='redis', port=6379, decode_responses=True)
mail = Mail(app)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
from resources.routes import initialize_routes

app.config["MONGODB_SETTINGS"] = [
    {
        "db": "movieapp",
        "host": "mongodb_container",
        "port": 27017,
    }
]
initialize_db(app)
initialize_routes(api)


@celery.task
def send_async_email(email_data):
    """Background task to send an email with Flask-Mail."""
    msg = Message(email_data['subject'],
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email_data['to']])
    msg.body = email_data['body']
    with app.app_context():
        mail.send(msg)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', email=session.get('email', ''))
    email = request.form['email']
    session['email'] = email

    # send the email
    email_data = {
        'subject': 'Hello from Flask',
        'to': email,
        'body': 'This is a test email sent from a background Celery task.'
    }
    if request.form['submit'] == 'Send':
        # send right away
        send_async_email(email_data)
        flash('Sending email to {0}'.format(email))
    else:
        # send in one minute
        send_async_email.apply_async(args=[email_data], countdown=60)
        flash('An email will be sent to {0} in one minute'.format(email))

    return redirect(url_for('index'))