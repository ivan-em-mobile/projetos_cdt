import os

# Mapeia o caminho subindo um nível para sair da pasta 'app' e salvar na raiz do projeto
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-secreta-muito-segura'
    
    # Define o local do banco de dados na raiz da pasta do projeto
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'finance.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False