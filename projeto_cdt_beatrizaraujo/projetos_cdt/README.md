Automatização de Tarefas 📌

Este é um aplicativo desktop para gerenciamento e organização de
tarefas, desenvolvido em Python utilizando a biblioteca gráfica
Tkinter. O sistema transforma solicitações escritas em linguagem
natural em tarefas organizadas, identificando automaticamente
informações como responsável, prazo, prioridade e categoria.

O projeto utiliza SQLite para persistência local dos dados, JSON
para importação e exportação das tarefas e Faker para geração
automática de dados de teste.

────────

🛠️ Tecnologias Utilizadas

• Python 3 — linguagem principal do projeto
• Tkinter — construção da interface gráfica desktop
• ttk — componentes visuais adicionais, como a tabela de tarefas
• SQLite3 — banco de dados local para armazenamento das tarefas
• JSON — importação e exportação de dados
• Faker — geração automática de tarefas fictícias para testes
• re (Regex) — identificação de informações dentro das
solicitações
• datetime / date / timedelta — tratamento e cálculo de datas

────────

🚀 Funcionalidades do Sistema

📝 Criação de tarefas por linguagem natural

O usuário pode escrever uma solicitação normalmente, sem precisar
preencher vários campos manualmente.

Exemplo:

> “O Ivan precisa preparar o relatório para o cliente até sexta. É
> urgente.”

O sistema interpreta a frase e transforma automaticamente a solicitação
em uma tarefa estruturada.

🤖 Identificação automática de informações

Durante a interpretação da solicitação, o sistema tenta identificar:

• Responsável
• Prazo
• Prioridade
• Categoria
• Título
• Data de criação
• Status inicial

Caso alguma informação não seja encontrada, o sistema utiliza valores
padrão como “Não definido”.

👤 Identificação do responsável

O sistema utiliza expressões regulares (Regex) para reconhecer
diferentes formas de indicar quem deverá realizar uma tarefa.

Exemplos de padrões reconhecidos:

• “responsável é João”
• “João precisa fazer…”
• “tarefa para João”
• “preciso que João faça…”
• “é para João”

📅 Identificação de prazos

O sistema reconhece diferentes formatos de prazo, incluindo:

• hoje
• amanhã
• 25/09/2026
• 25-09-2026
• 25/09
• até dia 25
• dias da semana, como segunda, terça, sexta
• datas escritas, como 10 de outubro

O sistema calcula a data correspondente utilizando a data atual do
computador.

🚦 Classificação automática de prioridade

A prioridade é definida com base em palavras encontradas na solicitação.

ALTA - urgente - urgência - imediato - imediatamente - agora -
crítico - pra ontem - o quanto antes

MÉDIA - importante - prioridade - atenção

Quando nenhuma dessas palavras é encontrada, a tarefa recebe prioridade
BAIXA.

🗂️ Classificação automática por categoria

O sistema identifica categorias com base no conteúdo da solicitação:

• DOCUMENTOS
• REUNIÃO
• CLIENTE / VENDAS
• FINANCEIRO
• TECNOLOGIA
• GERAL

📊 Dashboard / Visão geral

A tela inicial apresenta um resumo das tarefas cadastradas, contendo:

• Total de tarefas
• Tarefas pendentes
• Tarefas concluídas
• Tarefas de alta prioridade

Também exibe as tarefas mais recentes e permite criar uma nova
solicitação diretamente pelo dashboard.

📋 Gerenciamento de tarefas

Na seção Minhas tarefas, é possível:

• Visualizar todas as tarefas cadastradas
• Pesquisar tarefas
• Consultar responsável
• Consultar prazo
• Consultar prioridade
• Consultar categoria
• Consultar status
• Consultar data de criação
• Marcar uma tarefa como concluída
• Excluir uma tarefa

🔎 Pesquisa de tarefas

A tabela possui um campo de busca que filtra as tarefas em tempo real
conforme o usuário digita.

A pesquisa considera os dados presentes na tarefa, permitindo localizar
registros por diferentes informações.

✅ Conclusão de tarefas

Uma tarefa selecionada pode ser marcada como:

