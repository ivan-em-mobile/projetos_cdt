from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from .config import Config  

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Carrega as configurações oficiais
    app.config.from_object(Config)

    # Inicializa as extensões
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Importa e registra as rotas (Blueprints)
    from app.routes.auth_routes import auth  
    from app.routes.onboarding_routes import onboarding_bp
    from app.routes.dashboard_routes import dashboard_bp  

    app.register_blueprint(auth)
    app.register_blueprint(onboarding_bp)
    app.register_blueprint(dashboard_bp)

    # Cria o banco de dados sqlite se ele não existir
    with app.app_context():
        db.create_all()

    return app