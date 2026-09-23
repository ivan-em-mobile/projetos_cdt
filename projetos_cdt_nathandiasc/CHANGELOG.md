# Changelog

Todas as alterações relevantes deste projeto serão documentadas neste arquivo.

O projeto utiliza versionamento semântico no formato:

```text
MAJOR.MINOR.PATCH
```

---

## [1.0.0] - 2026-09-22

### Adicionado

- Documentação final do projeto.
- Registro dos testes realizados com usuários.
- Arquivo `docs/testes_usuarios.md`.
- Registro da validação por instalação limpa através de novo `git clone`.
- Documentação da versão Web pública.
- Documentação do executável local.
- Documentação das limitações conhecidas do projeto.

### Validado

- Projeto clonado em uma nova pasta diretamente do GitHub.
- Dependências instaladas através do `requirements.txt`.
- CLI executada após clone limpo.
- GUI executada após clone limpo.
- aplicação Web executada após clone limpo.
- 38 testes automatizados executados com sucesso após clone limpo.
- versão Web pública validada no Render.
- QR Code público validado através de dispositivo móvel.
- executável Windows validado.
- persistência SQLite validada no executável.
- exportação JSON validada no executável.
- aplicação validada por usuários externos ao desenvolvimento.

### Alterado

- Projeto promovido de versão de desenvolvimento para primeira versão estável.
- README atualizado para refletir o estado final da aplicação.
- Roadmap atualizado com todas as etapas principais concluídas.
- Status do projeto atualizado para versão estável.

---

## [0.7.1] - 2026-09-22

### Corrigido

- Campo CPF passou a limitar a entrada a 11 dígitos.
- Adicionada máscara automática no formato `000.000.000-00`.
- CPF passou a ser padronizado antes do armazenamento.
- Cadastro passou a aceitar CPF com ou sem máscara.
- Busca de aluno por CPF passou a considerar CPF formatado ou não formatado.
- Validação de duplicidade passou a impedir cadastro do mesmo CPF com representações diferentes.
- Corrigido teste Web que ainda consultava o CPF no formato antigo.
- Corrigido fluxo Web que consultava um CPF diferente daquele cadastrado.

### Adicionado

- Validação centralizada de CPF no `aluno_service.py`.
- Máscara de CPF na interface Tkinter.
- Máscara de CPF na aplicação Web.
- Teste de CPF com menos de 11 dígitos.
- Teste de CPF com mais de 11 dígitos.
- Teste de CPF com caracteres inválidos.
- Teste de normalização do CPF.
- Teste de duplicidade entre CPF formatado e não formatado.

### Origem da melhoria

- A melhoria foi identificada durante teste realizado por usuário externo.
- O usuário observou que o campo CPF permitia quantidade arbitrária de caracteres.
- O feedback foi convertido em requisito e implementado nas diferentes camadas da aplicação.

### Testes

- Suíte automatizada ampliada de 35 para 38 testes.
- 38 testes automatizados executados com sucesso.
- Máscara validada manualmente na GUI.
- Máscara validada manualmente na Web.
- Versão publicada e validada no Render.

---

## [0.7.0] - 2026-09-22

### Adicionado

- Geração do executável Windows através de PyInstaller.
- Executável `SmartFitGymManager.exe`.
- Persistência do SQLite na execução através do executável.
- Exportação JSON através do executável.
- Compatibilidade de leitura do arquivo `VERSION` no ambiente PyInstaller.
- Suporte à localização de recursos através de `sys._MEIPASS`.
- Gunicorn como servidor WSGI para publicação Web.
- Publicação da aplicação Flask no Render.
- URL pública da aplicação.
- QR Code funcionando através da URL pública.
- acesso à aplicação Web por dispositivos fora da rede local.

### Alterado

- Caminhos de banco e exportação adaptados para execução normal e execução empacotada.
- `requirements.txt` atualizado para publicação com Gunicorn.
- Render configurado com diretório raiz específico do projeto dentro do repositório.
- aplicação passou a possuir uma versão local executável e uma versão Web pública.

### Validado

- executável abre corretamente através de duplo clique.
- persistência do banco validada após fechar e reabrir o executável.
- exportação JSON validada no executável.
- aplicação Web publicada com sucesso no Render.
- Dashboard público validado.
- QR Code público validado em dispositivo móvel.
- aplicação acessada através da Internet.

---

## [0.6.0] - 2026-09-21

### Adicionado

