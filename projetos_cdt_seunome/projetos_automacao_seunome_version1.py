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
# INTERFACE GRÁFICA (TKINTER) COM FLUXO 100% AUTOMATIZADO
# =============================================================================
class AplicacaoAprovacao100Automated:
    def __init__(self, root):
        self.root = root
        self.root.title("Automação EAD - Correção e Retorno Automático")
        self.root.geometry("520x420")
        self.root.resizable(False, False)
        
        # Configuração do estilo visual
        style = ttk.Style()
        style.theme_use('clam')

        # ---------------------------------------------------------------------
        # Campo de Entrada de Dados (Nome do Jovem)
        # ---------------------------------------------------------------------
        frame_inputs = ttk.LabelFrame(self.root, text=" Dados do Aluno ", padding=15)
        frame_inputs.pack(fill="x", padx=15, pady=10)

        ttk.Label(frame_inputs, text="Nome do Jovem:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_aluno = ttk.Entry(frame_inputs, width=40)
        self.entry_aluno.insert(0, "Leandro do Carmo Xavier")
        self.entry_aluno.grid(row=0, column=1, pady=5, padx=5)

        # ---------------------------------------------------------------------
        # Botão de Disparo do Processo
        # ---------------------------------------------------------------------
        self.btn_iniciar = ttk.Button(
            self.root, 
            text="🚀 Iniciar Correção 100% Automática", 
            command=self.iniciar_processo_thread
        )
        self.btn_iniciar.pack(fill="x", padx=15, pady=5)

        # ---------------------------------------------------------------------
        # Console de Logs na Tela
        # ---------------------------------------------------------------------
        frame_log = ttk.LabelFrame(self.root, text=" Status da Execução ", padding=10)
        frame_log.pack(fill="both", expand=True, padx=15, pady=10)

        self.txt_log = tk.Text(
            frame_log, 
            state='disabled', 
            height=9, 
            wrap='word', 
            bg='#1e1e1e', 
            fg='#00ff00', 
            font=('Consolas', 9)
        )
        self.txt_log.pack(fill="both", expand=True)

    def log(self, mensagem):
        """ Atualiza a caixa de texto da interface com o progresso """
        self.txt_log.config(state='normal')
        self.txt_log.insert(tk.END, f"> {mensagem}\n")
        self.txt_log.see(tk.END)
        self.txt_log.config(state='disabled')

    def iniciar_processo_thread(self):
        """ Executa a automação em segundo plano """
        nome_aluno = self.entry_aluno.get().strip()

        if not nome_aluno:
            messagebox.showwarning("Atenção", "Por favor, digite o nome do jovem!")
            return

        self.btn_iniciar.config(state='disabled')
        
        thread_automacao = threading.Thread(
            target=self.executar_loop_automacao, 
            args=(nome_aluno,),
            daemon=True
        )
        thread_automacao.start()

    # =============================================================================
    # LÓGICA DE AUTOMAÇÃO COM APROVAÇÃO E RETORNO AUTOMÁTICO
    # =============================================================================
    def executar_loop_automacao(self, nome_aluno):
        try:
            self.log(f"Iniciando automação total para: '{nome_aluno}'")
            
            # Conexão com o Chrome aberto na porta 9222
            opcoes_chrome = Options()
            opcoes_chrome.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            
            navegador = webdriver.Chrome(options=opcoes_chrome)
            espera_longa = WebDriverWait(navegador, 10)
            espera_curta = WebDriverWait(navegador, 4)

            atividades_processadas = 0

            # Loop contínuo para tratar todas as pendências
            while True:
                # Step 1: Pesquisa pelo nome do aluno no sistema
                self.log(f"\nPesquisando por '{nome_aluno}' na tabela...")
                campo_busca = espera_longa.until(
                    EC.element_to_be_clickable((
                        By.XPATH, 
                        "//input[@type='text' or @type='search' or contains(@class, 'form-control') or contains(@placeholder, 'Pesquisar')]"
                    ))
                )
                campo_busca.clear()
                campo_busca.send_keys(nome_aluno)
                campo_busca.send_keys(Keys.RETURN)
                time.sleep(3) # Aguarda o carregamento dos resultados filtrados

                # Step 2: Verifica se existe algum registro com status 'Pendente'
                try:
                    self.log("Buscando registros pendentes...")
                    linha_pendente = espera_curta.until(
                        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Pendente')]"))
                    )
                except Exception:
                    # Se não houver mais a palavra 'Pendente', encerra o ciclo com sucesso
                    self.log(f"\n[SUCESSO] Todas as provas de {nome_aluno} foram corrigidas!")
                    break

                # Step 3: Acessa a prova pendente
                self.log("Abrindo a avaliação do aluno...")
                navegador.execute_script("arguments[0].scrollIntoView({block: 'center'});", linha_pendente)
                time.sleep(1)
                navegador.execute_script("arguments[0].click();", linha_pendente)
                time.sleep(3)

                # Step 4: Atribui a nota 0,75
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

                # Step 5: Clica no botão de APROVAR / SALVAR a avaliação
                self.log("Clicando no botão 'Aprovar/Salvar'...")
                try:
                    botao_aprovar = espera_longa.until(
                        EC.presence_of_element_located((
                            By.XPATH, 
                            "//button[contains(text(), 'Aprovar') or contains(text(), 'Salvar') or contains(text(), 'Confirmar') or contains(text(), 'Enviar')]"
                        ))
                    )
                    navegador.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_aprovar)
                    time.sleep(1)
                    navegador.execute_script("arguments[0].click();", botao_aprovar)
                    self.log("Avaliação aprovada e confirmada!")
                    time.sleep(2)
                except Exception:
                    self.log("Nota selecionada (botão de aprovação direta ou autosave).")

                atividades_processadas += 1
                self.log(f"Atividade nº {atividades_processadas} finalizada!")

                # Step 6: Retorno automático para a lista de pesquisa
                self.log("Retornando para a lista de alunos...")
                try:
                    # Verifica se existe um botão de fechar modal/pop-up
                    botao_fechar = navegador.find_element(
                        By.XPATH, 
                        "//button[contains(text(), 'Fechar') or contains(@class, 'close')]"
                    )
                    navegador.execute_script("arguments[0].click();", botao_fechar)
                    time.sleep(2)
                except Exception:
                    # Caso a prova tenha aberto em outra tela, faz a navegação de voltar
                    navegador.back()
                    time.sleep(3)

            # Finalização do processo
            self.log(f"\n=== PROCESSO CONCLUÍDO COM SUCESSO ===")
            self.log(f"Total de provas aprovadas para {nome_aluno}: {atividades_processadas}")
            messagebox.showinfo("Sucesso", f"Processo finalizado!\nTotal de avaliações corrigidas: {atividades_processadas}")

        except Exception as erro:
            self.log(f"Erro no processo: {erro}")
            messagebox.showerror("Erro", f"Ocorreu uma falha: {erro}")
            
        finally:
            self.btn_iniciar.config(state='normal')

# =============================================================================
# INICIALIZAÇÃO DA APLICAÇÃO
# =============================================================================
if __name__ == "__main__":
    janela_principal = tk.Tk()
    app = AplicacaoAprovacao100Automated(janela_principal)
    janela_principal.mainloop()