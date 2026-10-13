"""
Baixador de fotos do WhatsApp Web com Interface Gráfica (Tkinter).

Requisitos:
    pip install selenium webdriver-manager
    (Tkinter já vem embutido no Python)
"""

import base64
import threading
import time
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ======== CONFIGURAÇÕES ========
PERFIL_SELENIUM = Path.home() / "whatsapp_selenium_profile"
PHONE_NUMBER = "+5511947541829"
QUANTIDADE = 60
DESKTOP_PATH = Path.home() / "Desktop"
DEST_FOLDER = DESKTOP_PATH / "Fotoss WhatsApp Galeria"

JS_BLOB = """
const src = arguments[0];
const done = arguments[arguments.length - 1];
fetch(src)
  .then(r => r.blob())
  .then(b => {
    const fr = new FileReader();
    fr.onloadend = () => done(fr.result);
    fr.readAsDataURL(b);
  })
  .catch(() => done(null));
"""

def iniciar_driver():
    DEST_FOLDER.mkdir(parents=True, exist_ok=True)
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={PERFIL_SELENIUM}")
    options.add_argument("--start-maximized")
    options.add_experimental_option("prefs", {
        "download.default_directory": str(DEST_FOLDER),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "profile.default_content_setting_values.automatic_downloads": 1,
    })

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_script_timeout(30)
    driver.get("https://web.whatsapp.com")
    return driver

def aguardar_login(driver, timeout=180):
    print("Aguardando o WhatsApp Web carregar...")
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, '//div[@id="pane-side"]'))
    )
    time.sleep(4)
    print("WhatsApp Web carregado com sucesso.")

def abrir_conversa_por_telefone(driver, numero, timeout=30):
    url = f"https://web.whatsapp.com/send?phone={numero.strip()}"
    print(f"Abrindo a conversa com o número {numero}...")
    driver.get(url)
    
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, '//div[@id="main"]'))
    )
    time.sleep(4)
    print("Conversa aberta.")

def abrir_painel_midias(driver):
    print("Abrindo o painel de mídias da conversa...")
    try:
        cabecalho = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@id="main"]//header'))
        )
        cabecalho.click()
        time.sleep(2)

        opcao_midia = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "Mídias") or contains(text(), "Media")]'))
        )
        opcao_midia.click()
        time.sleep(3)
        print("Painel de mídias aberto.")
    except Exception as e:
        print(f"Aviso ao abrir mídias automaticamente: {e}")

def salvar_via_blob(driver, src, caminho_destino):
    try:
        dados = driver.execute_async_script(JS_BLOB, src)
        if not dados or "," not in dados:
            return False
        _, b64 = dados.split(",", 1)
        caminho_destino.write_bytes(base64.b64decode(b64))
        return True
    except Exception:
        return False

def executar_automacao(status_label, botao_iniciar):
    """Função principal que executa o Selenium em segundo plano."""
    driver = None
    try:
        status_label.config(text="Status: Iniciando o navegador...", fg="blue")
        driver = iniciar_driver()
        
        status_label.config(text="Status: Aguardando login / WhatsApp...", fg="blue")
        aguardar_login(driver)
        
        status_label.config(text="Status: Abrindo a conversa...", fg="blue")
        abrir_conversa_por_telefone(driver, PHONE_NUMBER)
        
        status_label.config(text="Status: Acessando painel de mídias...", fg="blue")
        abrir_painel_midias(driver)
        
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        baixadas = 0

        status_label.config(text="Status: Localizando primeira foto...", fg="blue")
        time.sleep(2)

        miniatura_imgs = driver.find_elements(By.XPATH, '//div[@data-testid="media-gallery"]//img | //section//img[starts-with(@src, "blob:")] | //div[contains(@class, "row-container")]//img')
        if not miniatura_imgs:
            miniatura_imgs = driver.find_elements(By.XPATH, '//div[@id="app"]//img[contains(@src, "blob:")]')

        if not miniatura_imgs:
            raise RuntimeError("Nenhuma miniatura de foto encontrada na aba de mídias.")

        primeira_foto = miniatura_imgs[0]
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", primeira_foto)
        time.sleep(1)
        primeira_foto.click()
        time.sleep(2.5)

        anterior = None
        for i in range(1, QUANTIDADE + 1):
            status_label.config(text=f"Status: Baixando foto {i}...", fg="orange")
            img_grande = None
            for _ in range(10):
                imgs_vis = driver.find_elements(By.XPATH, '//div[@data-testid="media-viewer"]//img[starts-with(@src, "blob:")] | //div[@id="app"]//img[starts-with(@src, "blob:") and not(ancestor::div[@id="side"])]')
                if imgs_vis:
                    img_grande = max(imgs_vis, key=lambda el: el.size.get("width", 0))
                    if img_grande and img_grande.size.get("width", 0) > 300:
                        break
                time.sleep(0.5)

            if not img_grande:
                break

            src = img_grande.get_attribute("src")
            if not src or src == anterior:
                break

            caminho = DEST_FOLDER / f"foto_{timestamp_str}_{i:03d}.jpg"
            if salvar_via_blob(driver, src, caminho):
                baixadas += 1

            anterior = src
            ActionChains(driver).send_keys(Keys.ARROW_LEFT).perform()
            time.sleep(2)

        try:
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        except:
            pass

        status_label.config(text="Status: Concluído com sucesso!", fg="green")
        messagebox.showinfo("Sucesso", f"Processo concluído!\nTotal de {baixadas} fotos salvas em:\n{DEST_FOLDER}")

    except Exception as e:
        status_label.config(text="Status: Erro na execução.", fg="red")
        # CORREÇÃO APLICADA AQUI: f"..." em vez de fOcorreu...
        messagebox.showerror("Erro", f"Ocorreu um erro durante a execução:\n{e}")
    
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
        botao_iniciar.config(state=tk.NORMAL)

def iniciar_thread(status_label, botao_iniciar):
    botao_iniciar.config(state=tk.DISABLED)
    t = threading.Thread(target=executar_automacao, args=(status_label, botao_iniciar))
    t.daemon = True
    t.start()

def montar_interface():
    janela = tk.Tk()
    janela.title("Baixador de Fotos do WhatsApp")
    janela.geometry("400x250")
    janela.resizable(False, False)

    titulo = tk.Label(janela, text="Baixador de Fotos - WhatsApp Web", font=("Arial", 12, "bold"))
    titulo.pack(pady=15)

    info_lbl = tk.Label(janela, text=f"Contato: {PHONE_NUMBER}\nDestino: Área de Trabalho/Fotos WhatsApp Galeria", font=("Arial", 9), justify=tk.CENTER)
    info_lbl.pack(pady=5)

    botao_iniciar = tk.Button(janela, text="Iniciar Download das Fotos", font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5)
    botao_iniciar.pack(pady=15)

    status_label = tk.Label(janela, text="Status: Aguardando comando...", font=("Arial", 9), fg="gray")
    status_label.pack(pady=5)

    botao_iniciar.config(command=lambda: iniciar_thread(status_label, botao_iniciar))

    janela.mainloop()

if __name__ == "__main__":
    montar_interface()