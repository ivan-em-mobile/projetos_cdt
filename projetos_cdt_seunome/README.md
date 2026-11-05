
### Panorama Geral da Solução

Para organizar este `README.md` de forma clara e profissional, dividiremos a documentação em **6 secções principais**:

1. **Título e Descrição Geral do Projeto:** Uma breve apresentação sobre o propósito do robô (automação da reavaliação/aprovação de atividades de alunos no EAD).
2. **Funcionalidades:** Lista dos recursos do robô (pesquisa automática, atribuição de nota 0,75, ciclo contínuo em `while` e tratamento de pendências).
3. **Pré-requisitos e Dependências:** O que precisa de estar instalado no computador (Python 3.x, biblioteca `selenium` e o navegador Google Chrome).
4. **Configuração do Ambiente:** Instruções passo a passo de como abrir o Chrome na porta de depuração (`9222`) para reaproveitar a sessão logada.
5. **Como Executar o Script:** Como iniciar o script via VS Code ou linha de comandos.
6. **Estrutura e Explicação do Código:** Um resumo didático do fluxo do código Python e dos seus parâmetros (como a variável com o nome do jovem).

---

### Apresentação da Documentação `README.md`

Abaixo encontras o conteúdo completo formatado em **Markdown**. Podes copiar diretamente o bloco abaixo e colá-lo num novo ficheiro chamado `README.md` na mesma pasta onde está o teu ficheiro Python.

```markdown
# 🤖 Automador de Aprovação de Atividades - Plataforma EAD

Este projeto consiste numa automação em Python desenvolvida com **Selenium WebDriver** para otimizar o processo de lançamento de notas e aprovação de atividades pendentes de alunos numa plataforma EAD.

O robô conecta-se a uma sessão ativa do Google Chrome, pesquisa o aluno desejado e processa continuamente todas as suas atividades com o status **Pendente**, atribuindo a nota **0,75** e retornando à listagem até que todas as pendências daquele aluno sejam concluídas.

---

## 📌 Funcionalidades

- **Conexão com Sessão Ativa:** Conecta-se ao navegador Google Chrome já aberto, evitando a necessidade de realizar login e resolver *captchas* a cada execução.
- **Busca Dinâmica:** Localiza o campo de pesquisa e filtra as atividades pelo nome do jovem informado.
- **Atribuição Automática de Nota:** Acessa a prova e seleciona automaticamente a opção de nota **0,75**.
- **Processamento Contínuo (Loop `while`):** Repete o ciclo automaticamente para todas as atividades pendentes do aluno até que a fila seja zerada.
- **Navegação Segura:** Utiliza comandos via JavaScript (`scrollIntoView` e `click`) para garantir a interação correta com os elementos visuais da página.

---

## 🛠️ Pré-requisitos

Antes de executar o projeto, certifique-se de ter instalado no seu computador:

1. **Python 3.x**: [Download do Python](https://www.python.org/downloads/)
2. **Google Chrome**: Navegador instalado.
3. **Biblioteca Selenium**: Instalada via terminal.

```bash
pip install selenium

```

---

## 🚀 Passo a Passo de Configuração e Execução

### Passo 1: Abrir o Google Chrome na Porta de Depuração (`9222`)

Para que o script controle a sua janela aberta do Chrome com o login já efetuado, é necessário iniciar o navegador através do **Prompt de Comando (CMD)** do Windows:

1. Feche todas as janelas abertas do Google Chrome.
2. Abra o **Prompt de Comando (CMD)** do Windows.
3. Cole e execute o seguinte comando:

```cmd
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\selenium\AutomationProfile"

```

### Passo 2: Acessar a Plataforma EAD

1. Na janela do Chrome que acabou de abrir, aceda à plataforma EAD.
2. Faça o seu login normalmente e navegue até a página de **Listagem de Provas/Atividades**.

### Passo 3: Executar o Script Python

1. Abra a pasta do projeto no **VS Code**.
2. Abra o ficheiro do script Python (ex: `automacao_provas.py`).
3. No final do ficheiro, defina o nome do aluno na variável `jovem_para_aprovar`:

```python
if __name__ == "__main__":
    # Insira aqui o nome do aluno que deseja processar:
    jovem_para_aprovar = "Leandro do Carmo Xavier"
    
    aprovar_todas_pendencias_aluno(jovem_para_aprovar)

