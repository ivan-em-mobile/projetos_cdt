import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "localhost:9222")

driver = webdriver.Chrome(options=options)

encontrou = False
for handle in driver.window_handles:
    driver.switch_to.window(handle)
    if "web.whatsapp.com" in driver.current_url:
        encontrou = True
        break

if not encontrou:
    driver.execute_script("window.open('https://web.whatsapp.com', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])

wait = WebDriverWait(driver, 60)
print("Conectado ao navegador. Aguardando renderização do WhatsApp Web...")

# PASSO CRÍTICO: Espera até que a estrutura principal da página saia do estado 'wf-loading'
wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="app"]//div[@id="side"]')))

def encontrar_elemento(driver, opcoes, descricao, timeout_por_opcao=15):
    ultimo_erro = None
    for by, valor in opcoes:
        try:
            return WebDriverWait(driver, timeout_por_opcao).until(
                EC.element_to_be_clickable((by, valor))
            )
        except Exception as e:
            ultimo_erro = e
            continue
    driver.save_screenshot("erro_debug.png")
    with open("erro_debug.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print(f"Não encontrei: {descricao}. Print salvo em erro_debug.png e HTML em erro_debug.html")
    raise ultimo_erro

# Busca pela caixa de pesquisa (incluindo o elemento input validado)
search_box = encontrar_elemento(driver, [
    (By.CSS_SELECTOR, 'input[data-tab="3"]'),
    (By.XPATH, '//input[@aria-label="Pesquisar ou começar uma nova conversa"]'),
    (By.XPATH, '//div[@aria-placeholder="Pesquisar ou começar uma nova conversa"]'),
    (By.CSS_SELECTOR, '#side div[contenteditable="true"]'),
], "caixa de busca")

nome_grupo = "Programação 2/26 B/Tarde"

search_box.click()
search_box.clear()
search_box.send_keys(nome_grupo)

# Aguarda explicitamente a lista de conversas atualizar com o resultado
chat = wait.until(EC.element_to_be_clickable(
    (By.XPATH, f'//span[@title="{nome_grupo}"]')
))
chat.click()

# Busca pela caixa de mensagem no chat aberto
msg_box = encontrar_elemento(driver, [
    (By.XPATH, '//footer//div[@contenteditable="true"]'),
    (By.XPATH, '//div[@aria-placeholder="Digite uma mensagem"]'),
    (By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'),
], "caixa de mensagem")

msg_box.click()
msg_box.send_keys("@nicolemendes")
msg_box.send_keys(Keys.ENTER)

print("Mensagem enviada com sucesso!")
time.sleep(3)
