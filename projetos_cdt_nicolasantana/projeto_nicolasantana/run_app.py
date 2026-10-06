import os
import sys
import time
import threading
import webbrowser
import streamlit.web.cli as stcli

def resolve_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def open_browser():
    # Aguarda 4 segundos para garantir a inicialização do servidor em máquinas mais lentas
    time.sleep(4)
    webbrowser.open_new_tab("http://127.0.0.1:8501")

if __name__ == "__main__":
    script_path = resolve_path("app_web.py")
    
    # Inicia a abertura do navegador em uma thread separada
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Configurações explícitas de servidor, porta e headless
    sys.argv = [
        "streamlit",
        "run",
        script_path,
        "--server.headless=true",
        "--server.port=8501",
        "--server.address=127.0.0.1",
        "--global.developmentMode=false"
    ]
    
    sys.exit(stcli.main())