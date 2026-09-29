# projetos_cdt
Repositório dedicado ao estudo e prática de Metodologias Ágeis. Este espaço visa compartilhar conhecimento sobre os frameworks mais populares (Scrum, Kanban, etc.), princípios de desenvolvimento ágil e ferramentas que promovem flexibilidade e eficiência. Sinta-se à vontade para explorar, aprender e contribuir!


# 💜 Power Up — Sistema de Treinos

O **Power Up** é uma aplicação web desenvolvida em **Python com Flask**, criada para auxiliar usuários na montagem de treinos personalizados e na consulta de informações sobre exercícios físicos.

O sistema possui autenticação de usuários, cadastro, banco de dados SQLite, geração automática de treinos, organização por grupos musculares e uma assistente virtual chamada **Wendy**.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3** — Linguagem principal do projeto
* **Flask** — Framework utilizado para desenvolvimento da aplicação web
* **SQLite3** — Banco de dados local
* **HTML5** — Estrutura das páginas
* **CSS3** — Estilização e responsividade
* **Jinja2** — Renderização dinâmica dos templates
* **Hash SHA-256** — Criptografia das senhas armazenadas
* **JSON** — Exportação dos dados dos usuários

---

## 🚀 Funcionalidades do Sistema

### 🔐 Sistema de Login

O sistema possui autenticação de usuários utilizando e-mail e senha.

As credenciais são verificadas diretamente no banco de dados e, após o login, uma sessão é criada para manter o usuário autenticado.

Também existe um acesso administrativo chamado **root**.

> **Usuário:** `root`
> **Senha:** `root`

O usuário root possui acesso a uma funcionalidade adicional para exportação dos usuários cadastrados.

---

### 📝 Cadastro de Usuários

Novos usuários podem criar uma conta informando:

* Nome
* E-mail
* Telefone
* CEP
* Data de nascimento
* Academia
* Senha
* Confirmação de senha

O sistema verifica se as duas senhas são iguais antes de realizar o cadastro.

O e-mail é utilizado como identificador do usuário e não pode ser cadastrado mais de uma vez.

---

### 🏠 Página Inicial

Após o login, o usuário é direcionado para a página principal do Power Up.

Nela são disponibilizadas as principais funcionalidades:

* 🏋️ Montagem de treino
* 💬 Assistente virtual Wendy
* ❓ Dúvidas sobre exercícios
* 🚪 Encerramento da sessão

Usuários administrativos também visualizam a área de exportação dos dados.

---

### 💬 Wendy — Assistente Virtual

A **Wendy** é a assistente virtual do Power Up.

Ela funciona como uma interface de auxílio ao usuário, oferecendo acesso rápido a:

* Montagem de treinos
* Informações sobre exercícios
* Retorno à página inicial

A aplicação também disponibiliza um botão flutuante da Wendy na página principal.

---

### ❓ Informações sobre Exercícios

O sistema permite consultar os exercícios cadastrados no banco de dados.

Para cada exercício são apresentados:

* Nome do exercício
* Músculos trabalhados
* Instruções de execução

As informações são carregadas dinamicamente da tabela `exercicios` do banco SQLite.

Os exercícios são organizados de acordo com seus respectivos grupos musculares.

---

## 🏋️ Montagem Automática de Treinos

Uma das principais funcionalidades do Power Up é a geração automática de uma sugestão de treino.

O usuário pode selecionar:

### 🎯 Objetivos

É possível escolher até **2 objetivos**:

* Ganhar massa muscular
* Melhorar condicionamento
* Fortalecer o corpo
* Melhorar resistência

---

### 💪 Grupos Musculares

É possível selecionar até **3 grupos musculares**:

* Glúteos
* Quadríceps
* Posteriores
* Panturrilhas
* Costas
* Peito
* Ombros
* Bíceps
* Tríceps
* Abdômen

---

### 📅 Dias da Semana

O usuário pode selecionar os dias em que deseja realizar os treinos:

* Segunda-feira
* Terça-feira
* Quarta-feira
* Quinta-feira
* Sexta-feira
* Sábado
* Domingo

---

### ⏱️ Tempo Disponível

O sistema oferece quatro opções de duração:

* 30 minutos
* 45 minutos
* 60 minutos
* 90 minutos

A quantidade de exercícios sugerida é calculada automaticamente de acordo com o tempo disponível.

| Tempo      | Exercícios sugeridos |
| ---------- | -------------------: |
| 30 minutos |                    3 |
| 45 minutos |                    4 |
| 60 minutos |                    6 |
| 90 minutos |                    8 |

Para usuários iniciantes, a quantidade é reduzida em um exercício, respeitando um mínimo de dois exercícios.

