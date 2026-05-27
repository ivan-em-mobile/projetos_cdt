import customtkinter as ctk
import random
import time

# Configuração inicial do CustomTkinter
ctk.set_appearance_mode("System")  # Opções: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Opções: "blue", "green", "dark-blue"


class AppBarbearia(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Configurações da Janela Principal
        self.title("Barbearia Andrades - Sistema Integrado")
        self.geometry("500x650")  # Aumentei um pouquinho a altura para acomodar o menu novo
        self.resizable(False, False)

        # Lista global de serviços
        self.lista_servicos = [
            "Degradê - R$ 35",
            "Corte social - R$ 30",
            "Barba completa - R$ 25",
            "Pigmentação - R$ 40",
            "Hidratação capilar - R$ 50",
            "Platinado - R$ 120",
            "Combo corte + barba - R$ 50",
        ]

        # Banco de dados temporário (em memória)
        self.nome_salvo = ""
        self.data_salva = ""
        self.horario_salvo = ""
        self.servico_salvo = ""

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
        label_titulo.pack(pady=(25, 5))

        label_subtitulo = ctk.CTkLabel(
            self,
            text="Seja Bem-Vindo! Escolha uma opção:",
            font=ctk.CTkFont(size=14),
        )
        label_subtitulo.pack(pady=(0, 20))

        # --- BOTÕES DO MENU ATUALIZADOS ---
        
        btn_servicos = ctk.CTkButton(
            self, text="1 - Serviços Disponíveis", width=250, height=40, command=self.tela_servicos
        )
        btn_servicos.pack(pady=8)

        btn_agendar = ctk.CTkButton(
            self, text="2 - Agendar Horário", width=250, height=40, command=self.tela_agendar
        )
        btn_agendar.pack(pady=8)

        btn_cancelar = ctk.CTkButton(
            self, text="3 - Cancelar Agendamento", width=250, height=40, command=self.tela_cancelar
        )
        btn_cancelar.pack(pady=8)

        # NOVA OPÇÃO: Chat de Suporte com IA
        btn_suporte = ctk.CTkButton(
            self, 
            text="4 - Chat de Suporte (IA)", 
            width=250, 
            height=40, 
            fg_color="#1F6AA5",
            command=self.tela_suporte_ia
        )
        btn_suporte.pack(pady=8)

        btn_contato = ctk.CTkButton(
            self, text="5 - Localização e Contato", width=250, height=40, command=self.tela_contato
        )
        btn_contato.pack(pady=8)

        btn_avaliar = ctk.CTkButton(
            self, text="6 - Avalie Nosso Serviço", width=250, height=40, command=self.tela_avaliar
        )
        btn_avaliar.pack(pady=8)

        btn_sair = ctk.CTkButton(
            self,
            text="0 - Sair",
            width=250,
            height=40,
            fg_color="#A83232",
            hover_color="#7A2222",
            command=self.destroy,
        )
        btn_sair.pack(pady=(25, 10))

    # --- TELA 1: SERVIÇOS ---
    def tela_servicos(self):
        self.limpar_janela()
        ctk.CTkLabel(self, text="Serviços Disponíveis", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        textbox = ctk.CTkTextbox(self, width=320, height=220, font=("Arial", 14))
        textbox.pack(pady=10)
        for item in self.lista_servicos:
            textbox.insert("end", f"• {item}\n\n")
        textbox.configure(state="disabled")
        ctk.CTkButton(self, text="Ir para Agendamento", fg_color="#1F6AA5", command=self.tela_agendar).pack(pady=10)
        ctk.CTkButton(self, text="Voltar ao Menu", fg_color="gray", hover_color="#555555", command=self.mostrar_menu_principal).pack(pady=5)

    # --- TELA 2: AGENDAR ---
    def tela_agendar(self):
        self.limpar_janela()
        ctk.CTkLabel(self, text="Agendamento de Horário", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=15)
        
        ctk.CTkLabel(self, text="Seu Nome:").pack(anchor="w", padx=120)
        entry_nome = ctk.CTkEntry(self, width=260, placeholder_text="Digite seu nome")
        entry_nome.pack(pady=(0, 10))

        ctk.CTkLabel(self, text="Escolha o Serviço:").pack(anchor="w", padx=120)
        menu_servico = ctk.CTkOptionMenu(self, width=260, values=self.lista_servicos)
        menu_servico.set("Selecione um corte...")
        menu_servico.pack(pady=(0, 10))

        ctk.CTkLabel(self, text="Data (EX: 09/10/2026):").pack(anchor="w", padx=120)
        entry_data = ctk.CTkEntry(self, width=260, placeholder_text="09/10/2026")
        entry_data.pack(pady=(0, 10))

        ctk.CTkLabel(self, text="Horário (EX: 17:30):").pack(anchor="w", padx=120)
        entry_horario = ctk.CTkEntry(self, width=260, placeholder_text="17:30")
        entry_horario.pack(pady=(0, 15))

        lbl_status = ctk.CTkLabel(self, text="", text_color="green", font=("Arial", 12))
        lbl_status.pack(pady=5)

        def salvar_agendamento():
            if not entry_nome.get() or not entry_data.get() or not entry_horario.get() or menu_servico.get() == "Selecione um corte...":
                lbl_status.configure(text="Por favor, preencha todos os campos e selecione o corte!", text_color="red")
                return
            self.nome_salvo = entry_nome.get()
            self.data_salva = entry_data.get()
            self.horario_salvo = entry_horario.get()
            self.servico_salvo = menu_servico.get() 
            lbl_status.configure(
                text=f"Agendamento realizado com sucesso, {self.nome_salvo}!\nServiço: {self.servico_salvo}\nData: {self.data_salva} às {self.horario_salvo}\nObrigado pela preferência! >.<",
                text_color="#22C55E",
            )

        btn_salvar = ctk.CTkButton(self, text="Confirmar Agendamento", command=salvar_agendamento)
        btn_salvar.pack(pady=10)
        ctk.CTkButton(self, text="Voltar ao Menu", fg_color="gray", hover_color="#555555", command=self.mostrar_menu_principal).pack(pady=10)

    # --- TELA 3: CANCELAR ---
    def tela_cancelar(self):
        self.limpar_janela()
        ctk.CTkLabel(self, text="Cancelar Agendamento", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        if self.nome_salvo == "":
            ctk.CTkLabel(self, text="Você ainda não possui um agendamento ativo.\n\nPor favor, volte e agende um horário.", text_color="yellow").pack(pady=30)
        else:
            ctk.CTkLabel(self, text=f"Agendamento Atual:\n{self.servico_salvo}\nDia {self.data_salva} às {self.horario_salvo}", font=("Arial", 13, "italic"), text_color="#AAAAAA").pack(pady=10)
            ctk.CTkLabel(self, text="Para cancelar, confirme seu nome:").pack(pady=5)
            entry_cancela_nome = ctk.CTkEntry(self, width=260)
            entry_cancela_nome.pack(pady=10)
            lbl_status_cancelar = ctk.CTkLabel(self, text="")
            lbl_status_cancelar.pack(pady=5)

            def efetuar_cancelamento():
                if entry_cancela_nome.get() == self.nome_salvo:
                    lbl_status_cancelar.configure(text=f"Agendamento de {self.nome_salvo} ({self.servico_salvo}) foi CANCELADO!", text_color="red")
                    self.nome_salvo = self.data_salva = self.horario_salvo = self.servico_salvo = ""
                else:
                    lbl_status_cancelar.configure(text="Nome diferente do agendado! Tente novamente.", text_color="red")

            btn_confirma_cancelar = ctk.CTkButton(self, text="Confirmar Cancelamento", fg_color="#A83232", hover_color="#7A2222", command=efetuar_cancelamento)
            btn_confirma_cancelar.pack(pady=10)
        ctk.CTkButton(self, text="Voltar ao Menu", fg_color="gray", hover_color="#555555", command=self.mostrar_menu_principal).pack(pady=20)

    # --- NOVA TELA 4: CHAT DE SUPORTE COM IA ---
    def tela_suporte_ia(self):
        self.limpar_janela()

        ctk.CTkLabel(
            self, text="Suporte Inteligente - Barbearia Andrades", font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=10)

        # Área de exibição das mensagens (Chat)
        txt_chat = ctk.CTkTextbox(self, width=420, height=340, font=("Arial", 13))
        txt_chat.pack(pady=10)
        
        # Mensagem inicial da IA
        txt_chat.insert("end", "IA: Olá! Sou o assistente virtual da Barbearia Andrades. 🤖\nComo posso te ajudar hoje? Você pode me perguntar sobre preços, horários, endereço ou funcionamento!\n\n")
        txt_chat.configure(state="disabled")

        # Container para o campo de texto de envio e o botão
        frame_envio = ctk.CTkFrame(self, fg_color="transparent")
        frame_envio.pack(pady=5, fill="x", padx=40)

        entry_msg = ctk.CTkEntry(frame_envio, placeholder_text="Digite sua dúvida aqui...", width=300)
        entry_msg.pack(side="left", padx=(0, 10))

        def processar_resposta_ia(pergunta):
            pergunta = pergunta.lower()
            
            # Base de conhecimento da IA
            def processar_resposta_ia(pergunta):
                pergunta = pergunta.lower() 
            
            # 1. Filtro de Saudação (opcional, para ser educada antes de checar o tema)
            if any(saudacao in pergunta for saudacao in ["olá", "ola", "bom dia", "boa tarde", "boa noite", "tudo bem"]):
                return "IA: Olá! Tudo bem? Como posso te ajudar com os serviços da Barbearia Andrades hoje?"
            
            # 2. Verificação de palavras-chave relacionadas à barbearia
            if "preco" in pergunta or "preço" in pergunta or "valor" in pergunta or "custa" in pergunta or "serviço" in pergunta or "tabela" in pergunta:
                return "IA: Nós oferecemos vários serviços! Os principais são: Degradê (R$35), Corte Social (R$30), Barba (R$25) e o nosso Combo Corte + Barba por apenas R$50. Você pode conferir todos na aba 'Serviços Disponíveis' do menu!"
            
            elif "endereco" in pergunta or "endereço" in pergunta or "onde fica" in pergunta or "localiza" in pergunta or "rua" in pergunta or "bairro" in pergunta:
                return "IA: Estamos localizados no Jardim Macedônia, na Rua Póva de Varzim, Nº67. Venha nos visitar!"
            
            elif "horario" in pergunta or "horário" in pergunta or "funciona" in pergunta or "aberto" in pergunta or "fecha" in pergunta:
                return "IA: Nosso horário de atendimento padrão é de Terça a Sábado, das 09:00 às 20:00. O horário específico do seu agendamento você escolhe na tela de marcação!"
            
            elif "contato" in pergunta or "whatsapp" in pergunta or "telefone" in pergunta or "celular" in pergunta:
                return "IA: Você pode falar com a gente diretamente pelo WhatsApp no número: +55 11 91539-7314."
            
            elif "cancelar" in pergunta or "desmarcar" in pergunta or "mudar" in pergunta:
                return "IA: Para cancelar um horário, basta ir na opção '3 - Cancelar Agendamento' no menu principal e confirmar o nome cadastrado."
            
            elif "obrigado" in pergunta or "valeu" in pergunta or "obrigada" in pergunta:
                return "IA: De nada! Estou aqui para ajudar. Se precisar de algo sobre nossos serviços, é só chamar! ✂️💈"
            
            # 3. SE NÃO FOR SOBRE A BARBEARIA: Bloqueio imediato
            else:
                return "IA: Desculpe, não posso responder ou te ajudar com isso. Sou um assistente exclusivo para dúvidas sobre a Barbearia Andrades."
            if "preco" in pergunta or "preço" in pergunta or "valor" in pergunta or "custa" in pergunta or "serviço" in pergunta:
                return "IA: Nós oferecemos vários serviços! Os principais são: Degradê (R$35), Corte Social (R$30), Barba (R$25) e o nosso Combo Corte + Barba por apenas R$50. Você pode conferir todos na aba 'Serviços Disponíveis' do menu!"
            elif "endereco" in pergunta or "endereço" in pergunta or "onde fica" in pergunta or "localiza" in pergunta or "rua" in pergunta:
                return "IA: Estamos localizados no Jardim Macedônia, na Rua Póva de Varzim, Nº67. Venha nos visitar!"
            elif "horario" in pergunta or "horário" in pergunta or "funciona" in pergunta or "aberto" in pergunta:
                return "IA: Nosso horário de atendimento padrão é de Terça a Sábado, das 09:00 às 20:00. O horário específico do seu agendamento você escolhe na tela de marcação!"
            elif "contato" in pergunta or "whatsapp" in pergunta or "telefone" in pergunta or "celular" in pergunta:
                return "IA: Você pode falar com a gente diretamente pelo WhatsApp no número: +55 11 91539-7314."
            elif "cancelar" in pergunta or "desmarcar" in pergunta:
                return "IA: Para cancelar um horário, basta ir na opção '3 - Cancelar Agendamento' no menu principal e confirmar o nome cadastrado."
            elif "obrigado" in pergunta or "valeu" in pergunta or "obrigada" in pergunta:
                return "IA: De nada! Estou aqui para ajudar. Se precisar de mais alguma coisa, é só chamar! ✂️💈"
            elif "bom dia" in pergunta or "boa tarde" in pergunta or "boa noite" in pergunta or "ola" in pergunta or "olá" in pergunta:
                return "IA: Olá! Tudo bem? Como posso te ajudar com os serviços da Barbearia Andrades hoje?"
            else:
                respostas_padrao = [
                    "IA: Entendi! Para essa dúvida específica, recomendo dar uma olhada nas opções do nosso menu ou falar com um de nossos barbeiros no WhatsApp: +55 11 91539-7314. Posso te ajudar com mais alguma informação sobre os cortes?",
                    "IA: Boa pergunta! Como sou um assistente virtual focado na barbearia, não tenho certeza sobre isso. Mas você pode checar nossa tabela de preços ou marcar um horário no menu anterior!",
                    "IA: Desculpe, não consegui entender perfeitamente. Você gostaria de saber sobre nossos preços, localização, ou como agendar um corte?"
                ]
                return random.choice(respostas_padrao)

            # Nota: Se você quiser IA real com o Ollama instalado no PC rodando o modelo Llama3, bastaria fazer:
            # import ollama
            # response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': pergunta}])
            # return "IA: " + response['message']['content']

        def enviar_mensagem():
            msg_usuario = entry_msg.get().strip()
            if not msg_usuario:
                return

            # Ativa o campo para adicionar a mensagem do usuário
            txt_chat.configure(state="normal")
            txt_chat.insert("end", f"Você: {msg_usuario}\n\n")
            entry_msg.delete(0, "end")
            
            # Gera e insere a resposta da IA
            resposta = processar_resposta_ia(msg_usuario)
            txt_chat.insert("end", f"{resposta}\n\n")
            
            # Desativa novamente e rola para o fim do chat
            txt_chat.configure(state="disabled")
            txt_chat.see("end")

        btn_enviar = ctk.CTkButton(frame_envio, text="Enviar", width=80, command=enviar_mensagem)
        btn_enviar.pack(side="right")

        # Permite enviar apertando a tecla 'Enter'
        self.bind("<Return>", lambda event: enviar_mensagem())

        ctk.CTkButton(
            self, text="Voltar ao Menu", fg_color="gray", hover_color="#555555", command=self.mostrar_menu_principal
        ).pack(pady=15)

    # --- TELA 5: CONTATO ---
    def tela_contato(self):
        self.limpar_janela()
        ctk.CTkLabel(self, text="Contato e Localização", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        texto_contato = "📍 Endereço:\nJardim Macedônia\nRua Póva de Varzim - Nº67\n\n📞 Contato:\n+55 11 91539-7314"
        ctk.CTkLabel(self, text=texto_contato, font=ctk.CTkFont(size=15), justify="center").pack(pady=30)
        ctk.CTkButton(self, text="Voltar ao Menu", fg_color="gray", hover_color="#555555", command=self.mostrar_menu_principal).pack(pady=10)

    # --- TELA 6: AVALIAÇÃO ---
    def tela_avaliar(self):
        self.limpar_janela()
        ctk.CTkLabel(self, text="Avalie Nosso Serviço", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        lbl_feedback = ctk.CTkLabel(self, text="Sua opinião é muito importante para nós!", font=("Arial", 13))
        lbl_feedback.pack(pady=10)

        def enviar_nota(nota):
            if nota in [1, 2]:
                lbl_feedback.configure(text="Sentimos MUITO, vamos procurar melhorar! :(", text_color="red")
            elif nota == 3:
                lbl_feedback.configure(text="Vamos nos esforçar mais, Obrigado! 🛠️", text_color="yellow")
            else:
                lbl_feedback.configure(text="Muito obrigado, Volte sempre! ⭐⭐⭐", text_color="green")

        frame_notas = ctk.CTkFrame(self, fg_color="transparent")
        frame_notas.pack(pady=15)
        for i in range(1, 6):
            btn_nota = ctk.CTkButton(frame_notas, text=str(i), width=45, height=45, font=ctk.CTkFont(size=14, weight="bold"), command=lambda n=i: enviar_nota(n))
            btn_nota.pack(side="left", padx=5)

        ctk.CTkButton(self, text="Voltar ao Menu", fg_color="gray", hover_color="#555555", command=self.mostrar_menu_principal).pack(pady=30)


# Executa o aplicativo
if __name__ == "__main__":
    app = AppBarbearia()
    app.mainloop()
