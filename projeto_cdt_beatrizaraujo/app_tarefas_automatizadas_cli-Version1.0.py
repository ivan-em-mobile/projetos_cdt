import sqlite3
import json
import re
from datetime import datetime, date, timedelta
from faker import Faker
BANCO = "tarefas.db"
fake = Faker("pt_BR")
def conectar():
    return sqlite3.connect(BANCO)
def criar_banco():
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texto_original TEXT NOT NULL,
            titulo TEXT NOT NULL,
            responsavel TEXT NOT NULL,
            prazo TEXT NOT NULL,
            prioridade TEXT NOT NULL,
            categoria TEXT NOT NULL,
            status TEXT NOT NULL,
            criada_em TEXT NOT NULL
        )
    """)
    con.commit()
    con.close()
def identificar_responsavel(texto):
    texto = " ".join(texto.split())
    padroes = [
        r"\brespons[aá]vel\s*(?:é|e|:|-)?\s*(?:o|a)?\s*([A-Za-zÀ-ÿ]+)",
        r"\bpreciso\s+que\s+(?:o|a)?\s*([A-Za-zÀ-ÿ]+)\s+(?:faça|faca|fazer)\b",
        r"\bquero\s+que\s+(?:o|a)?\s*([A-Za-zÀ-ÿ]+)\s+(?:faça|faca|fazer)\b",
        r"\b(?:o|a)\s+([A-Za-zÀ-ÿ]+)\s+(?:precisa|deve|vai|irá|ira|fica|ficará|ficara)\b",
        r"\b([A-Za-zÀ-ÿ]+)\s+(?:precisa|deve|vai|irá|ira|fica|ficará|ficara)\b",
        r"\btarefa\s+para\s+(?:o|a)?\s*([A-Za-zÀ-ÿ]+)",
        r"\bpara\s*:\s*([A-Za-zÀ-ÿ]+)",
        r"\bé\s+para\s+(?:o|a)?\s*([A-Za-zÀ-ÿ]+)"
    ]
    proibidas = {
        "fazer", "faça", "faca", "precisa", "deve", "vai",
        "entregar", "enviar", "realizar", "preparar", "criar",
        "organizar", "finalizar", "relatório", "relatorio",
        "documento", "planilha", "arquivo", "projeto", "tarefa",
        "cliente", "reunião", "reuniao", "pagamento", "sistema",
        "código", "codigo", "hoje", "amanhã", "amanha", "sexta",
        "segunda", "terça", "terca", "quarta", "quinta", "sábado",
        "sabado", "domingo", "urgente", "importante", "até", "ate",
        "para", "com", "de", "do", "da"
    }
    for padrao in padroes:
        resultado = re.search(padrao, texto, re.IGNORECASE)
        if resultado:
            nome = resultado.group(1).strip()
            if nome.lower() not in proibidas:
                return nome.title()
    return "Não definido"
def identificar_prazo(texto):
    texto = texto.lower()
    hoje = date.today()
    if re.search(r"\bhoje\b", texto):
        return hoje.strftime("%d/%m/%Y")
    if re.search(r"\bamanh[ãa]\b", texto):
        return (hoje + timedelta(days=1)).strftime("%d/%m/%Y")
    resultado = re.search(
        r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b",
        texto
    )
    if resultado:
        try:
            data = date(
                int(resultado.group(3)),
                int(resultado.group(2)),
                int(resultado.group(1))
            )
            return data.strftime("%d/%m/%Y")
        except ValueError:
            return "Data inválida"
    resultado = re.search(
        r"\b(\d{1,2})[/-](\d{1,2})\b",
        texto
    )
    if resultado:
        dia = int(resultado.group(1))
        mes = int(resultado.group(2))
        try:
            data = date(hoje.year, mes, dia)
            if data < hoje:
                data = date(hoje.year + 1, mes, dia)
            return data.strftime("%d/%m/%Y")
        except ValueError:
            return "Data inválida"
    resultado = re.search(
        r"\b(?:até|ate)\s+(?:o\s+)?dia\s+(\d{1,2})",
        texto
    )
    if resultado:
        dia = int(resultado.group(1))
        try:
            data = date(hoje.year, hoje.month, dia)
            if data < hoje:
                if hoje.month == 12:
                    data = date(hoje.year + 1, 1, dia)
                else:
                    data = date(hoje.year, hoje.month + 1, dia)
            return data.strftime("%d/%m/%Y")
        except ValueError:
            return "Data inválida"
    dias = {
        "segunda": 0,
        "terça": 1,
        "terca": 1,
        "quarta": 2,
        "quinta": 3,
        "sexta": 4,
        "sábado": 5,
        "sabado": 5,
        "domingo": 6
    }
    for nome, numero in dias.items():
        if re.search(
            r"\b(?:até|ate|na|no|para|nesta|neste|"
            r"próxima|proxima|próximo|proximo)?\s*" +
            re.escape(nome),
            texto
        ):
            diferenca = (numero - hoje.weekday()) % 7
            if diferenca == 0:
                diferenca = 7
            data = hoje + timedelta(days=diferenca)
            return data.strftime("%d/%m/%Y")
    meses = {
        "janeiro": 1,
        "fevereiro": 2,
        "março": 3,
        "marco": 3,
        "abril": 4,
        "maio": 5,
        "junho": 6,
        "julho": 7,
        "agosto": 8,
        "setembro": 9,
        "outubro": 10,
        "novembro": 11,
        "dezembro": 12
    }
    for nome, numero in meses.items():
        resultado = re.search(
            rf"\b(?:dia\s+)?(\d{{1,2}})\s+de\s+{nome}\b",
            texto
        )
        if resultado:
            try:
                dia = int(resultado.group(1))
                data = date(hoje.year, numero, dia)
                if data < hoje:
                    data = date(hoje.year + 1, numero, dia)
                return data.strftime("%d/%m/%Y")
            except ValueError:
                return "Data inválida"
    return "Não definido"
def identificar_prioridade(texto):
    texto = texto.lower()
    alta = [
        "urgente",
        "urgência",
        "urgencia",
        "imediato",
        "imediatamente",
        "agora",
        "crítico",
        "critico",
        "pra ontem",
        "o quanto antes"
    ]
    media = [
        "importante",
        "prioridade",
        "atenção",
        "atencao"
    ]
    if any(p in texto for p in alta):
        return "ALTA"
    if any(p in texto for p in media):
        return "MÉDIA"
    return "BAIXA"
def identificar_categoria(texto):
    texto = texto.lower()
    if any(p in texto for p in [
        "relatório", "relatorio", "documento",
        "planilha", "arquivo", "pdf"
    ]):
        return "DOCUMENTOS"
    if any(p in texto for p in [
        "reunião", "reuniao", "call", "meeting", "encontro"
    ]):
        return "REUNIÃO"
    if any(p in texto for p in [
        "cliente", "venda", "vendas", "proposta"
    ]):
        return "CLIENTE / VENDAS"
    if any(p in texto for p in [
        "pagamento", "cobrança", "cobranca",
        "financeiro", "dinheiro"
    ]):
        return "FINANCEIRO"
    if any(p in texto for p in [
        "programar", "programação", "programacao",
        "código", "codigo", "sistema", "software", "computador"
    ]):
        return "TECNOLOGIA"
    return "GERAL"
def criar_titulo(texto):
    titulo = texto.strip()
    for inicio in [
        "preciso que",
        "precisamos que",
        "por favor",
        "favor",
        "quero que"
    ]:
        if titulo.lower().startswith(inicio):
            titulo = titulo[len(inicio):].strip()
    titulo = titulo.rstrip(".!?")
    if len(titulo) > 75:
        titulo = titulo[:75] + "..."
    return titulo
def interpretar(texto):
    return {
        "texto_original": texto,
        "titulo": criar_titulo(texto),
        "responsavel": identificar_responsavel(texto),
        "prazo": identificar_prazo(texto),
        "prioridade": identificar_prioridade(texto),
        "categoria": identificar_categoria(texto),
        "status": "PENDENTE",
        "criada_em": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
def inserir(tarefa):
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        INSERT INTO tarefas
        (texto_original, titulo, responsavel, prazo,
         prioridade, categoria, status, criada_em)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        tarefa["texto_original"],
        tarefa["titulo"],
        tarefa["responsavel"],
        tarefa["prazo"],
        tarefa["prioridade"],
        tarefa["categoria"],
        tarefa["status"],
        tarefa["criada_em"]
    ))
    con.commit()
    con.close()
def buscar():
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        SELECT id, titulo, responsavel, prazo,
               prioridade, categoria, status, criada_em
        FROM tarefas
        ORDER BY id DESC
    """)
    dados = cur.fetchall()
    con.close()
    return dados
