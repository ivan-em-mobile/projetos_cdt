"""# ⚡ ImpulseWork - Plataforma de Aceleração de Carreiras

O **ImpulseWork** é uma aplicação web desenvolvida em Python com a biblioteca **Flask** e **Flask-SQLAlchemy**. O objetivo do sistema é encurtar a distância entre candidatos e empresas parceiras, permitindo o registo de perfis profissionais, submissão automatizada de candidaturas e exportação do currículo em formato de texto.

---

## 📋 Funcionalidades Principais

- **Criar Perfil e Gerar Currículo:** Formulário completo para recolha de dados pessoais, contacto, cargo pretendido, formação académica e resumo profissional.
- **Candidatura Automatizada:** Envio do currículo para todas as empresas parceiras registadas na base de dados num único clique.
- **Download do Currículo:** Opção de descarregar uma cópia formatada em ficheiro `.txt`.
- **Gestão de Candidaturas:** Painel para o utilizador acompanhar o histórico e o estado das suas candidaturas.
- **Área da Empresa:** Registo de novas empresas parceiras e visualização da lista de empresas no sistema.
- **Interface Responsiva e Temas:** Suporte para alternar entre modo claro e modo escuro (Dark/Light Mode) com persistência local no navegador.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.x
- **Framework Web:** Flask
- **ORM / Base de Dados:** Flask-SQLAlchemy (SQLite)
- **Frontend:** HTML5, CSS3 (Variáveis CSS para Temas) e JavaScript

---

## 🗂️ Estrutura de Pastas do Projeto

```text
projetos_cdt_ivanemmobile/
│
└── projeto_cdt_manuellaandrade/
    ├── instance/
    │   └── impulsework.db     # Ficheiro da base de dados SQLite (criado automaticamente)
    ├── app.py                 # Ficheiro principal da aplicação Flask
    ├── Procfile               # Configuração de implantação (Heroku)
    ├── requirements.txt       # Dependências do projeto
    └── README.md              # Documentação do projeto

```

---

## 🗄️ Estrutura da Base de Dados

A base de dados é gerada automaticamente no ficheiro `instance/impulsework.db` e contém 4 tabelas principais:

1. **`Usuario`**: Guarda as informações de perfil do candidato (`id`, `nome`, `email`, `telefone`, `cargo`, `resumo`).
2. **`Formacao`**: Regista os dados académicos associados a um utilizador (`id`, `usuario_id`, `instituicao`, `curso`, `ano_conclusao`).
3. **`Empresa`**: Armazena as empresas parceiras cadastradas (`id`, `nome`, `area`, `site`).
4. **`Candidatura`**: Relaciona utilizadores com empresas (`id`, `usuario_id`, `empresa_id`, `data_envio`, `status`).

---

## 🚀 Como Executar o Projeto Localmente

### 1. Pré-requisitos

Certifica-te de ter o **Python** instalado na tua máquina.

### 2. Instalação das Dependências

Abre o terminal na pasta do projeto e instala os pacotes necessários:

```bash
pip install -r requirements.txt

```

*(Caso não tenhas o ficheiro `requirements.txt`, podes instalar diretamente: `pip install flask flask-sqlalchemy`)*

### 3. Execução do Servidor

Executa o ficheiro principal:

```bash
python app.py

```

Após a execução, o terminal exibirá a confirmação de criação da base de dados `impulsework.db` e a aplicação estará acessível no navegador no endereço:

```text
[http://127.0.0.1:5000](http://127.0.0.1:5000)

```

---

## 📄 Licença e Uso

Este projeto foi desenvolvido para fins didáticos e de demonstração prática de aplicações web com Python e Flask.
"""

with open("README.md", "w", encoding="utf-8") as f:
f.write(readme_content)

print("Ficheiro README.md criado com sucesso.")

```

```text?code_stdout&code_event_index=1
Ficheiro README.md criado com sucesso.


