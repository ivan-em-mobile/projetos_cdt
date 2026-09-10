# ❄️ Pinguim Financeiro - Planejador de Gastos

O **Pinguim Financeiro** é uma aplicação web interativa desenvolvida em Flask para ajudar usuários a organizarem suas finanças de forma simples e visual. Através de uma interface moderna baseada na regra orçamentária 50/30/10/10, o sistema calcula automaticamente a distribuição da renda do usuário e oferece simulações inteligentes para investimentos futuros.

---

## 🚀 Funcionalidades

* **Tela de Onboarding:** Cadastro simples do nome do usuário, objetivo financeiro, instituição bancária e renda mensal total.
* **Dashboard Interativo:** Divisão visual automática dos gastos com base na renda informada:
  * 🔸 **50%** para Contas Fixas
  * 🟡 **30%** para Moradia e Aluguel
  * 🟢 **10%** para Lazer e Estilo de Vida
  * 🟣 **10%** Sobra Líquida para Investimentos
* **Gráfico de Rosquinha:** Renderização dinâmica dos percentuais utilizando a biblioteca `Chart.js`, adaptando-se visualmente ao tema da página.
* **Simulador de Investimentos Dinâmico:** Análise comparativa entre **Consórcio** e **Financiamento** para diferentes categorias (Imóveis, Automóveis e Compras Gerais), trazendo alertas realistas sobre análise de risco bancário e juros com base na sobra financeira do usuário.

---

## 📂 Estrutura do Projeto

Abaixo está a organização de pastas e arquivos estruturada na arquitetura MVC (Model-View-Controller) utilizada no desenvolvimento:

```text
PROJETOS_CDT_LALA/
│
├── Projeto_financas/
│   ├── app/
│   │   ├── models/                   # Modelos de dados do sistema
│   │   │   ├── financial_plan.py
│   │   │   ├── goal.py
│   │   │   └── user.py
│   │   ├── routes/                   # Controladores e rotas das páginas
│   │   │   ├── auth_routes.py
│   │   │   ├── dashboard_routes.py
│   │   │   ├── financial_routes.py
│   │   │   └── onboarding_routes.py
│   │   ├── services/                 # Lógicas de negócios e cálculos separados
│   │   │   ├── credit_analysis.py
│   │   │   ├── finance_service.py
│   │   │   └── onboarding.py
│   │   ├── static/                   # Arquivos estáticos front-end
│   │   │   ├── css/
│   │   │   │   ├── script.js
│   │   │   │   └── style.css
│   │   │   └── img/                  # Imagens e ícones
│   │   ├── templates/                # Telas estruturadas em HTML
│   │   │   ├── base.html
│   │   │   ├── dashboard.html
│   │   │   ├── index.html
│   │   │   ├── login.html
│   │   │   ├── onboarding.html
│   │   │   └── register.html
│   │   ├── __init__.py               # Inicialização do app Flask
│   │   └── config.py                 # Configurações do ambiente
│   │
│   ├── instance/
│   │   └── projeto.db                # Banco de dados local (SQLite)
│   │
│   ├── README.md
│   ├── requirements.txt              # Dependências do Python para o Render
│   └── run.py                        # Arquivo principal que roda o projeto
│
├── venv/                             # Ambiente virtual Python
├── .gitignore                        # Arquivos ignorados pelo Git
└── LICENSE                           # Licença do repositório

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python e Flask
* **Frontend:** HTML5, CSS3 (Variáveis nativas e efeitos de transição) e JavaScript (Vanilla)
* **Gráficos:** Chart.js
* **Ícones:** Font Awesome

---

## 📦 Como Rodar o Projeto Localmente (via VS Code)

Para executar este projeto na sua máquina, siga os passos abaixo no terminal do seu VS Code:

### 1. Clonar o Repositório
```bash
git clone [https://github.com/LaiSPaiv4/projetos_cdt_lala.git](https://github.com/LaiSPaiv4/projetos_cdt_lala.git)
```

### 2. Execute o servidor Flask rodando o arquivo principal
```bash
python run.py
```

### 3. Abra o seu navegador e acesse o endereço local gerado pelo Flask:
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 👥 Autores

Este projeto foi desenvolvido com muito carinho e dedicação por:
* **Lais Renta**
* **Henrique Souza** 

---