def estatisticas():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM tarefas")
    total = cur.fetchone()[0]
    cur.execute("""
        SELECT COUNT(*) FROM tarefas
        WHERE status = 'PENDENTE'
    """)
    pendentes = cur.fetchone()[0]
    cur.execute("""
        SELECT COUNT(*) FROM tarefas
        WHERE status = 'CONCLUÍDA'
    """)
    concluidas = cur.fetchone()[0]
    cur.execute("""
        SELECT COUNT(*) FROM tarefas
        WHERE prioridade = 'ALTA'
    """)
    urgentes = cur.fetchone()[0]
    con.close()
    return total, pendentes, concluidas, urgentes
def criar_tarefa():
    print("\n" + "=" * 60)
    print("NOVA SOLICITAÇÃO")
    print("=" * 60)
    texto = input("\nDigite a solicitação: ").strip()
    if not texto:
        print("\nSolicitação vazia.")
        return
    tarefa = interpretar(texto)
    inserir(tarefa)
    print("\nTAREFA CRIADA")
    print("-" * 60)
    print(f"Título:       {tarefa['titulo']}")
    print(f"Responsável:  {tarefa['responsavel']}")
    print(f"Prazo:        {tarefa['prazo']}")
    print(f"Prioridade:   {tarefa['prioridade']}")
    print(f"Categoria:    {tarefa['categoria']}")
    print(f"Status:       {tarefa['status']}")
    print("-" * 60)
