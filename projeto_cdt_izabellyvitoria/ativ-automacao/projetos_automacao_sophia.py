import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ==============================
# CONFIGURAÇÕES
# ==============================

NOME_DO_GRUPO = "Programação 2/26 B/Tarde"
MENSAGEM = "@sophianeris"

# ==============================
# ABRIR O WHATSAPP WEB
# ==============================

options = Options()

# Cria um perfil separado para manter o WhatsApp conectado
options.add_argument("--user-data-dir=C:/automacao_whatsapp")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 40)

driver.get("https://web.whatsapp.com")

print("Abrindo WhatsApp Web...")
time.sleep(8)

# ==============================
# PROCURAR O GRUPO
# ==============================

print("Procurando o grupo...")

campo_busca = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, '//div[@contenteditable="true"][@role="textbox"]')
    )
)

campo_busca.click()
campo_busca.send_keys(NOME_DO_GRUPO)

time.sleep(3)

# ==============================
# ABRIR O GRUPO
# ==============================

grupo = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, f'//span[@title="{NOME_DO_GRUPO}"]')
    )
)

grupo.click()

print("Grupo encontrado!")
time.sleep(3)

# ==============================
# ENVIAR A MENSAGEM
# ==============================

caixa_mensagem = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, '//div[@contenteditable="true"][@role="textbox"]')
    )
)

caixa_mensagem.click()
caixa_mensagem.send_keys(MENSAGEM)
caixa_mensagem.send_keys(Keys.ENTER)

print("Mensagem enviada com sucesso!")

time.sleep(5)

driver.quit()