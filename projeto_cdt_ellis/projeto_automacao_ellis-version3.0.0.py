"""
🍦 Sorveteria Glacê — sistema de gestão (Gradio)

Como executar no Visual Studio Code:
    1. pip install gradio
    2. python sorveteria_glace.py
    3. Abra http://127.0.0.1:7860 (abre sozinho no navegador)
"""

import re
import threading
import unicodedata

import gradio as gr

# O Gradio 6 mudou onde 'theme' e 'css' são passados (agora no launch) e
# removeu o parâmetro 'type' do Chatbot. Este código funciona nas duas versões.
GRADIO_MAJOR = int(gr.__version__.split(".")[0])

# ==========================================================
# 💰 ESTADO DA APLICAÇÃO (Memória Global)
# ==========================================================
# O Gradio atende várias requisições em threads diferentes, então todas as
# alterações no estado passam por este lock para evitar condições de corrida.
LOCK = threading.Lock()

caixa = 500.00
vendas_dia = 0
itens_vendidos = 0

sabores = {
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
    "Pistache": [13.00, 140],
}

historico = [
    {"Operação": "Abertura", "Detalhes": "Caixa inicial", "Valor": "R$ 500,00"}
]

LIMITE_ESTOQUE_BAIXO = 5


# ==========================================================
# 💵 FUNÇÕES AUXILIARES
# ==========================================================
def dinheiro(valor):
    """Formata valores no padrão brasileiro: R$ 1.234,50."""
    texto = f"{valor:,.2f}"  # 1,234.50
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def normalizar(texto):
    """Minúsculas e sem acentos, para comparar 'Limão' com 'limao'."""
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto.lower().strip()


def contem_palavra(texto, palavras):
    """True se alguma das palavras aparece como palavra inteira no texto.
    Evita falsos positivos como 'ola' dentro de 'chocolate'."""
    padrao = r"\b(" + "|".join(re.escape(p) for p in palavras) + r")\b"
    return re.search(padrao, texto) is not None


# ==========================================================
# 📊 GERADORES DE DADOS PARA A TELA
# ==========================================================
def obter_metricas():
    """Indicadores do topo da página."""
    baixos = sum(1 for _, est in sabores.values() if est <= LIMITE_ESTOQUE_BAIXO)
    return (
        f"💰 Caixa: {dinheiro(caixa)}",
        f"🛒 Vendas: {vendas_dia}",
        f"🍨 Itens Vendidos: {itens_vendidos}",
        f"⚠️ Estoque Baixo: {baixos}",
    )


def gerar_tabela_estoque():
    tabela = []
    for sabor, (preco, estoque) in sabores.items():
        if estoque == 0:
            status = "❌ Esgotado"
        elif estoque <= LIMITE_ESTOQUE_BAIXO:
            status = "⚠️ Baixo"
        else:
            status = "✓ Normal"
        tabela.append([sabor, estoque, dinheiro(preco), status])
    return tabela


def gerar_extrato():
    return [[h["Operação"], h["Detalhes"], h["Valor"]] for h in reversed(historico)]


def atualizar_tudo():
    """Atualiza métricas, estoque e extrato (usado ao abrir/recarregar a página)."""
    return (*obter_metricas(), gerar_tabela_estoque(), gerar_extrato())