```

4. Execute o ficheiro no terminal:

```bash
python automacao_provas.py

```

---

## 🧠 Como o Código Funciona (Estrutura)

1. **`Options.debuggerAddress = "127.0.0.1:9222"`**: Conecta o Selenium à janela do Chrome já aberta.
2. **`while True`**: Inicia um ciclo infinito para verificar e processar pendências.
3. **`campo_busca.send_keys(nome_aluno)`**: Pesquisa o nome do jovem na tabela.
4. **`espera_curta.until(...)`**: Tenta encontrar o texto *"Pendente"*. Se não encontrar mais nenhum registro, o laço é encerrado (`break`).
5. **`botao_nota` (0,75)**: Clica na nota desejada.
6. **`navegador.back()`**: Retorna para a página anterior para iniciar a próxima verificação.

---

## 📄 Licença e Uso

Projeto desenvolvido para fins educacionais e de automação de tarefas administrativas repetitivas.

```

---

### Instruções Detalhadas de Implementação

1. **Criar o Ficheiro no VS Code:**
   * No VS Code, clica no ícone de **Novo Ficheiro** na barra lateral esquerda.
   * Dá-lhe o nome exato: `README.md`.
2. **Colar o Conteúdo:**
   * Copia todo o código Markdown do bloco acima e cola dentro desse novo ficheiro `README.md`.
3. **Guardar o Ficheiro:**
   * Pressiona `Ctrl + S` para guardar.
4. **Visualizar a Formatação (Opcional):**
   * No VS Code, podes clicar com o botão direito no ficheiro `README.md` e selecionar **"Abrir Pré-visualização"** (ou usar o atalho `Ctrl + Shift + V`) para ver o resultado visual formatado com os ícones e blocos de código estilizados.


# 🤖 Automação Integrada: Download e Organização de Holerites (2022 - 2026)

Este repositório contém uma solução completa desenvolvida em **Python** para automatizar o fluxo de obtenção e gestão de recibos de pagamento (holerites). A solução resolve dois problemas principais em sequência:

1. **Download Automático:** Extração e download em lote dos holerites diretamente de uma plataforma de RH via navegação automatizada.
2. **Leitura e Organização Inteligente:** Análise de texto dos PDFs baixados com leitura por OCR/extração e reestruturação dos nomes de arquivo com base nas datas e períodos encontrados.

---

## 🎯 Panorama Geral da Solução

O projeto funciona como uma pipeline dividida em duas etapas principais:

```
[ Plataforma Convenia / RH ] 
             │
             ▼ (Script 1: Selenium Webdriver)
[ Download dos PDFs Brutos na Pasta ]
             │
             ▼ (Script 2: PyPDF + Regex)
[ Identificação de Mês/Ano e Renomeação Padronizada ]
```

### O que o sistema faz:
* **Persistência de Sessão:** Utiliza o perfil local do Google Chrome no Selenium para salvar a autenticação do usuário. Não é necessário fazer login toda vez que o script roda.
* **Ação de Hover e Clique Interativo:** Mapeia a tabela da interface web, simula o movimento do mouse para revelar botões ocultos de download e baixa os arquivos.
* **Varredura Regex Multi-padrão:** Analisa diferentes variações de formato em textos de holerites ao longo dos anos (2022 até 2026).
* **Prevenção de Sobreposição:** Renomeia os arquivos automaticamente no formato `folha_mes_de_ano.pdf` e impede o apagamento acidental de arquivos com nomes duplicados.

---

## 🛠️ Pré-requisitos e Instalação

Para executar este projeto, você precisará do **Python 3.8+** e das seguintes bibliotecas instaladas no seu ambiente:

```bash
pip install selenium webdriver-manager pypdf
```

