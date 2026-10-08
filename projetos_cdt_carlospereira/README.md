# 🍔 Gourmet Service

> **Sistema completo de pedidos para uma hamburgueria/restaurante, desenvolvido em Python com Tkinter e SQLite.**

O **Gourmet Service** é uma aplicação desktop criada para simular a experiência de um sistema real de pedidos de uma hamburgueria/restaurante.

O projeto reúne em um único sistema **cadastro e login de usuários, cardápio, carrinho de compras, checkout, banco de dados, consulta de endereço por CEP e um Assistente IA capaz de conversar com o cliente sobre os produtos do estabelecimento.**

A proposta é transformar um simples programa de pedidos em uma experiência mais completa, organizada e interativa. 🍔🤖

---

## 📌 Sobre o projeto

O Gourmet Service foi desenvolvido em **Python**, utilizando principalmente a biblioteca **Tkinter** para construir a interface gráfica e **SQLite** para armazenar os dados.

O sistema foi pensado para funcionar como um pequeno aplicativo de restaurante, permitindo que o cliente:

* Crie uma conta;
* Faça login;
* Navegue pelo cardápio;
* Consulte hambúrgueres, pizzas e bebidas;
* Veja preços e descrições;
* Adicione produtos ao carrinho;
* Altere a quantidade dos produtos;
* Acompanhe o carrinho enquanto escolhe os produtos;
* Converse com um Assistente IA;
* Pergunte sobre os produtos;
* Peça recomendações;
* Adicione produtos ao carrinho através da IA;
* Consulte o próprio carrinho pela IA;
* Informe endereço e forma de pagamento;
* Finalize o pedido;
* Salve o pedido no banco de dados.

---

# 🚀 Funcionalidades

## 🔐 Sistema de login

O Gourmet Service possui um sistema de autenticação para identificar o cliente.

Na tela inicial, o usuário pode informar:

* Usuário;
* Senha.

Caso os dados estejam corretos, o sistema libera o acesso ao aplicativo.

Se o usuário ainda não possuir uma conta, existe a opção:

> 📝 **Criar nova conta**

O cadastro solicita:

* Nome;
* Usuário;
* Senha.

Os usuários são armazenados no banco de dados SQLite.

---

# 🏠 Tela inicial

Depois do login, o usuário encontra uma página inicial organizada com quatro opções principais:

### 🍔 Hambúrgueres

Leva diretamente para a categoria de hambúrgueres do cardápio.

### 🍕 Pizzas

Leva diretamente para a categoria de pizzas.

### 🥤 Bebidas

Leva diretamente para as bebidas disponíveis.

### 🤖 Assistente IA

Abre diretamente a área de conversa com o assistente.

Isso torna a navegação mais simples, permitindo que o usuário encontre rapidamente aquilo que procura.

---

# 🍔 Cardápio

O cardápio é dividido em três categorias principais:

## 🍔 Hambúrgueres

* **Poderoso Chefão** — R$ 34,90
* **Clássico Smash** — R$ 22,00
* **Duplo Bacon** — R$ 38,50
* **Chicken Crispy** — R$ 25,90

Cada produto possui:

* Nome;
* Preço;
* Descrição;
* Imagem;
* Botão para adicionar ao carrinho.

---

## 🍕 Pizzas

O sistema possui:

* **Calabresa** — R$ 45,00
* **Marguerita** — R$ 42,00
* **Quatro Queijos** — R$ 50,00

Cada pizza também possui sua descrição e imagem.

---

## 🥤 Bebidas

As opções disponíveis são:

* **Soda Artesanal** — R$ 12,00
* **Milkshake** — R$ 18,00
* **Refrigerante** — R$ 6,50

---

# 🛒 Carrinho lateral

Uma das funcionalidades adicionadas ao projeto é o **carrinho lateral**.

Enquanto o cliente navega pelo cardápio, ele consegue visualizar seu carrinho sem precisar ficar trocando de aba.

O painel mostra:

* Produtos adicionados;
* Quantidade;
* Preço;
* Total da compra.

Também existem botões para:

**➕** Aumentar quantidade

**➖** Diminuir quantidade

Além disso, o usuário pode:

> 🛒 **VER CARRINHO**

ou

> ✅ **FINALIZAR PEDIDO**

Essa funcionalidade deixa o processo de compra muito mais prático.

