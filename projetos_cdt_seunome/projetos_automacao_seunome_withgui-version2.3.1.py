import time
import subprocess
import os
import threading
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def iniciar_chrome_debug(porta: int, pasta_perfil: str):
    """
    Abre o Google Chrome via linha de comando em modo de depuração remota.
    """
    caminho_chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    comando = f'"{caminho_chrome}" --remote-debugging-port={porta} --user-data-dir="{pasta_perfil}"'
    
    print(f"[SISTEMA] Iniciando o Google Chrome na porta {porta}...")
    subprocess.Popen(comando, shell=True)
    time.sleep(3)  # Tempo para o navegador inicializar

def executar_automacao(nome_aluno: str, porta_debug: int, janela_gui):
    """
    Função que executa toda a lógica do Selenium. 
    Executada em uma thread separada para não travar a interface gráfica.
    """
    try:
        pasta_perfil_chrome = os.path.join("C:\\", "selenium", f"Perfil_{porta_debug}")
        iniciar_chrome_debug(porta_debug, pasta_perfil_chrome)

        opcoes_chrome = Options()
        opcoes_chrome.add_experimental_option("debuggerAddress", f"127.0.0.1:{porta_debug}")
        
        try:
            navegador = webdriver.Chrome(options=opcoes_chrome)
            print(f"[SISTEMA] Conectado ao Chrome com sucesso!")
        except Exception as erro:
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao Chrome:\n{erro}")
            return

        # Configuração de tempos de espera
        espera_longa = WebDriverWait(navegador, 10)
        espera_curta = WebDriverWait(navegador, 4)

        atividades_processadas = 0

        # Laço de Repetição - Processar todas as pendências
        while True:
            # Pesquisa o nome do aluno na página atual
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
            time.sleep(3)

            # Verifica se ainda existe algum registro com status 'Pendente'
            try:
                print("Verificando se ainda existem pendências...")
                linha_pendente = espera_curta.until(
                    EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Pendente')]"))
                )
            except Exception:
                print(f"\n[SUCESSO] Nenhuma pendência restante para {nome_aluno}!")
                break

            # Acessa a atividade pendente
            print("Pendência localizada! Acessando a avaliação...")
            navegador.execute_script("arguments[0].scrollIntoView({block: 'center'});", linha_pendente)
            time.sleep(1)
            navegador.execute_script("arguments[0].click();", linha_pendente)
            time.sleep(3)

            # Atribui a nota 0,75
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

            # Retorna para a página da lista de pendências
            print("Retornando para a tela inicial...\n")
            navegador.back()
            time.sleep(3)

        messagebox.showinfo("Processo Finalizado", f"Sucesso!\nTotal de atividades aprovadas para {nome_aluno}: {atividades_processadas}")

    except Exception as erro:
        messagebox.showerror("Erro na Automação", f"Ocorreu uma falha durante o processo:\n{erro}")

# =============================================================================
# CONFIGURAÇÃO DA INTERFACE GRÁFICA (GUI)
# =============================================================================
def iniciar_interface():
    def botao_clicado():
        nome = entrada_nome.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Por favor, digite o nome do aluno!")
            return
        
        # Fecha a janela ou avisa que iniciou, e dispara a automação em uma thread separada
        messagebox.info = messagebox.showinfo("Aviso", "A automação vai começar. Certifique-se de que posicionou o navegador na página correta se necessário!")
        
        # Usa threading para o navegador não travar a janela do Tkinter
        t = threading.Thread(target=executar_automacao, args=(nome, 9222, janela))
        t.start()

    # Criação da janela principal
    janela = tk.Tk()
    janela.title("Automação de Notas - Sistema")
    janela.geometry("400x200")
    janela.resizable(False, False)

    # Rótulo de instrução
    label_instrucao = tk.Label(janela, text="Digite o nome completo do aluno:", font=("Arial", 11))
    label_instrucao.pack(pady=15)

    # Campo de texto (Input)
    entrada_nome = tk.Entry(janela, font=("Arial", 12), width=30)
    entrada_nome.insert(0, "Gabriel Carvalho da Silva")  # Valor padrão opcional
    entrada_nome.pack(pady=5)

    # Botão de iniciar
    botao_iniciar = tk.Button(janela, text="Iniciar Automação", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", command=botao_clicado)
    botao_iniciar.pack(pady=20)

    # Mantém a janela aberta
    janela.mainloop()

if __name__ == "__main__":
    iniciar_interface()