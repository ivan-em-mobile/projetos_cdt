import datetime
import os
import random
import threading
import time
import customtkinter as ctk
from PIL import Image
from pynput import keyboard
from tkVideoPlayer import TkinterVideo

# Tenta importar o psutil sem quebrar o código caso ele não esteja instalado
try:
    import psutil

    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

# --- CONFIGURAÇÕES VISUAIS DO CUSTOMTKINTER ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class MotorIALocalAvancado:
    """Gerenciador local de IA/Comandos offline com sistema de respostas expansível."""

    def __init__(self):
        self.historico_interacoes = []
        self.conhecimento = {
            "ajuda": (
                "📌 **Comandos e Recursos Disponíveis:**\n"
                "- `status`: Diagnóstico do sistema e performance.\n"
                "- `atalhos`: Como usar as teclas de atalho.\n"
                "- `recursos`: Informações de CPU/RAM em uso.\n"
                "- `notas`: Instruções do bloco de notas integrado.\n"
                "- `limpar`: Reseta a janela de chat atual."
            ),
            "status": "🟢 **Sistema 100% Operacional!** Vídeo, overlay e escuta global ativos.",
            "atalhos": "⌨️  Pressione **Alt + Z** para ocultar ou exibir a janela a qualquer momento.",
            "recursos": "📊 Veja o consumo em tempo real na aba 'Sistema' no menu esquerdo.",
            "notas": "📝 Use a aba 'Notas' para rascunhos rápidos. As anotações podem ser salvas localmente.",
            "oi": "Olá! Como posso te auxiliar em sua área de trabalho hoje?",
            "olá": "Olá! Como posso te auxiliar em sua área de trabalho hoje?",
            "bom dia": "Bom dia! Pronto para começar o trabalho?",
            "boa tarde": "Boa tarde! Como estão as tarefas por aí?",
            "boa noite": "Boa noite! Precisando de um vídeo de apoio ou notas rápidas?",
            "omnioverlay": "O OmniOverlay é uma suíte flutuante com player de vídeo, anotações e IA local.",
        }

    def processar_mensagem(self, mensagem: str) -> str:
        texto = mensagem.lower().strip()
        self.historico_interacoes.append(texto)

        # Busca por palavras-chave registradas
        for chave, resposta in self.conhecimento.items():
            if chave in texto:
                return resposta

        # Lógica de fallback para entradas desconhecidas
        respostas_fallback = [
            (
                "Estou operando em modo local. Não reconheci o comando. Digite"
                " 'ajuda' para ver a lista."
            ),
            (
                "Comando offline não mapeado. Experimente digitar 'status' ou"
                " 'atalhos'."
            ),
            "Instrução não encontrada. Digite 'ajuda' para ver todas as opções.",
        ]
        return random.choice(respostas_fallback)


class OmniOverlayApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # --- CONFIGURAÇÕES DA JANELA ---
        self.title("OmniOverlay Dashboard & Assistant")
        self.geometry("1000x620")
        self.minsize(850, 500)
        self.attributes("-topmost", True)
        self.visible = True

        self.ia = MotorIALocalAvancado()
        self.video_duration = 0
        self.updating_slider = False

        # --- ESTRUTURA DA INTERFACE (SIDEBAR + CONTEÚDO) ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._criar_sidebar()
        self._criar_container_principal()

        # Iniciar abas
        self._criar_aba_midia()
        self._criar_aba_chat()
        self._criar_aba_notas()
        self._criar_aba_sistema()

        # Selecionar aba inicial (Mídia)
        self.selecionar_aba("midia")

        # Iniciar Threads do Sistema
        self.iniciar_atalho_global()
        self.iniciar_monitoramento_sistema()

    # ==========================================
    # CRIAÇÃO DE ELEMENTOS DA UI
    # ==========================================
    def _criar_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=170, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.lbl_logo = ctk.CTkLabel(
            self.sidebar_frame,
            text="OMNI OVERLAY",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        self.lbl_logo.grid(row=0, column=0, padx=15, pady=20)

        self.btn_nav_midia = ctk.CTkButton(
            self.sidebar_frame,
            text="📺 Mídia & Player",
            command=lambda: self.selecionar_aba("midia"),
        )
        self.btn_nav_midia.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.btn_nav_chat = ctk.CTkButton(
            self.sidebar_frame,
            text="🤖 Assistente IA",
            command=lambda: self.selecionar_aba("chat"),
        )
        self.btn_nav_chat.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.btn_nav_notas = ctk.CTkButton(
            self.sidebar_frame,
            text="📝 Bloco de Notas",
            command=lambda: self.selecionar_aba("notas"),
        )
        self.btn_nav_notas.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.btn_nav_sistema = ctk.CTkButton(
            self.sidebar_frame,
            text="⚙️ Sistema",
            command=lambda: self.selecionar_aba("sistema"),
        )
        self.btn_nav_sistema.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        # Status rápido no rodapé da sidebar
        self.lbl_status_topmost = ctk.CTkLabel(
            self.sidebar_frame,
            text="📌 Sempre no Topo: Ativo",
            font=ctk.CTkFont(size=10),
        )
        self.lbl_status_topmost.grid(row=6, column=0, padx=10, pady=10)

    def _criar_container_principal(self):
        self.content_frame = ctk.CTkFrame(
            self, corner_radius=10, fg_color="transparent"
        )
        self.content_frame.grid(
            row=0, column=1, padx=15, pady=15, sticky="nsew"
        )
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

    def selecionar_aba(self, aba: str):
        # Esconde todas as abas
        self.frame_aba_midia.grid_forget()
        self.frame_aba_chat.grid_forget()
        self.frame_aba_notas.grid_forget()
        self.frame_aba_sistema.grid_forget()

        # Exibe a aba solicitada
        if aba == "midia":
            self.frame_aba_midia.grid(row=0, column=0, sticky="nsew")
        elif aba == "chat":
            self.frame_aba_chat.grid(row=0, column=0, sticky="nsew")
        elif aba == "notas":
            self.frame_aba_notas.grid(row=0, column=0, sticky="nsew")
        elif aba == "sistema":
            self.frame_aba_sistema.grid(row=0, column=0, sticky="nsew")

    # ==========================================
    # ABA 1: PLAYER DE VÍDEO
    # ==========================================
    def _criar_aba_midia(self):
        self.frame_aba_midia = ctk.CTkFrame(
            self.content_frame, corner_radius=10
        )
        self.frame_aba_midia.grid_rowconfigure(1, weight=1)
        self.frame_aba_midia.grid_columnconfigure(0, weight=1)

        # Cabeçalho
        lbl_head = ctk.CTkLabel(
            self.frame_aba_midia,
            text="Central de Mídia Flutuante",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        lbl_head.grid(row=0, column=0, pady=10)

        # Player
        self.video_player = TkinterVideo(
            master=self.frame_aba_midia, scaled=True
        )
        self.video_player.grid(
            row=1, column=0, padx=10, pady=5, sticky="nsew"
        )

        # Eventos do Player
        self.video_player.bind(
            "<<Duration>>", self._on_video_duration_found
        )
        self.video_player.bind("<<SecondChanged>>", self._on_second_changed)
        self.video_player.bind("<<Ended>>", self._on_video_ended)

        # Controles (Corrigido o sticky="ew" no lugar de fill="x")
        frame_controls = ctk.CTkFrame(
            self.frame_aba_midia, fg_color="transparent"
        )
        frame_controls.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        # Linha 1 dos Controles: Slider + Tempo
        frame_slider = ctk.CTkFrame(frame_controls, fg_color="transparent")
        frame_slider.pack(fill="x", pady=2)

        self.lbl_tempo_atual = ctk.CTkLabel(
            frame_slider, text="00:00", font=ctk.CTkFont(size=11)
        )
        self.lbl_tempo_atual.pack(side="left", padx=5)

        self.slider_progresso = ctk.CTkSlider(
            frame_slider,
            from_=0,
            to=100,
            command=self._on_seek_slider,
        )
        self.slider_progresso.set(0)
        self.slider_progresso.pack(side="left", fill="x", expand=True, padx=5)

        self.lbl_tempo_total = ctk.CTkLabel(
            frame_slider, text="00:00", font=ctk.CTkFont(size=11)
        )
        self.lbl_tempo_total.pack(side="right", padx=5)

        # Linha 2 dos Controles: Botões
        frame_botoes = ctk.CTkFrame(frame_controls, fg_color="transparent")
        frame_botoes.pack(fill="x", pady=5)

        btn_load = ctk.CTkButton(
            frame_botoes,
            text="📁 Abrir Arquivo",
            command=self.carregar_video,
            width=110,
        )
        btn_load.pack(side="left", padx=5)

        btn_rewind = ctk.CTkButton(
            frame_botoes,
            text="⏪ -5s",
            command=lambda: self.avancar_recuar(-5),
            width=65,
        )
        btn_rewind.pack(side="left", padx=2)

        self.btn_play_pause = ctk.CTkButton(
            frame_botoes,
            text="▶ Play",
            command=self.toggle_video,
            width=90,
        )
        self.btn_play_pause.pack(side="left", padx=2)

        btn_forward = ctk.CTkButton(
            frame_botoes,
            text="⏩ +5s",
            command=lambda: self.avancar_recuar(5),
            width=65,
        )
        btn_forward.pack(side="left", padx=2)

    def carregar_video(self):
        file_path = ctk.filedialog.askopenfilename(
            filetypes=[
                (
                    "Arquivos de Vídeo",
                    "*.mp4 *.mkv *.avi *.mov *.flv *.wmv",
                )
            ]
        )
        if file_path:
            self.video_player.load(file_path)
            self.video_player.play()
            self.btn_play_pause.configure(text="⏸ Pause")

    def toggle_video(self):
        if self.video_player.is_paused():
            self.video_player.play()
            self.btn_play_pause.configure(text="⏸ Pause")
        else:
            self.video_player.pause()
            self.btn_play_pause.configure(text="▶ Play")

    def avancar_recuar(self, segundos):
        if self.video_duration > 0:
            pos_atual = self.slider_progresso.get()
            nova_pos = max(0, min(self.video_duration, pos_atual + segundos))
            self.video_player.seek(int(nova_pos))

    def _on_video_duration_found(self, event):
        info = self.video_player.video_info()
        self.video_duration = info.get("duration", 0)
        self.slider_progresso.configure(to=self.video_duration)
        self.lbl_tempo_total.configure(
            text=str(datetime.timedelta(seconds=int(self.video_duration)))
        )

    def _on_second_changed(self, event):
        if not self.updating_slider and self.video_duration > 0:
            pos = self.slider_progresso.get() + 1
            if pos <= self.video_duration:
                self.slider_progresso.set(pos)
                self.lbl_tempo_atual.configure(
                    text=str(datetime.timedelta(seconds=int(pos)))
                )

    def _on_seek_slider(self, value):
        self.updating_slider = True
        self.video_player.seek(int(value))
        self.lbl_tempo_atual.configure(
            text=str(datetime.timedelta(seconds=int(value)))
        )
        self.updating_slider = False

    def _on_video_ended(self, event):
        self.btn_play_pause.configure(text="▶ Play")
        self.slider_progresso.set(0)
        self.lbl_tempo_atual.configure(text="00:00")

    # ==========================================
    # ABA 2: CHAT ASSISTENTE LOCAL
    # ==========================================
    def _criar_aba_chat(self):
        self.frame_aba_chat = ctk.CTkFrame(self.content_frame, corner_radius=10)
        self.frame_aba_chat.grid_rowconfigure(1, weight=1)
        self.frame_aba_chat.grid_columnconfigure(0, weight=1)

        lbl_head = ctk.CTkLabel(
            self.frame_aba_chat,
            text="Assistente Local Omni (Sem API)",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        lbl_head.grid(row=0, column=0, pady=10)

        self.txt_chat = ctk.CTkTextbox(self.frame_aba_chat, state="disabled")
        self.txt_chat.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        frame_in = ctk.CTkFrame(self.frame_aba_chat, fg_color="transparent")
        frame_in.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        self.entry_chat = ctk.CTkEntry(
            frame_in, placeholder_text="Digite 'ajuda' para comandos..."
        )
        self.entry_chat.pack(side="left", fill="x", expand=True, padx=5)
        self.entry_chat.bind("<Return>", lambda e: self.enviar_msg_chat())

        btn_send = ctk.CTkButton(
            frame_in, text="Enviar", width=80, command=self.enviar_msg_chat
        )
        btn_send.pack(side="right", padx=5)

        self.adicionar_log_chat(
            "Sistema",
            "Assistente offline inicializado. Digite 'ajuda' para ver comandos.",
        )

    def enviar_msg_chat(self):
        txt = self.entry_chat.get().strip()
        if not txt:
            return

        self.entry_chat.delete(0, "end")
        self.adicionar_log_chat("Você", txt)

        if txt.lower() == "limpar":
            self.txt_chat.configure(state="normal")
            self.txt_chat.delete("1.0", "end")
            self.txt_chat.configure(state="disabled")
            self.adicionar_log_chat("Sistema", "Chat resetado com sucesso.")
            return

        resp = self.ia.processar_mensagem(txt)
        self.adicionar_log_chat("OmniBot", resp)

    def adicionar_log_chat(self, autor, msg):
        self.txt_chat.configure(state="normal")
        self.txt_chat.insert("end", f"[{autor}]: {msg}\n\n")
        self.txt_chat.see("end")
        self.txt_chat.configure(state="disabled")

    # ==========================================
    # ABA 3: BLOCO DE NOTAS RÁPIDAS
    # ==========================================
    def _criar_aba_notas(self):
        self.frame_aba_notas = ctk.CTkFrame(
            self.content_frame, corner_radius=10
        )
        self.frame_aba_notas.grid_rowconfigure(1, weight=1)
        self.frame_aba_notas.grid_columnconfigure(0, weight=1)

        lbl_head = ctk.CTkLabel(
            self.frame_aba_notas,
            text="Bloco de Anotações Rápidas",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        lbl_head.grid(row=0, column=0, pady=10)

        self.txt_notas = ctk.CTkTextbox(
            self.frame_aba_notas, font=ctk.CTkFont(size=13)
        )
        self.txt_notas.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        frame_btn = ctk.CTkFrame(self.frame_aba_notas, fg_color="transparent")
        frame_btn.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        btn_salvar = ctk.CTkButton(
            frame_btn, text="💾 Salvar Nota", command=self.salvar_nota
        )
        btn_salvar.pack(side="left", padx=5)

        btn_limpar = ctk.CTkButton(
            frame_btn, text="🗑️ Limpar Texto", command=self.limpar_nota
        )
        btn_limpar.pack(side="left", padx=5)

    def salvar_nota(self):
        conteudo = self.txt_notas.get("1.0", "end-1c")
        if conteudo.strip():
            filepath = ctk.filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Texto", "*.txt"), ("Todos os arquivos", "*.*")],
            )
            if filepath:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(conteudo)

    def limpar_nota(self):
        self.txt_notas.delete("1.0", "end")

    # ==========================================
    # ABA 4: DIAGNÓSTICO DO SISTEMA
    # ==========================================
    def _criar_aba_sistema(self):
        self.frame_aba_sistema = ctk.CTkFrame(
            self.content_frame, corner_radius=10
        )
        self.frame_aba_sistema.grid_columnconfigure(0, weight=1)

        lbl_head = ctk.CTkLabel(
            self.frame_aba_sistema,
            text="Monitoramento do Sistema & Configurações",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        lbl_head.grid(row=0, column=0, pady=15)

        # Medidor de CPU
        self.lbl_cpu = ctk.CTkLabel(
            self.frame_aba_sistema, text="CPU: 0%", font=ctk.CTkFont(size=14)
        )
        self.lbl_cpu.grid(row=1, column=0, pady=5)

        self.progress_cpu = ctk.CTkProgressBar(self.frame_aba_sistema, width=300)
        self.progress_cpu.set(0)
        self.progress_cpu.grid(row=2, column=0, pady=5)

        # Medidor de RAM
        self.lbl_ram = ctk.CTkLabel(
            self.frame_aba_sistema,
            text="RAM: 0%",
            font=ctk.CTkFont(size=14),
        )
        self.lbl_ram.grid(row=3, column=0, pady=(15, 5))

        self.progress_ram = ctk.CTkProgressBar(self.frame_aba_sistema, width=300)
        self.progress_ram.set(0)
        self.progress_ram.grid(row=4, column=0, pady=5)

        # Opções adicionais
        self.switch_topmost = ctk.CTkSwitch(
            self.frame_aba_sistema,
            text="Manter Janela Sempre no Topo",
            command=self.toggle_topmost,
        )
        self.switch_topmost.select()
        self.switch_topmost.grid(row=5, column=0, pady=25)

    def toggle_topmost(self):
        estado = bool(self.switch_topmost.get())
        self.attributes("-topmost", estado)
        self.lbl_status_topmost.configure(
            text=f"📌 Sempre no Topo: {'Ativo' if estado else 'Inativo'}"
        )

    def iniciar_monitoramento_sistema(self):
        def atualizar_metricas():
            while True:
                if HAS_PSUTIL:
                    cpu_usage = psutil.cpu_percent(interval=1)
                    ram_usage = psutil.virtual_memory().percent
                else:
                    cpu_usage = 0
                    ram_usage = 0

                try:
                    if HAS_PSUTIL:
                        self.lbl_cpu.configure(text=f"CPU: {cpu_usage}%")
                        self.progress_cpu.set(cpu_usage / 100.0)

                        self.lbl_ram.configure(text=f"RAM: {ram_usage}%")
                        self.progress_ram.set(ram_usage / 100.0)
                    else:
                        self.lbl_cpu.configure(text="CPU: N/A (psutil ausente)")
                        self.lbl_ram.configure(text="RAM: N/A (psutil ausente)")
                except Exception:
                    break
                time.sleep(1)

        t = threading.Thread(target=atualizar_metricas, daemon=True)
        t.start()

    # ==========================================
    # ATALHO GLOBAL (ALT + Z)
    # ==========================================
    def alternar_visibilidade(self):
        if self.visible:
            self.withdraw()
            self.visible = False
        else:
            self.deiconify()
            self.attributes("-topmost", self.switch_topmost.get() == 1)
            self.visible = True

    def iniciar_atalho_global(self):
        def listener():
            with keyboard.GlobalHotKeys(
                {"<alt>+z": self.alternar_visibilidade}
            ) as h:
                h.join()

        t = threading.Thread(target=listener, daemon=True)
        t.start()


# --- PONTO DE ENTRADA DO PROGRAMA ---
if __name__ == "__main__":
    app = OmniOverlayApp()
    app.mainloop()