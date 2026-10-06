# STARK IA — Assistente de Carreira e Busca de Vagas (Versão Desktop)

A **STARK IA** é uma aplicação desktop desenvolvida em Python que combina um chat interativo de orientação profissional com a automação de pesquisa de vagas de emprego em tempo real no portal da Catho.

---

## 📌 Visão Geral do Projeto

O programa oferece uma interface gráfica moderna e intuitiva em modo escuro onde o utilizador pode:
- **Receber orientações de carreira:** Dicas para entrevistas, elaboração de currículos, transição de carreira e competências de mercado.
- **Buscar vagas automatizadas:** O robô identifica o cargo e a região mencionados na conversa e realiza a pesquisa automaticamente no navegador Chrome via Selenium.
- **Experiência sem travamentos:** A busca corre em segundo plano (*threading*), mantendo a janela do chat sempre responsiva.

---

## 🚀 Funcionalidades Principais

- **Interface Gráfica Moderna:** Desenvolvida com `customtkinter` em tema escuro (*Dark Mode*).
- **Processamento de Linguagem Natural (NLP Básico):** Extração inteligente de cargos e mapeamento de cidades/estados brasileiros via *Regex*.
- **Automação Web com Selenium:** Abertura e navegação automática na página de vagas da Catho.
- **Processamento Assíncrono:** Execução das buscas em *threads* separadas para não congelar a interface.
- **Filtro de Conteúdo:** Respostas direcionadas exclusivamente para temas profissionais e de carreira.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Interface Gráfica:** `customtkinter`
- **Automação Web:** `selenium`
- **Manipulação de Texto:** Expressões Regulares (`re`) e `urllib.parse`
- **Multiprocessamento:** `threading`

---

## 📋 Pré-requisitos

Antes de executar o projeto, garante que tens instalado no teu computador:

1. **Python 3.10** ou superior.
2. **Navegador Google Chrome** instalado.
3. Gerenciador de pacotes **pip** atualizado.

---

## 🔧 Passo a Passo de Instalação e Execução

### 1. Clonar ou Baixar o Repositório
Transfere os ficheiros do projeto para uma pasta no teu computador.

### 2. Criar um Ambiente Virtual (Opcional, mas Recomendado)
No terminal do teu sistema operativo, navega até à pasta do projeto e executa:

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar no Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Ativar no Linux / macOS
source venv/bin/activate

```

### 3. Instalar as Dependências

Com o ambiente ativado (ou no terminal padrão), instala os pacotes necessários através do ficheiro `requirements.txt`:

```bash
pip install -r requirements.txt

```

### 4. Executar a Aplicação

Executa o ficheiro principal da aplicação desktop:

```bash
python app_starkai_lucasprates.py

```

---

## 📂 Estrutura de Ficheiros

```text
├── app_starkai_lucasprates.py          # Código principal da aplicação desktop (CustomTkinter + Selenium)
├── requirements.txt    # Lista de dependências do projeto
├── stark_logo.ico      # Ícone da aplicação (opcional)
└── README.md           # Documentação do projeto

```

---

## 💡 Como Usar a STARK IA

1. Abra a aplicação executando o `app_starkai_lucasprates.py`.
2. No campo de texto na parte inferior, digite a sua dúvida ou o que procura:
* *Exemplo de Orientação:* "Como devo me preparar para uma entrevista de emprego?"
* *Exemplo de Busca de Vagas:* "Quero vagas para Engenheiro Químico em São Paulo"


3. O robô irá responder no chat e abrirá uma janela do navegador Chrome com as vagas correspondentes já filtradas na Catho.

---
