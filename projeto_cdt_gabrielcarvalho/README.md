🏋️ FitFlow — Sistema Web para Academia

Sistema web desenvolvido para a FitFlow, uma academia fictícia, com o objetivo de apresentar serviços, planos, aulas coletivas e uma área de acesso do aluno.

O projeto também possui uma aplicação em Python/Flask com um painel de testes que utiliza Selenium para automatizar interações com as páginas do sistema.

📋 Sobre o Projeto

O FitFlow foi desenvolvido como um projeto acadêmico para praticar conceitos de desenvolvimento web, Python, Flask, JavaScript e automação de testes com Selenium.

O sistema possui duas formas de apresentação:

Páginas HTML independentes, compostas por index.html, planos.html, aulas.html e login.html.

Aplicação Flask, concentrada no arquivo projetos_automacao_victor.py, que reproduz as páginas através de render_template_string e acrescenta um painel de automação.

O repositório atualmente contém 5 commits e está organizado na branch main.

🛠️ Tecnologias Utilizadas

HTML5 — Estrutura das páginas

CSS3 — Estilização e responsividade

JavaScript — Interações das páginas

Python 3 — Linguagem utilizada no backend e nas automações

Flask — Framework utilizado para disponibilizar a aplicação web

Selenium — Automação das interações com o navegador

WebDriver Manager — Gerenciamento do ChromeDriver

JSON — Comunicação entre o painel Flask e as rotas de automação

Git/GitHub — Versionamento e armazenamento do projeto

🚀 Funcionalidades do Sistema

🏠 Página Inicial

A página inicial apresenta a proposta da FitFlow e seus principais diferenciais:

Equipamentos modernos;

Aulas diversificadas;

Acompanhamento profissional;

Navegação entre as áreas do sistema;

Chatbot de atendimento.

A página também possui layout responsivo para telas menores. citeturn3view0

💳 Planos

O sistema apresenta dois planos de academia:

Plano Mensal — R$ 99/mês

Acesso livre à musculação;

Horários ilimitados;

Sem fidelidade.

Plano VIP — R$ 149/mês

Acesso total à musculação;

Aulas coletivas inclusas;

Acesso ao App de Treino;

1 avaliação física mensal.

Os botões de assinatura exibem uma confirmação após a seleção do plano. citeturn3view0

🏋️ Agendamento de Aulas

O sistema disponibiliza aulas coletivas para reserva:

Crossfit — Segunda e Quarta às 07:00;

Spinning — Terça e Quinta às 18:30;

Pilates — Sexta-feira às 09:00.

Ao clicar em Reservar Vaga, uma mensagem de confirmação é apresentada ao usuário. citeturn3view0

A página HTML independente aulas.html possui uma grade própria, com horários apresentados como Crossfit 07:00, Spinning 18:00 e Pilates 19:30. citeturn3view1

👤 Área do Aluno

A área do aluno possui:

Campo para e-mail ou matrícula;

Campo de senha;

Botão de entrada;

Dashboard com status do plano;

Ficha de treino.

Na versão principal em index.html, o dashboard apresenta um exemplo de treino de peito e tríceps. citeturn3view0

A versão independente login.html utiliza usuário/CPF e senha e apresenta uma mensagem de autenticação após o envio do formulário. citeturn2view5

Observação: o login apresentado no projeto é uma demonstração de interface e não representa um sistema de autenticação com banco de dados.

💬 Chatbot

A página inicial possui um chatbot visual integrado.

O chatbot pode responder perguntas relacionadas a:

Horário de funcionamento;

Planos;

Preços;

Aulas;

Saudações.

A interface possui caixa de mensagens, campo de texto e botão para envio. citeturn3view0

🤖 Sistema de Automação

O arquivo projetos_automacao_victor.py contém uma aplicação Flask e a classe AutomacaoGymFit, responsável pelas automações com Selenium.

O Selenium cria uma instância do Chrome através do ChromeDriverManager e utiliza WebDriverWait para localizar elementos antes de realizar as ações. citeturn2view2

Automações disponíveis

🔑 Login

A automação:

Abre a página /login;

Localiza o campo de usuário;

Preenche usuário e senha;

Clica no botão de entrada;

Aguarda a execução;

Fecha o navegador.

💳 Assinatura de Plano

A automação:

Abre /planos;

Identifica o plano selecionado;

Localiza o botão correspondente;

Clica no botão;

Aguarda a execução;

Fecha o navegador.

🏋️ Reserva de Aula

A automação:

Abre /aulas;

Identifica a modalidade;

Localiza o botão correspondente;

Realiza a reserva;

Aguarda a execução;

Fecha o navegador.

💬 Chatbot

A automação:

Abre a página inicial;

Localiza o campo do chatbot;

Digita a mensagem;

Clica em enviar;

Aguarda a resposta;

Fecha o navegador. citeturn3view2

⚙️ Painel de Testes

A aplicação Flask possui uma página /painel para disparar as automações.

O painel permite testar:

Login;

Assinatura do Plano Mensal;

Assinatura do Plano VIP;

Agendamento de Crossfit;

Agendamento de Spinning;

Agendamento de Pilates;

Chatbot.

As ações do painel são enviadas através de requisições POST utilizando JavaScript fetch. citeturn3view2

