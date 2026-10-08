# Sintonia

O **Sintonia** é uma aplicação web desenvolvida em **Python** com **Flask**, criada para gerar playlists personalizadas no Spotify a partir do momento do usuário.

A aplicação combina informações como **cidade, clima, humor e artista favorito** para realizar uma busca de músicas e criar automaticamente uma playlist na conta do Spotify conectada.

Além da criação de playlists, o projeto possui **banco de dados SQLite** e uma **área administrativa Master**, permitindo a exportação dos dados armazenados para um arquivo JSON.

---

## Tecnologias Utilizadas

* **Python 3** — Linguagem principal do projeto.
* **Flask** — Framework utilizado para o desenvolvimento da aplicação web.
* **Spotipy** — Biblioteca Python para integração com a Spotify Web API.
* **Spotify Web API** — Utilizada para autenticação, pesquisa de músicas e criação de playlists.
* **OpenWeather API** — Utilizada para consulta das condições climáticas.
* **SQLite3** — Banco de dados local utilizado para persistência dos dados.
* **HTML5** — Estrutura das páginas da aplicação.
* **CSS3** — Estilização e interface visual.
* **python-dotenv** — Gerenciamento das variáveis de ambiente.

---

## Funcionalidades

### Criação de playlists personalizadas

O usuário informa as características que deseja utilizar para sua playlist:

* Cidade;
* Humor;
* Artista favorito.

A partir dessas informações, o Sintonia realiza uma busca no Spotify e cria uma nova playlist automaticamente.

### Integração com OpenWeather

A cidade informada pelo usuário é utilizada para consultar informações meteorológicas através da OpenWeather API.

Entre os dados obtidos estão:

* temperatura;
* condição climática;
* descrição do clima.

Essas informações podem ser utilizadas como parte dos critérios para a busca musical.

### Integração com Spotify

Através da autenticação OAuth, o usuário conecta sua conta do Spotify ao sistema.

A aplicação utiliza a API para:

* autenticar o usuário;
* pesquisar músicas;
* criar playlists;
* adicionar músicas à playlist criada;
* direcionar o usuário para a playlist no Spotify.

### Banco de dados

O projeto utiliza **SQLite** para armazenamento local dos dados.

O banco utilizado pela aplicação é:

```text
database.db
```

### Área Master

O sistema possui uma área administrativa acessível através de:

```text
http://127.0.0.1:8888/root
```

Credenciais definidas para o ambiente de desenvolvimento:

```text
Usuário: root
Senha: root
```

O painel permite acessar a função de exportação do banco de dados.

### Exportação para JSON

A área Master permite exportar os dados armazenados no SQLite para um arquivo JSON:

```text
sintonia_database.json
```

A exportação reúne os registros das tabelas existentes no banco em uma estrutura JSON, facilitando a consulta e o armazenamento de uma cópia dos dados.

---

## Interface

O Sintonia possui uma interface web com uma identidade visual baseada em tons de rosa, com suporte a temas claro e escuro.

A aplicação conta com:

* página de login;
* dashboard para criação de playlists;
* formulário de personalização;
* área Master;
* painel de exportação do banco;
* layout adaptado para diferentes tamanhos de tela.

---

## Estrutura do Projeto

A organização principal dos arquivos é:

```text
meu_player/
│
├── app.py
├── admin.py
├── database.db
├── .env
│
└── templates/
    ├── login.html
    ├── dashboard.html
    ├── root_login.html
    └── root_panel.html
```

### Arquivos principais

**`app.py`**
Arquivo principal da aplicação. Contém o servidor Flask, as rotas, a autenticação do Spotify, a consulta do clima e a lógica de criação das playlists.

**`admin.py`**
Contém as funções relacionadas à administração e à exportação dos dados do banco.

**`database.db`**
Banco de dados SQLite utilizado pelo projeto.

**`.env`**
Arquivo utilizado para armazenar credenciais e chaves de API.

