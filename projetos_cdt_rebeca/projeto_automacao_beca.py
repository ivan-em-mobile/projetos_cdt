import streamlit as st
import re
import json

st.set_page_config(page_title="Sorveteria Glacê", page_icon="🍦", layout="wide")

# ==========================================================
# 💰 ESTADO DA APLICAÇÃO (Memória do Servidor)
# ==========================================================

if "caixa" not in st.session_state:
    st.session_state.caixa = 500.00
if "vendas_dia" not in st.session_state:
    st.session_state.vendas_dia = 0
if "itens_vendidos" not in st.session_state:
    st.session_state.itens_vendidos = 0
if "sabores" not in st.session_state:
    st.session_state.sabores = {
        "Chocolate": [8.00, 140],
        "Morango": [8.00, 140],
        "Baunilha": [8.00, 140],
        "Coco": [9.00, 140],
        "Limão": [8.50, 140],
        "Blue Ice": [10.00, 140],
        "Flocos": [9.00, 140],
        "Brigadeiro": [10.00, 140],
        "Beijinho": [10.00, 140],
        "Nutella": [12.00, 140],
        "Oreo": [11.00, 140],
        "Açaí": [11.00, 140],
        "Leite Ninho": [11.00, 140],
        "Paçoca": [10.00, 140],
        "Pistache": [13.00, 140]
    }
if "historico" not in st.session_state:
    st.session_state.historico = [
        {"operacao": "Abertura", "detalhes": "Caixa inicial", "valor": "R$ 500,00"}
    ]
if "chat_mensagens" not in st.session_state:
    st.session_state.chat_mensagens = [
        {"remetente": "🍦 Sorveteria Glacê", "texto": "Olá! Seja bem-vindo(a)! 💙\nEu sou o atendimento automático da Glacê. Como posso ajudar?"}
    ]

# ==========================================================
# 💵 FUNÇÃO AUXILIAR
# ==========================================================

def dinheiro(valor):
    return f"R$ {valor:.2f}".replace(".", ",")

# ==========================================================
# 🍦 CABEÇALHO & CARDS
# ==========================================================

st.title("🍦 Sorveteria Glacê 🎀")
st.caption("Gestão da sorveteria 💙")

baixos = sum(1 for dados in st.session_state.sabores.values() if 0 < dados[1] <= 5)

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 CAIXA", dinheiro(st.session_state.caixa))
col2.metric("🛒 VENDAS", st.session_state.vendas_dia)
col3.metric("🍨 ITENS", st.session_state.itens_vendidos)
col4.metric("⚠️ ESTOQUE BAIXO", baixos)

st.divider()

# ==========================================================
# 📑 ABAS DA APLICAÇÃO
# ==========================================================

aba_vendas, aba_estoque, aba_extrato, aba_chat = st.tabs([
    "💰 Vendas", "📦 Estoque", "📋 Extrato", "💬 Chat"
])

# ---------------- ABAS: VENDAS ----------------
with aba_vendas:
    st.subheader("🛒 Nova Venda")
    
    with st.form("form_venda"):
        sabor = st.selectbox("🍨 Sabor:", list(st.session_state.sabores.keys()))
        qtd = st.number_input("🔢 Quantidade:", min_value=1, value=1, step=1)
        pagamento = st.selectbox("💳 Pagamento:", ["Pix", "Cartão de Crédito", "Cartão de Débito", "Dinheiro"])
        pago = st.number_input("💵 Valor entregue (se Dinheiro):", min_value=0.0, value=0.0, step=1.0)
        
        btn_vender = st.form_submit_button("✓ CONFIRMAR VENDA")
        
        if btn_vender:
            preco = st.session_state.sabores[sabor][0]
            estoque = st.session_state.sabores[sabor][1]
            total = preco * qtd
            
            if qtd > estoque:
                st.error(f"📦 Estoque insuficiente. Temos apenas {estoque} unidade(s).")
            elif pagamento == "Dinheiro" and pago < total:
                st.error("💵 Valor entregue é menor que o total da compra.")
            else:
                st.session_state.sabores[sabor][1] -= qtd
                st.session_state.caixa += total
                st.session_state.vendas_dia += 1
                st.session_state.itens_vendidos += qtd
                
                st.session_state.historico.append({
                    "operacao": "🛒 Venda",
                    "detalhes": f"{qtd}x {sabor} - {pagamento}",
                    "valor": dinheiro(total)
                })
                
                troco = pago - total if pagamento == "Dinheiro" else 0
                msg = f"✨ Venda realizada com sucesso! Total: {dinheiro(total)}"
                if pagamento == "Dinheiro":
                    msg += f" | Troco: {dinheiro(troco)}"
                st.success(msg)
                st.rerun()

