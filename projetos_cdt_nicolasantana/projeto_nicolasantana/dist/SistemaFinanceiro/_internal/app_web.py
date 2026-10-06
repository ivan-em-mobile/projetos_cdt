import streamlit as st
import pandas as pd
import datetime
import os
import services
from database import init_db

# Inicializa as tabelas do banco de dados
init_db()

st.set_page_config(
    page_title="Sistema Integrado de Monitoramento Financeiro",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sistema Integrado de Monitoramento Financeiro")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💱 Conversor & Moedas",
    "🎯 Metas & Orçamento",
    "📊 Gráficos & Resumos",
    "📄 Relatórios & Logs",
    "♿ Guia & Acessibilidade"
])

MOEDAS = {
    "BRL": "Real Brasileiro (R$)",
    "USD": "Dólar Americano ($)",
    "EUR": "Euro (€)",
    "GBP": "Libra Esterlina (£)",
    "JPY": "Iene Japonês (¥)",
    "CAD": "Dólar Canadense (C$)",
    "CHF": "Franco Suíço (CHF)",
    "AUD": "Dólar Australiano (A$)",
    "BTC": "Bitcoin (BTC)"
}

# -------------------------------------------------------------------
# ABA 1: CONVERSOR & COTAÇÕES
# -------------------------------------------------------------------
with tab1:
    st.header("💱 Painel de Cotações & Conversor Customizado")
    
    cotacoes = services.obter_cotacoes()
    
    if cotacoes:
        st.subheader("Cotações Principais (em relação ao BRL)")
        col1, col2, col3, col4 = st.columns(4)

        # Tratamento seguro contra KeyError / ausência de dados na nuvem
        usd = cotacoes.get('USDBRL') or cotacoes.get('USD-BRL', {})
        eur = cotacoes.get('EURBRL') or cotacoes.get('EUR-BRL', {})
        gbp = cotacoes.get('GBPBRL') or cotacoes.get('GBP-BRL', {})
        btc = cotacoes.get('BTCBRL') or cotacoes.get('BTC-BRL', {})

        col1.metric("Dólar (USD)", f"R$ {float(usd.get('bid', 0)):,.2f}" if usd.get('bid') else "N/A")
        col2.metric("Euro (EUR)", f"R$ {float(eur.get('bid', 0)):,.2f}" if eur.get('bid') else "N/A")
        col3.metric("Libra (GBP)", f"R$ {float(gbp.get('bid', 0)):,.2f}" if gbp.get('bid') else "N/A")
        col4.metric("Bitcoin (BTC)", f"R$ {float(btc.get('bid', 0)):,.2f}" if btc.get('bid') else "N/A")
    else:
        st.warning("Não foi possível carregar as cotações em tempo real no momento.")

    st.divider()
    st.subheader("🔄 Calculadora de Conversão")
    col_valor, col_de, col_para = st.columns([2, 2, 2])

    with col_valor:
        valor_input = st.number_input("Valor a converter:", min_value=0.01, value=100.0, step=10.0)

    with col_de:
        moeda_origem = st.selectbox(
            "De (Origem):",
            options=list(MOEDAS.keys()),
            format_func=lambda c: f"{c} - {MOEDAS[c]}",
            index=1
        )

    with col_para:
        moeda_destino = st.selectbox(
            "Para (Destino):",
            options=list(MOEDAS.keys()),
            format_func=lambda c: f"{c} - {MOEDAS[c]}",
            index=0
        )

    if st.button("🔄 Realizar Conversão", type="primary"):
        if moeda_origem == moeda_destino:
            st.info("As moedas de origem e destino selecionadas são iguais.")
        else:
            with st.spinner("Buscando taxa de câmbio atualizada..."):
                resultado, taxa = services.converter_moeda(moeda_origem, moeda_destino, valor_input)
                if resultado is not None:
                    st.success(f"### Resultado: {valor_input:,.2f} {moeda_origem} = **{resultado:,.2f} {moeda_destino}**")
                    st.caption(f"Taxa de câmbio aplicada: 1 {moeda_origem} = {taxa} {moeda_destino}")
                else:
                    st.error("Erro ao obter cotação. Tente novamente em instantes.")

