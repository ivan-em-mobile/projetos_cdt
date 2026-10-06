'''
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\selenium\Perfil1"

Executar a plataforma de automação com o comando acima no terminal antes de rodar este script.

'''

import time
import subprocess
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def iniciar_chrome_debug(porta: int, pasta_perfil: str):
    """
    Abre o Google Chrome via linha de comando em modo de depuração remota.
    
    Parâmetros:
    - porta (int): A porta de depuração (ex: 9222 ou 9223).
    - pasta_perfil (str): O caminho da pasta onde o perfil do Chrome será mantido.
    """
    caminho_chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    # Comando do sistema para iniciar o Chrome com a porta de debug habilitada
    comando = f'"{caminho_chrome}" --remote-debugging-port={porta} --user-data-dir="{pasta_perfil}"'
    
    print(f"[SISTEMA] Iniciando o Google Chrome na porta {porta}...")
    subprocess.Popen(comando, shell=True)
    time.sleep(3)  # Tempo para o navegador inicializar


def aprovar_todas_pendencias_aluno(nome_aluno: str, porta_debug: int = 9222):
    """
    Conecta ao Chrome aberto, usa a página que já estiver ativa na tela
    e aprova todas as pendências do aluno pesquisado.
    
    Parâmetros:
    - nome_aluno (str): Nome do aluno a ser pesquisado na tabela.
    - porta_debug (int): Porta de depuração do Chrome (padrão: 9222).
    """
    # -------------------------------------------------------------------------
    # Passo 1: Iniciar e Conectar ao Chrome
    # -------------------------------------------------------------------------
    pasta_perfil_chrome = os.path.join("C:\\", "selenium", f"Perfil_{porta_debug}")
    iniciar_chrome_debug(porta_debug, pasta_perfil_chrome)

    opcoes_chrome = Options()
    opcoes_chrome.add_experimental_option("debuggerAddress", f"127.0.0.1:{porta_debug}")
    
    try:
        navegador = webdriver.Chrome(options=opcoes_chrome)
        print(f"[SISTEMA] Conectado ao Chrome com sucesso!")
    except Exception as erro:
        print(f"\n[ERRO] Não foi possível conectar ao Chrome: {erro}")
        return

    # -------------------------------------------------------------------------
    # Passo 2: Instração de Navegação Manual
    # -------------------------------------------------------------------------
    print("\n" + "="*60)
    print(" INSTRUÇÕES:")
    print(" 1. Vá até a janela do Chrome que abriu.")
    print(" 2. Acesse o sistema e entre na página da listagem de alunos.")
    print(" 3. Volte a esta tela do terminal e pressione ENTER.")
    print("="*60)
    input("\n--> Pressione ENTER assim que estiver na página de pendências...")

    # Configuração de tempos de espera para localizar elementos na tela
    espera_longa = WebDriverWait(navegador, 10)
    espera_curta = WebDriverWait(navegador, 4)

    try:
        print(f"\n==================================================")
        print(f"Iniciando automação na página atual para: {nome_aluno}")
        print(f"==================================================\n")
        
        atividades_processadas = 0

        # -------------------------------------------------------------------------
        # Passo 3: Laço de Repetição - Processar todas as pendências
        # -------------------------------------------------------------------------
        while True:
            # 3.1 Pesquisa o nome do jovem na página atual
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
            time.sleep(3) # Aguarda a atualização da tabela

            # 3.2 Verifica se ainda existe algum registro com status 'Pendente'
            try:
                print("Verificando se ainda existem pendências...")
                linha_pendente = espera_curta.until(
                    EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Pendente')]"))
                )
            except Exception:
                # Se não encontrar 'Pendente', encerra o ciclo
                print(f"\n[SUCESSO] Nenhuma pendência restante para {nome_aluno}!")
                break

            # 3.3 Acessa a atividade pendente
            print("Pendência localizada! Acessando a avaliação...")
            navegador.execute_script("arguments[0].scrollIntoView({block: 'center'});", linha_pendente)
            time.sleep(1)
            navegador.execute_script("arguments[0].click();", linha_pendente)
            time.sleep(3)

            # 3.4 Atribui a nota 0,75
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

            # 3.5 Retorna para a página da lista de pendências
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
    # 1. Nome do aluno cujas notas serão lançadas
    ALUNO = "Jamily Do Carmo Santos"
    
    # 2. Defina a porta de depuração do Chrome (9222 para Usuário 1, 9223 para Usuário 2)
    PORTA = 9222

    # Executa a automação diretamente na aba aberta
    aprovar_todas_pendencias_aluno(
        nome_aluno=ALUNO, 
        porta_debug=PORTA
    )