---

# 🛒 Tela do carrinho

Além do carrinho lateral, existe uma aba exclusiva para visualizar todos os produtos escolhidos.

O sistema calcula automaticamente:

```text
Preço do produto × quantidade
```

e soma todos os subtotais para gerar o valor final.

Por exemplo:

```text
2x Clássico Smash
2x Refrigerante

Total: R$ 57,00
```

O usuário também pode aumentar ou diminuir a quantidade diretamente nessa tela.

---

# 🤖 Assistente IA

Uma das principais funcionalidades do Gourmet Service é o **Assistente IA**.

O usuário não precisa navegar pelo sistema procurando todas as informações.

Ele pode simplesmente abrir a aba:

> 🤖 Assistente IA

e digitar uma pergunta.

A interface possui uma **barra de texto na parte inferior**, semelhante a um aplicativo de conversa.

O usuário pode escrever a pergunta e:

* Clicar em **📨 ENVIAR**
* Ou pressionar **Enter**

A mensagem aparece na área de conversa e o assistente gera uma resposta.

---

# 💬 Conversando com a IA

O assistente consegue interpretar diversas perguntas relacionadas ao restaurante.

### Exemplo:

```text
Usuário:
Quais hambúrgueres vocês têm?
```

A IA identifica que a pergunta está relacionada à categoria de hambúrgueres e apresenta os produtos disponíveis.

Outro exemplo:

```text
Usuário:
Quanto custa o smash?
```

A IA identifica o produto **Clássico Smash** e informa seu preço.

Também é possível perguntar:

```text
O que vem no Poderoso Chefão?
```

E o sistema apresenta a descrição cadastrada do produto.

---

# 🛍️ IA integrada ao carrinho

A IA não serve apenas para responder perguntas.

Ela também consegue interagir com o carrinho.

Por exemplo:

```text
Quero 2 smash
```

O sistema identifica o produto e adiciona duas unidades ao carrinho.

Depois, o usuário pode perguntar:

```text
Mostra meu carrinho
```

e o assistente apresenta os produtos adicionados e o valor total.

Também é possível solicitar:

```text
Limpar meu carrinho
```

e o sistema remove os produtos.

Isso cria uma experiência de pedido mais próxima de um atendimento automatizado.

---

# 🧠 Como funciona a inteligência da IA?

O Assistente IA deste projeto funciona localmente através de **regras de interpretação de texto**.

Ele não depende de uma API externa de inteligência artificial para executar essas funções.

O programa analisa o texto digitado pelo usuário e tenta identificar:

* Intenção da pergunta;
* Categoria;
* Produto;
* Quantidade;
* Preço;
* Comandos relacionados ao carrinho.

Para melhorar a identificação das mensagens, o código utiliza técnicas como:

### 🔤 Normalização de texto

A função `normalizar()` transforma o texto para facilitar a comparação.

Por exemplo:

```text
"Quanto custa o PÃO?"
```

pode ser convertido para uma forma padronizada para facilitar sua análise.

Também são removidos acentos de determinadas palavras.

---

## 🔎 Busca aproximada

O projeto utiliza a biblioteca:

```python
difflib
```

para realizar comparações aproximadas entre textos.

Isso permite que o sistema tente reconhecer nomes mesmo quando o usuário não escreve exatamente da mesma maneira que o produto está cadastrado.

---

# 💡 Recomendações

O Assistente também consegue responder perguntas relacionadas a recomendações.

Por exemplo:

```text
O que você recomenda?
```

A IA pode apresentar uma sugestão baseada nos produtos cadastrados no cardápio.

O objetivo é transformar o sistema em algo mais parecido com um atendimento digital, em vez de apenas uma tela tradicional de pedidos.

---

# 💰 Consulta de preços

O cliente pode perguntar diretamente sobre o valor de um produto.

Exemplos:

```text
Quanto custa a pizza?
```

```text
Qual o preço do Milkshake?
```

```text
Quanto custa o Duplo Bacon?
```

O sistema procura o produto correspondente e retorna seu preço.

---

# 🥇 Produto mais barato e mais caro

A IA também consegue analisar os produtos cadastrados.

É possível perguntar:

```text
Qual é o mais barato?
```

ou:

```text
Qual é o mais caro?
```

O sistema percorre os produtos disponíveis e identifica o menor ou maior preço.

