import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# =============================================================================
# CLASSE DA INTERFACE GRÁFICA (TKINTER)
# =============================================================================
class AppAprovacaoEAD:
    def __init__(self, root):
        self.root = root
        self.root.title("Automação EAD - Aprovação Contínua")
        self.root.geometry("540x450")
        self.root.resizable(False, False)

        # Configuração do tema visual
        estilo = ttk.Style()
        estilo.theme_use('clam')

        # ---------------------------------------------------------------------
        # 1. Campo para inserção do nome do Aluno
        # ---------------------------------------------------------------------
        frame_aluno = ttk.LabelFrame(self.root, text=" Identificação do Jovem ", padding=15)
        frame_aluno.pack(fill="x", padx=15, pady=10)

        ttk.Label(frame_aluno, text="Nome do Aluno:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_nome = ttk.Entry(frame_aluno, width=42)
        self.entry_nome.insert(0, "Pedro Henrique Melo de Sousa Santos")
        self.entry_nome.grid(row=0, column=1, pady=5, padx=5)

        # ---------------------------------------------------------------------
        # 2. Botão de Execução
        # ---------------------------------------------------------------------
        self.btn_iniciar = ttk.Button(
            self.root, 
            text="🚀 Iniciar Aprovação Contínua", 
            command=self.iniciar_thread_automacao
        )
        self.btn_iniciar.pack(fill="x", padx=15, pady=5)

        # ---------------------------------------------------------------------
        # 3. Console de Logs em Tempo Real
        # ---------------------------------------------------------------------
        frame_log = ttk.LabelFrame(self.root, text=" Progresso do Processo ", padding=10)
        frame_log.pack(fill="both", expand=True, padx=15, pady=10)

        self.txt_log = tk.Text(
            frame_log, 
            state='disabled', 
            height=10, 
            wrap='word', 
            bg='#1e1e1e', 
            fg='#00ff00', 
            font=('Consolas', 9)
        )
        self.txt_log.pack(fill="both", expand=True)

    def log(self, mensagem):
        """ Função auxiliar para exibir o progresso no console da janela """
        self.txt_log.config(state='normal')
        self.txt_log.insert(tk.END, f"> {mensagem}\n")
        self.txt_log.see(tk.END)
        self.txt_log.config(state='disabled')

    def iniciar_thread_automacao(self):
        """ Valida o nome do aluno e inicia o Selenium em segundo plano """
        nome_aluno = self.entry_nome.get().strip()

        if not nome_aluno:
            messagebox.showwarning("Atenção", "Por favor, digite o nome do jovem!")
            return

        # Desabilita o botão para evitar cliques múltiplos
        self.btn_iniciar.config(state='disabled')
        
        # Cria a Thread para não travar a janela do Tkinter
        thread = threading.Thread(
            target=self.executar_loop_selenium, 
            args=(nome_aluno,),
            daemon=True
        )
        thread.start()

    # =========================================================================
    # LÓGICA DE AUTOMAÇÃO (SELENIUM)
    # =========================================================================
    def executar_loop_selenium(self, nome_aluno):
        try:
            self.log(f"Iniciando automação para: '{nome_aluno}'")
            
            # Conexão com o Chrome já aberto na porta 9222
            opcoes_chrome = Options()
            opcoes_chrome.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            
            navegador = webdriver.Chrome(options=opcoes_chrome)
            espera_longa = WebDriverWait(navegador, 10)
            espera_curta = WebDriverWait(navegador, 4)

            atividades_processadas = 0

            # Loop principal do seu código original
            while True:
                # Passo 1: Busca o nome do aluno na listagem
                self.log(f"Pesquisando '{nome_aluno}' na tabela...")
                campo_busca = espera_longa.until(
                    EC.element_to_be_clickable((
                        By.XPATH, 
                        "//input[@type='text' or @type='search' or contains(@class, 'form-control')]"
                    ))
                )
                campo_busca.clear()
                campo_busca.send_keys(nome_aluno)
                campo_busca.send_keys(Keys.RETURN)
                time.sleep(3) # Aguarda atualizar a tabela

                # Passo 2: Procura por itens pendentes
                try:
                    self.log("Buscando registros 'Pendente'...")
                    linha_pendente = espera_curta.until(
                        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Pendente')]"))
                    )
                except Exception:
                    # Quando não houver mais 'Pendente', o loop encerra com sucesso!
                    self.log(f"\n[SUCESSO] Nenhuma pendência restante para {nome_aluno}!")
                    break

                # Passo 3: Acessa a atividade
                self.log("Acessando a atividade pendente...")
                navegador.execute_script("arguments[0].scrollIntoView({block: 'center'});", linha_pendente)
                time.sleep(1)
                navegador.execute_script("arguments[0].click();", linha_pendente)
                time.sleep(3)

                # Passo 4: Atribui a nota 0,75
                self.log("Atribuindo nota 0,75...")
                botao_nota = espera_longa.until(
                    EC.presence_of_element_located((
                        By.XPATH, 
                        "//*[contains(@class, 'correct075') or contains(text(), '0,75')]"
                    ))
                )
                navegador.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_nota)
                time.sleep(1)
                navegador.execute_script("arguments[0].click();", botao_nota)
                time.sleep(1)

                # Passo 5: Tenta clicar no botão de confirmar/aprovar (se houver no sistema)
                try:
                    botao_aprovar = espera_curta.until(
                        EC.element_to_be_clickable((
                            By.XPATH, 
                            "//button[contains(text(), 'Aprovar') or contains(text(), 'Salvar') or contains(text(), 'Confirmar')]"
                        ))
                    )
                    navegador.execute_script("arguments[0].click();", botao_aprovar)
                    time.sleep(2)
                except Exception:
                    # Caso a nota seja salva automaticamente no clique
                    pass

                atividades_processadas += 1
                self.log(f"Atividade nº {atividades_processadas} aprovada!")

                # Passo 6: Retorno para a listagem
                self.log("Retornando para a página de listagem...")
                try:
                    # Tenta fechar caso seja um modal
                    botao_fechar = navegador.find_element(
                        By.XPATH, 
                        "//button[contains(text(), 'Fechar') or contains(@class, 'close')]"
                    )
                    navegador.execute_script("arguments[0].click();", botao_fechar)
                    time.sleep(2)
                except Exception:
                    # Se for uma página normal, realiza a navegação de voltar
                    navegador.back()
                    time.sleep(3)

            # Encerramento
            self.log(f"\n=== PROCESSO FINALIZADO ===")
            self.log(f"Total de pendências zeradas: {atividades_processadas}")
            messagebox.showinfo("Sucesso", f"Todas as pendências de {nome_aluno} foram corrigidas!\nTotal: {atividades_processadas} atividade(s).")

        except Exception as erro:
            self.log(f"Erro na execução: {erro}")
            messagebox.showerror("Erro", f"Ocorreu uma falha: {erro}")

        finally:
            self.btn_iniciar.config(state='normal')

# =============================================================================
# INICIALIZAÇÃO
# =============================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = AppAprovacaoEAD(root)
    root.mainloop()