🌐 Rotas da Aplicação Flask

A aplicação Flask disponibiliza as seguintes rotas:

Rota

Função

/

Página inicial

/planos

Página de planos

/aulas

Agendamento de aulas

/login

Área do aluno

/painel

Painel de testes

/executar-login

Executa automação de login

/executar-plano

Executa automação de assinatura

/executar-aula

Executa automação de aula

/executar-chat

Executa automação do chatbot

As rotas de página utilizam render_template_string, enquanto as rotas de automação recebem dados JSON através de requisições POST. citeturn3view2

📂 Estrutura Completa do Repositório

A estrutura atualmente presente no GitHub é:

📁 projeto_cdt
│
├── 📄 LICENSE
├── 📄 README.md
│
├── 🌐 index.html
│   └── Página principal da FitFlow
│
├── 🌐 planos.html
│   └── Página de planos
│
├── 🌐 aulas.html
│   └── Página de agendamento de aulas
│
├── 🌐 login.html
│   └── Área do aluno
│
└── 🐍 projetos_automacao_victor.py
    ├── Aplicação Flask
    ├── Páginas HTML integradas ao Flask
    ├── Painel de testes
    └── Automações com Selenium

Esses são os arquivos que aparecem atualmente na raiz do repositório. citeturn0view0

📦 Instalação

1. Clonar o repositório

git clone https://github.com/felixcandido50-coder/projeto_cdt.git

2. Entrar na pasta

cd projeto_cdt

3. Criar um ambiente virtual

Windows:

python -m venv venv
venv\Scripts\activate

Linux/macOS:

python3 -m venv venv
source venv/bin/activate

4. Instalar as dependências

Para executar a aplicação Flask/Selenium, instale:

pip install Flask selenium webdriver-manager

▶️ Executando as páginas HTML

As páginas HTML podem ser abertas diretamente no navegador:

index.html
planos.html
aulas.html
login.html

A navegação entre as páginas é feita pelos próprios links presentes nos arquivos HTML. citeturn2view5turn2view6

▶️ Executando a aplicação Flask

O arquivo responsável pelo backend é:

projetos_automacao_victor.py

Execute:

python projetos_automacao_victor.py

A aplicação Flask está configurada para iniciar na porta 5000 quando executada diretamente. citeturn3view2

Depois, acesse:

http://127.0.0.1:5000

Para abrir o painel de testes:

http://127.0.0.1:5000/painel

🌍 Deploy

A aplicação Flask pode ser preparada para hospedagem como Web Service em plataformas compatíveis com aplicações Python.

Para utilizar o projeto em produção, é necessário configurar as dependências Python e um servidor WSGI, como o Gunicorn.

Exemplo de dependências

Flask
selenium
webdriver-manager
gunicorn

Exemplo de Start Command

Como o arquivo Flask do repositório se chama projetos_automacao_victor.py e o objeto da aplicação se chama app, o comando correspondente é:

gunicorn --bind 0.0.0.0:$PORT projetos_automacao_victor:app

Importante: as automações Selenium dependem de um navegador compatível disponível no ambiente de execução. Portanto, o funcionamento do site e o funcionamento das automações podem exigir configurações diferentes no servidor.

🔄 Funcionamento da Automação

O fluxo geral do projeto pode ser representado assim:

👤 Usuário
    │
    ▼
🌐 Interface FitFlow
    │
    ▼
⚙️ Painel de Testes
    │
    ▼
📡 Requisição POST
    │
    ▼
🐍 Flask
    │
    ▼
🤖 AutomacaoGymFit
    │
    ▼
🌐 Selenium + Chrome
    │
    ▼
🖱️ Interação automática com o sistema

O Flask cria threads para disparar as automações e retorna uma mensagem informando que a execução foi iniciada. citeturn3view2

⚠️ Observações Técnicas

O projeto possui uma versão de interface em arquivos HTML independentes e uma implementação integrada ao Flask.

Os arquivos HTML independentes não dependem do Flask para serem visualizados.

A aplicação Flask utiliza render_template_string para manter o HTML dentro do arquivo Python.

O login é demonstrativo e não possui autenticação persistente.

As reservas e assinaturas apresentadas nas interfaces são confirmações de demonstração.

As automações Selenium precisam de navegador e WebDriver compatíveis.

O repositório atualmente não apresenta um arquivo requirements.txt; as dependências Python precisam ser instaladas manualmente ou adicionadas a esse arquivo para facilitar o deploy.

📚 Objetivo Acadêmico

Este projeto foi desenvolvido com finalidade acadêmica e educacional, buscando aplicar na prática conhecimentos relacionados a:

Desenvolvimento de interfaces web;

HTML, CSS e JavaScript;

Desenvolvimento de aplicações com Flask;

APIs e requisições HTTP;

Automação de testes;

Selenium WebDriver;

Organização de projetos;

Git e GitHub;

Metodologias de desenvolvimento de software.

👨‍💻 Projeto

FitFlow — Sistema Web para Academia

Repositório:

https://github.com/felixcandido50-coder/projeto_cdt

Desenvolvido para fins acadêmicos e de estudo.

📄 Licença

Este projeto possui um arquivo LICENSE no repositório. Consulte o arquivo para verificar os termos completos da licença. citeturn0view0