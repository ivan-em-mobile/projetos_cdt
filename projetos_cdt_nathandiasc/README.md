# SmartFit Gym Manager

Sistema de gerenciamento de academia desenvolvido em Python como projeto final de programação.

**Versão atual: `0.4.0`**

> Projeto acadêmico independente, sem vínculo oficial com a Smart Fit.

---

## Sobre o projeto

O **SmartFit Gym Manager** é uma aplicação desenvolvida para automatizar processos comuns de gerenciamento de uma academia.

O sistema reúne funcionalidades relacionadas a alunos, planos, assinaturas, pagamentos, inadimplência, controle de acesso, exercícios, fichas de treino, relatórios e exportação de dados.

A arquitetura foi organizada para permitir o reaproveitamento das mesmas regras de negócio em diferentes interfaces:

```text
                 CLI
                  │
                  │
GUI ───────── Services ───────── Web
                  │
                  ↓
               SQLite
```

Dessa forma, CLI, GUI e futuramente a aplicação Web utilizam os mesmos serviços e o mesmo banco de dados.

---

## Objetivos

O projeto tem como objetivo desenvolver uma aplicação capaz de:

- cadastrar e consultar alunos;
- cadastrar e consultar planos;
- criar assinaturas;
- gerar cobranças;
- registrar pagamentos;
- identificar automaticamente inadimplência;
- autorizar ou negar acesso à academia;
- armazenar histórico de acessos;
- cadastrar exercícios;
- criar fichas de treino;
- associar exercícios aos treinos;
- gerar dados fictícios com Faker;
- gerar relatórios administrativos;
- exportar o banco de dados para JSON;
- proteger a exportação através de autenticação administrativa;
- disponibilizar interfaces CLI, GUI e Web;
- gerar uma versão executável da aplicação;
- disponibilizar acesso Web através de QR Code.

---

# Tecnologias

## Implementadas

- Python
- SQLite
- JSON
- Faker
- Tkinter
- Pytest

## Planejadas para as próximas etapas

- Flask
- HTML
- CSS
- QR Code
- PyInstaller
- Render

---

# Arquitetura

O projeto utiliza uma organização modular para separar responsabilidades.

```text
Interface
   │
   ↓
Services
   │
   ↓
Models
   │
   ↓
SQLite
```

## Models

Representam as principais entidades do sistema:

- Aluno
- Plano
- Assinatura
- Pagamento
- Acesso
- Exercício
- Treino
- Usuário

## Services

Contêm as regras de negócio da aplicação.

Entre suas responsabilidades estão:

- gerenciamento de alunos;
- gerenciamento de planos;
- gerenciamento de assinaturas;
- gerenciamento de pagamentos;
- controle de inadimplência;
- controle de acesso;
- gerenciamento de exercícios;
- gerenciamento de treinos;
- geração de relatórios;
- geração de dados fictícios;
- autenticação administrativa;
- exportação JSON.

## Database

Responsável pela conexão e pela criação das tabelas do banco SQLite.

## Interfaces

O projeto foi planejado para possuir três formas principais de interação:

1. **CLI** — interface por terminal;
2. **GUI** — interface gráfica com Tkinter;
3. **Web** — aplicação Web com Flask.

---

# Estrutura do projeto

