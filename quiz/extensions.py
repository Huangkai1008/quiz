from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
