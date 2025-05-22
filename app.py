from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db  # Импортируем db из models.py
from flask_moment import Moment
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://domain_user:secure_password_123@31.129.101.116/domain_monitor'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
moment = Moment(app)
# Инициализируем db с нашим приложением
db.init_app(app)
migrate = Migrate(app, db)

# Импорт моделей должен быть после создания db
from models import Domain

# Импорт и инициализация маршрутов после создания app
from routes import init_routes
init_routes(app)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