```text
smartfit-gym-manager/
│
├── app/
│   ├── __init__.py
│   │
│   ├── cli/
│   │   ├── __init__.py
│   │   └── menu.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   └── schema.py
│   │
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── janela_principal.py
│   │   ├── tela_acesso.py
│   │   ├── tela_alunos.py
│   │   ├── tela_assinaturas.py
│   │   ├── tela_pagamentos.py
│   │   ├── tela_planos.py
│   │   └── tela_treinos.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── acesso.py
│   │   ├── aluno.py
│   │   ├── assinatura.py
│   │   ├── exercicio.py
│   │   ├── pagamento.py
│   │   ├── plano.py
│   │   ├── treino.py
│   │   └── usuario.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── acesso_service.py
│   │   ├── aluno_service.py
│   │   ├── assinatura_service.py
│   │   ├── exercicio_service.py
│   │   ├── export_service.py
│   │   ├── faker_service.py
│   │   ├── pagamento_service.py
│   │   ├── plano_service.py
│   │   ├── relatorio_service.py
│   │   ├── treino_service.py
│   │   └── usuario_service.py
│   │
│   └── web/
│       └── __init__.py
│
├── data/
│   ├── academia.db
│   └── exports/
│
├── docs/
│   ├── papeis_projeto.md
│   └── requisitos.md
│
├── tests/
│   ├── conftest.py
│   ├── test_acesso_service.py
│   ├── test_aluno_service.py
│   ├── test_database.py
│   ├── test_pagamento_service.py
│   ├── test_plano_service.py
│   ├── test_relatorio_service.py
│   └── test_usuario_service.py
│
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── main.py
├── README.md
├── requirements.txt
└── VERSION
```

---

# Banco de dados

O sistema utiliza **SQLite** como banco de dados local.

Arquivo principal:

```text
data/academia.db
```

O banco é criado automaticamente durante a inicialização da aplicação.

## Tabelas

Atualmente existem nove tabelas principais:

```text
alunos
planos
assinaturas
pagamentos
acessos
treinos
exercicios
treino_exercicios
usuarios
```

---

# Funcionalidades

## Alunos

O sistema permite:

- cadastrar alunos;
- listar alunos;
- buscar aluno por ID;
- buscar aluno por CPF;
- controlar status;
- impedir CPF duplicado;
- impedir e-mail duplicado.

---

## Planos

É possível:

- cadastrar planos;
- listar planos;
- buscar plano por ID;
- buscar plano por nome;
- controlar status;
- impedir nomes duplicados.

---

## Assinaturas

O sistema permite:

- associar alunos a planos;
- listar assinaturas;
- consultar assinatura ativa;
- impedir múltiplas assinaturas ativas para o mesmo aluno.

---

## Pagamentos

O módulo financeiro permite:

- gerar cobranças;
- definir vencimentos;
- registrar pagamentos;
- registrar forma de pagamento;
- listar pagamentos;
- identificar pagamentos pendentes;
- identificar pagamentos atrasados;
- atualizar automaticamente cobranças vencidas;
- identificar inadimplência.

---

# Controle de acesso

O acesso de um aluno é avaliado automaticamente.

```text
Aluno tenta acessar
        │
        ↓
Aluno existe?
        │
        ↓
Aluno está ativo?
        │
        ↓
Possui assinatura ativa?
        │
        ↓
Possui pagamento atrasado?
        │
        ↓
AUTORIZADO / NEGADO
        │
        ↓
Registro no histórico
```

Exemplo de acesso autorizado:

```text
ACESSO AUTORIZADO
```

Exemplo de bloqueio:

```text
ACESSO NEGADO
Motivo: Pagamento em atraso.
```

Todas as tentativas são registradas no banco.

---

# Exercícios e treinos

O sistema possui gerenciamento de exercícios e fichas de treino.

É possível:

- cadastrar exercícios;
- informar grupo muscular;
- adicionar descrição;
- criar treino para um aluno;
- informar objetivo do treino;
- associar exercícios;
- definir séries;
- definir repetições;
- definir carga;
- definir tempo de descanso;
- definir ordem dos exercícios;
- visualizar a ficha completa.

Exemplo:

```text
Treino A
Objetivo: Hipertrofia

1 - Supino Reto
Grupo: Peitoral
Séries: 4
Repetições: 8-12
Carga: 50 kg
Descanso: 90 segundos
```

---

# Relatórios

O sistema possui quatro tipos principais de relatório.

## Relatório geral

Apresenta:

- total de alunos;
- alunos ativos;
- assinaturas ativas;
- planos ativos.