- Aplicação Web completa utilizando Flask.
- Dashboard Web integrado aos mesmos Services utilizados pela CLI e GUI.
- Cadastro e consulta de alunos pela Web.
- Cadastro e consulta de planos pela Web.
- Criação e consulta de assinaturas pela Web.
- Geração de cobranças pela Web.
- Registro de pagamentos pela Web.
- Histórico financeiro pela Web.
- Controle de acesso pela Web.
- Registro de acessos autorizados e negados.
- Relatórios administrativos pela Web.
- Relatório geral.
- Relatório financeiro.
- Relatório de acessos.
- Ranking de frequência.
- Relatório de planos.
- Exportação JSON pela Web.
- Autenticação administrativa para exportação JSON.
- Download do arquivo JSON pelo navegador.
- Interface responsiva para dispositivos móveis.
- Validação específica em resolução 320 x 800.
- Servidor Flask acessível pela rede local.
- Acesso à aplicação através de dispositivos móveis.
- Geração dinâmica de QR Code.
- Página Web dedicada ao QR Code.
- Identificação automática do endereço local para geração do QR Code.
- Testes automatizados da camada Web.
- Teste de integração do fluxo principal:
  aluno → plano → assinatura → cobrança → pagamento → acesso.
- Teste automatizado das principais rotas Web.
- Teste automatizado da geração do QR Code.
- Teste de cadastro de aluno pela Web.
- Teste de duplicidade de plano pela Web.

### Alterado

- Servidor Flask configurado para aceitar conexões pela rede local através de `0.0.0.0`.
- Interface mobile refinada para evitar vazamento horizontal de conteúdo.
- Menu lateral passa para menu superior em telas pequenas.
- Cards e formulários passam para uma coluna em dispositivos móveis.
- Tabelas utilizam rolagem horizontal própria em telas menores.
- Arquitetura passou a possuir três interfaces funcionais compartilhando a mesma camada de Services e o mesmo banco SQLite.

### Testes

- Suíte automatizada ampliada de 30 para 35 testes.
- 35 testes automatizados executados com sucesso.
- CLI validada após implementação da Web.
- GUI validada após implementação da Web.
- Aplicação Web validada em desktop.
- Aplicação Web validada em resolução 320 x 800.
- Aplicação Web validada em dispositivo móvel real.
- QR Code validado através de acesso pelo celular.

---

## [0.5.1] - 2026-09-21

### Corrigido

- Corrigida a validação de nomes duplicados no cadastro de planos.
- Nomes de planos agora são comparados ignorando diferenças entre letras maiúsculas e minúsculas.
- Espaços no início e no final dos nomes dos planos são desconsiderados na validação e na busca.
- Adicionada validação explícita de duplicidade no `plano_service.py`.
- Adicionado índice único normalizado no SQLite utilizando `LOWER(TRIM(nome))`.
- Corrigida a duplicidade identificada durante os testes da interface Web.

### Testes

- Adicionados testes de regressão para nomes de planos com diferenças de capitalização.
- Adicionado teste para busca de planos ignorando capitalização e espaços.
- Suíte automatizada ampliada de 28 para 30 testes.
- 30 testes automatizados executados com sucesso.

---

## [0.5.0] - 2026-09-21

### Adicionado

- Interface gráfica completa utilizando Tkinter.
- Dashboard gráfico conectado ao banco SQLite.
- Tela de gerenciamento de alunos.
- Tela de gerenciamento de planos.
- Tela de gerenciamento de assinaturas.
- Tela de gerenciamento de pagamentos.
- Tela de controle de acesso.
- Retorno visual para acessos autorizados e negados.
- Histórico de acessos na interface gráfica.
- Interface para cadastro e consulta de exercícios.
- Interface para criação de treinos.
- Interface para montagem e visualização de fichas de treino.
- Tela de relatórios.
- Relatório geral na GUI.
- Relatório financeiro na GUI.
- Relatório de acessos e ranking de frequência na GUI.
- Relatório de planos na GUI.
- Exportação JSON através da interface gráfica.
- Autenticação administrativa para exportação JSON na GUI.
- Máscara de senha na autenticação gráfica.

### Alterado

- Aplicação passou a possuir duas interfaces funcionais: CLI e GUI.
- GUI passou a reutilizar os mesmos Services utilizados pela CLI.
- Navegação gráfica organizada através de menu lateral.
- Fluxos de alunos, planos, assinaturas, pagamentos, acesso e treinos integrados ao mesmo banco SQLite.
- README atualizado para refletir a conclusão da interface gráfica.

### Testes

- Interface gráfica validada manualmente.
- CLI executada novamente após a implementação da GUI.
- Dependências do projeto validadas através do `requirements.txt`.
- Suíte automatizada executada após a implementação da GUI.
- 28 testes automatizados executados com sucesso.

---

## [0.4.0] - 2026-09-21

### Adicionado