# ==========================================================
# ⚙️ LÓGICA DO NEGÓCIO
# ==========================================================
def realizar_venda(sabor, qtd, pagamento, pago):
    """Valida e processa a venda. Retorna (mensagem, métricas..., estoque, extrato)."""
    global caixa, vendas_dia, itens_vendidos

    with LOCK:
        if sabor not in sabores:
            return ("❌ Selecione um sabor válido.", *atualizar_tudo())

        # gr.Number devolve None quando o campo fica vazio
        if qtd is None or qtd < 1:
            return ("❌ Informe uma quantidade maior que zero.", *atualizar_tudo())
        qtd = int(qtd)

        preco, estoque_atual = sabores[sabor]
        total = round(preco * qtd, 2)

        if qtd > estoque_atual:
            return (
                f"❌ Estoque insuficiente. Temos apenas {estoque_atual} unidade(s).",
                *atualizar_tudo(),
            )

        if pagamento == "Dinheiro":
            pago = pago or 0.0
            if pago < total:
                return (
                    f"❌ Valor entregue ({dinheiro(pago)}) é menor que o total ({dinheiro(total)}).",
                    *atualizar_tudo(),
                )

        sabores[sabor][1] -= qtd
        caixa += total
        vendas_dia += 1
        itens_vendidos += qtd

        historico.append({
            "Operação": "🛒 Venda",
            "Detalhes": f"{qtd}x {sabor} - {pagamento}",
            "Valor": dinheiro(total),
        })

        msg = f"✨ Venda realizada com sucesso!\nTotal: {dinheiro(total)}"
        if pagamento == "Dinheiro":
            msg += f" | Troco: {dinheiro(round(pago - total, 2))}"

        return (msg, *atualizar_tudo())


def repor_estoque(sabor, qtd):
    """Adiciona unidades ao estoque de um sabor."""
    with LOCK:
        if sabor not in sabores:
            return ("❌ Selecione um sabor válido.", *atualizar_tudo())

        if qtd is None or qtd < 1:
            return ("❌ Informe uma quantidade maior que zero.", *atualizar_tudo())
        qtd = int(qtd)

        sabores[sabor][1] += qtd
        historico.append({
            "Operação": "📦 Reposição",
            "Detalhes": f"+{qtd} unidades de {sabor}",
            "Valor": "-",
        })
        return (f"✨ {sabor} recebeu +{qtd} unidades.", *atualizar_tudo())


# ==========================================================
# 💬 ATENDIMENTO AUTOMÁTICO
# ==========================================================
def responder_chat(mensagem, chat_history):
    """Responde à mensagem do cliente (formato de mensagens: role/content)."""
    chat_history = chat_history or []

    if not mensagem or not mensagem.strip():
        return "", chat_history

    texto = normalizar(mensagem)
    resposta = None

    # 1) Cardápio
    if contem_palavra(texto, ["cardapio", "sabores", "precos", "preco"]):
        lista = "\n".join(
            f"🍨 {sabor} — {dinheiro(dados[0])}" for sabor, dados in sabores.items()
        )
        resposta = "Nosso cardápio é:\n\n" + lista

    # 2) Pedido ("quero 2 chocolate"): vem antes da saudação para que
    #    "oi, quero 2 oreo" seja tratado como pedido.
    if resposta is None:
        for sabor, (preco, estoque) in sabores.items():
            if re.search(rf"\b{re.escape(normalizar(sabor))}s?\b", texto):
                numeros = re.findall(r"\d+", texto)
                qtd = int(numeros[0]) if numeros else 1
                if qtd < 1:
                    resposta = "A quantidade precisa ser de pelo menos 1. 😊"
                elif qtd > estoque:
                    resposta = (
                        f"Poxa, temos só {estoque} unidade(s) de {sabor} no momento. 😢"
                    )
                else:
                    resposta = (
                        f"Seu pedido ficou:\n\n🍨 {qtd}x {sabor}\n"
                        f"💰 Total: {dinheiro(preco * qtd)}\n\n"
                        "Para confirmar a compra no caixa, utilize a aba '💰 Vendas'."
                    )
                break

    # 3) Suporte
    if resposta is None and contem_palavra(
        texto, ["suporte", "problema", "reclamacao", "ajuda"]
    ):
        resposta = "Claro! 😊\n\nDigite sua dúvida ou descreva o problema."

    # 4) Agradecimento
    if resposta is None and contem_palavra(texto, ["obrigado", "obrigada", "valeu", "thanks"]):
        resposta = "Por nada! 🍦💖"

    # 5) Saudação
    if resposta is None and contem_palavra(
        texto, ["oi", "ola", "bom dia", "boa tarde", "boa noite"]
    ):
        resposta = "Olá! 💕😊\n\nPosso ajudar com o seu pedido ou suporte."

    # 6) Não entendeu
    if resposta is None:
        resposta = (
            "Não consegui entender. 😅\n\nVocê pode escrever:\n"
            "• Cardápio\n• Quero 2 Chocolate\n• Suporte\n• Preços"
        )

    chat_history.append({"role": "user", "content": mensagem})
    chat_history.append({"role": "assistant", "content": resposta})
    return "", chat_history


