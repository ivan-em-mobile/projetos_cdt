from flask import Flask, render_template, request, redirect, session, Response
from models import (
    get_produtos,
    salvar_pedido,
    get_pedidos,
    verificar_login,
    atualizar_estoque,
    excluir_pedido,
    calcular_faturamento,
    verificar_estoque,
    diminuir_estoque,
    atualizar_status
)
import json
import os


app = Flask(__name__, template_folder="templates")
app.secret_key = "cafe123"


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("home.html")


# ---------------- PRODUTOS ----------------
@app.route("/produtos")
def produtos():
    categoria = request.args.get("categoria")
    lista = get_produtos(categoria)
    return render_template("produtos.html", produtos=lista)


# ---------------- ADD CARRINHO ----------------
@app.route("/add/<nome>/<preco>")
def add(nome, preco):
    nome = nome.replace("%20", " ")

    estoque = verificar_estoque(nome)
    if estoque <= 0:
        return f"{nome} está esgotado 😭"

    diminuir_estoque(nome)

    carrinho = session.get("carrinho", [])

    carrinho.append({
        "nome": nome,
        "preco": float(preco)
    })

    session["carrinho"] = carrinho

    return redirect("/produtos")


# ---------------- CARRINHO ----------------
@app.route("/carrinho")
def carrinho():
    itens = session.get("carrinho", [])
    total = sum(i["preco"] for i in itens)

    return render_template("carrinho.html", itens=itens, total=total)


# ---------------- PAGAMENTO ----------------
@app.route("/pagamento", methods=["GET", "POST"])
def pagamento():
    itens = session.get("carrinho", [])

    if request.method == "POST":
        return redirect("/finalizar")

    total = sum(i["preco"] for i in itens)

    return render_template("pagamento.html", total=total)


@app.route("/finalizar", methods=["GET", "POST"])
def finalizar():
    itens = session.get("carrinho", [])

    if request.method == "POST":
        cliente = request.form["cliente"]
        endereco = request.form["endereco"]
        email = request.form["email"]
        telefone = request.form["telefone"]
        pagamento = request.form["pagamento"]
        
        itens_com_obs = []
        
        # Coleta as observações e salva individualmente
        for idx, i in enumerate(itens):
            obs_item = request.form.get(f"obs_{idx}", "")
            
            # 1. Salva no seu banco de dados/models
            salvar_pedido(cliente, endereco, obs_item, i["nome"], i["preco"])
            
            # 2. Cria uma cópia do item contendo a observação para a sessão usar na tela
            item_copia = i.copy()
            item_copia["obs"] = obs_item
            itens_com_obs.append(item_copia)

        # Guardamos a lista ATUALIZADA com as observações na sessão
        session["pedido"] = {
           "status": "Recebido",
           "cliente": cliente,
           "endereco": endereco,
           "email": email,
           "telefone": telefone,
           "pagamento": pagamento,
           "itens": itens_com_obs
}

        session["carrinho"] = []
        return redirect("/pedido-finalizado")

    return render_template("finalizar.html", itens=itens)


# ---------------- PEDIDO FINALIZADO (CORRIGIDO) ----------------
@app.route("/pedido-finalizado")
def pedido_finalizado():
    pedido = session.get("pedido")
    return render_template("finalizado.html", pedido=pedido)


# ---------------- ACOMPANHAR PEDIDO (CORRIGIDO) ----------------
id="hnj9if"
@app.route("/acompanhar")
def acompanhar():

    pedido_sessao = session.get("pedido")

    if not pedido_sessao:
        return "Nenhum pedido encontrado ☕"

    pedidos = get_pedidos()

    pedido_encontrado = None

    for p in pedidos:

        # p[1] = cliente
        if p[1] == pedido_sessao["cliente"]:

            pedido_encontrado = {
                "id": p[0],
                "cliente": p[1],
                "endereco": p[2],
                "observacao": p[3],
                "produto": p[4],
                "preco": p[5],
                "status": p[6]
            }

    if not pedido_encontrado:
        return "Pedido não encontrado 😭"

    return render_template(
        "acompanhar.html",
        pedido=pedido_encontrado
    )


@app.route("/atualizar-status", methods=["POST"])
def atualizar_status_route():

    id_pedido = request.form["id_pedido"]
    status = request.form["status"]

    atualizar_status(id_pedido, status)

    return redirect("/admin")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        user = verificar_login(usuario, senha)

        if user:
            return redirect("/admin")
        else:
            return "Login inválido"

    return render_template("login.html")


# ---------------- ADMIN ----------------
@app.route("/admin")
def admin():
    pedidos = get_pedidos()
    produtos = get_produtos()
    faturamento = calcular_faturamento()

    return render_template("admin.html",
                           pedidos=pedidos,
                           produtos=produtos,
                           faturamento=faturamento)


# ---------------- JSON EXPORT ----------------
@app.route("/exportar-json")
def exportar_json():
    pedidos = get_pedidos()
    dados_json = json.dumps(pedidos, ensure_ascii=False)

    return Response(
        dados_json,
        mimetype="application/json",
        headers={"Content-Disposition": "attachment;filename=pedidos.json"}
    )


# ---------------- ESTOQUE ----------------
@app.route("/atualizar-estoque", methods=["POST"])
def atualizar_estoque_route():
    nome = request.form["nome"]
    estoque = request.form["estoque"]

    atualizar_estoque(nome, estoque)

    return redirect("/admin")


# ---------------- EXCLUIR PEDIDO ----------------
@app.route("/excluir-pedido/<int:id_pedido>")
def excluir_pedido_route(id_pedido):
    excluir_pedido(id_pedido)
    return redirect("/admin")


# ---------------- DEBUG (opcional) ----------------
print("PASTA ATUAL:", os.getcwd())
print("TEMPLATES EXISTE?:", os.path.exists("templates"))
print("FILES:", os.listdir())


# ---------------- RUN ----------------
app = app
if __name__ == "__main__":
    app.run(debug=True)
