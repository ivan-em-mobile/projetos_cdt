import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, timedelta
import json, webbrowser

# ================= CONFIG =================

ROOT_USER = "Root master"
ROOT_PASS = "root"
ARQUIVO = "agendamentos.json"

SERVICOS = [
"Encanador","Eletricista","Pintor","Pedreiro","Marceneiro","Mecânico",
"Chaveiro","Informática","Faxineiro","Jardineiro","Vidraceiro",
"Ar-condicionado","Celular","Televisão","Geladeira","Máquina de lavar",
"Internet","Manicure","Cabeleireiro","Barbeiro","Maquiadora","Esteticista",
"Massagista","Professor particular","Professor de inglês","Professor de matemática",
"Professor de música","Personal trainer","Fotógrafo","Editor de vídeo",
"Desenvolvedor de sites","Designer gráfico","Social media","Contador","Advogado",
"Arquiteto","Engenheiro","Corretor de imóveis","Veterinário","Adestrador",
"Passeador de cães","Cuidador de idosos","Babá","DJ","Organizador de festas",
"Decorador","Buffet","Garçom","Cerimonialista","Motorista","Entregador",
"Guincho","Borracheiro","Lava-rápido","Funileiro","Pintor automotivo",
"Eletricista automotivo","Montador de móveis","Instalador de câmeras",
"Energia solar","Técnico de impressora","Técnico de computador","Tradutor",
"Redator","Digitador","Marketing","Designer de interiores","Fotógrafo de eventos",
"Técnico de som","Instalador de alarmes","Costureira","Sapateiro","Piscineiro",
"Serralheiro","Técnico de gás","Tapeceiro","Calheiro","Desentupidora",
"Dedetizador","Cuidador de animais","Professor de dança","Professor de reforço",
"Micro-ondas","Limpeza de sofá","Limpeza de piscina","Limpeza pós-obra",
"Impermeabilização","Instalador de cortinas","Montador de cozinha",
"Montador de TV","Instalador de energia","Outro problema"
]

NOMES = [
"João","Ana","Carlos","Marcos","Julia","Lucas","Beatriz","Rafael",
"Gabriela","Pedro","Larissa","Matheus","Camila","Felipe","Amanda",
"Diego","Isabela","Bruno","Mariana","Gustavo"
]

HORARIOS = ["08:00","10:00","13:00","15:00","17:00","19:00"]

# 10 profissionais para cada serviço
PROFISSIONAIS = []
for i, servico in enumerate(SERVICOS):
    for j in range(10):
        PROFISSIONAIS.append({
            "nome": NOMES[(i+j)%len(NOMES)] + f" {j+1}",
            "servico": servico,
            "preco": 70 + ((i*19+j*17)%230),
            "nota": round(4.1+((i+j)%9)/10,1),
            "distancia": round(1+((i*3+j*2)%100)/10,1)
        })