---

### 📈 Nível de Experiência

O usuário pode informar seu nível:

* Iniciante
* Intermediário
* Avançado

Essa informação influencia a quantidade de exercícios sugerida para o treino.

---

## 🔗 Relação entre Grupos Musculares

O sistema possui uma lógica para incluir grupos musculares relacionados ao grupo escolhido.

Por exemplo:

* Glúteos → Posteriores e Quadríceps
* Quadríceps → Glúteos e Posteriores
* Posteriores → Glúteos e Quadríceps
* Costas → Bíceps
* Peito → Tríceps
* Ombros → Tríceps
* Bíceps → Costas
* Tríceps → Peito
* Panturrilhas → Quadríceps

Essa lógica permite que o sistema encontre exercícios complementares para a montagem do treino.

---

## 📊 Resultado do Treino

Depois que o usuário envia suas preferências, o sistema gera uma rotina organizada por dia da semana.

Cada exercício apresenta:

* Nome
* Músculos trabalhados
* Instruções de execução

O resultado também apresenta um resumo contendo:

* Objetivos escolhidos
* Grupos musculares
* Tempo disponível
* Nível de experiência

Caso o usuário não escolha determinados campos, o sistema utiliza valores padrão.

---

## 🗄️ Banco de Dados

O sistema utiliza **SQLite3** para armazenamento local.

O banco é localizado automaticamente na mesma pasta do projeto:

```text
power_up.db
```

O caminho é definido através de:

```python
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "power_up.db")
```

---

## 👤 Tabela de Usuários

O sistema espera uma tabela chamada `usuarios` contendo informações como:

```text
id
nome
email
telefone
cep
data_nascimento
academia
senha
```

As senhas são armazenadas utilizando um hash SHA-256.

---

## 🏋️ Tabela de Exercícios

O sistema também utiliza uma tabela chamada `exercicios`.

Os campos utilizados pela aplicação são:

```text
id
nome
grupo_muscular
musculos
execucao
```

Os exercícios são carregados automaticamente do banco e agrupados pelo campo `grupo_muscular`.

---

## 👑 Área Administrativa

Usuários autenticados como `root` possuem acesso a uma função adicional:

### 📄 Exportação de usuários

A rota:

```text
/exportar-json
```

gera um arquivo JSON contendo os dados cadastrais dos usuários.

O arquivo é disponibilizado para download com o nome:

```text
usuarios_power_up.json
```

Por segurança dentro da lógica da aplicação, essa rota verifica se a sessão atual possui:

```python
session.get("root")
```

Somente o usuário administrativo consegue realizar a exportação.

---

## 📁 Estrutura do Projeto

Uma estrutura recomendada para o projeto é:

```text
📁 power_up/
│
├── 🐍 app.py
│
├── 🗃️ power_up.db
│
├── 📄 README.md
│
└── 📁 static/
    └── arquivos estáticos, caso sejam adicionados futuramente
```

O código atual utiliza `render_template_string()`, portanto os arquivos HTML estão definidos diretamente no arquivo Python.

---

## ▶️ Como Executar o Projeto

### 1. Instalar o Python

Certifique-se de possuir o **Python 3** instalado.

Verifique com:

```bash
python --version
```

ou:

```bash
python3 --version
```

---

### 2. Instalar o Flask

No terminal, execute:

```bash
pip install flask
```

---

### 3. Configurar o banco de dados

Coloque o arquivo:

```text
power_up.db
```

na mesma pasta do arquivo Python.

O banco deve possuir as tabelas necessárias, principalmente:

```text
usuarios
exercicios
```

---

### 4. Executar a aplicação

Execute:

```bash
python app.py
```

O servidor será iniciado na porta:

```text
5000
```

Como o código utiliza:

```python
app.run(
    host="0.0.0.0",
    port=5000,
    debug=True
)
```

a aplicação poderá ser acessada pelo navegador através do endereço local:

```text
http://localhost:5000
```

---

## 🔑 Acesso Administrativo

Para acessar a área administrativa integrada ao sistema:

```text
Usuário: root
Senha: root
```

Após o login, a página inicial exibirá a opção:

```text
📄 Exportar usuários em JSON
```

---

## 🔄 Fluxo Principal da Aplicação

O funcionamento básico do sistema segue o seguinte fluxo:

```text
                    ┌──────────────┐
                    │    LOGIN     │
                    └──────┬───────┘
                           │
             ┌─────────────┴─────────────┐
             │                           │
          Cadastro                   Usuário
             │                           │
             └─────────────┬─────────────┘
                           │
                    ┌──────▼───────┐
                    │     HOME     │
                    └──────┬───────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
            ▼              ▼              ▼
       Montar treino     Wendy       Exercícios
            │              │              │
            ▼              └──────┬───────┘
     Preferências                  │
            │                      │
            ▼                      ▼
     Geração do treino       Informações
            │
            ▼
      Resultado semanal
```

