from app import app

app.config['SECRET_KEY'] = 't1NP63m4wnBg6nyHYKfmc2TpCOGI4nss'
app.config['SESSION_TYPE'] = 'memcached'
app.run()