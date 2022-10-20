from flask_migrate import Migrate
from src.app import create_app
from src.models import db
from datetime import timedelta

env_name = 'development'
app = create_app(env_name)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
@app.before_first_request
def create_tables():
  db.create_all()
db.init_app(app)

migrate = Migrate(app=app, db=db) # Registering database


if __name__ == '__main__':
  app.run()