import tkinter as tk
from tkinter import messagebox

# --- Lógica da Cifra (Mantida do código anterior) ---
ZENIT = "ZENIT"
POLAR = "POLAR"

def criar_mapa_substituicao(chave1, chave2):
    # ... (A mesma lógica de criação de mapa)
    mapa = {}
    for i in range(len(chave1)):
        letra_chave1 = chave1[i]
        letra_chave2 = chave2[i]
        mapa[letra_chave1] = letra_chave2
        mapa[letra_chave2] = letra_chave1
    return mapa

def processar_cifra(texto, mapa):
    # ... (A mesma lógica de processamento)
    texto_processado = ""
    for char in texto:
        if char.isalpha():
            char_maiuscula = char.upper()
            if char_maiuscula in mapa:
                substituto_maiusculo = mapa[char_maiuscula]
                if char.isupper():
                    char_substituido = substituto_maiusculo
                else:
                    char_substituido = substituto_maiusculo.lower()
                texto_processado += char_substituido
            else:
                texto_processado += char
        else:
            texto_processado += char
    return texto_processado

# --- Nova Classe: Aplicação GUI com Tkinter ---

class CifraApp:
    def __init__(self, master):
        self.master = master
        master.title("Cifra ZENIT POLAR")

        self.mapa_cifra = criar_mapa_substituicao(ZENIT, POLAR)

        # 1. Rótulo de Instrução
        self.label = tk.Label(master, text="Digite a mensagem para cifrar/decifrar:")
        self.label.pack(pady=10)

        # 2. Área de Entrada de Texto
        self.entrada_texto = tk.Entry(master, width=50)
        self.entrada_texto.pack(pady=5)

        # 3. Botão de Processamento
        self.botao_processar = tk.Button(master, text="Processar Mensagem", command=self.executar_cifra)
        self.botao_processar.pack(pady=10)

        # 4. Rótulo de Resultado
        self.resultado_label = tk.Label(master, text="Resultado aparecerá aqui.", fg="blue")
        self.resultado_label.pack(pady=10)

    def executar_cifra(self):
        """Função chamada ao clicar no botão."""
        texto_digitado = self.entrada_texto.get()
        
        if not texto_digitado:
            messagebox.showwarning("Aviso", "Por favor, digite uma mensagem.")
            return

        # O mesmo processamento serve para cifrar ou decifrar
        resultado = processar_cifra(texto_digitado, self.mapa_cifra)
        
        # Atualiza o rótulo de resultado
        self.resultado_label.config(text=f"Resultado: {resultado}")

# --- Inicialização da Aplicação ---
if __name__ == "__main__":
    root = tk.Tk()
    app = CifraApp(root)
    root.mainloop()