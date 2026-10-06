import os
import re
import time
import urllib.parse
from flask import Flask, jsonify, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

# Variável global para manter o último cargo pesquisado na sessão
ultimo_cargo = ""


def normalizar_palavra(palavra):
  return re.sub(r"(.)\1{2,}", r"\1", palavra)


def executar_busca_selenium(cargo, regiao_chave, mapeamento_regioes):
  navegador = None
  try:
    opcoes = Options()
    # Argumentos obrigatórios para rodar o Chrome na nuvem (Render) sem tela (Headless)
    opcoes.add_argument("--headless")
    opcoes.add_argument("--no-sandbox")
    opcoes.add_argument("--disable-dev-shm-usage")
    opcoes.add_argument("--disable-gpu")
    opcoes.add_argument("--disable-blink-features=AutomationControlled")
    opcoes.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Inicializa o ChromeDriver no modo invisível
    navegador = webdriver.Chrome(options=opcoes)

    cargo_url = cargo.lower().strip()
    cargo_url = (
        cargo_url.replace("á", "a")
        .replace("à", "a")
        .replace("ã", "a")
        .replace("â", "a")
        .replace("é", "e")
        .replace("ê", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ô", "o")
        .replace("õ", "o")
        .replace("ú", "u")
        .replace("ç", "c")
    )
    cargo_url = re.sub(r"[^a-z0-9\s]", "", cargo_url)
    cargo_url = cargo_url.replace(" ", "-")

    if regiao_chave:
      regiao_url = mapeamento_regioes.get(regiao_chave)
      url_busca = f"https://www.catho.com.br/vagas/{cargo_url}/{regiao_url}/"
      navegador.get(url_busca)
      time.sleep(2.0)
    else:
      navegador.get("https://www.catho.com.br/")
      time.sleep(1.5)

    return f"Busca realizada com sucesso para '{cargo}' na região '{regiao_chave or 'Geral'}'."

  except Exception as e:
    return f"Erro durante a automação: {str(e)}"
  finally:
    if navegador:
      navegador.quit()


@app.route("/", methods=["GET"])
def home():
  # Renderiza a interface gráfica do chat localizada na pasta 'templates'
  return render_template("index.html")


@app.route("/chat", methods=["POST"])
def processar_chat():
  global ultimo_cargo
  dados = request.get_json() or {}
  mensagem = dados.get("mensagem", "").strip()

  if not mensagem:
    return jsonify({"erro": "Nenhuma mensagem enviada."}), 400

  msg_raw = mensagem
  msg_lower = msg_raw.lower()

  if "entrevista" in msg_lower:
    resp = (
        "Para ir bem em uma entrevista, pesquise bem sobre a empresa com"
        " antecedência, treine falar sobre suas principais conquistas"
        " profissionais com confiança e demonstre entusiasmo genuíno pela"
        " vaga!"
    )
    return jsonify({"resposta": resp})

  elif (
      "currículo" in msg_lower
      or "curriculo" in msg_lower
      or "perfil" in msg_lower
  ):
    resp = (
        "Para destacar seu perfil, use verbos de ação nas suas experiências"
        " anteriores, coloque resultados numéricos alcançados e mantenha suas"
        " competências técnicas atualizadas de acordo com a vaga desejada."
    )
    return jsonify({"resposta": resp})

  elif "transição" in msg_lower or "transicao" in msg_lower:
    resp = (
        "Uma transição segura envolve mapear as habilidades que você já tem"
        " (soft skills), estudar os requisitos da nova área e buscar cursos"
        " práticos ou projetos voluntários para construir portfólio."
    )
    return jsonify({"resposta": resp})

  elif "habilidades" in msg_lower or "competências" in msg_lower:
    resp = (
        "Atualmente, o mercado valoriza muito a capacidade de adaptação"
        " rápida, inteligência emocional, resolução de problemas complexos e"
        " familiaridade com ferramentas tecnológicas modernas."
    )
    return jsonify({"resposta": resp})

  assuntos_proibidos = [
      "receita",
      "bolo",
      "futebol",
      "jogo",
      "fofoca",
      "filme",
      "piada",
      "musica",
      "música",
      "clima",
      "tempo",
      "historia",
      "história",
      "alemanha",
      "politica",
      "política",
      "presidente",
  ]
  if any(ap in msg_lower for ap in assuntos_proibidos):
    resp = (
        "Desculpe, sou especializada em ajudar na busca por vagas de emprego e"
        " orientações de carreira. Como posso te ajudar nessa área?"
    )
    return jsonify({"resposta": resp})

  gatilhos_busca = [
      "procura",
      "procurar",
      "busca",
      "buscar",
      "vaga",
      "vagas",
      "emprego",
      "quero",
      "preciso",
      "estágio",
      "estagio",
      "ser",
      "trabalhar",
      "trampar",
  ]
  tem_intencao_busca = any(g in msg_lower for g in gatilhos_busca)

  if not tem_intencao_busca and not ultimo_cargo and len(msg_lower.split()) < 2:
    resp = (
        "Com certeza! Pode me dizer qual cargo e região você gostaria de"
        " pesquisar."
    )
    return jsonify({"resposta": resp})

  mapeamento_regioes = {
      "sao paulo": "sao-paulo-sp",
      "são paulo": "sao-paulo-sp",
      "sp": "sao-paulo-sp",
      "rio de janeiro": "rio-de-janeiro-rj",
      "rj": "rio-de-janeiro-rj",
      "belo horizonte": "belo-horizonte-mg",
      "minas gerais": "belo-horizonte-mg",
      "mg": "belo-horizonte-mg",
      "vitoria": "vitoria-es",
      "vitória": "vitoria-es",
      "espirito santo": "vitoria-es",
      "espírito santo": "vitoria-es",
      "es": "vitoria-es",
      "curitiba": "curitiba-pr",
      "parana": "curitiba-pr",
      "paraná": "curitiba-pr",
      "pr": "curitiba-pr",
      "florianopolis": "florianopolis-sc",
      "florianópolis": "florianopolis-sc",
      "santa catarina": "florianopolis-sc",
      "sc": "florianopolis-sc",
      "porto alegre": "porto-alegre-rs",
      "rio grande do sul": "porto-alegre-rs",
      "rs": "porto-alegre-rs",
      "salvador": "salvador-ba",
      "bahia": "salvador-ba",
      "ba": "salvador-ba",
      "recife": "recife-pe",
      "pernambuco": "recife-pe",
      "pe": "recife-pe",
      "fortaleza": "fortaleza-ce",
      "ceara": "fortaleza-ce",
      "ceará": "fortaleza-ce",
      "ce": "fortaleza-ce",
      "sao luis": "sao-luis-ma",
      "são luís": "sao-luis-ma",
      "maranhao": "sao-luis-ma",
      "maranhão": "sao-luis-ma",
      "ma": "sao-luis-ma",
      "natal": "natal-rn",
      "rio grande do norte": "natal-rn",
      "rn": "natal-rn",
      "joao pessoa": "joao-pessoa-pb",
      "joão pessoa": "joao-pessoa-pb",
      "paraiba": "joao-pessoa-pb",
      "paraíba": "joao-pessoa-pb",
      "pb": "joao-pessoa-pb",
      "maceio": "maceio-al",
      "maceió": "maceio-al",
      "alagoas": "maceio-al",
      "al": "maceio-al",
      "aracaju": "aracaju-se",
      "sergipe": "aracaju-se",
      "se": "aracaju-se",
      "teresina": "teresina-pi",
      "piaui": "teresina-pi",
      "piauí": "teresina-pi",
      "pi": "teresina-pi",
      "manaus": "manaus-am",
      "amazonas": "manaus-am",
      "am": "manaus-am",
      "belem": "belem-pa",
      "belém": "belem-pa",
      "para": "belem-pa",
      "pará": "belem-pa",
      "pa": "belem-pa",
      "porto velho": "porto-velho-ro",
      "rondonia": "porto-velho-ro",
      "rondônia": "porto-velho-ro",
      "ro": "porto-velho-ro",
      "rio branco": "rio-branco-ac",
      "acre": "rio-branco-ac",
      "ac": "rio-branco-ac",
      "macapa": "macapa-ap",
      "macapá": "macapa-ap",
      "amapa": "macapa-ap",
      "amapá": "macapa-ap",
      "ap": "macapa-ap",
      "boa vista": "boa-vista-rr",
      "roraima": "boa-vista-rr",
      "rr": "boa-vista-rr",
      "palmas": "palmas-to",
      "tocantins": "palmas-to",
      "to": "palmas-to",
      "brasilia": "brasilia-df",
      "brasília": "brasilia-df",
      "df": "brasilia-df",
      "distrito federal": "brasilia-df",
      "goiania": "goiania-go",
      "goiânia": "goiania-go",
      "goias": "goiania-go",
      "goiás": "goiania-go",
      "go": "goiania-go",
      "cuiaba": "cuiaba-mt",
      "cuiabá": "cuiaba-mt",
      "mato grosso": "cuiaba-mt",
      "mt": "cuiaba-mt",
      "campo grande": "campo-grande-ms",
      "mato grosso do sul": "campo-grande-ms",
      "ms": "campo-grande-ms",
      "campinas": "campinas-sp",
      "santos": "santos-sp",
      "osasco": "osasco-sp",
      "niteroi": "niteroi-rj",
      "niteroí": "niteroi-rj",
      "londrina": "londrina-pr",
  }

  regiao_encontrada = None
  for regiao in sorted(mapeamento_regioes.keys(), key=len, reverse=True):
    padrao = r"(?:\b(?:em|no|na)\s+)?\b(" + re.escape(regiao) + r")\b"
    match = re.search(padrao, msg_lower)
    if match:
      regiao_encontrada = regiao
      msg_lower = msg_lower.replace(match.group(0), "")
      break

  palavras_descartaveis = {
      "ola",
      "olá",
      "oi",
      "eai",
      "e ai",
      "salve",
      "suave",
      "fala",
      "hey",
      "opa",
      "mano",
      "cara",
      "velho",
      "bom",
      "dia",
      "boa",
      "tarde",
      "noite",
      "tudo",
      "bem",
      "ta",
      "tá",
      "beleza",
      "blz",
      "ok",
      "okay",
      "entendi",
      "certo",
      "pode",
      "ser",
      "sim",
      "massa",
      "top",
      "show",
      "perfeito",
      "obrigado",
      "obrigada",
      "valeu",
      "vlw",
      "agora",
      "quero",
      "querendo",
      "queria",
      "virar",
      "arrumar",
      "arranja",
      "busco",
      "buscar",
      "procurar",
      "procura",
      "pesquisar",
      "pesquisa",
      "achar",
      "encontrar",
      "preciso",
      "ver",
      "mostra",
      "mostre",
      "tem",
      "consigo",
      "vaga",
      "vagas",
      "emprego",
      "empregos",
      "oportunidade",
      "oportunidades",
      "trampo",
      "trabalhar",
      "trabalho",
      "trampar",
      "para",
      "em",
      "no",
      "na",
      "nos",
      "nas",
      "por",
      "hoje",
      "favor",
      "pfv",
      "porfavor",
      "um",
      "uma",
      "uns",
      "umas",
      "me",
      "mim",
      "pra",
      "pro",
      "ter",
      "como",
      "entao",
      "então",
      "estagio",
      "estágio",
      "grande",
      "empresa",
      "junior",
      "júnior",
  }

  cargos_curtos_validos = {"ti", "rh", "ui", "ux", "pr", "sem"}

  texto_limpo = re.sub(r"[^\w\s]", " ", msg_lower)
  tokens = texto_limpo.split()
  tokens_normalizados = [normalizar_palavra(word) for word in tokens]

  tokens_cargo = [
      word
      for word in tokens_normalizados
      if word not in palavras_descartaveis
      and (len(word) > 2 or word in cargos_curtos_validos)
  ]
  cargo_final = " ".join(tokens_cargo).strip()

  if not cargo_final and ultimo_cargo:
    cargo_final = ultimo_cargo
  elif cargo_final:
    ultimo_cargo = cargo_final

  if not cargo_final:
    resp = "Por favor, me informe qual cargo profissional você procura."
    return jsonify({"resposta": resp})

  # Executa o Selenium em background para realizar a automação na nuvem
  resultado_automacao = executar_busca_selenium(
      cargo_final, regiao_encontrada, mapeamento_regioes
  )

  if regiao_encontrada:
    resp = (
        f"Prontinho! Automação concluída para '{cargo_final.title()}' em"
        f" {regiao_encontrada.title()}. Status: {resultado_automacao}"
    )
  else:
    resp = (
        f"Prontinho! Automação concluída para '{cargo_final.title()}'."
        f" Status: {resultado_automacao}"
    )

  return jsonify({"resposta": resp})


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)