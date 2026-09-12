import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def aprovar_todas_pendencias_aluno(nome_aluno):
    """
    Função que pesquisa o aluno e aprova em loop TODAS as suas atividades
    que estiverem com o status 'Pendente', até não restar nenhuma.
    """
    # -------------------------------------------------------------------------
    # Passo 1: Conexão ao navegador Google Chrome ativo (porta de depuração 9222)
    # -------------------------------------------------------------------------
    opcoes_chrome = Options()
    opcoes_chrome.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    navegador = webdriver.Chrome(options=opcoes_chrome)
    # Define um tempo limite de espera para busca de elementos
    espera_longa = WebDriverWait(navegador, 10)
    espera_curta = WebDriverWait(navegador, 4) # Tempo menor para verificar se ainda há pendências
    
    try:
        print(f"--- Iniciando automação contínua para o jovem: {nome_aluno} ---")
        
        # Contador para acompanhar quantas atividades foram aprovadas
        atividades_processadas = 0
        
        # -------------------------------------------------------------------------
        # Passo 2: Laço de repetição (Loop) para processar todas as pendências
        # -------------------------------------------------------------------------
        while True:
            # 2.1. Garante a pesquisa do nome do aluno na tabela
            print("\nPesquisando o nome do jovem na listagem...")
            campo_busca = espera_longa.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='text' or @type='search' or contains(@class, 'form-control')]"))
            )
            campo_busca.clear()
            campo_busca.send_keys(nome_aluno)
            campo_busca.send_keys(Keys.RETURN)
            time.sleep(3) # Aguarda a tabela atualizar com os resultados
            
            # 2.2. Tenta localizar um registro com status 'Pendente'
            try:
                print("Verificando se ainda existem registros com status 'Pendente'...")
                linha_pendente = espera_curta.until(
                    EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Pendente')]"))
                )
            except Exception:
                # Se o Selenium não encontrar mais o texto 'Pendente', o loop é encerrado
                print(f"\n[SUCESSO] Nenhuma pendência restante encontrada para {nome_aluno}!")
                break
            
            # 2.3. Acessa a atividade pendente encontrada
            print("Pendência localizada! Acessando a atividade...")
            navegador.execute_script("arguments[0].scrollIntoView({block: 'center'});", linha_pendente)
            navegador.execute_script("arguments[0].click();", linha_pendente)
            time.sleep(3)
            
            # 2.4. Seleciona a nota 0,75 na tela da prova
            print("Atribuindo a nota 0,75...")
            botao_nota = espera_longa.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'correct075') or contains(text(), '0,75')]"))
            )
            navegador.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_nota)
            time.sleep(1)
            navegador.execute_script("arguments[0].click();", botao_nota)
            print("Nota 0,75 selecionada com sucesso!")
            time.sleep(2)
            
            # Incrementa o contador de atividades
            atividades_processadas += 1
            print(f"Atividade nº {atividades_processadas} concluída!")
            
            # 2.5. Retorna para a tela de listagem inicial para o próximo ciclo
            print("Retornando para a listagem inicial para verificar o próximo item...")
            navegador.back()
            time.sleep(3)

        print(f"\n=== PROCESSO FINALIZADO ===")
        print(f"Total de atividades aprovadas para {nome_aluno}: {atividades_processadas}")

    except Exception as erro:
        print(f"Ocorreu um erro durante a execução do processo: {erro}")

# ==========================================
# EXECUÇÃO DO PROGRAMA
# ==========================================
if __name__ == "__main__":
    # Define aqui o nome do jovem cujas pendências você quer zerar:
    jovem_para_aprovar = "Felipe Mendes do Prado"
    
    aprovar_todas_pendencias_aluno(jovem_para_aprovar)