**`login.html`**
Página inicial da aplicação e entrada para autenticação com o Spotify.

**`dashboard.html`**
Interface principal onde o usuário informa cidade, humor e artista para gerar sua playlist.

**`root_login.html`**
Página de autenticação da área Master.

**`root_panel.html`**
Painel administrativo com as funções disponíveis para o usuário Master.

---

## Configuração

Antes de executar o projeto, é necessário configurar as credenciais das APIs.

Crie um arquivo `.env` na pasta principal:

```env
SPOTIPY_CLIENT_ID=SEU_CLIENT_ID
SPOTIPY_CLIENT_SECRET=SEU_CLIENT_SECRET
WEATHER_API_KEY=SUA_API_KEY
FLASK_SECRET_KEY=SUA_CHAVE_SECRETA
```

As credenciais reais devem ser inseridas apenas no ambiente local.

### Redirect URI do Spotify

Para execução local, o Spotify deve estar configurado com:

```text
http://127.0.0.1:8888/callback
```

O mesmo endereço deve estar definido no código da aplicação.

---

## Instalação

Com o Python 3 instalado, abra o terminal na pasta do projeto e execute:

```bash
pip install flask spotipy requests python-dotenv
```

Depois de instalar as dependências e configurar o `.env`, execute:

```bash
python app.py
```

A aplicação estará disponível em:

```text
http://127.0.0.1:8888
```

---

## Funcionamento

O fluxo principal do Sintonia funciona da seguinte maneira:

```text
                 Sintonia
                    |
                    v
             Página inicial
                    |
                    v
              Login Spotify
                    |
                    v
            Autenticação OAuth
                    |
                    v
                Dashboard
                    |
          +---------+---------+
          |         |         |
          v         v         v
       Cidade     Humor     Artista
          |         |         |
          +---------+---------+
                    |
                    v
             Consulta do clima
                    |
                    v
             Busca no Spotify
                    |
                    v
           Criação da playlist
                    |
                    v
                 Spotify
```

---

## Área Master

O acesso à área administrativa é realizado através de:

```text
http://127.0.0.1:8888/root
```

O administrador utiliza as credenciais:

```text
Usuário: root
Senha: root
```

Após a autenticação, o painel disponibiliza a opção de exportação do banco.

O fluxo administrativo é:

```text
/root
  |
  v
Login Master
  |
  v
Painel Master
  |
  v
Exportar banco de dados
  |
  v
sintonia_database.json
```

---

## Segurança

As credenciais utilizadas pelas APIs devem permanecer protegidas.

O arquivo `.env` **não deve ser publicado em repositórios públicos**, pois contém informações sensíveis.

Recomenda-se utilizar um `.gitignore` contendo:

```gitignore
.env
.cache
__pycache__/
*.pyc
```

A combinação `root / root` foi definida para fins de desenvolvimento e apresentação do projeto. Em uma aplicação destinada ao uso real, as credenciais administrativas devem ser substituídas por uma senha forte e armazenadas de forma segura.

---

## Objetivo do Projeto

O Sintonia foi desenvolvido com o objetivo de aplicar conhecimentos de **Python, desenvolvimento web, APIs, banco de dados e automação** em uma aplicação prática.

A proposta é transformar informações simples sobre o momento do usuário em uma experiência musical personalizada, utilizando serviços externos para enriquecer a seleção de músicas.

O projeto também permite colocar em prática conceitos como:

* integração entre sistemas;
* autenticação OAuth;
* consumo de APIs REST;
* manipulação de dados;
* operações com SQLite;
* geração de arquivos JSON;
* desenvolvimento de interfaces web;
* organização de uma aplicação em diferentes módulos.

---

## Status do Projeto

**Em desenvolvimento.**

O projeto pode receber novas funcionalidades, melhorias na personalização das playlists, aprimoramentos na área administrativa e novas formas de interação com o usuário.

---

## Autoria

Projeto desenvolvido para fins **educacionais**, como projeto de automação em Python.
