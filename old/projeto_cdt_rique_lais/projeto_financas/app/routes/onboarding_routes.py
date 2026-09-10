'''Rota do onboarding'''
from flask import Blueprint, render_template, request, redirect, url_for
from app.models.user import FinancialProfile
from app import db

onboarding_bp = Blueprint('onboarding', __name__)

@onboarding_bp.route('/', methods=['GET', 'POST'])
def onboarding():
    if request.method == 'POST':
        # Buscamos 'renda_mensal' ou 'renda' para garantir que capture o valor do HTML
        renda_raw = request.form.get('renda_mensal') or request.form.get('renda') or 0
        
        try:
            renda_final = float(renda_raw)
        except (ValueError, TypeError):
            renda_final = 0.0

        novo_perfil = FinancialProfile(
            nome=request.form.get('nome'),
            meta=request.form.get('meta'),
            renda_mensal=renda_final, 
            banco_principal=request.form.get('banco')
        )
        
        db.session.add(novo_perfil)
        db.session.commit()

        return redirect(url_for('dashboard.dashboard', profile_id=novo_perfil.id))
    
    return render_template('onboarding.html')