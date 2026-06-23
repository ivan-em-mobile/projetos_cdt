import tkinter as tk
from tkinter import messagebox

# --- LÓGICA DA CIFRA (Sua lógica original preservada) ---

ZENIT = "ZENIT"
POLAR = "POLAR"

def criar_mapa_substituicao(chave1, chave2):
    mapa = {}
    for i in range(len(chave1)):
        mapa[chave1[i]] = chave2[i]
        mapa[chave2[i]] = chave1[i]
    return mapa

MAPA_ZENIT_POLAR = criar_mapa_substituicao(ZENIT, POLAR)

def processar_cifra(texto):
    """Cifra ou decifra o texto usando o mapa global."""
    texto_processado = ""
    for char in texto:
        if char.isalpha():
            char_maiuscula = char.upper()
            if char_maiuscula in MAPA_ZENIT_POLAR:
                substituto = MAPA_ZENIT_POLAR[char_maiuscula]
                # Preserva maiúsculas/minúsculas
                char_substituido = substituto if char.isupper() else substituto.lower()
                texto_processado += char_substituido
            else:
                texto_processado += char
        else:
            texto_processado += char
    return texto_processado

# --- INTERFACE GRÁFICA (GUI) ---

class AppCifra:
    def __init__(self, root):
        self.root = root
        self.root.title("Cifrador ZENIT POLAR")
        self.root.geometry("500x450")
        self.root.configure(bg="#2C3E50") # Azul escuro elegante

        # Título
        tk.Label(
            root, text="🔑 ZENIT POLAR", font=("Helvetica", 20, "bold"),
            bg="#2C3E50", fg="#ECF0F1"
        ).pack(pady=20)

        # Rótulo Entrada
        tk.Label(root, text="Digite sua mensagem:", bg="#2C3E50", fg="#BDC3C7").pack()
        
        # Campo de Entrada (Texto longo)
        self.entrada_texto = tk.Text(root, height=5, width=50, font=("Consolas", 12))
        self.entrada_texto.pack(pady=10, padx=20)

        # Botão Processar
        self.btn_converter = tk.Button(
            root, text="CIFRAR / DECIFRAR", font=("Helvetica", 12, "bold"),
            bg="#E67E22", fg="white", command=self.converter,
            activebackground="#D35400", cursor="hand2"
        )
        self.btn_converter.pack(pady=10)

        # Rótulo Saída
        tk.Label(root, text="Resultado:", bg="#2C3E50", fg="#BDC3C7").pack()

        # Campo de Saída (Apenas leitura)
        self.saida_texto = tk.Text(root, height=5, width=50, font=("Consolas", 12), bg="#ECF0F1")
        self.saida_texto.pack(pady=10, padx=20)

        # Botão Limpar
        tk.Button(root, text="Limpar", command=self.limpar).pack()

    def converter(self):
        # Pega o texto da entrada
        conteudo = self.entrada_texto.get("1.0", tk.END).strip()
        if not conteudo:
            messagebox.showwarning("Aviso", "Por favor, digite algum texto!")
            return

        # Processa
        resultado = processar_cifra(conteudo)

        # Exibe na saída
        self.saida_texto.delete("1.0", tk.END)
        self.saida_texto.insert(tk.END, resultado)

    def limpar(self):
        self.entrada_texto.delete("1.0", tk.END)
        self.saida_texto.delete("1.0", tk.END)

# Execução
if __name__ == "__main__":
    root = tk.Tk()
    AppCifra(root)
    root.mainloop()