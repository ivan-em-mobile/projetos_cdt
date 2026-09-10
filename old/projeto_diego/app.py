from flask import Flask, request, render_template

app = Flask(__name__)

# PÁGINA INICIAL
@app.route("/")
def home():
    return render_template("index.html")


# PÁGINA CADASTRO
@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")


# CADASTRO FINALIZADO
@app.route("/cadastro_ok")
def cadastro_ok():
    return render_template("cadastro_ok.html")


# SISTEMA DE AGENDAMENTO
@app.route("/agendar", methods=["POST"])
def agendar():

    nome = request.form.get("nome")
    servico = request.form.get("servico")
    horario = request.form.get("horario")

    return f"""

    <h1 style='color:gold'>
    HORÁRIO AGENDADO 💈
    </h1>

    <hr>

    <h2>Cliente:</h2>
    <p>{nome}</p>

    <h2>Serviço:</h2>
    <p>{servico}</p>

    <h2>Horário:</h2>
    <p>{horario}</p>

    <br>

    <a href='/'>
    Voltar ao site
    </a>

    """


# TELA LOGIN
@app.route("/login")
def login():
    return render_template("login.html")


# VERIFICAR LOGIN
@app.route("/entrar", methods=["POST"])
def entrar():

    usuario = request.form.get("usuario")
    senha = request.form.get("senha")

    # LOGIN
    if usuario == "admin" and senha == "123":

        return """

        <h1 style='color:green'>
        LOGIN REALIZADO COM SUCESSO 💈
        </h1>

        <h2>
        Bem-vindo ao painel da Barbearia SMD
        </h2>

        <br>

        <a href='/'>
        Voltar ao site
        </a>

        """

    else:

        return """

        <h1 style='color:red'>
        Usuário ou senha incorretos
        </h1>

        <br>

        <a href='/login'>
        Tentar novamente
        </a>

        """


# INICIAR SERVIDOR
if __name__ == "__main__":
    app.run(debug=True)