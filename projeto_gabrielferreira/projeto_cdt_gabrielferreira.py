import customtkinter as ctk

# Configuração inicial do CustomTkinter
ctk.set_appearance_mode("System")  # Opções: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Opções: "blue", "green", "dark-blue"


class AppBarbearia(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Configurações da Janela Principal
        self.title("Barbearia Andrades - Agendamento")
        self.geometry("500x600")
        self.resizable(False, False)

        # Banco de dados temporário (em memória)
        self.nome_salvo = ""
        self.data_salva = ""
        self.horario_salvo = ""

        # Inicializa exibindo o Menu Principal
        self.mostrar_menu_principal()

    def limpar_janela(self):
        """Remove todos os componentes da janela atual antes de desenhar a nova tela."""
        for widget in self.winfo_children():
            widget.destroy()

    def mostrar_menu_principal(self):
        self.limpar_janela()

        # Título
        label_titulo = ctk.CTkLabel(
            self,
            text="Barbearia Andrades",
            font=ctk.CTkFont(size=26, weight="bold"),
        )
        label_titulo.pack(pady=(30, 5))

        label_subtitulo = ctk.CTkLabel(
            self,
            text="Seja Bem-Vindo! Escolha uma opção:",
            font=ctk.CTkFont(size=14),
        )
        label_subtitulo.pack(pady=(0, 25))

        # Botões do Menu
        btn_agendar = ctk.CTkButton(
            self,
            text="1 - Agendar Horário",
            width=250,
            height=40,
            command=self.tela_agendar,
        )
        btn_agendar.pack(pady=10)

        btn_cancelar = ctk.CTkButton(
            self,
            text="2 - Cancelar Agendamento",
            width=250,
            height=40,
            command=self.tela_cancelar,
        )
        btn_cancelar.pack(pady=10)

        btn_servicos = ctk.CTkButton(
            self,
            text="3 - Serviços Disponíveis",
            width=250,
            height=40,
            command=self.tela_servicos,
        )
        btn_servicos.pack(pady=10)

        btn_contato = ctk.CTkButton(
            self,
            text="4 - Localização e Contato",
            width=250,
            height=40,
            command=self.tela_contato,
        )
        btn_contato.pack(pady=10)

        btn_avaliar = ctk.CTkButton(
            self,
            text="5 - Avalie Nosso Serviço",
            width=250,
            height=40,
            command=self.tela_avaliar,
        )
        btn_avaliar.pack(pady=10)

        btn_sair = ctk.CTkButton(
            self,
            text="0 - Sair",
            width=250,
            height=40,
            fg_color="#A83232",
            hover_color="#7A2222",
            command=self.destroy,
        )
        btn_sair.pack(pady=(30, 10))

    # --- TELA 1: AGENDAR ---
    def tela_agendar(self):
        self.limpar_janela()

        ctk.CTkLabel(
            self,
            text="Agendamento de Horário",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=20)

        # Campos de entrada
        ctk.CTkLabel(self, text="Seu Nome:").pack(anchor="w", padx=120)
        entry_nome = ctk.CTkEntry(
            self, width=260, placeholder_text="Digite seu nome"
        )
        entry_nome.pack(pady=(0, 15))

        ctk.CTkLabel(self, text="Data (EX: 09/10/2026):").pack(
            anchor="w", padx=120
        )
        entry_data = ctk.CTkEntry(
            self, width=260, placeholder_text="09/10/2026"
        )
        entry_data.pack(pady=(0, 15))

        ctk.CTkLabel(self, text="Horário (EX: 17:30):").pack(
            anchor="w", padx=120
        )
        entry_horario = ctk.CTkEntry(self, width=260, placeholder_text="17:30")
        entry_horario.pack(pady=(0, 25))

        # Label para mensagens de feedback
        lbl_status = ctk.CTkLabel(self, text="", text_color="green")
        lbl_status.pack(pady=5)

        def salvar_agendamento():
            if (
                not entry_nome.get()
                or not entry_data.get()
                or not entry_horario.get()
            ):
                lbl_status.configure(
                    text="Por favor, preencha todos os campos!",
                    text_color="red",
                )
                return

            self.nome_salvo = entry_nome.get()
            self.data_salva = entry_data.get()
            self.horario_salvo = entry_horario.get()

            lbl_status.configure(
                text=f"Agendamento realizado com sucesso, {self.nome_salvo}!\nObrigado pela preferência! >.<",
                text_color="#22C55E",
            )

        btn_salvar = ctk.CTkButton(
            self, text="Confirmar Agendamento", command=salvar_agendamento
        )
        btn_salvar.pack(pady=10)

        ctk.CTkButton(
            self,
            text="Voltar ao Menu",
            fg_color="gray",
            hover_color="#555555",
            command=self.mostrar_menu_principal,
        ).pack(pady=10)

    # --- TELA 2: CANCELAR ---
    def tela_cancelar(self):
        self.limpar_janela()

        ctk.CTkLabel(
            self,
            text="Cancelar Agendamento",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=20)

        if self.nome_salvo == "":
            ctk.CTkLabel(
                self,
                text="Você ainda não possui um agendamento ativo.\n\nPor favor, volte e agende um horário.",
                text_color="yellow",
            ).pack(pady=30)
        else:
            ctk.CTkLabel(
                self, text="Para cancelar, confirme seu nome:"
            ).pack(pady=10)
            entry_cancela_nome = ctk.CTkEntry(self, width=260)
            entry_cancela_nome.pack(pady=10)

            lbl_status_cancelar = ctk.CTkLabel(self, text="")
            lbl_status_cancelar.pack(pady=5)

            def efetuar_cancelamento():
                if entry_cancela_nome.get() == self.nome_salvo:
                    lbl_status_cancelar.configure(
                        text=f"Agendamento de {self.nome_salvo} para o dia {self.data_salva} às {self.horario_salvo} foi CANCELADO!",
                        text_color="red",
                    )
                    # Limpa as variáveis
                    self.nome_salvo = ""
                    self.data_salva = ""
                    self.horario_salvo = ""
                else:
                    lbl_status_cancelar.configure(
                        text="Nome diferente do agendado! Tente novamente.",
                        text_color="red",
                    )

            btn_confirma_cancelar = ctk.CTkButton(
                self,
                text="Confirmar Cancelamento",
                fg_color="#A83232",
                hover_color="#7A2222",
                command=efetuar_cancelamento,
            )
            btn_confirma_cancelar.pack(pady=10)

        ctk.CTkButton(
            self,
            text="Voltar ao Menu",
            fg_color="gray",
            hover_color="#555555",
            command=self.mostrar_menu_principal,
        ).pack(pady=20)

    # --- TELA 3: SERVIÇOS ---
    def tela_servicos(self):
        self.limpar_janela()

        ctk.CTkLabel(
            self,
            text="Serviços Disponíveis",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=20)

        servicos = [
            "Degradê - R$ 35",
            "Corte social - R$ 30",
            "Barba completa - R$ 25",
            "Pigmentação - R$ 40",
            "Hidratação capilar - R$ 50",
            "Platinado - R$ 120",
            "Combo corte + barba - R$ 50",
        ]

        # Criando uma caixinha de texto elegante para listar os preços
        textbox = ctk.CTkTextbox(self, width=320, height=220, font=("Arial", 14))
        textbox.pack(pady=10)
        
        for item in servicos:
            textbox.insert("end", f"• {item}\n\n")
        
        textbox.configure(state="disabled") # impede o usuário de digitar dentro

        ctk.CTkButton(
            self, text="Voltar ao Menu", command=self.mostrar_menu_principal
        ).pack(pady=20)

    # --- TELA 4: CONTATO ---
    def tela_contato(self):
        self.limpar_janela()

        ctk.CTkLabel(
            self, text="Contato e Localização", font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)

        texto_contato = (
            "📍 Endereço:\nJardim Macedônia\nRua Póva de Varzim - Nº67\n\n"
            "📞 Contato:\n+55 11 91539-7314"
        )

        ctk.CTkLabel(
            self,
            text=texto_contato,
            font=ctk.CTkFont(size=15),
            justify="center",
        ).pack(pady=30)

        ctk.CTkButton(
            self, text="Voltar ao Menu", command=self.mostrar_menu_principal
        ).pack(pady=10)

    # --- TELA 5: AVALIAÇÃO ---
    def tela_avaliar(self):
        self.limpar_janela()

        ctk.CTkLabel(
            self, text="Avalie Nosso Serviço", font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)

        lbl_feedback = ctk.CTkLabel(
            self, text="Sua opinião é muito importante para nós!", font=("Arial", 13)
        )
        lbl_feedback.pack(pady=10)

        def enviar_nota(nota):
            if nota in [1, 2]:
                lbl_feedback.configure(
                    text="Sentimos MUITO, vamos procurar melhorar! :(",
                    text_color="red",
                )
            elif nota == 3:
                lbl_feedback.configure(
                    text="Vamos nos esforçar mais, Obrigado! 🛠️",
                    text_color="yellow",
                )
            else:
                lbl_feedback.configure(
                    text="Muito obrigado, Volte sempre! ⭐⭐⭐",
                    text_color="green",
                )

        # Criando botões de estrelas/notas de 1 a 5 dispostos lado a lado
        frame_notas = ctk.CTkFrame(self, fg_color="transparent")
        frame_notas.pack(pady=15)

        for i in range(1, 6):
            btn_nota = ctk.CTkButton(
                frame_notas,
                text=str(i),
                width=45,
                height=45,
                font=ctk.CTkFont(size=14, weight="bold"),
                command=lambda n=i: enviar_nota(n),
            )
            btn_nota.pack(side="left", padx=5)

        ctk.CTkButton(
            self,
            text="Voltar ao Menu",
            fg_color="gray",
            hover_color="#555555",
            command=self.mostrar_menu_principal,
        ).pack(pady=30)


# Executa o aplicativo
if __name__ == "__main__":
    app = AppBarbearia()
    app.mainloop()
    
