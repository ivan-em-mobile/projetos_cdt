import tkinter as tk
from tkinter import messagebox

# --- Lógica de Operações ---

def adicionar(x, y):
    """Realiza a operação de adição."""
    return x + y

def subtrair(x, y):
    """Realiza a operação de subtração."""
    return x - y

def multiplicar(x, y):
    """Realiza a operação de multiplicação."""
    return x * y

def dividir(x, y):
    """Realiza a operação de divisão, com tratamento para divisão por zero."""
    if y == 0:
        return "Erro: Divisão por zero!"
    else:
        return x / y

# --- Aplicação Tkinter ---

class CalculadoraApp:
    def __init__(self, master):
        self.master = master
        master.title("Calculadora Simples")

        # Variáveis de Estado
        self.expressao_atual = ""
        self.operador_anterior = None
        self.primeiro_numero = None

        # Configuração da Tela de Exibição
        self.tela = tk.Entry(master, width=20, font=('Arial', 20), bd=5, relief=tk.SUNKEN, justify='right')
        self.tela.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # Definição dos Botões
        botoes = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3)
        ]
        
        # Criação e Posicionamento dos Botões
        for (texto, linha, coluna) in botoes:
            if texto == '=':
                comando = self.calcular_resultado
                cor_fundo = 'lightblue'
            elif texto in ('+', '-', '*', '/'):
                comando = lambda t=texto: self.definir_operador(t)
                cor_fundo = 'orange'
            elif texto == 'C':
                comando = self.limpar_tela
                cor_fundo = 'red'
            else:
                comando = lambda t=texto: self.clique_numero(t)
                cor_fundo = 'lightgray'

            tk.Button(master, text=texto, font=('Arial', 14), padx=20, pady=20, bg=cor_fundo,
                      command=comando).grid(row=linha, column=coluna, sticky="nsew")

        # Botão de Limpar (C)
        tk.Button(master, text='C', font=('Arial', 14), padx=20, pady=20, bg='red',
                  command=self.limpar_tela).grid(row=5, column=0, columnspan=4, sticky="nsew")


    def clique_numero(self, num):
        """ Adiciona o número ou ponto decimal à expressão atual. """
        self.expressao_atual += str(num)
        self.atualizar_tela()

    def definir_operador(self, op):
        """ Processa a definição de um operador (+, -, *, /). """
        try:
            # Garante que o primeiro_numero seja armazenado antes do operador
            if self.expressao_atual:
                self.primeiro_numero = float(self.expressao_atual)
                self.operador_anterior = op
                self.expressao_atual = "" # Limpa a tela para o próximo número
                self.atualizar_tela()
        except ValueError:
            messagebox.showerror("Erro", "Entrada inválida!")

    def calcular_resultado(self):
        """ Executa o cálculo quando o botão '=' é pressionado. """
        if self.primeiro_numero is None or not self.expressao_atual:
            return

        try:
            num2 = float(self.expressao_atual)
            
            if self.operador_anterior == '+':
                resultado = adicionar(self.primeiro_numero, num2)
            elif self.operador_anterior == '-':
                resultado = subtrair(self.primeiro_numero, num2)
            elif self.operador_anterior == '*':
                resultado = multiplicar(self.primeiro_numero, num2)
            elif self.operador_anterior == '/':
                resultado = dividir(self.primeiro_numero, num2)
            else:
                return

            self.exibir_resultado(resultado)
            
        except ValueError:
            messagebox.showerror("Erro", "Entrada inválida!")

    def exibir_resultado(self, resultado):
        """ Exibe o resultado e prepara para o próximo cálculo. """
        self.limpar_tela()
        
        if isinstance(resultado, str) and "Erro" in resultado:
            self.tela.insert(0, resultado)
            self.primeiro_numero = None
        else:
            # Formata o resultado para evitar números com muitas casas decimais
            self.tela.insert(0, str(round(resultado, 8)))
            
            # Armazena o resultado como o primeiro número para encadeamento
            self.primeiro_numero = resultado
            
        self.expressao_atual = ""
        self.operador_anterior = None


    def atualizar_tela(self):
        """ Atualiza o texto na tela de exibição. """
        self.tela.delete(0, tk.END)
        self.tela.insert(0, self.expressao_atual)

    def limpar_tela(self):
        """ Reseta todas as variáveis e limpa a tela. """
        self.expressao_atual = ""
        self.operador_anterior = None
        self.primeiro_numero = None
        self.tela.delete(0, tk.END)


if __name__ == '__main__':
    root = tk.Tk()
    app = CalculadoraApp(root)
    root.mainloop()