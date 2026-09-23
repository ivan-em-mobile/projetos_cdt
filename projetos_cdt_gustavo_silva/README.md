# 🛡️ OmniOverlay

**OmniOverlay** OmniOverlay é uma aplicação desktop moderna desenvolvida em Python com CustomTkinter, projetada para funcionar como um painel flutuante (overlay) completo. Ela oferece gerenciamento de perfis, atalhos customizados inteligentes, monitoramento de hardware em tempo real, assistente de IA integrada, player de vídeo e personalização visual avançada.

---

## 🏗️ Arquitetura do Sistema

### Fluxo de Componentes e Módulos


```text
+-------------------------------------------------------------------+
|                           OmniOverlayApp                          |
|  (Controlador Principal / Gerenciador de Janela e Configurações)  |
+---------------------------------+---------------------------------+
                                  |
         +------------------------+------------------------+
         |                                                 |
         v                                                 v
+-----------------------+                       +-----------------------+
|  ProfileSelectorFrame |                       |    DashboardFrame     |
| (Gerenciador Perfis)  |                       |  (Painel Principal)   |
+-----------------------+                       +-----------+-----------+
                                                            |
        +------------------+------------------+-------------+------------+
        |                  |                  |                          |
        v                  v                  v                          v
+---------------+  +---------------+  +---------------+  +-------------------+
|  Central de   |  |    OmniAI     |  |   Player de   |  |   Configurações   |
| Atalhos (Hub) |  |  (Assistente) |  |     Vídeo     |  | & Root Master ADM |
+---------------+  +---------------+  +---------------+  +-------------------+
```


### Estrutura de Camadas e Serviços Suporte

* **Persistência de Dados**: 
  * `config_perfis.json`: Armazena dados de aparência, atalhos do usuário e configurações de perfil.
  * `omnioverlay_data.db` (SQLite): Gerencia as credenciais administrativas e acesso do Root Master.
* **Serviços em Segundo Plano**:
  * `GlobalHotkeyManager` (`pynput`): Captura eventos globais do teclado (ex: tecla `F12` para alternar visibilidade).
  * `Thread de Hardware` (`psutil`): Monitora o consumo de CPU e RAM em tempo real sem travar a interface gráfica.

---

## 📦 Dependências do Projeto

| Biblioteca | Finalidade |
| :--- | :--- |
| `customtkinter` | Interface gráfica moderna e responsiva |
| `Pillow` (PIL) | Manipulação e renderização de avatares e ícones |
| `psutil` | Monitoramento de recursos do sistema (CPU/RAM) |
| `pynput` | Captura de atalhos de teclado globais |
| `tkVideoPlayer` | Execução de arquivos de vídeo locais em Tkinter |

---

## ⚡ Guia de Instalação e Execução

1. **Instale as dependências:**
   ```bash
   pip install customtkinter Pillow psutil pynput tkVideoPlayer

   Execute o aplicativo:

Bash
python main.py

1. Persistência de Dados & Banco SQLite
Python
# Inicialização do banco SQLite para credenciais administrativas
def inicializar_banco_sql():
    conn = sqlite3.connect("omnioverlay_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios_adm (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM usuarios_adm")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO usuarios_adm (usuario, senha) VALUES (?, ?)", ("admin", "1234"))
    conn.commit()
    conn.close()

# Gerenciador do arquivo JSON de perfis
class AccountManager:
    @staticmethod
    def carregar_dados():
        if os.path.exists("config_perfis.json"):
            with open("config_perfis.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return {"modo_tema": "dark", "ultimo_perfil": "p1", "perfis": []}

    @staticmethod
    def salvar_dados(dados):
        with open("config_perfis.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
2. Monitoramento de Hardware e Atalhos Globais
Python
# Thread paralela para atualizar a barra de status de hardware
def loop_monitoramento_hardware(self):
    while True:
        try:
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent
            if hasattr(self, "lbl_hw_info"):
                self.lbl_hw_info.configure(text=f"CPU: {cpu}% | RAM: {ram}%")
        except Exception:
            pass
        time.sleep(1)

# Gerenciador de teclas de atalho globais
class GlobalHotkeyManager:
    def __init__(self, app_controller):
        self.app = app_controller

    def iniciar(self):
        def on_press(key):
            if key == keyboard.Key.f12:
                self.app.alternar_visibilidade_overlay()

        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()
3. Abertura Inteligente de Atalhos
Python
# Função para abrir URLs web ou executáveis locais (.exe, .bat)
def abrir_inteligente(self, alvo):
    try:
        if alvo.startswith("http://") or alvo.startswith("https://"):
            webbrowser.open(alvo)
        elif os.path.exists(alvo):
            os.startfile(alvo)
        else:
            subprocess.Popen(alvo, shell=True)
    except Exception as e:
        print(f"[ERRO] Falha ao abrir: {e}")
4. Controlador Principal do App
Python
class OmniOverlayApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        inicializar_banco_sql()
        
        self.title("OmniOverlay")
        self.geometry("920x800")
        self.overrideredirect(True) # Janela sem bordas padrões
        self.attributes("-alpha", 0.98)

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.profile_frame = ProfileSelectorFrame(self.container, self)
        self.dashboard_frame = DashboardFrame(self.container, self)

        self.hotkey_manager = GlobalHotkeyManager(self)
        self.hotkey_manager.iniciar()

        self.verificar_perfil_inicial()

    def alternar_visibilidade_overlay(self):
        if self.state() == "withdrawn":
            self.deiconify()
            self.focus_force()
        else:
            self.withdraw()

if __name__ == "__main__":
    app = OmniOverlayApp()
    app.mainloop()