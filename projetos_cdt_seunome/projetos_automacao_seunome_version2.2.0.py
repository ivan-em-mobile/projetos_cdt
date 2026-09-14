import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def aprovar_todas_pendencias_aluno(nome_aluno):
    """
    Conecta ao Google Chrome aberto na porta 9222, pesquisa o aluno informado
    e aprova sequencialmente todas as avaliações com status 'Pendente'.
    """
    # -------------------------------------------------------------------------
    # Configuração de Conexão: Usa a sessão do Chrome já aberta pelo usuário
    # -------------------------------------------------------------------------
    opcoes_chrome = Options()
    opcoes_chrome.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        navegador = webdriver.Chrome(options=opcoes_chrome)
    except Exception as e:
        print("\n[ERRO] Não foi possível conectar ao Google Chrome!")
        print("Certifique-se de ter iniciado o Chrome via terminal com o comando:")
        print(r'"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile"')
        return

    # Tempos limite de espera para os elementos da página
    espera_longa = WebDriverWait(navegador, 10)
    espera_curta = WebDriverWait(navegador, 4)

    try:
        print(f"\n==================================================")
        print(f"Iniciando automação para o jovem: {nome_aluno}")
        print(f"==================================================\n")
        
        atividades_processadas = 0

        # -------------------------------------------------------------------------
        # Laço de Repetição: Processa todas as pendências até zerar
        # -------------------------------------------------------------------------
        while True:
            # 1. Pesquisa o nome do jovem na listagem
            print(f"Pesquisando '{nome_aluno}' na listagem...")
            campo_busca = espera_longa.until(
                EC.element_to_be_clickable((
                    By.XPATH, 
                    "//input[@type='text' or @type='search' or contains(@class, 'form-control')]"
                ))
            )
            campo_busca.clear()
            campo_busca.send_keys(nome_aluno)
            campo_busca.send_keys(Keys.RETURN)
            time.sleep(3) # Tempo para atualização da tabela na tela

            # 2. Verifica se ainda existe registro com status 'Pendente'
            try:
                print("Verificando se ainda existem pendências...")
                linha_pendente = espera_curta.until(
                    EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Pendente')]"))
                )
            except Exception:
                # Se não encontrar a palavra 'Pendente', o loop é finalizado
                print(f"\n[SUCESSO] Nenhuma pendência restante para {nome_aluno}!")
                break

            # 3. Acessa a atividade pendente
            print("Pendência localizada! Acessando a avaliação...")
            navegador.execute_script("arguments[0].scrollIntoView({block: 'center'});", linha_pendente)
            time.sleep(1)
            navegador.execute_script("arguments[0].click();", linha_pendente)
            time.sleep(3)

            # 4. Atribui a nota 0,75
            print("Atribuindo a nota 0,75...")
            botao_nota = espera_longa.until(
                EC.presence_of_element_located((
                    By.XPATH, 
                    "//*[contains(@class, 'correct075') or contains(text(), '0,75')]"
                ))
            )
            navegador.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_nota)
            time.sleep(1)
            navegador.execute_script("arguments[0].click();", botao_nota)
            print("Nota 0,75 lançada com sucesso!")
            time.sleep(2)

            atividades_processadas += 1
            print(f"-> Atividade nº {atividades_processadas} concluída!")

            # 5. Retorna para a listagem para o próximo ciclo
            print("Retornando para a tela inicial...\n")
            navegador.back()
            time.sleep(3)

        print(f"==================================================")
        print(f"PROCESSO FINALIZADO!")
        print(f"Total de atividades aprovadas para {nome_aluno}: {atividades_processadas}")
        print(f"==================================================")

    except Exception as erro:
        print(f"\n[ERRO] Ocorreu uma falha durante o processo: {erro}")

# =============================================================================
# EXECUÇÃO DO SCRIPT
# =============================================================================
if __name__ == "__main__":
    # Nome do jovem cujas pendências serão zeradas
    jovem_para_aprovar = "Felipe Mendes do Prado"
    
    aprovar_todas_pendencias_aluno(jovem_para_aprovar)