---

# 💳 Pagamento

Durante o checkout, o cliente pode escolher uma forma de pagamento.

As opções disponíveis são:

* PIX;
* Cartão;
* Dinheiro.

A forma escolhida é armazenada junto com os dados do pedido.

---

# 📍 Endereço e CEP

Durante a finalização do pedido, o sistema solicita:

* CEP;
* Endereço;
* Número.

O CEP é validado para garantir que possui oito dígitos.

O projeto também foi preparado para trabalhar com consulta de endereço através do **ViaCEP**.

Isso permite utilizar o CEP informado para buscar informações de endereço automaticamente.

---

# ✅ Finalização do pedido

Quando o cliente decide finalizar sua compra, o sistema abre uma tela específica para o checkout.

Nessa etapa são reunidas as informações necessárias para registrar o pedido.

O sistema salva:

```text
Cliente
Data e hora
Produtos
Quantidade
Total
CEP
Endereço
Número
Forma de pagamento
```

Depois que o pedido é salvo, o carrinho é limpo e o sistema apresenta uma confirmação com o número do pedido e o valor total.

---

# 🗄️ Banco de dados SQLite

O Gourmet Service utiliza o **SQLite** para armazenar as informações.

O banco é criado automaticamente no arquivo:

```text
restaurante.db
```

O projeto utiliza duas tabelas principais.

## 👤 Tabela `usuarios`

Armazena informações relacionadas às contas.

Estrutura:

```text
usuario
nome
senha
```

---

## 📦 Tabela `pedidos`

Armazena os pedidos realizados.

Estrutura:

```text
id
cliente
data_hora
itens
total
cep
endereco
numero
forma_pagamento
```

Dessa forma, os pedidos não ficam apenas na memória do programa.

Eles são registrados no banco de dados.

---

# 🎨 Interface gráfica

A interface foi construída utilizando:

```python
Tkinter
```

O projeto utiliza um estilo escuro e moderno.

Principais cores:

```text
Fundo: #0F0F12
Cards: #1A1A20
Cards secundários: #22222A
Roxo principal: #7C3AED
Roxo secundário: #9B5CFF
Branco: #FFFFFF
Cinza: #A7A7B2
Verde: #22C55E
Vermelho: #EF4444
```

O roxo é utilizado como cor principal dos botões e elementos de destaque.

O verde representa informações positivas, como valores e ações de sucesso.

O vermelho é utilizado para ações de remoção ou redução.

---

# 🖼️ Imagens dos produtos

Os produtos possuem imagens para deixar o cardápio mais visual.

As imagens são carregadas através de URLs e processadas utilizando:

```python
Pillow
```

A biblioteca é importada através de:

```python
from PIL import Image, ImageTk
```

O programa também utiliza `requests` para realizar as requisições necessárias.

---

# 📦 Bibliotecas utilizadas

O projeto utiliza principalmente:

### Python

Linguagem principal do projeto.

### Tkinter

Responsável pela interface gráfica.

### SQLite3

Responsável pelo banco de dados.

### Requests

Utilizado para requisições HTTP, como carregamento de imagens e integração com serviços externos.

### Pillow

Utilizado para trabalhar com imagens.

### JSON

Utilizado para organizar informações estruturadas, especialmente os itens dos pedidos.

### Datetime

Utilizado para registrar a data e hora dos pedidos.

### Regex

Utilizado através de:

```python
re
```

para identificar números e quantidades digitadas pelo usuário.

### Difflib

Utilizado para realizar comparação aproximada de textos e ajudar o Assistente IA a reconhecer produtos.

---

# 📁 Estrutura do projeto

Uma estrutura simples para o projeto pode ser:

```text
Gourmet-Service/
│
├── main.py
│
├── restaurante.db
│
└── README.md
```

O arquivo `restaurante.db` é criado automaticamente pelo programa caso ainda não exista.

---

# ⚙️ Instalação

Primeiro, certifique-se de possuir o Python instalado.

Depois, instale as bibliotecas externas:

```bash
pip install requests pillow
```

O Tkinter e o SQLite normalmente já acompanham instalações padrão do Python no Windows.

Depois execute:

```bash
python main.py
```

---

# 🧪 Exemplo de utilização

Ao iniciar o programa:

```text
🔥 GOURMET SERVICE 🔥
```

