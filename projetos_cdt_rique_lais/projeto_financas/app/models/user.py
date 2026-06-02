'''Criando a config para o usuário preencher'''
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    
    # MUDANÇA AQUI: nullable=True permite que o formulário de perguntas funcione sem pedir e-mail/senha
    username = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(60), nullable=True)
    
    # Campos do seu formulário
    nome = db.Column(db.String(100))
    meta = db.Column(db.String(100))
    renda_mensal = db.Column(db.Float, default=0.0)
    banco_principal = db.Column(db.String(50))

    def calcular_plano_503020(self):
        return {
            "essencial": self.renda_mensal * 0.5,
            "estilo_vida": self.renda_mensal * 0.3,
            "reserva_investimento": self.renda_mensal * 0.2
        }

# Isso mantém a compatibilidade com o resto do seu código
FinancialProfile = User

'''class FinancialProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    meta = db.Column(db.String(100)) # "Investir" ou "Organizar"
    renda_mensal = db.Column(db.Float)
    banco_principal = db.Column(db.String(50)) # "Nubank" ou "Inter"

    def calcular_plano_503020(self):
        # A mágica da matemática financeira
        return {
            "essencial": self.renda_mensal * 0.5,
            "estilo_vida": self.renda_mensal * 0.3,
            "reserva_investimento": self.renda_mensal * 0.2
        }
'''