def carregar():
    try:
        with open(ARQUIVO,"r",encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def salvar(x):
    with open(ARQUIVO,"w",encoding="utf-8") as f:
        json.dump(x,f,ensure_ascii=False,indent=4)

# ================= SISTEMA =================

root=tk.Tk()
root.title("RESOLUCIONADOR")
root.geometry("760x620")
root.resizable(False,False)

escuro=[False]
servico=[""]
profissional=[None]

def limpar():
    for w in root.winfo_children():
        w.destroy()

def cores():
    fundo="#111827" if escuro[0] else "#F5F3FF"
    texto="#FFFFFF" if escuro[0] else "#171329"
    root.configure(bg=fundo)
    for w in root.winfo_children():
        try:
            w.configure(bg=fundo,fg=texto)
        except:
            pass

def tema():
    escuro[0]=not escuro[0]
    tela_inicio()

# ================= INTRODUÇÃO =================

def tela_inicio():

    limpar()

    tk.Label(
        root,text="⚡ RESOLUCIONADOR",
        font=("Arial",30,"bold")
    ).pack(pady=(70,5))

    tk.Label(
        root,text="DE PROBLEMAS",
        font=("Arial",22,"bold")
    ).pack()

    tk.Label(
        root,
        text="Seu problema entra. Uma solução sai.",
        font=("Arial",13)
    ).pack(pady=15)

    tk.Label(
        root,
        text="Um sistema automatizado que identifica o serviço,\n"
             "encontra profissionais e organiza seu atendimento.",
        font=("Arial",11)
    ).pack(pady=10)

    tk.Button(
        root,text="🚀 INICIAR SISTEMA",
        command=login,
        width=28,height=2,
        bg="#6C4BF4",fg="white",
        font=("Arial",11,"bold")
    ).pack(pady=30)

    tk.Button(
        root,
        text="☀️ Modo claro" if escuro[0] else "🌙 Modo escuro",
        command=tema,width=20
    ).pack()

    cores()

# ================= ROOT =================

def login():

    limpar()

    tk.Label(
        root,text="🔐 CENTRAL DE ACESSO",
        font=("Arial",24,"bold")
    ).pack(pady=65)

    tk.Label(root,text="Usuário").pack()
    usuario=tk.Entry(root,width=32)
    usuario.pack(pady=8)

    tk.Label(root,text="Senha").pack()
    senha=tk.Entry(root,width=32,show="●")
    senha.pack(pady=8)

    def entrar():
        if usuario.get()==ROOT_USER and senha.get()==ROOT_PASS:
            sistema()
        else:
            messagebox.showerror("Acesso negado","Dados incorretos.")

    tk.Button(
        root,text="ENTRAR NO SISTEMA",
        command=entrar,width=28,height=2,
        bg="#6C4BF4",fg="white"
    ).pack(pady=25)

    tk.Button(root,text="← Voltar",command=tela_inicio).pack()

    cores()

# ================= SISTEMA AUTOMÁTICO =================

def sistema():

    limpar()

    tk.Label(
        root,text="🧠 CENTRAL INTELIGENTE",
        font=("Arial",24,"bold")
    ).pack(pady=35)

    tk.Label(
        root,
        text="Conte o que aconteceu. O sistema encontra o caminho.",
        font=("Arial",12)
    ).pack()

    problema=tk.Entry(
        root,width=65,font=("Arial",12)
    )
    problema.pack(pady=20)

    def analisar():

        texto=problema.get().lower()

        if not texto:
            messagebox.showwarning(
                "Atenção","Descreva seu problema."
            )
            return

        # identificação automática
        palavras={
            "vazamento":"Encanador",
            "torneira":"Encanador",
            "tomada":"Eletricista",
            "luz":"Eletricista",
            "geladeira":"Geladeira",
            "celular":"Celular",
            "computador":"Informática",
            "notebook":"Informática",
            "internet":"Internet",
            "cabelo":"Cabeleireiro",
            "unha":"Manicure",
            "carro":"Mecânico",
            "pneu":"Borracheiro",
            "piscina":"Piscineiro",
            "cachorro":"Veterinário",
            "gato":"Veterinário"
        }

        achou="Outro problema"

        for palavra,serv in palavras.items():
            if palavra in texto:
                achou=serv
                break

        servico[0]=achou
        profissionais()

    tk.Button(
        root,text="🤖 ANALISAR E RESOLVER",
        command=analisar,width=30,height=2,
        bg="#6C4BF4",fg="white"
    ).pack(pady=15)

    tk.Button(
        root,
        text="🌙/☀️ Alterar tema",
        command=tema
    ).pack()

    cores()

# ================= PROFISSIONAIS =================

def profissionais():

    limpar()

    lista=[
        p for p in PROFISSIONAIS
        if p["servico"]==servico[0]
    ]

    # melhor combinação de preço + nota + distância
    melhor=max(
        lista,
        key=lambda p:p["nota"]*20-p["preco"]*0.08-p["distancia"]
    )

    tk.Label(
        root,text="✨ SOLUÇÃO ENCONTRADA",
        font=("Arial",23,"bold")
    ).pack(pady=25)

    tk.Label(
        root,text=f"Serviço identificado: {servico[0]}",
        font=("Arial",12)
    ).pack()

    tk.Label(
        root,
        text=f"🤖 Recomendação automática: {melhor['nome']}\n"
             f"⭐ {melhor['nota']}  •  R$ {melhor['preco']:.2f}  •  "
             f"📍 {melhor['distancia']} km",
        font=("Arial",12,"bold")
    ).pack(pady=15)

    lista_box=tk.Listbox(
        root,width=85,height=10
    )
    lista_box.pack()

    for p in lista:
        lista_box.insert(
            tk.END,
            f"{p['nome']} | ⭐ {p['nota']} | "
            f"R$ {p['preco']:.2f} | {p['distancia']} km"
        )

    def escolher():

        if not lista_box.curselection():
            messagebox.showwarning(
                "Atenção","Escolha um profissional."
            )
            return

        profissional[0]=lista[
            lista_box.curselection()[0]
        ]

        agendamento()

    tk.Button(
        root,text="✅ USAR ESTA SOLUÇÃO",
        command=escolher,width=28,height=2,
        bg="#6C4BF4",fg="white"
    ).pack(pady=15)

# ================= AGENDAMENTO =================

def agendamento():

    limpar()

    p=profissional[0]

    tk.Label(
        root,text="📅 FINALIZAR SOLUÇÃO",
        font=("Arial",23,"bold")
    ).pack(pady=30)

    tk.Label(
        root,
        text=f"{p['nome']}  •  ⭐ {p['nota']}  •  "
             f"R$ {p['preco']:.2f}",
        font=("Arial",12)
    ).pack()

    datas=[
        (date.today()+timedelta(days=i)).strftime("%d/%m/%Y")
        for i in range(7)
    ]

    tk.Label(root,text="Quando você quer resolver?").pack(pady=(25,5))

    data=ttk.Combobox(
        root,values=datas,state="readonly",width=25
    )
    data.pack()
    data.set(datas[0])

    horario=ttk.Combobox(
        root,values=HORARIOS,state="readonly",width=20
    )
    horario.pack(pady=15)
    horario.set(HORARIOS[0])

    def confirmar():

        x=carregar()

        x.append({
            "profissional":p["nome"],
            "servico":p["servico"],
            "valor":p["preco"],
            "data":data.get(),
            "horario":horario.get(),
            "status":"Confirmado"
        })

        salvar(x)

        messagebox.showinfo(
            "Tudo certo! 🎉",
            "Seu problema foi encaminhado com sucesso!"
        )

        sistema()

    tk.Button(
        root,text="🚀 RESOLVER AGORA",
        command=confirmar,width=28,height=2,
        bg="#6C4BF4",fg="white"
    ).pack(pady=25)

# ================= INÍCIO =================

tela_inicio()
root.mainloop()