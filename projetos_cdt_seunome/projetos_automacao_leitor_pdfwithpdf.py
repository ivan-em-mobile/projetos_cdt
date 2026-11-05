import os
import re
from pypdf import PdfReader

# Caminho da pasta atualizada contendo todos os recibos de 2022 a 2026
PASTA_DESTINO = r"C:\Users\NotePCoder\Desktop\holerites de 2022 - 2026"

def extrair_mes_ano(texto_completo):
    """
    Função auxiliar que testa diferentes padrões de Regex para identificar
    o mês e o ano em recibos de diferentes anos (2022, 2023, 2024, 2025 e 2026).
    """
    padroes = [
        # Padrão 1: Formato de 2026 (ex: "Folha Mensal Junho de 2026")[cite: 1, 2, 3, 4]
        r"Folha[\s\n]+Mensal.*?([A-Za-zÇçãõéêíóú]+\s+de\s+(202[2-6]))",
        
        # Padrão 2: Formato de 2023 (ex: "Mês: Janeiro/2023")[cite: 9]
        r"Mês:\s*([A-Za-zÇçãõéêíóú]+)/(202[2-6])",
        
        # Padrão 3: Formato de 2022 (ex: "OUTUBRO/2022", "NOVEMBRO/2022")[cite: 6, 7, 8]
        r"\b(JANEIRO|FEVEREIRO|MARÇO|ABRIL|MAIO|JUNHO|JULHO|AGOSTO|SETEMBRO|OUTUBRO|NOVEMBRO|DEZEMBRO)/(202[2-6])\b"
    ]
    
    for i, padrao in enumerate(padroes):
        resultado = re.search(padrao, texto_completo, re.IGNORECASE | re.DOTALL)
        if resultado:
            if i == 0:
                # Retorna o texto capturado no formato 2026
                return resultado.group(1).lower()
            elif i == 1 or i == 2:
                # Padroniza os formatos de 2023 e 2022 para "mês de ano"
                mes = resultado.group(1).lower()
                ano = resultado.group(2)
                return f"{mes} de {ano}"
                
    return None

def processar_holerites_periodo(caminho_pasta):
    """
    Função principal que percorre a pasta, lê cada PDF e gerencia a renomeação e os erros.
    """
    if not os.path.exists(caminho_pasta):
        print(f"Erro: A pasta '{caminho_pasta}' não foi encontrada.")
        return

    print(f"Inspecionando a pasta: {caminho_pasta}\n" + "-"*50)
    
    arquivos = os.listdir(caminho_pasta)
    sucessos = 0
    divergencias = 0

    for arquivo in arquivos:
        if arquivo.lower().endswith(".pdf"):
            caminho_antigo = os.path.join(caminho_pasta, arquivo)
            print(f"Analisando arquivo: {arquivo}")
            
            try:
                # Leitura do texto de todas as páginas do PDF
                leitor = PdfReader(caminho_antigo)
                texto_completo = ""
                for pagina in leitor.pages:
                    texto_extraido = pagina.extract_text()
                    if texto_extraido:
                        texto_completo += texto_extraido + "\n"
                
                # Aplicação da busca inteligente de mês/ano
                mes_ano_encontrado = extrair_mes_ano(texto_completo)
                
                if mes_ano_encontrado:
                    # Formata o novo nome substituindo espaços por underlines
                    nome_formatado = mes_ano_encontrado.replace(" ", "_")
                    novo_nome = f"folha_{nome_formatado}.pdf"
                    caminho_novo = os.path.join(caminho_pasta, novo_nome)
                    
                    if caminho_antigo != caminho_novo:
                        if os.path.exists(caminho_novo):
                            print(f"  [Aviso] O arquivo '{novo_nome}' já existe. Pulando para evitar sobrescrever.\n")
                            continue
                        
                        os.rename(caminho_antigo, caminho_novo)
                        print(f"  [Sucesso] Renomeado para: {novo_nome}\n")
                        sucessos += 1
                    else:
                        print(f"  [Info] O arquivo já está com o nome correto.\n")
                else:
                    # Tratamento de divergência: Arquivo não reconhecido pelos padrões
                    print(f"  [Atenção] Não foi possível identificar o mês e o ano neste arquivo PDF.\n")
                    divergencias += 1
                    
            except Exception as e:
                # Tratamento de erro de leitura do arquivo
                print(f"  [Erro] Falha ao processar o arquivo '{arquivo}'. Detalhe: {e}\n")
                divergencias += 1

    print("-" * 50)
    print(f"Processo finalizado!")
    print(f"Total de arquivos renomeados com sucesso: {sucessos}")
    print(f"Total de arquivos com divergências/erros de leitura: {divergencias}")

if __name__ == "__main__":
    processar_holerites_periodo(PASTA_DESTINO)