CONCLUÍDA

O status é atualizado diretamente no banco de dados SQLite.

🗑️ Exclusão de tarefas

O usuário pode excluir uma tarefa selecionada. Antes da exclusão, o
sistema apresenta uma confirmação para evitar remoções acidentais.

📤 Exportação para JSON

As tarefas cadastradas podem ser exportadas para um arquivo:

tarefas.json

O arquivo contém informações como:

• ID
• Título
• Responsável
• Prazo
• Prioridade
• Categoria
• Status
• Data de criação

📥 Importação de JSON

O sistema permite selecionar um arquivo .json e importar as tarefas
novamente para o banco de dados.

A importação também possui valores padrão para campos ausentes no
arquivo.

🧪 Geração de dados com Faker

A seção Dados & automação possui uma função para gerar
automaticamente 5 tarefas de teste.

Os nomes dos responsáveis são criados utilizando o Faker configurado
para português do Brasil:

Faker("pt_BR")

As datas também são geradas automaticamente dentro de um período de até
30 dias.

────────

🗃️ Banco de Dados

O sistema utiliza um banco de dados SQLite chamado:

tarefas.db

A tabela principal utilizada pelo aplicativo é:

tarefas

Estrutura da tabela

Campo              Tipo      Descrição

────────

id               INTEGER   Identificador único da tarefa
texto_original   TEXT      Solicitação original digitada pelo usuário
titulo           TEXT      Título gerado para a tarefa
responsavel      TEXT      Pessoa responsável pela tarefa
prazo            TEXT      Prazo identificado
prioridade       TEXT      Prioridade da tarefa
categoria        TEXT      Categoria identificada
status           TEXT      Status atual da tarefa
criada_em        TEXT      Data e hora de criação

O campo id é configurado como chave primária com incremento
automático.

────────

🧠 Fluxo de funcionamento

O funcionamento principal do sistema segue este fluxo:

```text
┌───────────────────────────────┐
│ Usuário escreve uma solicitação│
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│        interpretar()          │
└───────────────┬───────────────┘
                ↓
      ┌─────────┼─────────┐
      ↓         ↓         ↓
 Responsável  Prazo   Prioridade
      │         │         │
      └─────────┼─────────┘
                ↓
          Categoria
                ↓
┌───────────────────────────────┐
│     Tarefa estruturada        │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│      Banco SQLite             │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│ Dashboard / Tabela / JSON     │
└───────────────────────────────┘
```

────────

📂 Estrutura Completa de Caminhos e Arquivos

A estrutura principal do projeto pode ser organizada da seguinte forma:

```text
📁 caixa-de-entrada-acao/
│
├── 🐍 tarefas.py
│   └── Código-fonte principal do sistema
│
├── 🗃️ tarefas.db
│   └── Banco de dados SQLite criado automaticamente pelo programa
│
└── 📄 README.md
    └── Documentação do projeto
```

Estrutura após execução

Ao executar o programa pela primeira vez, o arquivo do banco de dados é
criado automaticamente:

```text
📁 projeto/
│
├── 🐍 tarefas.py
├── 🗃️ tarefas.db
└── 📄 README.md
```

O banco não precisa ser criado manualmente, pois a função
criar_banco() verifica se a tabela existe e cria a estrutura
necessária.

────────

▶️ Como Executar

1. Instale o Python

É necessário possuir o Python 3 instalado no computador.

2. Instale a dependência externa

O projeto utiliza a biblioteca Faker.

No terminal:

```bash
pip install Faker
```

O Tkinter e o SQLite3 fazem parte da distribuição padrão do Python em
instalações comuns.

3. Execute o programa

No terminal, dentro da pasta do projeto:

```bash
python tarefas.py
```

A janela do sistema será aberta automaticamente.

────────

💾 Persistência dos Dados

Os dados ficam armazenados localmente no arquivo:

```text
tarefas.db
```

Isso significa que as tarefas continuam disponíveis depois que o
aplicativo é fechado e aberto novamente.

O SQLite é utilizado diretamente pelo Python através do módulo:

```python
import sqlite3
```

────────

