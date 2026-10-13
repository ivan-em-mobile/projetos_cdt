"""
Baixa fotos de um grupo do WhatsApp Web (WhatsApp Business) e as organiza
em uma pasta na área de trabalho.

Requisitos:
    pip install selenium webdriver-manager

ANTES DE RODAR:
1. Feche TODAS as janelas do Chrome (o script usa o seu perfil salvo).
2. Ajuste CHROME_PROFILE_PATH (veja em chrome://version, linha "Caminho do perfil").
3. Ajuste GROUP_NAME para o nome exato do grupo no WhatsApp.
"""

import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ======== CONFIGURAÇÕES ========
# O "Caminho do perfil" do Chrome normalmente termina em "Profile 2".
# Aqui usamos a pasta "User Data" e informamos o perfil separadamente.
CHROME_PROFILE_PATH = r"C:\Users\ivsilva\AppData\Local\Google\Chrome\User Data\Profile 2"  # Ajuste para o seu caminho
CHROME_PROFILE_DIRECTORY = "Profile 2"  # ou "Default", "Profile 1"...

# Nome exato do grupo onde as fotos foram enviadas
GROUP_NAME = "YOU_LIKE_4EVER!"

# Quantas fotos mais recentes baixar
QUANTIDADE = 90

# Pasta de destino. Se sua área de trabalho estiver no OneDrive, use:
# Path.home() / "OneDrive" / "Desktop"
DESKTOP_PATH = Path.home() / "Desktop"
DEST_FOLDER = DESKTOP_PATH / "Fotos Setembro 2026"

DOWNLOADS_PATH = Path.home() / "Downloads"
EXTENSOES = (".jpg", ".jpeg", ".png", ".webp")
# =================================


def iniciar_driver():
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={CHROME_PROFILE_PATH}")
    options.add_argument(f"profile-directory={CHROME_PROFILE_DIRECTORY}")
    options.add_argument("--start-maximized")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://web.whatsapp.com")
    return driver


def aguardar_login(driver, timeout=120):
    print("Aguardando o WhatsApp Web carregar (escaneie o QR Code se pedir)...")
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, '//div[@id="pane-side"]'))
    )
    print("WhatsApp Web carregado.")


def abrir_grupo(driver, nome_grupo, timeout=30):
    campo_busca = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(
            (By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        )
    )
    campo_busca.click()
    campo_busca.clear()
    campo_busca.send_keys(nome_grupo)
    time.sleep(2)

    resultado = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(
            (By.XPATH, f'//span[@title="{nome_grupo}"]')
        )
    )
    resultado.click()
    time.sleep(2)


def baixar_fotos(driver, quantidade):
    xpath_imgs = (
        '//div[contains(@class,"message-in") or contains(@class,"message-out")]'
        '//img[contains(@src,"blob:")]'
    )
    imagens = driver.find_elements(By.XPATH, xpath_imgs)[-quantidade:]
    print(f"Encontradas {len(imagens)} imagens na conversa.")

    for i, img in enumerate(imagens, start=1):
        try:
            img.click()
            time.sleep(1.5)

            botao = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//div[@aria-label="Baixar"] | //span[@data-icon="download"]')
                )
            )
            botao.click()
            time.sleep(1.5)

            driver.find_element(By.XPATH, '//div[@aria-label="Fechar"]').click()
            time.sleep(1)
            print(f"Imagem {i} baixada.")
        except Exception as e:
            print(f"Erro na imagem {i}: {e}")


def listar_imagens_downloads():
    return {
        p for p in DOWNLOADS_PATH.iterdir()
        if p.is_file() and p.suffix.lower() in EXTENSOES
    }


def mover_novos_arquivos(antes):
    """Move só o que apareceu em Downloads durante esta execução."""
    DEST_FOLDER.mkdir(parents=True, exist_ok=True)
    novos = listar_imagens_downloads() - antes

    for arquivo in novos:
        destino = DEST_FOLDER / arquivo.name
        arquivo.rename(destino)

    print(f"{len(novos)} arquivos movidos para {DEST_FOLDER}")


def main():
    antes = listar_imagens_downloads()
    driver = iniciar_driver()
    try:
        aguardar_login(driver)
        abrir_grupo(driver, GROUP_NAME)
        baixar_fotos(driver, QUANTIDADE)
        time.sleep(3)
        mover_novos_arquivos(antes)
    finally:
        input("Pressione Enter para fechar o navegador...")
        driver.quit()


if __name__ == "__main__":
    main()