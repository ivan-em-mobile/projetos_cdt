# Papéis do Projeto

## SmartFit Gym Manager

Este documento descreve os principais papéis considerados durante o desenvolvimento do projeto SmartFit Gym Manager.

Como o projeto é desenvolvido individualmente, uma mesma pessoa pode assumir diferentes responsabilidades durante as etapas de planejamento, desenvolvimento, validação e documentação.

---

## Product Owner - PO

O Product Owner é responsável pela definição das necessidades do sistema, organização das prioridades e acompanhamento do escopo do projeto.

### Responsabilidades

- Definir os objetivos do sistema.
- Identificar as funcionalidades necessárias.
- Organizar prioridades de desenvolvimento.
- Validar se as funcionalidades implementadas atendem aos requisitos.
- Controlar alterações de escopo.
- Acompanhar a evolução das versões do sistema.

---

## Quality Assurance - QA

O papel de QA é responsável pela validação do funcionamento da aplicação e identificação de problemas durante o desenvolvimento.

### Responsabilidades

- Testar funcionalidades implementadas.
- Validar entradas e saídas do sistema.
- Identificar comportamentos inesperados.
- Testar regras de negócio.
- Testar o banco de dados.
- Validar autenticação e permissões.
- Executar testes automatizados.
- Registrar e corrigir erros encontrados.

Durante o desenvolvimento foram realizados testes manuais progressivos pela interface CLI.

Também serão utilizados testes automatizados com Pytest.

---

## User Experience - UX

O papel de UX é responsável por organizar a interação entre o usuário e o sistema.

### Responsabilidades

- Organizar os menus da aplicação.
- Tornar mensagens e opções compreensíveis.
- Padronizar entradas de dados.
- Melhorar mensagens de sucesso e erro.
- Planejar a futura interface gráfica.
- Planejar a interface web para dispositivos móveis.

A aplicação será desenvolvida progressivamente através das seguintes interfaces:

1. CLI - interface pelo terminal.
2. GUI - interface gráfica com Tkinter.
3. Web - interface acessada através de navegador.

A versão web deverá considerar viewport de 320 x 800 pixels para utilização em dispositivos móveis.

---

## Tech Lead / Desenvolvedor

O papel de Tech Lead / Desenvolvedor concentra as responsabilidades técnicas relacionadas à arquitetura e implementação da aplicação.

### Responsabilidades

- Definir a arquitetura do sistema.
- Desenvolver os módulos Python.
- Criar models e services.
- Implementar o banco SQLite.
- Criar regras de negócio.
- Implementar autenticação.
- Desenvolver automações.
- Implementar exportação JSON.
- Integrar Faker.
- Criar relatórios.
- Implementar CLI, GUI e aplicação Web.
- Realizar integração entre os componentes.
- Gerenciar versionamento do sistema.

---

## Inteligência Artificial - IA

Ferramentas de Inteligência Artificial são utilizadas como apoio durante o desenvolvimento do projeto.

### Utilizações

- Apoio na organização da arquitetura.
- Explicação de conceitos de programação.
- Sugestão de estruturas de código.
- Revisão de código.
- Identificação de possíveis erros.
- Apoio na criação de testes.
- Apoio na elaboração da documentação.
- Apoio na evolução da interface do sistema.

As decisões, testes, validações e implementação do projeto permanecem sob responsabilidade do desenvolvedor.