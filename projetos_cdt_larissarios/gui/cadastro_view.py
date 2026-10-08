import sys
import types

# --- PROTEÇÃO PARA O TF_KERAS (MOCK) ---
if 'tf_keras' not in sys.modules:
    tf_keras_mock = types.ModuleType('tf_keras')
    tf_keras_mock.__version__ = '2.15.0'
    sys.modules['tf_keras'] = tf_keras_mock
else:
    if not hasattr(sys.modules['tf_keras'], '__version__'):
        sys.modules['tf_keras'].__version__ = '2.15.0'

import os
os.environ['TF_USE_LEGACY_KERAS'] = '1'

import tkinter as tk
from tkinter import messagebox
import cv2
import sqlite3
from deepface import DeepFace

DB_NAME = 'acaiteria.db'

def garantir_estrutura_banco():
    """Cria a tabela se não existir e garante dinamicamente a presença da coluna foto_path[cite: 9]."""
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            acai_preferido TEXT
        );
    """)
    
    cursor.execute("PRAGMA table_info(clientes);")
    colunas = [info[1] for info in cursor.fetchall()]
    if 'foto_path' not in colunas:
        try:
            cursor.execute("ALTER TABLE clientes ADD COLUMN foto_path TEXT;")
            print("[BD] Coluna 'foto_path' adicionada com sucesso à tabela existente[cite: 9].")
        except Exception as e:
            print(f"[AVISO] Não foi possível adicionar a coluna automaticamente: {e}")
            
    conexao.commit()
    conexao.close()

def salvar_novo_cliente(nome, acai, frame_atual):
    """Captura a foto do novo cliente, guarda no disco e regista os dados no SQLite[cite: 9]."""
    if not nome or not acai:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos!")
        return

    garantir_estrutura_banco()

    os.makedirs("imagens_clientes", exist_ok=True)
    foto_path = f"imagens_clientes/{nome.strip().replace(' ', '_')}.jpg"
    
    cv2.imwrite(foto_path, frame_atual)

    try:
        conexao = sqlite3.connect(DB_NAME)
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO clientes (nome, acai_preferido, foto_path) 
            VALUES (?, ?, ?);
        """, (nome, acai, foto_path))
        conexao.commit()
        conexao.close()
        
        messagebox.showinfo("Sucesso", f"Cliente {nome} cadastrado com sucesso!")
        janela_cadastro.destroy()
    except Exception as e:
        messagebox.showerror("Erro na Base de Dados", f"Não foi possível salvar: {e}")

def capturar_foto_cadastro():
    """Abre a webcam para capturar o rosto do novo cliente[cite: 9]."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Erro", "Não foi possível aceder à webcam.")
        return

    frame_capturado = None
    messagebox.showinfo("Câmera", "Olhe para a câmara e pressione a tecla 'ESPAÇO' para tirar a foto.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        cv2.putText(frame, "Pressione ESPAÇO para capturar", (30, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Delirio Roxo - Cadastro de Cliente", frame)
        
        tecla = cv2.waitKey(1) & 0xFF
        if tecla == 32: # ESPAÇO
            frame_capturado = frame.copy()
            break
        elif tecla == 27: # ESC
            break

    cap.release()
    cv2.destroyAllWindows()
    return frame_capturado

# --- INTERFACE GRÁFICA DE CADASTRO ---
garantir_estrutura_banco()

janela_cadastro = tk.Tk()
janela_cadastro.title("Delírio Roxo - Cadastro de Novo Cliente")
janela_cadastro.geometry("400x400")
janela_cadastro.config(bg="#f4f0fa")

tk.Label(janela_cadastro, text="💜 Novo Cliente - Delírio Roxo 💜", font=("Helvetica", 13, "bold"), bg="#f4f0fa", fg="#4a154b").pack(pady=15)

tk.Label(janela_cadastro, text="Nome do Cliente:", bg="#f4f0fa", font=("Helvetica", 10)).pack(anchor="w", padx=40)
entry_nome = tk.Entry(janela_cadastro, font=("Helvetica", 11), width=25)
entry_nome.pack(pady=5, padx=40)

tk.Label(janela_cadastro, text="Açaí Preferido:", bg="#f4f0fa", font=("Helvetica", 10)).pack(anchor="w", padx=40)
entry_acai = tk.Entry(janela_cadastro, font=("Helvetica", 11), width=25)
entry_acai.pack(pady=5, padx=40)

frame_foto_capturada = [None]

def acao_capturar():
    img = capturar_foto_cadastro()
    if img is not None:
        frame_foto_capturada[0] = img
        lbl_foto_status.config(text="Status: Foto capturada com sucesso! ✅", fg="green")

btn_foto = tk.Button(janela_cadastro, text="Tirar Foto Biométrica", command=acao_capturar, font=("Helvetica", 10), bg="#512da8", fg="white", width=22)
btn_foto.pack(pady=15)

lbl_foto_status = tk.Label(janela_cadastro, text="Status: Nenhuma foto tirada", font=("Helvetica", 9), bg="#f4f0fa", fg="#666")
lbl_foto_status.pack(pady=5)

def acao_salvar():
    if frame_foto_capturada[0] is None:
        messagebox.showwarning("Aviso", "Tens de tirar uma foto antes de salvar o cadastro!")
        return
    salvar_novo_cliente(entry_nome.get(), entry_acai.get(), frame_foto_capturada[0])

btn_salvar = tk.Button(janela_cadastro, text="Salvar Cadastro", command=acao_salvar, font=("Helvetica", 11, "bold"), bg="#2e7d32", fg="white", width=22)
btn_salvar.pack(pady=15)

janela_cadastro.mainloop()