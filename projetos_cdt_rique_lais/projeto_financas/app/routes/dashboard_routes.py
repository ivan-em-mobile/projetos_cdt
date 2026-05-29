'''Rota do dashboard'''
from flask import Blueprint, render_template
from app.models.user import FinancialProfile  # Usando o modelo correto aqui!
from app import db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard/<int:profile_id>')
def dashboard(profile_id):
    # Busca o perfil correto gerado no onboarding
    usuario_banco = FinancialProfile.query.get_or_404(profile_id)
    
    renda_salva = usuario_banco.renda_mensal if usuario_banco.renda_mensal else 0.0
    
    # Monta o dicionário com a chave exata que o seu HTML original usa para calcular
    perfil_usuario = {
        'nome': usuario_banco.nome,
        'renda_mensal': float(renda_salva)
    }
    
    return render_template(
        'dashboard.html', 
        usuario=perfil_usuario, 
        renda_mensal=float(renda_salva)
    )