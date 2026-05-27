
# 🎯 Projeto Final: Sistema de Gestão para Salão de Beleza

Olá! 👋 Bem-vindo ao repositório do projeto final do curso **Código_Transformação**. Este sistema foi desenvolvido para gerenciar de forma prática e automatizada a operação de um Salão de Beleza, unindo um backend robusto em Python com uma interface web leve e intuitiva.

O projeto cumpre todos os requisitos do **Módulo 15**, integrando banco de dados relacional, APIs estruturadas, regras de negócio restritas e preparação completa para deploy em nuvem.

---

## 💻 Visão Geral do Projeto

O sistema simula a rotina real de um salão de beleza focado em agendamentos, cadastros e controle financeiro de produtos e serviços. 

### 🛠️ Tecnologias Utilizadas:
* **Backend:** Python 3 com o framework **Flask** (API RESTful)
* **Banco de Dados:** **SQLite3** (Relacional)
* **Frontend:** HTML5, CSS3 (Design Responsivo) e JavaScript (Vanilla ES6)
* **Deploy & Hospedagem:** Estruturado e configurado para a **Vercel**

---

## ⚙️ Regras de Negócio Implementadas

Para tornar o desafio mais realista, o sistema conta com validações rígidas no backend:

1.  **Restrição de Operador:** Apenas o **Recepcionista-Andrei** tem permissão no sistema para efetuar e validar novos agendamentos na agenda.
2.  **Dias de Funcionamento:** Os agendamentos só são aceites se forem marcados para os dias de funcionamento do salão: **Quarta, Quinta, Sexta, Sábado e Domingo**.
3.  **Flexibilidade de Preços:** Todos os valores dos serviços e produtos do catálogo são 100% editáveis diretamente pelo painel e salvos no banco de dados.
4.  **Portabilidade de Dados (JSON):** O sistema possui um botão exclusivo que faz o dump do banco de dados relacional e exporta um arquivo `.json` estruturado direto para a máquina do usuário.

---

## 🗄️ Estrutura do Banco de Dados (Entidades Fixas)

O banco de dados é inicializado automaticamente no primeiro boot com os seguintes dados base:

* **5 Funcionários:** * Cabeleireiro-Andre
    * Cabeleireira-Andreia
    * Cabeleireiro-Antonio
    * Podóloga-Andressa
    * Recepcionista-Andrei
* **3 Serviços (Preços Editáveis):** Corte, Pintura e Tratamento Químico.
* **3 Produtos (Preços Editáveis):** Shampoo, Creme e Máscara Capilar.
* **Clientes & Agendamentos:** Cadastrados dinamicamente.

---

## 📂 Estrutura de Arquivos do Repositório

```text
PROJETO_CDT_ALUNOIVAN/
│
├── app.py              # Código principal da API Flask e regras de negócio
├── vercel.json         # Arquivo de configuração de rotas para deploy na Vercel
├── requirements.txt    # Dependências do projeto (Flask)
│
├── static/             # Arquivos estáticos do Frontend
│   ├── style.css       # Estilização visual do painel
│   └── script.js       # Consumo da API e manipulação do DOM via Fetch
│
└── templates/          # Páginas HTML renderizadas pelo Jinja2
    └── index.html      # Painel administrativo do salão

```

---

## 🚀 Como Testar e Rodar o Projeto Localmente

Se quiseres clonar e executar este projeto na tua máquina local, segue estes passos simples:

### 1. Clonar o Repositório

```bash
git clone [https://github.com/teu-usuario/PROJETO_CDT_ALUNOIVAN.git](https://github.com/teu-usuario/PROJETO_CDT_ALUNOIVAN.git)
cd PROJETO_CDT_ALUNOIVAN

```

### 2. Instalar as Dependências

Certifica-te de que tens o Python instalado e executa:

```bash
pip install -r requirements.txt

```

### 3. Iniciar o Servidor Flask

```bash
python app.py

```

### 4. Aceder no Navegador

Abre o teu navegador web e acede ao endereço local:
👉 [http://127.0.0.1:5000/](https://www.google.com/search?q=http://127.0.0.1:5000/)

---

## ☁️ Configuração para Deploy (Vercel)

Este projeto foi modificado com uma arquitetura flexível para funcionar perfeitamente na infraestrutura serverless da Vercel:

* O arquivo `vercel.json` gerencia o roteamento de arquivos estáticos e redireciona as requisições para o script do Python.
* O `app.py` detecta dinamicamente o ambiente produtivo e redireciona a criação do banco SQLite para o diretório `/tmp/salao.db`, contornando a proteção de arquivos *read-only* da Vercel.

---

**Projeto Finalizado com Sucesso! #BoraCodar** 🚀✨

---