def listar_tarefas():
    tarefas = buscar()
    print("\n" + "=" * 100)
    print("MINHAS TAREFAS")
    print("=" * 100)
    if not tarefas:
        print("\nNenhuma tarefa cadastrada.")
        return
    for tarefa in tarefas:
        print(f"""
ID: {tarefa[0]}
Título: {tarefa[1]}
Responsável: {tarefa[2]}
Prazo: {tarefa[3]}
Prioridade: {tarefa[4]}
Categoria: {tarefa[5]}
Status: {tarefa[6]}
Criada em: {tarefa[7]}
{"-" * 100}""")
def concluir_tarefa():
    listar_tarefas()
    tarefas = buscar()
    if not tarefas:
        return
    try:
        id_tarefa = int(input("\nDigite o ID da tarefa que deseja concluir: "))
    except ValueError:
        print("\nID inválido.")
        return
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        UPDATE tarefas
        SET status = 'CONCLUÍDA'
        WHERE id = ?
    """, (id_tarefa,))
    if cur.rowcount == 0:
        print("\nTarefa não encontrada.")
    else:
        con.commit()
        print("\nTarefa concluída com sucesso.")
    con.close()
def excluir_tarefa():
    listar_tarefas()
    tarefas = buscar()
    if not tarefas:
        return
    try:
        id_tarefa = int(input("\nDigite o ID da tarefa que deseja excluir: "))
    except ValueError:
        print("\nID inválido.")
        return
    con = conectar()
    cur = con.cursor()
    cur.execute(
        "SELECT titulo FROM tarefas WHERE id = ?",
        (id_tarefa,)
    )
    tarefa = cur.fetchone()
    if not tarefa:
        print("\nTarefa não encontrada.")
        con.close()
        return
    confirmacao = input(
        f'\nDeseja realmente excluir "{tarefa[0]}"? (s/n): '
    ).strip().lower()
    if confirmacao != "s":
        print("\nExclusão cancelada.")
        con.close()
        return
    cur.execute(
        "DELETE FROM tarefas WHERE id = ?",
        (id_tarefa,)
    )
    con.commit()
    con.close()
    print("\nTarefa excluída com sucesso.")
def exportar():
    dados = []
    for tarefa in buscar():
        dados.append({
            "id": tarefa[0],
            "titulo": tarefa[1],
            "responsavel": tarefa[2],
            "prazo": tarefa[3],
            "prioridade": tarefa[4],
            "categoria": tarefa[5],
            "status": tarefa[6],
            "criada_em": tarefa[7]
        })
    nome_arquivo = input(
        "\nNome do arquivo para exportar [tarefas.json]: "
    ).strip()
    if not nome_arquivo:
        nome_arquivo = "tarefas.json"
    if not nome_arquivo.endswith(".json"):
        nome_arquivo += ".json"
    with open(
        nome_arquivo,
        "w",
        encoding="utf-8"
    ) as arquivo:
        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=4
        )
    print(f"\nTarefas exportadas para {nome_arquivo}.")
def importar():
    nome_arquivo = input(
        "\nNome do arquivo JSON para importar: "
    ).strip()
    if not nome_arquivo:
        print("\nNome de arquivo inválido.")
        return
    try:
        with open(
            nome_arquivo,
            "r",
            encoding="utf-8"
        ) as arquivo:
            dados = json.load(arquivo)
        quantidade = 0
        for tarefa in dados:
            nova = {
                "texto_original": tarefa.get(
                    "texto_original",
                    tarefa.get(
                        "titulo",
                        "Tarefa importada"
                    )
                ),
                "titulo": tarefa.get(
                    "titulo",
                    "Tarefa importada"
                ),
                "responsavel": tarefa.get(
                    "responsavel",
                    "Não definido"
                ),
                "prazo": tarefa.get(
                    "prazo",
                    "Não definido"
                ),
                "prioridade": tarefa.get(
                    "prioridade",
                    "BAIXA"
                ),
                "categoria": tarefa.get(
                    "categoria",
                    "GERAL"
                ),
                "status": tarefa.get(
                    "status",
                    "PENDENTE"
                ),
                "criada_em": tarefa.get(
                    "criada_em",
                    datetime.now().strftime(
                        "%d/%m/%Y %H:%M"
                    )
                )
            }
            inserir(nova)
            quantidade += 1
        print(f"\n{quantidade} tarefa(s) importada(s) com sucesso.")
    except FileNotFoundError:
        print("\nArquivo não encontrado.")
    except json.JSONDecodeError:
        print("\nO arquivo não contém um JSON válido.")
    except Exception as erro:
        print(f"\nErro ao importar: {erro}")
def gerar_faker():
    atividades = [
        "entregar o relatório",
        "organizar o documento",
        "preparar a planilha",
        "enviar a proposta para o cliente",
        "finalizar o projeto"
    ]
    for atividade in atividades:
        nome = fake.first_name()
        data = fake.date_between(
            start_date="+1d",
            end_date="+30d"
        )
        texto = (
            f"{nome} precisa {atividade} "
            f"até {data.strftime('%d/%m/%Y')}."
        )
        inserir(
            interpretar(texto)
        )
    print("\n5 tarefas de teste foram criadas com Faker.")
def mostrar_estatisticas():
    total, pendentes, concluidas, urgentes = estatisticas()
    print("\n" + "=" * 50)
    print("ESTATÍSTICAS")
    print("=" * 50)
    print(f"\nTotal de tarefas: {total}")
    print(f"Pendentes:        {pendentes}")
    print(f"Concluídas:       {concluidas}")
    print(f"Alta prioridade:  {urgentes}")
def mostrar_menu():
    print("\n")
    print("╔══════════════════════════════════════════════════════╗")
    print("║             CAIXA DE ENTRADA → AÇÃO                 ║")
    print("╚══════════════════════════════════════════════════════╝")
    print()
    print("1. Nova solicitação")
    print("2. Minhas tarefas")
    print("3. Concluir tarefa")
    print("4. Excluir tarefa")
    print("5. Estatísticas")
    print("6. Exportar JSON")
    print("7. Importar JSON")
    print("8. Gerar dados com Faker")
    print("9. Sair")
def main():
    criar_banco()
    while True:
        mostrar_menu()
        opcao = input("\nEscolha uma opção: ").strip()
        if opcao == "1":
            criar_tarefa()
        elif opcao == "2":
            listar_tarefas()
        elif opcao == "3":
            concluir_tarefa()
        elif opcao == "4":
            excluir_tarefa()
        elif opcao == "5":
            mostrar_estatisticas()
        elif opcao == "6":
            exportar()
        elif opcao == "7":
            importar()
        elif opcao == "8":
            gerar_faker()
        elif opcao == "9":
            print("\nEncerrando o Caixa de Entrada → Ação...")
            break
        else:
            print("\nOpção inválida. Escolha uma opção de 1 a 9.")
if __name__ == "__main__":
    main()