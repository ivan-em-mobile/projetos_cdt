# 📅 Agenda Vocação

A **Agenda Vocação** é uma aplicação desktop desenvolvida em Python que permite o gerenciamento de compromissos (CRUD). O sistema conta com uma interface gráfica amigável feita em **Tkinter**, armazenamento local utilizando **SQLite3** e controle de permissões por nível de usuário.

---

## 🚀 Funcionalidades

* **Controle de Acesso (Login):** Tela de autenticação integrada com o banco de dados.
* **Gerenciamento de Compromissos (CRUD):** * **Criar:** Adiciona novos compromissos validando se os dias (1-31) e meses (1-12) são numéricos e válidos.
    * **Visualizar:** Tabela dinâmica (`Treeview`) que exibe todos os eventos agendados.
    * **Editar:** Clique em qualquer linha da tabela para carregar os dados nos campos e salvar as alterações.
    * **Deletar:** Remoção de compromissos com janela de confirmação de segurança.
* **Exportação de Dados:** Exporta todos os dados da agenda para um arquivo formato `.json` estruturado.

---

## 👥 Níveis de Permissão

O sistema diferencia as ações com base no tipo de usuário logado:

| Usuário | Senha | Permissões |
| :--- | :--- | :--- |
| `user` | `123` | Visualizar, Adicionar, Editar e Deletar compromissos. |
| `admin` | `123` | **Todas as permissões do usuário comum** + Exportar banco de dados para JSON. |

> ℹ️ **Nota:** Os usuários padrão acima são criados automaticamente na primeira inicialização do sistema caso o banco de dados ainda não exista.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Interface Gráfica:** `tkinter` e `ttk` (Componentes visuais e estilização de temas)
* **Banco de Dados:** `sqlite3` (Banco relacional local e leve)
* **Formatos de Arquivos:** `json` (Para exportação de relatórios)

---

## 📦 Pré-requisitos e Como Executar

O projeto utiliza apenas bibliotecas nativas do ecossistema Python, ou seja, **não é necessário instalar nenhuma dependência externa via `pip`**.

### Passo a Passo:

1. **Clone o repositório** ou baixe o arquivo com o código-fonte.
2. Certifique-se de ter o **Python 3** instalado em sua máquina.
3. Abra o terminal/prompt de comando na pasta do arquivo e execute:

```bash
python nome_do_seu_arquivo.py