import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

def baixar_holerites_corrigido():
    # 1. Definir o caminho da Área de Trabalho e a pasta de destino
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    pasta_destino = os.path.join(desktop_path, "recibos de 2026")
    
    # Cria a pasta caso ela não exista
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
        print(f"Pasta criada: {pasta_destino}")
    
    # 2. Configurar perfil do Chrome para manter a sessão salva (sem pedir e-mail/senha)
    profile_dir = os.path.join(os.path.expanduser("~"), "chrome_profile_convenia")
    
    options = Options()
    options.add_argument(f"--user-data-dir={profile_dir}")
    
    # Configurar preferências para baixar os PDFs diretamente na nossa pasta
    prefs = {
        "download.default_directory": pasta_destino,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    }
    options.add_experimental_option("prefs", prefs)
    
    print("Iniciando o navegador...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    actions = ActionChains(driver)
    
    try:
        # 3. Acessar a página de recibos de pagamento[cite: 1]
        url = "https://colaborador.convenia.com.br/recibos-pagamento"
        driver.get(url)
        
        print("-" * 50)
        print("Se necessário, faça o login manualmente na sua conta.")
        print("Nas próximas execuções, o login estará salvo automaticamente.")
        input("Pressione ENTER no terminal assim que a lista de holerites estiver visível na tela... ")
        print("-" * 50)
        
        # 4. Localizar as linhas/registros da tabela de holerites
        time.sleep(2)
        
        # Procuramos por cada linha (tr) ou bloco que contém os recibos na tabela
        linhas_recibos = driver.find_elements(By.XPATH, "//tr[contains(., 'Holerite')] | //div[contains(@class, 'row') and contains(., 'Holerite')]")
        
        # Se não encontrar por linha de tabela, busca blocos gerais que tenham a palavra 'ANEXO'
        if not linhas_recibos:
            linhas_recibos = driver.find_elements(By.XPATH, "//*[contains(text(), 'ANEXO')]/ancestor::tr")
            
        print(f"Foram encontrados {len(linhas_recibos)} registros de holerites na página.")
        
        for index, linha in enumerate(linhas_recibos, start=1):
            try:
                # Rola a tela até a linha do holerite para garantir visibilidade
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", linha)
                time.sleep(1)
                
                # Passo A: Simula o movimento do mouse (Hover) em cima da linha inteira
                actions.move_to_element(linha).perform()
                time.sleep(1) # Aguarda o botão de download surgir visualmente
                
                # Passo B: Procura o botão/link de download específico que apareceu dentro desta linha
                # Buscamos por links (<a>) ou botões dentro da linha atual
                try:
                    botao_download = linha.find_element(By.XPATH, ".//a | .//button | .//*[contains(text(), 'ANEXO')]")
                    # Clica no botão descoberto
                    driver.execute_script("arguments[0].click();", botao_download)
                except:
                    # Caso alternativo: clica direto na linha se o botão estiver integrado
                    actions.click(linha).perform()
                    
                print(f"-> Holerite {index} processado e download acionado.")
                time.sleep(2.5) # Pausa para o navegador iniciar o download do PDF
                
            except Exception as e:
                print(f"Não foi possível baixar o item {index}: {e}")
                
        print("\nProcesso de cliques finalizado. Verificando os arquivos salvos...")
        
        # 5. Verificação automática na pasta criada
        time.sleep(5)
        arquivos_baixados = [f for f in os.listdir(pasta_destino) if f.endswith('.pdf')]
        
        print("\n" + "=" * 50)
        print(f" RELATÓRIO DA PASTA: 'recibos de 2026'")
        print("=" * 50)
        if arquivos_baixados:
            print("Arquivos PDF salvos com sucesso:")
            for arquivo in arquivos_baixados:
                print(f" 📄 {arquivo}")
        else:
            print("Nenhum arquivo PDF novo foi encontrado na pasta. Verifique a estrutura da página.")
        print("=" * 50)
        
    except Exception as erro:
        print(f"Ocorreu um erro durante a execução: {erro}")
        
    finally:
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    baixar_holerites_corrigido()