## Relatório financeiro

Apresenta:

- total recebido;
- total pendente;
- total em atraso;
- quantidade de pagamentos realizados;
- quantidade de pagamentos pendentes;
- quantidade de pagamentos atrasados.

Antes da consulta, pagamentos vencidos são atualizados automaticamente.

## Relatório de acessos

Apresenta:

- total de acessos;
- acessos autorizados;
- acessos negados;
- ranking de frequência dos alunos.

## Relatório de planos

Apresenta:

- plano;
- valor;
- quantidade de assinaturas ativas.

---

# Faker

O projeto utiliza a biblioteca **Faker** para geração automática de dados fictícios.

Podem ser criados automaticamente:

- alunos;
- assinaturas;
- pagamentos;
- acessos.

Exemplo na CLI:

```text
19 - Gerar dados fictícios com Faker
```

Esses registros são gravados no mesmo banco SQLite utilizado pela aplicação.

---

# Exportação JSON

O banco de dados pode ser exportado para arquivos JSON.

Os arquivos são armazenados em:

```text
data/exports/
```

O nome do arquivo utiliza data e horário da exportação:

```text
academia_YYYYMMDD_HHMMSS.json
```

A exportação contém os registros das principais tabelas do sistema.

---

# Usuário administrador

A exportação JSON é uma funcionalidade protegida por autenticação.

Credenciais definidas para o projeto:

```text
Usuário: root master
Senha: root
```

A senha não é armazenada diretamente em texto puro no banco.

O sistema armazena seu hash e realiza a comparação durante a autenticação.

Na CLI, a senha é exibida de forma mascarada:

```text
Usuário: root master
Senha: ****
```

> As credenciais acima existem para fins acadêmicos e de demonstração. Em uma aplicação real, credenciais padrão não devem ser publicadas e o armazenamento de senhas deve utilizar mecanismos próprios para password hashing.

---

# Interface CLI

A CLI representa a primeira versão funcional da aplicação.

## Executar

Na raiz do projeto:

```bash
py main.py
```

## Menu

```text
1  - Cadastrar aluno
2  - Listar alunos

3  - Cadastrar plano
4  - Listar planos

5  - Criar assinatura
6  - Listar assinaturas

7  - Gerar cobrança
8  - Listar pagamentos
9  - Registrar pagamento

10 - Registrar acesso
11 - Histórico de acessos

12 - Cadastrar exercício
13 - Listar exercícios

14 - Criar treino
15 - Listar treinos de um aluno
16 - Adicionar exercício ao treino
17 - Visualizar ficha de treino

18 - Exportar banco para JSON
19 - Gerar dados fictícios com Faker
20 - Relatórios

0  - Sair
```

---

# Interface GUI

A segunda interface utiliza **Tkinter**.

## Executar

```bash
py -m app.gui.janela_principal
```

A GUI utiliza os mesmos `services` e o mesmo banco SQLite da CLI.

```text
CLI ──┐
      │
      ├──── Services ──── SQLite
      │
GUI ──┘
```

Isso significa que um aluno cadastrado pela GUI também aparece na CLI e vice-versa.

## Dashboard

O Dashboard exibe indicadores como:

- total de alunos;
- assinaturas ativas;
- total recebido;
- quantidade de acessos;
- alunos ativos;
- planos ativos;
- pagamentos pendentes;
- pagamentos atrasados;
- acessos autorizados;
- acessos negados.

## Módulos da GUI

Atualmente estão sendo construídos os seguintes módulos:

```text
Dashboard
Alunos
Planos
Assinaturas
Pagamentos
Controle de Acesso
Treinos
Relatórios
Exportação JSON
```

Já foram implementadas as bases gráficas para:

- Dashboard;
- Alunos;
- Planos;
- Assinaturas;
- Pagamentos;
- Controle de Acesso;
- Treinos.

Ainda serão concluídas:

