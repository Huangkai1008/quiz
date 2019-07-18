from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