# ==========================================================
# 🎨 ESTILIZAÇÃO CSS (Tons Claros: Rosa, Marsala, Creme)
# ==========================================================
estilo_css = """
/* Fundo claro geral */
.gradio-container {
    background-color: #FAF9F6 !important;
    color: #4A2E35 !important;
}

/* Títulos */
#titulo-principal h1 {
    color: #6B2D5C !important;
    text-align: center;
    font-weight: 800;
}
#subtitulo h3 {
    color: #800020 !important;
    text-align: center;
}

/* Botões principais em tom Marsala */
button.primary {
    background: linear-gradient(135deg, #6B2D5C 0%, #800020 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: bold !important;
}
button.primary:hover {
    background: linear-gradient(135deg, #800020 0%, #6B2D5C 100%) !important;
}

/* Abas em Creme e Rosa Pastel */
button[role="tab"] {
    background-color: #FFFDD0 !important;
    color: #6B2D5C !important;
    border-radius: 8px 8px 0 0 !important;
    font-weight: 600 !important;
}
button[role="tab"][aria-selected="true"] {
    background-color: #FFD1DC !important;
    color: #800020 !important;
    border-bottom: 3px solid #800020 !important;
}

/* Campos de entrada com fundo claro e borda rosa */
input, textarea, select {
    background-color: #FFFFFF !important;
    color: #4A2E35 !important;
    border: 1px solid #FFD1DC !important;
}

/* Tabelas */
table th {
    background-color: #6B2D5C !important;
    color: #FFFFFF !important;
}
table td {
    background-color: #FFFFFF !important;
    color: #4A2E35 !important;
}
"""

tema_claro = gr.themes.Soft(primary_hue="pink", neutral_hue="rose")

# ==========================================================
# 🖼️ INTERFACE GRÁFICA (Gradio)
# ==========================================================
blocks_kwargs = {"title": "Sorveteria Glacê"}
launch_kwargs = {"inbrowser": True}
if GRADIO_MAJOR >= 6:
    launch_kwargs.update(theme=tema_claro, css=estilo_css)
else:
    blocks_kwargs.update(theme=tema_claro, css=estilo_css)

chatbot_kwargs = {}
if GRADIO_MAJOR < 6:
    chatbot_kwargs["type"] = "messages"

