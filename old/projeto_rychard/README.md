# 🍔 Sistema de Hamburgueria (Desktop)

Este é um aplicativo desktop completo para gerenciamento de pedidos de uma hamburgueria, desenvolvido em **Python** utilizando a biblioteca gráfica **Tkinter**. O sistema conta com banco de dados local para persistência de dados e integração com API externa para busca automatizada de endereço.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3** (Linguagem base)
* **Tkinter** (Interface gráfica integrada)
* **SQLite3** (Banco de dados local e leve)
* **Requests** (Para consumo da API externa do ViaCEP)

---

## 🚀 Funcionalidades do Sistema

* **Sistema de Cadastro e Login:** Permite que novos clientes se cadastrem e façam login com validação direto no banco de dados (garantindo que não haja e-mails duplicados).
* **Cardápio Dinâmico:** Janelas separadas para seleção de Combos (Hambúrgueres) e Bebidas com seus respectivos preços.
* **Carrinho de Compras:** Adiciona itens ao carrinho em tempo real com alertas visuais.
* **Cupom de Desconto:** Validação do cupom promocional `DESCONTO10`, que aplica automaticamente 10% de desconto no valor total do carrinho.
* **Integração com ViaCEP:** Ao digitar o CEP na finalização do pedido, o sistema preenche automaticamente os campos de *Rua*, *Bairro* e *Cidade*, restando ao usuário apenas digitar o número.
* **Histórico de Pedidos:** Salva todos os pedidos finalizados com o resumo de itens, endereço, forma de pagamento e valor total na tabela do banco de dados.
* **Sistema de Avaliação:** Permite que o cliente dê uma nota de 0 a 5 para o estabelecimento.

---

## 📂 Estrutura Completa de Caminhos e Arquivos

Abaixo está o mapeamento exato de como os arquivos estão organizados no diretório do projeto após a compilação com o PyInstaller:

```text
📁 Área de Trabalho (Desktop)
└── 📁 projetos_cdt-main
    └── 📁 projetos_cdt/                      # Pasta principal do projeto
        │
        ├── 📁 build/                         # Arquivos temporários de compilação
        │   └── 📁 hamburgueria/              # Subpasta criada pelo PyInstaller
        │       ├── 📁 localpycs/             # Arquivos Python compilados em bytecode (.pyc)
        │       ├── 📁 base_library.zip       # Biblioteca padrão do Python compactada
        │       ├── 📄 Analysis-00.toc        # Tabela de conteúdos da análise de dependências
        │       ├── 📄 EXE-00.toc             # Metadados de criação do executável
        │       ├── 📄 PKG-00.toc             # Metadados do pacote de arquivos
        │       ├── 📄 PYZ-00.pyz & .toc      # Arquivos compactados com scripts Python do sistema
        │       ├── 📄 hamburgueria.pkg       # Pacote bruto do aplicativo gerado
        │       ├── 📄 warn-hamburgueria      # Registro de avisos/alertas da compilação
        │       └── 📄 xref-hamburgueria      # Tabela de referências cruzadas do código
        │
        ├── 📁 dist/                          # PASTA DO PROGRAMA PRONTO PARA USO
        │   ├── ⚙️ hamburgueria                # O Executável final do seu sistema (Aplicação)
        │   └── 🗃️ hamburgueria               # Banco de dados utilizado pelo Executável
        │
        ├── 🗃️ hamburgueria                   # Banco de dados utilizado pelo código fonte .py
        ├── 🐍 hamburgueria.py                 # Seu código fonte original em Python
        ├── 📄 hamburgueria.spec               # Arquivo de configuração de compilação do PyInstaller
        └── 📄 README.md                       # Documentação do projeto