📦 Importação e Exportação

O sistema utiliza dois formatos principais de armazenamento:

SQLite

Responsável pelo armazenamento permanente das tarefas durante o uso
normal do aplicativo.

JSON

Responsável pela transferência e backup das tarefas.

Exemplo de estrutura exportada:

```json
[
    {
        "id": 1,
        "titulo": "enviar a proposta ao cliente até sexta",
        "responsavel": "Beatriz",
        "prazo": "25/09/2026",
        "prioridade": "ALTA",
        "categoria": "CLIENTE / VENDAS",
        "status": "PENDENTE",
        "criada_em": "21/09/2026 10:30"
    }
]
```

────────

🎨 Interface

A interface foi desenvolvida com uma proposta visual de sistema
administrativo moderno, utilizando:

• Sidebar lateral
• Dashboard
• Cards de estatísticas
• Tabela de tarefas
• Janelas de confirmação
• Botões de ação
• Campo de pesquisa
• Paleta em vinho, creme, branco e dourado
• Tipografia com diferentes níveis de hierarquia visual

A aplicação possui as seguintes áreas principais:

```text
┌──────────────────────┬────────────────────────────────────┐
│                      │                                    │
│  CAIXA DE ENTRADA    │           VISÃO GERAL              │
│       AÇÃO           │                                    │
│                      │   Tarefas  Pendentes  Concluídas   │
│  ⌂ Visão geral       │                                    │
│  ＋ Nova solicitação │   ┌──────────┐  ┌──────────────┐   │
│  ☷ Minhas tarefas   │   │ Solicitação │ │ Atividade   │  │
│  ⇅ Dados             │   │            │ │ recente     │  │
│                      │   └──────────┘  └──────────────┘  │
│  Automação inteligente│                                  │
│                      │                                    │
└──────────────────────┴────────────────────────────────────┘
```

────────

🧩 Principais Funções do Código

Função                        Responsabilidade

────────

conectar()                  Abre conexão com o banco SQLite
criar_banco()               Cria a tabela de tarefas
identificar_responsavel()   Localiza o responsável na frase
identificar_prazo()         Identifica e calcula o prazo
identificar_prioridade()    Define a prioridade
identificar_categoria()     Define a categoria
criar_titulo()              Cria o título da tarefa
interpretar()               Reúne todas as informações da solicitação
inserir()                   Salva uma tarefa no banco
buscar()                    Recupera as tarefas cadastradas
estatisticas()              Calcula os indicadores do dashboard
exportar()                  Exporta tarefas para JSON
importar()                  Importa tarefas de JSON
gerar_faker()               Cria tarefas fictícias para teste
concluir()                  Marca uma tarefa como concluída
excluir()                   Remove uma tarefa
atualizar_tabela()          Atualiza a tabela exibida na interface
atualizar_tudo()            Atualiza as informações da aplicação

────────

🏗️ Arquitetura Simplificada

O projeto está dividido conceitualmente em três partes principais:

```text
┌──────────────────────────────────┐
│          INTERFACE               │
│              Tkinter             │
├──────────────────────────────────┤
│       LÓGICA DE AUTOMAÇÃO        │
│ Regex • Datas • Classificação    │
├──────────────────────────────────┤
│        PERSISTÊNCIA              │
│       SQLite • JSON              │
└──────────────────────────────────┘
```

O Faker atua como ferramenta auxiliar para geração de dados
fictícios durante os testes.

────────

📌 Observações

• O banco de dados é criado automaticamente na primeira execução.
• O sistema funciona localmente, sem necessidade de servidor.
• A interpretação das solicitações é baseada em regras e expressões
regulares.
• O sistema não utiliza uma API de inteligência artificial externa
para interpretar as frases.
• O recurso Faker é destinado principalmente à geração de dados de
teste.
• O arquivo tarefas.db deve permanecer na pasta do programa para que
os dados existentes continuem disponíveis.

────────

👩‍💻 Projeto

Automatização de Tarefas

Aplicação desktop desenvolvida em Python + Tkinter, com persistência
em SQLite, manipulação de dados em JSON e geração de dados de
teste com Faker.