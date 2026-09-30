import os
import json
import datetime
import requests
from database import get_connection

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "activity_log.json")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def log_event_json(tipo_evento, detalhe):
    """Registra eventos no arquivo de log em formato JSON."""
    evento = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tipo": tipo_evento,
        "detalhes": detalhe
    }
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except Exception:
            logs = []
    logs.append(evento)
    try:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Erro ao salvar JSON log: {e}")

def obter_cotacoes():
    """Busca cotações em tempo real usando APIs abertas livres de rate-limit na nuvem."""
    dados_cotacoes = {}

    # 1. Busca Moedas Tradicionais (USD, EUR, GBP) via ExchangeRate-API (Pública/Sem Key)
    try:
        res = requests.get("https://open.er-api.com/v6/latest/BRL", headers=HEADERS, timeout=5)
        if res.status_code == 200:
            rates = res.json().get("rates", {})
            if rates:
                if "USD" in rates and rates["USD"] > 0:
                    val_usd = 1 / rates["USD"]
                    dados_cotacoes["USDBRL"] = {"bid": str(round(val_usd, 2))}
                    dados_cotacoes["USD-BRL"] = {"bid": str(round(val_usd, 2))}

                if "EUR" in rates and rates["EUR"] > 0:
                    val_eur = 1 / rates["EUR"]
                    dados_cotacoes["EURBRL"] = {"bid": str(round(val_eur, 2))}
                    dados_cotacoes["EUR-BRL"] = {"bid": str(round(val_eur, 2))}

                if "GBP" in rates and rates["GBP"] > 0:
                    val_gbp = 1 / rates["GBP"]
                    dados_cotacoes["GBPBRL"] = {"bid": str(round(val_gbp, 2))}
                    dados_cotacoes["GBP-BRL"] = {"bid": str(round(val_gbp, 2))}
    except Exception as e:
        print(f"[Erro] Falha ao buscar moedas tradicionais: {e}")

    # 2. Busca Bitcoin via CoinGecko API Pública
    try:
        res_btc = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=brl", headers=HEADERS, timeout=5)
        if res_btc.status_code == 200:
            btc_price = res_btc.json().get("bitcoin", {}).get("brl")
            if btc_price:
                dados_cotacoes["BTCBRL"] = {"bid": str(round(float(btc_price), 2))}
                dados_cotacoes["BTC-BRL"] = {"bid": str(round(float(btc_price), 2))}
    except Exception as e:
        print(f"[Erro] Falha ao buscar BTC via CoinGecko: {e}")

    if dados_cotacoes:
        return dados_cotacoes

    return None

def converter_moeda(origem, destino, valor):
    """Realiza conversões de moedas utilizando a API open.er-api.com e CoinGecko."""
    if origem == destino:
        return valor, 1.0

    try:
        # Lógica especial para Bitcoin
        if origem == "BTC" or destino == "BTC":
            res_btc = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=brl,usd,eur,gbp", headers=HEADERS, timeout=5)
            if res_btc.status_code == 200:
                data = res_btc.json().get("bitcoin", {})
                if origem == "BTC":
                    taxa = data.get(destino.lower(), 0.0)
                else:
                    taxa_brl = data.get(origem.lower(), 0.0)
                    taxa = (1 / taxa_brl) if taxa_brl > 0 else 0.0

                if taxa > 0:
                    val_conv = valor * taxa
                    log_event_json("CONVERSAO_MOEDA", {"origem": origem, "destino": destino, "valor": valor, "resultado": val_conv})
                    return val_conv, taxa

        # Conversão de moedas fiduciárias via open.er-api
        res = requests.get(f"https://open.er-api.com/v6/latest/{origem}", headers=HEADERS, timeout=5)
        if res.status_code == 200:
            rates = res.json().get("rates", {})
            if destino in rates:
                taxa = float(rates[destino])
                val_conv = valor * taxa
                log_event_json("CONVERSAO_MOEDA", {"origem": origem, "destino": destino, "valor": valor, "resultado": val_conv})
                return val_conv, taxa
    except Exception as e:
        print(f"[Erro] Falha na conversão ({origem} -> {destino}): {e}")

    return None, None

def listar_metas():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, categoria, valor_alvo, valor_atual, data_limite FROM metas_financeiras")
        return [dict(row) for row in cursor.fetchall()]

def salvar_meta(nome, categoria, alvo, atual, limite):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO metas_financeiras (nome, categoria, valor_alvo, valor_atual, data_limite) VALUES (?, ?, ?, ?, ?)",
            (nome, categoria, alvo, atual, limite)
        )
        conn.commit()
    log_event_json("NOVA_META", {"nome": nome, "categoria": categoria, "alvo": alvo, "atual": atual})

def atualizar_saldo_meta(meta_id, novo_saldo):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE metas_financeiras SET valor_atual = ? WHERE id = ?", (novo_saldo, meta_id))
        conn.commit()
    log_event_json("APORTE_META", {"meta_id": meta_id, "novo_saldo": novo_saldo})

def excluir_meta(meta_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM metas_financeiras WHERE id = ?", (meta_id,))
        conn.commit()
    log_event_json("EXCLUSAO_META", {"meta_id": meta_id})