with gr.Blocks(**blocks_kwargs) as app:
    gr.Markdown("# 🍦 Sorveteria Glacê 🎀", elem_id="titulo-principal")
    gr.Markdown("### Gestão Elegante da Sorveteria 💖", elem_id="subtitulo")

    # Métricas no topo
    metricas_iniciais = obter_metricas()
    with gr.Row():
        m_caixa = gr.Textbox(value=metricas_iniciais[0], show_label=False, interactive=False)
        m_vendas = gr.Textbox(value=metricas_iniciais[1], show_label=False, interactive=False)
        m_itens = gr.Textbox(value=metricas_iniciais[2], show_label=False, interactive=False)
        m_baixos = gr.Textbox(value=metricas_iniciais[3], show_label=False, interactive=False)

    with gr.Tabs():
        # --- Aba 1: Vendas ---
        with gr.Tab("💰 Vendas"):
            gr.Markdown("### 🛒 Nova Venda")
            with gr.Row():
                input_sabor = gr.Dropdown(choices=list(sabores.keys()), value="Chocolate", label="🍨 Sabor:")
                input_qtd = gr.Number(value=1, precision=0, minimum=1, label="🔢 Quantidade:")
            with gr.Row():
                input_pagamento = gr.Dropdown(
                    choices=["Pix", "Cartão de Crédito", "Cartão de Débito", "Dinheiro"],
                    value="Pix",
                    label="💳 Pagamento:",
                )
                input_pago = gr.Number(value=0.0, minimum=0, label="💵 Valor entregue (se Dinheiro):")

            btn_vender = gr.Button("✓ CONFIRMAR VENDA", variant="primary")
            out_venda_status = gr.Textbox(label="Resultado da Operação", interactive=False)

        # --- Aba 2: Estoque ---
        with gr.Tab("📦 Estoque"):
            gr.Markdown("### 📦 Estoque Atual")
            tabela_estoque = gr.Dataframe(
                headers=["Sabor", "Quantidade", "Preço", "Status"],
                value=gerar_tabela_estoque(),
                interactive=False,
            )

            gr.Markdown("### Repor Estoque")
            with gr.Row():
                repor_sabor = gr.Dropdown(choices=list(sabores.keys()), value="Chocolate", label="Sabor para repor:")
                repor_qtd = gr.Number(value=10, precision=0, minimum=1, label="Quantidade:")
                btn_repor = gr.Button("+ Adicionar Reposição", variant="primary")

            out_repor_status = gr.Textbox(label="Status da Reposição", interactive=False)

        # --- Aba 3: Extrato ---
        with gr.Tab("📋 Extrato"):
            gr.Markdown("### 📋 Extrato de Operações")
            btn_atualizar_extrato = gr.Button("🔄 Atualizar Extrato")
            tabela_extrato = gr.Dataframe(
                headers=["Operação", "Detalhes", "Valor"],
                value=gerar_extrato(),
                interactive=False,
            )

        # --- Aba 4: Chat ---
        with gr.Tab("💬 Chat"):
            gr.Markdown("### 💬 Atendimento Automático")
            chatbot = gr.Chatbot(
                label="Sorveteria Glacê",
                value=[{
                    "role": "assistant",
                    "content": "Olá! Seja bem-vindo(a)! 💖\nEu sou o atendimento automático da Glacê. Como posso ajudar?",
                }],
                **chatbot_kwargs,
            )
            msg_input = gr.Textbox(placeholder="Digite sua mensagem...", show_label=False)
            btn_enviar = gr.Button("Enviar", variant="primary")

    # ------------------------------------------------------
    # Eventos: ficam DEPOIS de todos os componentes existirem,
    # pois dependem de tabela_estoque e tabela_extrato.
    # ------------------------------------------------------
    saidas_gerais = [m_caixa, m_vendas, m_itens, m_baixos, tabela_estoque, tabela_extrato]

    btn_vender.click(
        fn=realizar_venda,
        inputs=[input_sabor, input_qtd, input_pagamento, input_pago],
        outputs=[out_venda_status, *saidas_gerais],
    )

    btn_repor.click(
        fn=repor_estoque,
        inputs=[repor_sabor, repor_qtd],
        outputs=[out_repor_status, *saidas_gerais],
    )

    btn_atualizar_extrato.click(fn=gerar_extrato, outputs=tabela_extrato)

    btn_enviar.click(fn=responder_chat, inputs=[msg_input, chatbot], outputs=[msg_input, chatbot])
    msg_input.submit(fn=responder_chat, inputs=[msg_input, chatbot], outputs=[msg_input, chatbot])

    # Ao recarregar a página (F5), mostra o estado atual real em vez dos valores iniciais.
    app.load(fn=atualizar_tudo, outputs=saidas_gerais)


if __name__ == "__main__":
    app.launch(**launch_kwargs)