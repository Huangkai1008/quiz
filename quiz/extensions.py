from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from quiz.client.redis import RedisClient

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
redis_cli = RedisClient()