Além disso, certifique-se de ter o **Google Chrome** instalado na sua máquina.

---

## 🚀 Como Executar o Projeto

### Etapa 1: Baixar os Holerites
Execute o arquivo do primeiro script para iniciar a navegação automatizada:

```bash
python baixar_holerites.py
```
* **Nota de Uso:** Na primeira execução, o navegador abrirá para que você faça o login na plataforma (ex: Convenia). Nas próximas vezes, a sessão continuará aberta.
* Os arquivos baixados serão salvos na pasta configurada na sua Área de Trabalho.

### Etapa 2: Organizar e Renomear os PDFs
Após o término do download, execute o segundo script para processar os PDFs baixados:

```bash
python organizar_holerites.py
```
* O script lerá cada página, identificará a competência do documento e renomeará o arquivo para um formato padronizado (ex: `folha_junho_de_2026.pdf`).

---

## 💻 Códigos do Projeto

### 1. Script de Download (`baixar_holerites.py`)

```python
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
    
    # Configurar preferências para baixar os PDFs diretamente na pasta configurada
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
        # 3. Acessar a página de recibos de pagamento
        url = "https://colaborador.convenia.com.br/recibos-pagamento"
        driver.get(url)
        
        print("-" * 50)
        print("Se necessário, faça o login manualmente na sua conta.")
        print("Nas próximas execuções, o login estará salvo automaticamente.")
        input("Pressione ENTER no terminal assim que a lista de holerites estiver visível na tela... ")
        print("-" * 50)
        
        # 4. Localizar as linhas/registros da tabela de holerites
        time.sleep(2)
        
        # Busca por cada linha (tr) ou bloco que contém os recibos na tabela
        linhas_recibos = driver.find_elements(By.XPATH, "//tr[contains(., 'Holerite')] | //div[contains(@class, 'row') and contains(., 'Holerite')]")
        
        if not linhas_recibos:
            linhas_recibos = driver.find_elements(By.XPATH, "//*[contains(text(), 'ANEXO')]/ancestor::tr")
            
        print(f"Foram encontrados {len(linhas_recibos)} registros de holerites na página.")
        
        for index, linha in enumerate(linhas_recibos, start=1):
            try:
                # Rola a tela até a linha do holerite
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", linha)
                time.sleep(1)
                
                # Passo A: Simula movimento do mouse em cima da linha (Hover)
                actions.move_to_element(linha).perform()
                time.sleep(1)
                
                # Passo B: Localiza e clica no botão de download
                try:
                    botao_download = linha.find_element(By.XPATH, ".//a | .//button | .//*[contains(text(), 'ANEXO')]")
                    driver.execute_script("arguments[0].click();", botao_download)
                except:
                    actions.click(linha).perform()
                    
                print(f"-> Holerite {index} processado e download acionado.")
                time.sleep(2.5)
                
            except Exception as e:
                print(f"Não foi possível baixar o item {index}: {e}")
                
        print("\nProcesso de cliques finalizado. Verificando os arquivos salvos...")
        
        # 5. Relatório de verificação da pasta
        time.sleep(5)
        arquivos_baixados = [f for f in os.listdir(pasta_destino) if f.endswith('.pdf')]
        
        print("\n" + "=" * 50)
        print(" RELATÓRIO DA PASTA: 'recibos de 2026'")
        print("=" * 50)
        if arquivos_baixados:
            print("Arquivos PDF salvos com sucesso:")
            for arquivo in arquivos_baixados:
                print(f" 📄 {arquivo}")
        else:
            print("Nenhum arquivo PDF novo foi encontrado na pasta.")
        print("=" * 50)
        
    except Exception as erro:
        print(f"Ocorreu um erro durante a execução: {erro}")
        
    finally:
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    baixar_holerites_corrigido()
```

---

### 2. Script de Organização de PDFs (`organizar_holerites.py`)

