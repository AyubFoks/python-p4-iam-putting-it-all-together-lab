from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api

try:
    from .config import Config
except ImportError:
    from config import Config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

try:
    from .models import User, Recipe
except ImportError:
    from models import User, Recipe


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    try:
        from .resources import Signup, Login, Logout, CheckSession, RecipeIndex
    except ImportError:
        from resources import Signup, Login, Logout, CheckSession, RecipeIndex
    api = Api(app)
    api.add_resource(Signup, '/signup')
    api.add_resource(Login, '/login')
    api.add_resource(Logout, '/logout')
    api.add_resource(CheckSession, '/check_session')
    api.add_resource(RecipeIndex, '/recipes')

    return app


app = create_app()

if __name__ == '__main__':
    app.run(port=5555, debug=True)