# ---------------- ABAS: ESTOQUE ----------------
with aba_estoque:
    st.subheader("📦 Estoque")
    
    tabela = []
    for s, dados in st.session_state.sabores.items():
        status = "❌ Esgotado" if dados[1] == 0 else ("⚠️ Baixo" if dados[1] <= 5 else "✓ Normal")
        tabela.append({"Sabor": s, "Quantidade": dados[1], "Preço": dinheiro(dados[0]), "Status": status})
    
    st.dataframe(tabela, use_container_width=True)
    
    st.divider()
    st.subheader("Repor Estoque")
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        sabor_repor = st.selectbox("Sabor para repor:", list(st.session_state.sabores.keys()))
    with c2:
        qtd_repor = st.number_input("Quantidade:", min_value=1, value=10)
    with c3:
        st.write("")
        st.write("")
        if st.button("+ Adicionar"):
            st.session_state.sabores[sabor_repor][1] += qtd_repor
            st.session_state.historico.append({
                "operacao": "📦 Reposição",
                "detalhes": f"+{qtd_repor} unidades de {sabor_repor}",
                "valor": "-"
            })
            st.success(f"✨ {sabor_repor} recebeu +{qtd_repor} unidades.")
            st.rerun()

# ---------------- ABAS: EXTRATO ----------------
with aba_extrato:
    st.subheader("📋 Extrato de Operações")
    st.dataframe(list(reversed(st.session_state.historico)), use_container_width=True)

# ---------------- ABAS: CHAT ----------------
with aba_chat:
    st.subheader("💬 Atendimento")
    st.caption("Converse com a Sorveteria Glacê")
    
    # Exibir histórico do chat
    for msg in st.session_state.chat_mensagens:
        with st.chat_message("user" if msg["remetente"] == "👤 Você" else "assistant"):
            st.write(msg["texto"])
            
    # Entrada do chat
    if entrada := st.chat_input("Digite sua mensagem..."):
        st.session_state.chat_mensagens.append({"remetente": "👤 Você", "texto": entrada})
        
        texto = entrada.lower().strip()
        resposta = "Não consegui entender. 😅\n\nVocê pode escrever:\n• Cardápio\n• Quero 2 Chocolate\n• Suporte\n• Preços"
        
        if any(p in texto for p in ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite"]):
            resposta = "Olá! 💙😊\n\nPosso ajudar com seu pedido ou suporte."
        elif any(p in texto for p in ["cardápio", "cardapio", "sabores", "preços", "precos"]):
            lista = "\n".join(f"🍨 {sabor} — {dinheiro(dados[0])}" for sabor, dados in st.session_state.sabores.items())
            resposta = "Nosso cardápio é:\n\n" + lista
        elif any(p in texto for p in ["suporte", "problema", "reclamação", "reclamacao", "ajuda"]):
            resposta = "Claro! 😊\n\nDigite sua dúvida ou descreva o problema."
        elif any(p in texto for p in ["obrigado", "obrigada", "valeu", "thanks"]):
            resposta = "Por nada! 💙🍦"
        else:
            # Busca sabor no texto
            for sabor in st.session_state.sabores:
                if sabor.lower() in texto:
                    numeros = re.findall(r"\d+", texto)
                    qtd = int(numeros[0]) if numeros else 1
                    preco = st.session_state.sabores[sabor][0]
                    total = preco * qtd
                    resposta = f"Seu pedido ficou:\n\n🍨 {qtd}x {sabor}\n💰 Total: {dinheiro(total)}\n\nPara confirmar a compra no caixa, utilize a aba '💰 Vendas'."
                    break
                    
        st.session_state.chat_mensagens.append({"remetente": "🍦 Sorveteria Glacê", "texto": resposta})
        st.rerun()