```python
import os
import re
from pypdf import PdfReader

# Caminho da pasta contendo os recibos para análise e renomeação
PASTA_DESTINO = r"C:\Users\NotePCoder\Desktop\holerites de 2022 - 2026"

def extrair_mes_ano(texto_completo):
    """
    Função auxiliar com padrões Regex para identificar o mês e o ano
    em modelos de holerites de 2022 a 2026.
    """
    padroes = [
        # Padrão 1: Formato "Folha Mensal Junho de 2026"
        r"Folha[\s\n]+Mensal.*?([A-Za-zÇçãõéêíóú]+\s+de\s+(202[2-6]))",
        
        # Padrão 2: Formato "Mês: Janeiro/2023"
        r"Mês:\s*([A-Za-zÇçãõéêíóú]+)/(202[2-6])",
        
        # Padrão 3: Formato "OUTUBRO/2022"
        r"\b(JANEIRO|FEVEREIRO|MARÇO|ABRIL|MAIO|JUNHO|JULHO|AGOSTO|SETEMBRO|OUTUBRO|NOVEMBRO|DEZEMBRO)/(202[2-6])\b"
    ]
    
    for i, padrao in enumerate(padroes):
        resultado = re.search(padrao, texto_completo, re.IGNORECASE | re.DOTALL)
        if resultado:
            if i == 0:
                return resultado.group(1).lower()
            elif i == 1 or i == 2:
                mes = resultado.group(1).lower()
                ano = resultado.group(2)
                return f"{mes} de {ano}"
                
    return None

def processar_holerites_periodo(caminho_pasta):
    """
    Função principal para percorrer a pasta, ler os PDFs e aplicar a renomeação.
    """
    if not os.path.exists(caminho_pasta):
        print(f"Erro: A pasta '{caminho_pasta}' não foi encontrada.")
        return

    print(f"Inspecionando a pasta: {caminho_pasta}\n" + "-"*50)
    
    arquivos = os.listdir(caminho_pasta)
    sucessos = 0
    divergencias = 0

    for arquivo in arquivos:
        if arquivo.lower().endswith(".pdf"):
            caminho_antigo = os.path.join(caminho_pasta, arquivo)
            print(f"Analisando arquivo: {arquivo}")
            
            try:
                # Leitura do texto das páginas
                leitor = PdfReader(caminho_antigo)
                texto_completo = ""
                for pagina in leitor.pages:
                    texto_extraido = pagina.extract_text()
                    if texto_extraido:
                        texto_completo += texto_extraido + "\n"
                
                # Identificação de Mês e Ano
                mes_ano_encontrado = extrair_mes_ano(texto_completo)
                
                if mes_ano_encontrado:
                    nome_formatado = mes_ano_encontrado.replace(" ", "_")
                    novo_nome = f"folha_{nome_formatado}.pdf"
                    caminho_novo = os.path.join(caminho_pasta, novo_nome)
                    
                    if caminho_antigo != caminho_novo:
                        if os.path.exists(caminho_novo):
                            print(f"  [Aviso] O arquivo '{novo_nome}' já existe. Pulando para evitar sobrescrever.\n")
                            continue
                        
                        os.rename(caminho_antigo, caminho_novo)
                        print(f"  [Sucesso] Renomeado para: {novo_nome}\n")
                        sucessos += 1
                    else:
                        print(f"  [Info] O arquivo já está com o nome correto.\n")
                else:
                    print(f"  [Atenção] Não foi possível identificar o mês e o ano neste arquivo PDF.\n")
                    divergencias += 1
                    
            except Exception as e:
                print(f"  [Erro] Falha ao processar o arquivo '{arquivo}'. Detalhe: {e}\n")
                divergencias += 1

    print("-" * 50)
    print(f"Processo finalizado!")
    print(f"Total de arquivos renomeados com sucesso: {sucessos}")
    print(f"Total de arquivos com divergências/erros de leitura: {divergencias}")

if __name__ == "__main__":
    processar_holerites_periodo(PASTA_DESTINO)
```

---

## 📝 Licença e Uso

Este projeto tem fins educacionais e de automação pessoal/administrativa. Sinta-se à vontade para clonar o repositório, propor alterações ou ajustar as expressões regulares para adequar aos modelos de PDF da sua empresa.