---

## 🔒 Sessões

O Flask utiliza sessões para controlar o usuário autenticado.

São armazenadas informações como:

```python
session["usuario_id"]
session["nome"]
session["email"]
session["root"]
```

Quando o usuário encerra a sessão através da opção **Sair**, todos os dados da sessão são removidos.

---

## 🛡️ Segurança

O projeto possui alguns mecanismos básicos de segurança:

* Senhas não são armazenadas em texto puro.
* Consultas SQL utilizam parâmetros, reduzindo o risco de SQL Injection.
* Rotas internas verificam se o usuário está autenticado.
* A exportação de usuários verifica a permissão administrativa.
* Os dados exportados não incluem a senha dos usuários.

### ⚠️ Recomendações para produção

Antes de utilizar o sistema em um ambiente real, recomenda-se:

* Alterar a `secret_key`.
* Não utilizar `root/root` como credencial administrativa.
* Utilizar variáveis de ambiente para informações sensíveis.
* Substituir SHA-256 simples por um algoritmo próprio para senhas, como `Werkzeug Password Hashing`.
* Desativar `debug=True`.
* Implementar proteção contra CSRF.
* Validar e sanitizar os dados recebidos dos formulários.
* Adicionar controle de permissões mais completo.
* Utilizar HTTPS em produção.

---

## ⚠️ Aviso sobre os Treinos

Os treinos gerados pelo sistema são **sugestões automáticas para fins educativos e demonstrativos**.

O sistema não substitui a avaliação ou orientação de um profissional de Educação Física.

Antes de iniciar uma rotina de exercícios, especialmente em caso de limitações físicas ou condições específicas, recomenda-se buscar orientação profissional.

---

## 🎨 Interface

A interface utiliza uma identidade visual baseada em tons de roxo, com:

* Cards arredondados
* Gradientes
* Botões personalizados
* Layout responsivo
* Interface adaptada para dispositivos menores
* Navegação simplificada

A identidade visual utiliza o conceito:

> **POWER UP 💜**

---

## 📌 Principais Rotas

| Rota                  | Método   | Função                    |
| --------------------- | -------- | ------------------------- |
| `/`                   | GET/POST | Login                     |
| `/cadastro`           | GET/POST | Cadastro de usuários      |
| `/home`               | GET      | Página inicial            |
| `/wendy`              | GET      | Assistente Wendy          |
| `/duvidas-exercicios` | GET      | Consulta de exercícios    |
| `/treino`             | GET/POST | Montagem de treino        |
| `/exportar-json`      | GET      | Exportação administrativa |
| `/sair`               | GET      | Encerramento da sessão    |

---

## 📚 Organização do Código

O arquivo principal está organizado em diferentes seções:

```text
1. Importação das bibliotecas
2. Configuração do Flask
3. Conexão com o banco de dados
4. Função de hash de senha
5. Carregamento dos exercícios
6. Grupos musculares relacionados
7. Estilos CSS
8. Templates HTML
9. Funções de geração de treino
10. Rotas de login
11. Cadastro
12. Página inicial
13. Wendy
14. Consulta de exercícios
15. Montagem de treino
16. Exportação JSON
17. Logout
18. Inicialização do servidor
```

---

## 🚧 Possíveis Melhorias Futuras

O projeto pode ser expandido com diversas funcionalidades, como:

* 📱 Aplicativo mobile
* 📊 Histórico de treinos
* ✅ Marcação de exercícios concluídos
* ⏱️ Cronômetro de exercícios
* 📈 Acompanhamento de evolução
* ⚖️ Registro de peso e medidas
* 🏆 Sistema de metas
* 🔔 Lembretes de treino
* 🖼️ Imagens demonstrativas dos exercícios
* 🎥 Vídeos de execução
* 🔎 Pesquisa de exercícios
* ✏️ Edição do perfil
* 🔑 Recuperação de senha
* 👑 Painel administrativo completo
* 📊 Dashboard com estatísticas
* 🗓️ Calendário de treinos
* 💾 Salvamento dos treinos personalizados no banco de dados

---

## 👩🏻‍💻 Projeto

**Power Up** é um sistema web desenvolvido em Python com Flask com o objetivo de oferecer uma experiência simples para cadastro de usuários, consulta de exercícios e geração automática de sugestões de treino.

---

## 💜 Power Up

**Monte seu treino. Conheça os exercícios. Evolua no seu ritmo.**