- Exportação completa do banco SQLite para JSON.
- Diretório dedicado para arquivos exportados.
- Usuário administrativo `root master`.
- Autenticação para acesso à exportação JSON.
- Armazenamento da senha administrativa através de hash.
- Máscara visual de senha no terminal.
- Nova tabela `usuarios`.
- Model `Usuario`.
- Serviço de autenticação de usuários.
- Integração da biblioteca Faker.
- Geração automática de alunos fictícios.
- Geração automática de assinaturas fictícias.
- Geração automática de pagamentos fictícios.
- Geração automática de históricos de acesso fictícios.
- Relatório geral da academia.
- Relatório financeiro.
- Relatório de acessos.
- Ranking de frequência dos alunos.
- Relatório de planos.
- Submenu de relatórios na interface CLI.
- Documentação dos papéis de PO, QA, UX, Tech Lead/Dev e IA.
- Estrutura inicial de testes automatizados com Pytest.
- Banco SQLite temporário para execução isolada dos testes.

### Testes

- Teste automático da criação das tabelas.
- Testes de autenticação administrativa.
- Testes de cadastro e consulta de alunos.
- Testes de validação de CPF e e-mail duplicados.
- Testes de cadastro e consulta de planos.
- Teste de duplicidade de planos.
- Testes de geração de cobranças.
- Testes de registro de pagamentos.
- Testes de inadimplência.
- Testes de autorização de acesso.
- Testes de bloqueio de acesso por inadimplência.
- Teste de bloqueio para aluno sem assinatura.
- Testes de histórico de acesso.
- Testes dos relatórios geral, financeiro, acessos e planos.
- 28 testes automatizados executados com sucesso.

### Alterado

- Interface CLI ampliada com opções de Faker e relatórios.
- Exportação JSON passou a exigir autenticação administrativa.
- Relatório financeiro passou a atualizar automaticamente pagamentos vencidos antes da consulta.
- README ampliado com arquitetura, funcionalidades, instalação, autenticação, Faker, relatórios, interfaces planejadas e documentação.

---

## [0.3.0] - 2026-09-19

### Adicionado

- Serviço de gerenciamento de pagamentos.
- Geração de cobranças vinculadas às assinaturas.
- Registro de pagamentos e formas de pagamento.
- Atualização automática de pagamentos pendentes para atrasados.
- Verificação automática de inadimplência.
- Serviço de controle de acesso.
- Autorização automática de acesso para alunos regulares.
- Bloqueio automático de acesso em caso de inadimplência.
- Registro e histórico de acessos.
- Serviço de gerenciamento de exercícios.
- Cadastro e listagem de exercícios.
- Serviço de gerenciamento de treinos.
- Criação de fichas de treino.
- Associação de exercícios às fichas.
- Controle de séries, repetições, carga, descanso e ordem dos exercícios.
- Visualização completa da ficha de treino pela CLI.

### Validado

- Fluxo de pagamento pendente para pago.
- Detecção de pagamento atrasado.
- Acesso autorizado para aluno regular.
- Acesso negado por inadimplência.
- Persistência do histórico de acessos.
- Criação e consulta de fichas de treino.

---

## [0.2.0] - 2026-09-19

### Adicionado

- Primeira interface CLI funcional.
- Serviço de gerenciamento de alunos.
- Cadastro de alunos no banco SQLite.
- Listagem de alunos cadastrados.
- Busca de alunos por ID.
- Busca de alunos por CPF.
- Serviço de gerenciamento de planos.
- Cadastro e listagem de planos.
- Busca de planos por ID e nome.
- Serviço de gerenciamento de assinaturas.
- Associação entre aluno e plano.
- Listagem de assinaturas.
- Verificação de assinatura ativa por aluno.
- Menu interativo pelo terminal.
- Entrada de dados pelo usuário.

### Corrigido

- Entrada de data de nascimento adaptada para o formato brasileiro DD/MM/AAAA.
- Validação para impedir duplicidade de CPF e e-mail no cadastro de alunos.
- Validação para impedir duplicidade de nomes de planos.
- Verificação para evitar múltiplas assinaturas ativas para o mesmo aluno.

---

## [0.1.0] - 2026-09-19

### Adicionado

- Estrutura inicial do projeto.
- Organização dos módulos CLI, GUI e Web.
- Estrutura para banco de dados.
- Models de Aluno, Plano, Assinatura, Pagamento, Acesso, Treino e Exercício.
- Banco de dados SQLite.
- Criação automática das tabelas.
- Tabela de relacionamento entre treinos e exercícios.
- Diretório para exportação de dados em JSON.
- Diretório para documentação.
- Diretório para testes.
- Arquivo de versionamento.
- Arquivos iniciais de configuração do projeto.