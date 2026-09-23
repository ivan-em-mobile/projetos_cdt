import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# Configurações do Chrome
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument(r"--user-data-dir=C:\Users\Aluno\Desktop\PerfilChromeBot")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://web.whatsapp.com")

# Aguarda 15 segundos para a página e as conversas carregarem completamente
time.sleep(15)

try:
    # 1. Usa o atalho do teclado do WhatsApp Web para focar na caixa de pesquisa
    actions = ActionChains(driver)
    actions.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys("/").key_up(Keys.ALT).key_up(Keys.CONTROL).perform()
    time.sleep(1)

    # 2. Digita o nome do grupo e pressiona Enter para abrir
    actions.send_keys("YOU LIKE 4EVER! 🧐").perform()
    time.sleep(2)
    actions.send_keys(Keys.ENTER).perform()
    time.sleep(2)

    # 3. Digita a menção na mensagem
    actions.send_keys("teste de envio").perform()
    time.sleep(2)

    # Confirma a menção da lista com Enter
    actions.send_keys(Keys.ENTER).perform()
    time.sleep(1)

    # Clica diretamente no botão de enviar (ícone do aviãozinho)
    send_button = driver.find_element(By.XPATH, '//button[@aria-label="Enviar" or @data-tab="11"]')
    send_button.click()
    print("Mensagem enviada com sucesso!")

except Exception as e:
    print(f"Ocorreu um erro detalhado: {type(e).__name__} - {e}")