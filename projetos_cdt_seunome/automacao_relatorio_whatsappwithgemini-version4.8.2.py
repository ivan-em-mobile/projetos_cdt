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

import base64
import time
from datetime import datetime
from pathlib import Path

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

# Seu número de telefone configurado
PHONE_NUMBER = "+5511947541829"

# Quantidade máxima de fotos que deseja baixar
QUANTIDADE = 60

DESKTOP_PATH = Path.home() / "Desktop"
DEST_FOLDER = DESKTOP_PATH / "Fotos WhatsApp Galeria"

# Script JavaScript para ler a imagem blob da página e converter em base64
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
    """Configura e inicia o navegador Chrome com o perfil salvo."""
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
    """Aguarda o carregamento do WhatsApp Web."""
    print("Aguardando o WhatsApp Web carregar...")
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, '//div[@id="pane-side"]'))
    )
    time.sleep(4)
    print("WhatsApp Web carregado com sucesso.")

def abrir_conversa_por_telefone(driver, numero, timeout=30):
    """Abre diretamente a conversa utilizando o link oficial do WhatsApp."""
    url = f"https://web.whatsapp.com/send?phone={numero.strip()}"
    print(f"Abrindo a conversa com o número {numero}...")
    driver.get(url)
    
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, '//div[@id="main"]'))
    )
    time.sleep(4)
    print("Conversa aberta.")

def abrir_painel_midias(driver):
    """Clica no cabeçalho do chat e abre a aba de Mídias."""
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
        input("Por favor, abra manualmente a aba 'Mídias' no WhatsApp Web e pressione Enter aqui...")

def salvar_via_blob(driver, src, caminho_destino):
    """Extrai os dados da imagem diretamente da memória do navegador e salva no computador."""
    try:
        dados = driver.execute_async_script(JS_BLOB, src)
        if not dados or "," not in dados:
            return False
        _, b64 = dados.split(",", 1)
        caminho_destino.write_bytes(base64.b64decode(b64))
        return True
    except Exception:
        return False

def baixar_fotos_da_galeria(driver, quantidade_maxima):
    """Clica na primeira foto da galeria e navega pelas setas para baixar todas."""
    abrir_painel_midias(driver)
    
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    baixadas = 0

    print("Procurando a primeira foto na galeria...")
    time.sleep(2)

    try:
        # Busca pelas miniaturas na grade lateral de mídias
        miniatura_imgs = driver.find_elements(By.XPATH, '//div[@data-testid="media-gallery"]//img | //section//img[starts-with(@src, "blob:")] | //div[contains(@class, "row-container")]//img')
        
        if not miniatura_imgs:
            miniatura_imgs = driver.find_elements(By.XPATH, '//div[@id="app"]//img[contains(@src, "blob:")]')

        if not miniatura_imgs:
            raise RuntimeError("Nenhuma miniatura de foto encontrada na aba de mídias.")

        # Clica na primeira miniatura (a mais recente)
        primeira_foto = miniatura_imgs[0]
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", primeira_foto)
        time.sleep(1)
        primeira_foto.click()
        time.sleep(2.5) # Aguarda a animação do visualizador abrir
        print("Visualizador aberto na primeira foto.")

    except Exception as e:
        raise RuntimeError(f"Não foi possível abrir a primeira foto: {e}")

    anterior = None

    for i in range(1, quantidade_maxima + 1):
        try:
            # Procura de forma segura pela imagem aberta em tela cheia no visualizador
            img_grande = None
            for _ in range(10):
                imgs_vis = driver.find_elements(By.XPATH, '//div[@data-testid="media-viewer"]//img[starts-with(@src, "blob:")] | //div[@id="app"]//img[starts-with(@src, "blob:") and not(ancestor::div[@id="side"])]')
                if imgs_vis:
                    # Pega a maior imagem visível (que é a do visualizador)
                    img_grande = max(imgs_vis, key=lambda el: el.size.get("width", 0))
                    if img_grande and img_grande.size.get("width", 0) > 300:
                        break
                time.sleep(0.5)

            if not img_grande:
                print(f"Aviso: Não foi possível localizar a imagem grande no ciclo {i}.")
                break

            src = img_grande.get_attribute("src")

            if not src or src == anterior:
                print("Chegamos ao fim da galeria de fotos.")
                break

            caminho = DEST_FOLDER / f"foto_{timestamp_str}_{i:03d}.jpg"

            if salvar_via_blob(driver, src, caminho):
                baixadas += 1
                print(f"Foto {baixadas} salva com sucesso!")
            else:
                print(f"Aviso: Falha ao salvar a foto {i}.")

            anterior = src

            # Pressiona a tecla seta para a esquerda para ir para a foto anterior na ordem cronológica
            ActionChains(driver).send_keys(Keys.ARROW_LEFT).perform()
            time.sleep(2)  # Pausa para o WhatsApp carregar a próxima imagem

        except Exception as e:
            print(f"Erro no ciclo da foto {i}: {e}")
            break

    # Fecha o visualizador ao terminar
    try:
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    except:
        pass

    print(f"Processo concluído! Total de {baixadas} fotos salvas em {DEST_FOLDER}")

def main():
    driver = iniciar_driver()
    try:
        aguardar_login(driver)
        abrir_conversa_por_telefone(driver, PHONE_NUMBER)
        baixar_fotos_da_galeria(driver, QUANTIDADE)
    finally:
        input("Pressione Enter para fechar o navegador...")
        driver.quit()

if __name__ == "__main__":
    main()