```

Com certeza! Preparei a documentação completa em formato **`README.md`** para o teu projeto **ImpulseWork**.

O teu ficheiro **`README.md`** está pronto para ser descarregado:


---

### 🌐 Panorama Geral da Solução

O ficheiro **`README.md`** serve como a documentação oficial do teu projeto. Ele detalha o objetivo do programa, as funcionalidades disponíveis, a arquitetura da base de dados e os passos necessários para qualquer pessoa instalar e executar a aplicação no seu próprio computador.

---

### 💻 Conteúdo do Ficheiro `README.md`

Caso queiras criar o ficheiro manualmente no VS Code, cria um novo ficheiro chamado **`README.md`** na pasta do teu projeto e cola o seguinte conteúdo:

```markdown
# ⚡ ImpulseWork - Plataforma de Aceleração de Carreiras

O **ImpulseWork** é uma aplicação web desenvolvida em Python com a biblioteca **Flask** e **Flask-SQLAlchemy**. O objetivo do sistema é encurtar a distância entre candidatos e empresas parceiras, permitindo o registo de perfis profissionais, submissão automatizada de candidaturas e exportação do currículo em formato de texto.

---

## 📋 Funcionalidades Principais

- **Criar Perfil e Gerar Currículo:** Formulário completo para recolha de dados pessoais, contacto, cargo pretendido, formação académica e resumo profissional.
- **Candidatura Automatizada:** Envio do currículo para todas as empresas parceiras registadas na base de dados num único clique.
- **Download do Currículo:** Opção de descarregar uma cópia formatada em ficheiro `.txt`.
- **Gestão de Candidaturas:** Painel para o utilizador acompanhar o histórico e o estado das suas candidaturas.
- **Área da Empresa:** Registo de novas empresas parceiras e visualização da lista de empresas no sistema.
- **Interface Responsiva e Temas:** Suporte para alternar entre modo claro e modo escuro (Dark/Light Mode) com persistência local no navegador.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.x
- **Framework Web:** Flask
- **ORM / Base de Dados:** Flask-SQLAlchemy (SQLite)
- **Frontend:** HTML5, CSS3 (Variáveis CSS para Temas) e JavaScript

---

## 🗂️ Estrutura de Pastas do Projeto

```text
projetos_cdt_ivanemmobile/
│
└── projeto_cdt_manuellaandrade/
    ├── instance/
    │   └── impulsework.db     # Ficheiro da base de dados SQLite (criado automaticamente)
    ├── app.py                 # Ficheiro principal da aplicação Flask
    ├── Procfile               # Configuração de implantação (Heroku)
    ├── requirements.txt       # Dependências do projeto
    └── README.md              # Documentação do projeto

```

---

## 🗄️ Estrutura da Base de Dados

A base de dados é gerada automaticamente no ficheiro `instance/impulsework.db` e contém 4 tabelas principais:

1. **`Usuario`**: Guarda as informações de perfil do candidato (`id`, `nome`, `email`, `telefone`, `cargo`, `resumo`).
2. **`Formacao`**: Regista os dados académicos associados a um utilizador (`id`, `usuario_id`, `instituicao`, `curso`, `ano_conclusao`).
3. **`Empresa`**: Armazena as empresas parceiras cadastradas (`id`, `nome`, `area`, `site`).
4. **`Candidatura`**: Relaciona utilizadores com empresas (`id`, `usuario_id`, `empresa_id`, `data_envio`, `status`).

---

## 🚀 Como Executar o Projeto Localmente

### 1. Pré-requisitos

Certifica-te de ter o **Python** instalado na tua máquina.

### 2. Instalação das Dependências

Abre o terminal na pasta do projeto e instala os pacotes necessários:

```bash
pip install -r requirements.txt

```

*(Caso não tenhas o ficheiro `requirements.txt`, podes instalar diretamente: `pip install flask flask-sqlalchemy`)*

### 3. Execução do Servidor

Executa o ficheiro principal:

```bash
python app.py

```

Após a execução, o terminal exibirá a confirmação de criação da base de dados `impulsework.db` e a aplicação estará acessível no navegador no endereço:

```text
[http://127.0.0.1:5000](http://127.0.0.1:5000)

```

---

