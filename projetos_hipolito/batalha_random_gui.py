import customtkinter as ctk

class BatalhaRandomPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        label = ctk.CTkLabel(self, text="PÁGINA DE BATALHA ALEATÓRIA", font=("Arial", 30))
        label.pack(pady=50, padx=50, expand=True)

        btn_back = ctk.CTkButton(self, text="<< Voltar ao Menu", 
                                 command=lambda: controller.show_frame("MainPage"))
        btn_back.pack(pady=20, padx=20, anchor="nw")