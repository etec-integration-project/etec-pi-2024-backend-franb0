import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.environ['DATABASE_USERNAME']}:{os.environ['DATABASE_PASSWORD']}@{os.environ['DATABASE_HOST']}/{os.environ['DATABASE_NAME']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

from .routes import bp as users_bp
app.register_blueprint(users_bp)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3003)