O cliente cria sua conta e realiza o login.

Depois encontra:

```text
🏠 Início
🍔 Cardápio
🤖 Assistente IA
🛒 Carrinho
```

No cardápio, pode escolher seus produtos.

Enquanto escolhe, o carrinho fica visível na lateral.

Depois, pode conversar com a IA:

```text
👤 Você:
Quais pizzas vocês têm?

🤖 IA:
🍕 PIZZAS

• Calabresa — R$ 45,00
• Marguerita — R$ 42,00
• Quatro Queijos — R$ 50,00
```

Em seguida:

```text
👤 Você:
Quero uma marguerita
```

A IA adiciona o produto ao carrinho.

Por fim:

```text
👤 Você:
Mostra meu carrinho
```

E o sistema apresenta os produtos e o total.

---

# 🔄 Fluxo do sistema

O funcionamento geral pode ser representado assim:

```text
        INÍCIO
          │
          ▼
     🔐 LOGIN
          │
          ▼
     🏠 MENU PRINCIPAL
          │
    ┌─────┼─────┬─────┐
    ▼     ▼     ▼     ▼
   🍔    🍕    🥤    🤖
 CARDÁPIO       IA
    │           │
    └─────┬─────┘
          ▼
       🛒 CARRINHO
          │
          ▼
      ✅ CHECKOUT
          │
          ▼
      📍 ENDEREÇO
          │
          ▼
      💳 PAGAMENTO
          │
          ▼
      🗄️ SQLITE
          │
          ▼
     🎉 PEDIDO SALVO
```

---

# 🌟 Destaques do projeto

O Gourmet Service não foi desenvolvido apenas como uma tela de cardápio.

O projeto reúne diferentes conceitos de programação em uma única aplicação:

* Interfaces gráficas;
* Programação orientada a objetos;
* Banco de dados;
* CRUD e persistência de informações;
* Manipulação de arquivos;
* Requisições HTTP;
* Processamento de imagens;
* Reconhecimento de texto;
* Carrinho de compras;
* Sistema de login;
* Checkout;
* Integração entre diferentes partes do sistema;
* Automação de tarefas;
* Assistente conversacional.

Isso torna o projeto uma ótima demonstração de como diferentes conhecimentos de Python podem ser combinados para criar uma aplicação completa.

---

# 🚀 Possíveis melhorias futuras

O Gourmet Service pode continuar evoluindo.

Algumas ideias para versões futuras:

* 👨‍💼 Painel administrativo;
* 📦 Controle de estoque;
* 📊 Relatórios de vendas;
* 📈 Gráficos de faturamento;
* 👥 Histórico de pedidos por usuário;
* 🧾 Geração de recibos;
* 🖨️ Impressão de pedidos;
* ⭐ Sistema de avaliações;
* 🎁 Sistema de cupons e descontos;
* 🔔 Notificações de pedido;
* 🚚 Acompanhamento da entrega;
* 🧠 IA generativa mais avançada;
* 🎙️ Atendimento por voz;
* 📱 Versão para celular;
* 🌐 Sistema online conectado a um servidor.

---

# 🧠 O objetivo do projeto

Mais do que criar um sistema para pedir comida, o objetivo do **Gourmet Service** é demonstrar como a programação pode transformar uma ideia simples em uma aplicação completa.

O projeto começa com algo básico:

> "Quero fazer um sistema de pedidos."

E evolui para:

> **Login + Banco de Dados + Cardápio + Carrinho + Checkout + Endereço + Assistente IA + Persistência de pedidos.**

Cada funcionalidade adicionada representa um novo conceito de programação aplicado na prática.

---

# 🍔 Gourmet Service

**Um projeto feito para transformar código em uma experiência de restaurante.**

```text
🍔 Escolha.
🛒 Monte seu pedido.
🤖 Converse com a IA.
💳 Finalize.
🎉 Aproveite!
```

---

## 👨‍💻 Tecnologias

* Python
* Tkinter
* SQLite
* Requests
* Pillow
* JSON
* Regex
* Difflib
* ViaCEP

---

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais e de aprendizado em programação.

Sinta-se livre para estudar o código, modificar funcionalidades e continuar evoluindo o sistema.

---

# ⭐ Gourmet Service

> **Do código ao pedido: uma experiência completa construída em Python.** 🍔🐍
