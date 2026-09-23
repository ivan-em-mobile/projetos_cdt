# 💰 Sistema Integrado de Monitoramento Financeiro & Metas

Aplicação para acompanhamento de cotações de moedas em tempo real, conversão cambial, gerenciamento de metas orçamentárias pessoais e geração de relatórios/logs de atividades.

O projeto oferece duas interfaces de usuário independentes: uma **Interface Desktop (Tkinter)** e uma **Interface Web (Streamlit)**, compartilhando regras de negócio e persistência de dados em **SQLite**.

---

## 👥 Integrantes / Autores

* **Nicolas Santana de Melo**
* **Felipe Oliveira Araújo**

---

## 🚀 Funcionalidades Principais

* **💱 Cotações & Conversor Cambial:**
  * Consulta em tempo real das cotações de principais moedas globais (USD, EUR, GBP, JPY, CAD, CHF, AUD, BTC) via **AwesomeAPI**.
  * Calculadora de conversão dinâmica entre moedas.

* **🎯 Gestão de Metas & Orçamento Pessoal:**
  * Cadastro de metas financeiras categorizadas (Reserva de Emergência, Investimentos, Viagens, Tecnologia, Educação, etc.).
  * Realização de aportes dinâmicos para atualização do saldo acumulado.
  * Acompanhamento visual de progresso por barras de porcentagem.
  * Exclusão e manutenção de metas.

* **📊 Análises Visuais & Gráficos:**
  * Comparativo entre valor alvo e valor atual das metas via gráficos de barras (`Matplotlib` no Desktop / `Streamlit Charts` no Web).
  * Distribuição dos investimentos/alvos agrupados por categoria.

* **📄 Relatórios & Histórico de Atividades:**
  * Exportação de dados das metas cadastradas em arquivo **CSV**.
  * Geração de relatórios executivos formatados em **PDF** (`ReportLab`).
  * Registro de auditoria das operações e logs do sistema em formato **JSON** (`activity_log.json`).

* **♿ Recursos Extras & Acessibilidade:**
  * Leitor de voz/sintetizador de áudio para explicação do guia de uso (`pyttsx3`).
  * Atalhos de teclado no Desktop (`F1`, `Alt + 1` a `Alt + 6`).
  * Gerenciador de alertas de preços máximos e teto de cotações.

---

## 📂 Estrutura do Arquivo de Código

| Arquivo | Descrição |
| :--- | :--- |
| `app.py` | Aplicação Desktop completa desenvolvida em **Tkinter** com integração de atalhos, leitor de voz, Matplotlib e ReportLab. |
| `app_web.py` | Aplicação Web interativa desenvolvida em **Streamlit** dividida por abas para usabilidade no navegador. |
| `Services.py` | Módulo com a lógica de negócio, chamadas à API de câmbio, criação de logs JSON e operações CRUD do banco. |
| `Database.py` | Módulo de configuração e inicialização do banco de dados SQLite (`monitor_data.db`). |

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas

* **Linguagem:** Python 3.x
* **Banco de Dados:** SQLite 3
* **Interface Gráfica (GUI):** Tkinter (Desktop) / Streamlit (Web)
* **APIs Externas:** [AwesomeAPI Economia](https://docs.awesomeapi.com.br/api-de-moedas) (Cotações em tempo real)
* **Bibliotecas Python:**
  * `requests` — Requisições HTTP para a API de câmbio.
  * `pandas` — Manipulação de dados e geração de gráficos no Streamlit.
  * `matplotlib` — Renderização de gráficos na interface Tkinter.
  * `reportlab` — Geração e exportação de relatórios em PDF.
  * `pyttsx3` — Síntese de voz (Text-to-Speech) para acessibilidade.
  * `plyer` — Notificações do sistema operacional.

---

## 📦 Como Executar o Projeto

### 1. Pré-requisitos
Certifique-se de ter o **Python 3.8+** instalado em sua máquina.

### 2. Instalação das Dependências
Instale todas as dependências do projeto através do `pip`:

```bash
pip install requests pandas streamlit matplotlib reportlab pyttsx3 plyer
```

---

### 3. Executando a Aplicação Desktop (Tkinter)

Para iniciar a versão para desktop:

```bash
python app.py
```

* **Atalhos de Navegação:**
  * `F1`: Guia & Acessibilidade
  * `Alt + 1`: Cotações & Conversor
  * `Alt + 2`: Metas & Orçamento
  * `Alt + 3`: Alertas
  * `Alt + 4`: Gráficos
  * `Alt + 5`: Relatórios

---

### 4. Executando a Aplicação Web (Streamlit)

Para abrir a interface web no seu navegador:

```bash
streamlit run app_web.py
```

A aplicação será aberta automaticamente no endereço local `http://localhost:8501`.

---

## 💾 Banco de Dados & Logs

* **`monitor_data.db`**: Banco de dados relacional SQLite gerado automaticamente ao rodar a aplicação. Contém as tabelas `metas_financeiras`, `conversoes` e `alertas`.
* **`activity_log.json`**: Arquivo JSON criado para manter o histórico estruturado de todas as conversões, criações e alterações de metas efetuadas na aplicação.