# -------------------------------------------------------------------
# ABA 2: METAS & ORÇAMENTO
# -------------------------------------------------------------------
with tab2:
    st.header("🎯 Gestão de Metas Financeiras")
    
    col_add, col_aporte, col_del = st.columns([2, 2, 2])
    
    # 1. Formulário de Cadastro
    with col_add:
        with st.form("form_meta"):
            st.subheader("➕ Nova Meta")
            nome = st.text_input("Nome da Meta")
            cat = st.selectbox("Categoria", ["Reserva de Emergência", "Investimentos", "Viagem", "Tecnologia", "Educação", "Outros"])
            alvo = st.number_input("Valor Alvo (R$)", min_value=0.01, step=50.0)
            atual = st.number_input("Valor Atual (R$)", min_value=0.0, step=50.0)
            limite = st.date_input("Data Limite", datetime.date.today())
            
            if st.form_submit_button("Salvar Meta"):
                if nome:
                    services.salvar_meta(nome, cat, alvo, atual, str(limite))
                    st.success(f"Meta '{nome}' cadastrada!")
                    st.rerun()
                else:
                    st.error("Informe um nome para a meta.")

    metas = services.listar_metas()
    
    # 2. Aporte Rápido
    with col_aporte:
        st.subheader("💵 Fazer Aporte / Depósito")
        if metas:
            opcoes_metas_aporte = {f"{m['nome']} (Atual: R$ {m['valor_atual']:.2f})": m for m in metas}
            meta_sel_aporte = st.selectbox("Escolha a meta:", list(opcoes_metas_aporte.keys()), key="sb_aporte")
            valor_aporte = st.number_input("Valor do Aporte (R$):", min_value=0.01, step=50.0)
            
            if st.button("➕ Adicionar Aporte"):
                obj_meta = opcoes_metas_aporte[meta_sel_aporte]
                novo_saldo = obj_meta['valor_atual'] + valor_aporte
                services.atualizar_saldo_meta(obj_meta['id'], novo_saldo)
                st.success(f"Aporte de R$ {valor_aporte:.2f} adicionado à meta '{obj_meta['nome']}'!")
                st.rerun()
        else:
            st.info("Nenhuma meta para realizar aportes.")

    # 3. Exclusão de Meta
    with col_del:
        st.subheader("🗑️ Apagar Meta")
        if metas:
            opcoes_metas_del = {f"{m['id']} - {m['nome']}": m['id'] for m in metas}
            meta_sel_del = st.selectbox("Escolha para apagar:", list(opcoes_metas_del.keys()), key="sb_del")
            
            if st.button("❌ Excluir Meta", type="primary"):
                services.excluir_meta(opcoes_metas_del[meta_sel_del])
                st.success("Meta removida!")
                st.rerun()
        else:
            st.info("Nenhuma meta para exclusão.")

    st.divider()
    st.subheader("📋 Status Visual das Metas")
    if metas:
        for m in metas:
            pct = min(1.0, m['valor_atual'] / m['valor_alvo']) if m['valor_alvo'] > 0 else 0.0
            col_info, col_bar = st.columns([2, 4])
            with col_info:
                st.write(f"**{m['nome']}** ({m['categoria']})")
                st.caption(f"R$ {m['valor_atual']:,.2f} de R$ {m['valor_alvo']:,.2f} | Limite: {m['data_limite']}")
            with col_bar:
                st.progress(pct, text=f"{pct*100:.1f}% concluído")
    else:
        st.info("Sua lista de metas está vazia no momento.")

# -------------------------------------------------------------------
# ABA 3: GRÁFICOS & RESUMOS
# -------------------------------------------------------------------
with tab3:
    st.header("📊 Análise e Comparativo de Metas")
    metas = services.listar_metas()
    if metas:
        df = pd.DataFrame(metas)
        
        st.subheader("Comparativo Alvo vs Atual por Meta")
        st.bar_chart(df.set_index("nome")[["valor_alvo", "valor_atual"]])
        
        st.divider()
        st.subheader("Distribuição do Valor Alvo por Categoria")
        cat_group = df.groupby("categoria")[["valor_alvo", "valor_atual"]].sum()
        st.bar_chart(cat_group)
    else:
        st.info("Cadastre metas para visualizar as análises de desempenho.")

# -------------------------------------------------------------------
# ABA 4: RELATÓRIOS & LOGS
# -------------------------------------------------------------------
with tab4:
    st.header("📄 Exportação de Dados e Registros")
    metas = services.listar_metas()
    
    col_exp1, col_exp2 = st.columns(2)
    
    with col_exp1:
        st.subheader("📥 Relatório de Metas (CSV)")
        if metas:
            df_exp = pd.DataFrame(metas)
            csv = df_exp.to_csv(index=False).encode('utf-8')
            st.download_button("Baixar Metas (CSV)", data=csv, file_name="metas_financeiras.csv", mime="text/csv")
        else:
            st.info("Sem dados de metas cadastradas.")
            
    with col_exp2:
        st.subheader("📜 Histórico de Atividades (JSON Log)")
        if os.path.exists("activity_log.json"):
            with open("activity_log.json", "rb") as f:
                st.download_button("Baixar Logs do Sistema (JSON)", data=f, file_name="activity_log.json", mime="application/json")
        else:
            st.info("Nenhum registro de log gerado ainda.")

# -------------------------------------------------------------------
# ABA 5: GUIA DE ACESSIBILIDADE
# -------------------------------------------------------------------
with tab5:
    st.header("♿ Guia de Uso e Funcionalidades")
    st.markdown("""
    ### 1. Conversor & Moedas
    * Permite converter valores em tempo real entre as moedas globais mais utilizadas.
    
    ### 2. Metas & Orçamento
    * Permite criar metas, realizar aportes financeiros dinâmicos e apagar metas com visualização via barra de progresso.
    
    ### 3. Gráficos & Resumos
    * Exibe análises visuais comparativas e totais consolidados por categoria.
    
    ### 4. Relatórios & Logs
    * Permite o download da lista de metas em formato **CSV** e do log completo de interações do sistema em formato **JSON**.
    """)