- tela de Relatórios;
- exportação JSON com autenticação pela GUI;
- revisão e teste completo da interface.

---

# Interface Web

A versão Web será desenvolvida utilizando **Flask**.

Ela deverá reaproveitar os mesmos `services` utilizados pela CLI e pela GUI.

Arquitetura planejada:

```text
                 CLI
                  │
                  │
GUI ───────── Services ───────── WEB
                  │
                  ↓
               SQLite
```

A aplicação Web deverá disponibilizar funcionalidades como:

- Dashboard;
- alunos;
- planos;
- assinaturas;
- pagamentos;
- controle de acesso;
- relatórios;
- exportação de dados.

---

# Interface mobile

A versão Web será desenvolvida de forma responsiva.

Uma das dimensões de referência para teste será:

```text
320 x 800 px
```

A aplicação deverá funcionar adequadamente em dispositivos móveis.

---

# QR Code

Após a implementação do servidor Web será gerado um QR Code apontando para o endereço da aplicação.

Fluxo esperado:

```text
Servidor Web
     │
     ↓
URL da aplicação
     │
     ↓
QR Code
     │
     ↓
Celular
```

---

# Instalação

## 1. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
```

## 2. Entrar na pasta

```bash
cd smartfit-gym-manager
```

## 3. Instalar as dependências

```bash
py -m pip install -r requirements.txt
```

## 4. Executar a CLI

```bash
py main.py
```

## 5. Executar a GUI

```bash
py -m app.gui.janela_principal
```

---

# Dependências

O arquivo:

```text
requirements.txt
```

contém as dependências externas utilizadas ou previstas pelo projeto.

Exemplo:

```text
Flask
Faker
qrcode[pil]
pytest
pyinstaller
```

Algumas bibliotecas utilizadas fazem parte da biblioteca padrão do Python e não precisam ser instaladas via `pip`, como:

```text
sqlite3
json
hashlib
datetime
pathlib
```

---

# Testes automatizados

O sistema utiliza **Pytest** para validar suas principais regras de negócio.

## Executar os testes

```bash
py -m pytest -v
```

Os testes utilizam um banco SQLite temporário para evitar alterações no banco principal.

## Cobertura atual

São testados cenários relacionados a:

- criação das tabelas;
- criação do usuário administrativo;
- autenticação correta;
- autenticação inválida;
- cadastro de alunos;
- busca de alunos;
- CPF duplicado;
- e-mail duplicado;
- cadastro de planos;
- busca de planos;
- plano duplicado;
- geração de cobranças;
- registro de pagamentos;
- atualização automática de cobranças atrasadas;
- identificação de inadimplência;
- autorização de acesso;
- bloqueio por inadimplência;
- bloqueio para aluno sem assinatura;
- histórico de acessos;
- relatório geral;
- relatório financeiro;
- relatório de acessos;
- relatório de planos.

Resultado validado:

```text
28 passed
```

---

# Versionamento

O projeto utiliza **Versionamento Semântico**:

```text
MAJOR.MINOR.PATCH
```

Exemplo:

```text
0.4.0
```

## PATCH

Utilizado para correções de bugs.

```text
0.4.0 → 0.4.1
```

## MINOR

Utilizado quando novas funcionalidades compatíveis são adicionadas.

```text
0.4.0 → 0.5.0
```

## MAJOR

Utilizado para mudanças estruturais importantes ou lançamento de uma versão estável.

```text
0.9.0 → 1.0.0
```

A versão atual também está registrada no arquivo:

```text
VERSION
```

O histórico de alterações fica disponível em:

```text
CHANGELOG.md
```

---

# Versão atual

```text
0.4.0
```

A versão `0.4.0` consolidou funcionalidades como:

- CLI funcional;
- SQLite;
- autenticação;
- exportação JSON;
- Faker;
- relatórios;
- documentação;
- testes automatizados.

A GUI está sendo desenvolvida sobre essa base.

Quando o fluxo principal da interface gráfica estiver concluído e validado, a próxima versão planejada será:

```text
0.5.0
```

---

# Papéis do projeto

Durante o desenvolvimento foram considerados os seguintes papéis:

```text
PO - Product Owner
QA - Quality Assurance
UX - User Experience
Tech Lead / Desenvolvedor
IA - Inteligência Artificial
```

Como o projeto é acadêmico e individual, uma mesma pessoa pode assumir diferentes responsabilidades durante o desenvolvimento.

A Inteligência Artificial é utilizada como ferramenta de apoio para:

- planejamento;
- arquitetura;
- explicação de conceitos;
- desenvolvimento;
- revisão de código;
- identificação de possíveis erros;
- criação de testes;
- documentação.

Mais detalhes estão disponíveis em:

```text
docs/papeis_projeto.md
```

---

# Documentação

A documentação complementar está localizada em:

```text
docs/
```

Arquivos atuais:

```text
requisitos.md
papeis_projeto.md
```

---

# Executável

Está prevista a criação de uma versão executável utilizando **PyInstaller**.

Objetivo:

```text
SmartFitGymManager.exe
```

A versão executável deverá permitir abrir a aplicação gráfica diretamente, sem necessidade de executar comandos manualmente no terminal.

---

# Publicação Web

A aplicação Web será posteriormente publicada em um serviço compatível com aplicações Python/Flask.

A opção planejada é o **Render**.

Após a publicação, o projeto deverá possuir:

```text
URL pública
      │
      ↓
