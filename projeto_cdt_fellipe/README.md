# Catecismo Digital - API Católica

Este é um projeto de API e aplicação web desenvolvido em **Flask (Python)** com o objetivo de disponibilizar conteúdos doutrinários da Igreja Católica de forma categorizada, incluindo suporte a autenticação de usuários (cadastro e login). Os dados incluem explicações detalhadas baseadas no Catecismo Romano, Concílio de Trento e outras fontes magisteriais sobre o Credo, os Sacramentos, os Mandamentos, a Oração, Dogmas e a própria Igreja.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3**
* **Flask:** Framework web para estruturação da aplicação e rotas.
* **Flask-SQLAlchemy:** ORM para interação simplificada com o banco de dados.
* **Flask-CORS:** Gerenciamento de permissões de acesso externo (Cross-Origin Resource Sharing).
* **Werkzeug:** Criptografia segura de senhas utilizando hashes.
* **SQLite:** Banco de dados relacional local (configurado dinamicamente para deploy em plataformas como o Render).

---

## 📁 Estrutura do Projeto

Com base na estrutura de diretórios do repositório (conforme mapeado na imagem `image_74a3aa.png`), a organização do código está disposta da seguinte forma:

```text
├── estático/               # Arquivos estáticos (CSS, JS do front-end)
├── exemplo/                # Exemplos adicionais do projeto
├── modelos/                # Modelagens auxiliares ou índices
├── app.py                  # Arquivo principal (Configuração, Modelos e Rotas da API)
├── inicializador_bd.py     # Script para criação e povoamento inicial do banco de dados
├── dados_ijreja.json       # Arquivo de dados brutos de suporte
├── requisitos.txt          # Dependências do Python (pip install)
├── vercel.json             # Configurações para deploy na Vercel
├── LICENÇA                 # Termos de licença do projeto
└── README.md               # Documentação do sistema

```

---

## 🚀 Como Executar o Projeto Localmente

### 1. Clonar o Repositório e Instalar as Dependências

Abra o seu terminal no diretório do projeto e instale as bibliotecas necessárias listadas em `requisitos.txt`:

```bash
pip install -r requisitos.txt

```

### 2. Inicializar o Banco de Dados

Antes de rodar o servidor, você precisa criar o arquivo do banco de dados SQLite (`igreja_catolica.db`) e povoá-lo com as tabelas de conteúdos. Execute o script:

```bash
python inicializador_bd.py

```

> **Nota:** Se o banco já contiver informações, o script emitirá a mensagem *"Banco de dados já está povoado."* para evitar duplicidade.

### 3. Executar o Servidor Flask

Com o banco devidamente configurado, inicie a aplicação:

```bash
python app.py

```

O servidor estará disponível por padrão no endereço: `[http://127.0.0.1:5000/](http://127.0.0.1:5000/)`

---

## 🔌 Rotas da API e Endpoints

### 🏠 Front-End (Página Principal)

* **`GET /`**
* **Descrição:** Renderiza a interface principal do projeto contida em `templates/index.html`.



### 🔐 Autenticação de Usuários

* **`POST /api/cadastro`**
* **Descrição:** Registra um novo usuário no sistema salvando a senha de forma criptografada.
* **Corpo da Requisição (JSON):**
```json
{
  "usuario": "nome_do_usuario",
  "senha": "sua_senha_segura"
}

```





```

*   **`POST /api/login`**
    *   **Descrição:** Valida as credenciais do usuário.
    *   **Corpo da Requisição (JSON):**
        ```json
        {
          "usuario": "nome_do_usuario",
          "senha": "sua_senha_segura"
        }

```

### 📖 Conteúdo Doutrinário

* **`GET /api/conteudo/<int:categoria_id>/<int:opcao_id>`**
* **Descrição:** Retorna o título e o texto explicativo de um tema específico baseado nos identificadores de categoria e opção.
* **Exemplo de Resposta (JSON):**
```json
{
  "titulo": "O que é Sacramento?",
  "texto": "Conforme o Concílio de Trento, Sacramento é um sinal visível da graça invisível..."
}

```


#### 📌 Mapeamento de Categorias de Conteúdo (`categoria_id`):
| ID da Categoria | Descrição Temática |
| :---: | :--- |
| **1** | Artigos do Credo (Símbolo dos Apóstolos) |
| **2** | Os Sete Sacramentos |
| **3** | O Decálogo (Os Dez Mandamentos) |
| **4** | A Oração Dominical (Pai-Nosso e outras preces) |
| **5** | Dogmas de Fé da Igreja |
| **6** | Fontes da Revelação (Tradição, Escritura e Magistério) |
| **7** | Natureza e Propriedades da Igreja Católica |


## ☁️ Deploy e Nuvem

O código foi preparado para identificar automaticamente o ambiente de hospedagem. Se a variável de ambiente `RENDER` estiver ativa, o banco de dados SQLite será realocado de maneira temporária e otimizada para o caminho `/tmp/igreja_catolica.db`, garantindo compatibilidade com plataformas de infraestrutura como o **Render** e suporte a pipelines configurados via **Vercel** (`vercel.json`).

Link do projeto rodando no Render: https://projetos-cdt.onrender.com
