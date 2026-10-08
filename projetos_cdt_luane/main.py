import sys
import os
import subprocess
import tkinter as tk
from tkinter import messagebox

# Garante que o interpretador reconhece a pasta src e gui
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.camera import reconhecer_cliente

def executar_sistema_unificado():
    """
    Orquestrador Principal (main.py):
    - Aciona o reconhecimento facial inteligente via câmara.
    - Se o cliente for encontrado, transiciona para o PDV comercial (gui/pdv_view.py).
    - Se for novo cliente, abre o fluxo de registo (gui/cadastro_view.py).
    """
    print("[SISTEMA] A iniciar o módulo de biometria facial - Delírio Roxo...")
    
    # Executa a verificação biométrica na câmara
    resultado = reconhecer_cliente()
    
    if not resultado:
        print("[SISTEMA] Operação cancelada pelo operador.")
        sys.exit()

    status = resultado.get("status")

    if status == "encontrado":
        nome = resultado.get('nome', 'Cliente')
        acai = resultado.get('acai_preferido', 'Tradicional')
        print(f"[SUCESSO] Acesso autorizado para: {nome} | Açaí Favorito: {acai}")
        
        # Fecha a janela de transição leve
        root.destroy()
        
        # Dispara o PDV Principal (app.py otimizado)
        try:
            subprocess.run([sys.executable, "gui/pdv_view.py"], check=True)
        except Exception as e:
            print(f"[ERRO] Falha ao iniciar o PDV principal: {e}")
        
    elif status == "novo_cliente":
        print("[INFO] Rosto não registado. A abrir o ecrã de novo cadastro...")
        
        try:
            # Abre o ecrã de registo de forma síncrona
            subprocess.run([sys.executable, "gui/cadastro_view.py"], check=True)
            print("[INFO] Registo concluído. A reiniciar o sistema para login automático...")
            
            # Fecha a janela atual e reinicia o main.py
            root.destroy()
            subprocess.run([sys.executable, "main.py"])
        except Exception as e:
            print(f"[ERRO] Falha no fluxo de cadastro: {e}")
            root.destroy()
        
    elif status == "cancelado":
        print("[SISTEMA] Processo cancelado.")
        root.destroy()
    else:
        print("[SISTEMA] Erro crítico no reconhecimento.")
        root.destroy()

# --- JANELA LEVE DE TRANSIÇÃO INICIAL ---
root = tk.Tk()
root.title("Delírio Roxo - Terminal Inteligente")
root.geometry("400x260")
root.config(bg="#17062F")

tk.Label(root, text="💜 Delírio Roxo - Açaízon 💜", font=("Arial", 14, "bold"), bg="#17062F", fg="#FFFFFF").pack(pady=(25, 10))
tk.Label(root, text="Autenticação Biométrica Ativa", font=("Arial", 10), bg="#17062F", fg="#B9AFC8").pack(pady=5)

btn_iniciar = tk.Button(
    root, text="Iniciar Reconhecimento Facial", font=("Arial", 11, "bold"),
    bg="#E91E83", fg="#FFFFFF", relief="flat", cursor="hand2",
    command=executar_sistema_unificado
)
btn_iniciar.pack(pady=20, ipadx=10, ipady=8)

# Dispara a câmara automaticamente 400ms após abrir a janela
root.after(400, executar_sistema_unificado)

root.mainloop()