Aplicação Flask
      │
      ↓
QR Code
      │
      ↓
Acesso pelo celular
```

---

# Roadmap

## Concluído

- [x] Estrutura modular
- [x] Banco SQLite
- [x] Models
- [x] Services
- [x] CLI
- [x] Cadastro de alunos
- [x] Planos
- [x] Assinaturas
- [x] Pagamentos
- [x] Inadimplência
- [x] Controle de acesso
- [x] Exercícios
- [x] Treinos
- [x] Faker
- [x] Relatórios
- [x] Exportação JSON
- [x] Usuário `root master`
- [x] Autenticação
- [x] Documentação
- [x] Pytest
- [x] 28 testes automatizados aprovados
- [x] Estrutura inicial da GUI
- [x] Dashboard Tkinter
- [x] GUI de alunos
- [x] GUI de planos
- [x] GUI de assinaturas
- [x] GUI de pagamentos
- [x] GUI de controle de acesso
- [x] GUI de treinos

## Próximas etapas

- [ ] Relatórios na GUI
- [ ] Exportação JSON pela GUI
- [ ] Teste completo da GUI
- [ ] Versão `0.5.0`
- [ ] Aplicação Web com Flask
- [ ] Interface responsiva para `320 x 800`
- [ ] QR Code
- [ ] Publicação Web
- [ ] Executável com PyInstaller
- [ ] Testes com outros usuários
- [ ] Teste do projeto após `git clone`
- [ ] Revisão final do GitHub
- [ ] Documentação final
- [ ] Versão estável `1.0.0`
- [ ] Pitch final

---

# Status do projeto

| Componente | Status |
|---|---|
| Arquitetura | Concluído |
| SQLite | Concluído |
| Regras de negócio | Concluído |
| CLI | Concluído |
| JSON | Concluído |
| Faker | Concluído |
| Relatórios | Concluído |
| Autenticação | Concluído |
| Testes | 28 aprovados |
| GUI | Em desenvolvimento |
| Web | Não iniciada |
| Mobile | Não iniciado |
| QR Code | Não iniciado |
| Executável | Não iniciado |
| Deploy | Não iniciado |
| Versão estável | Não concluída |

---

# Licença

As condições de utilização do projeto estão disponíveis no arquivo:

```text
LICENSE
```

---

## Autor

Projeto desenvolvido como trabalho final de programação.
