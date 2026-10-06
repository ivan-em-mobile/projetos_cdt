<div align="center">

# 🍦 Sorveteria Glacê 🎀

**Um sistema desktop completo de Gestão de Vendas (PDV), Controle de Estoque e Atendimento Automatizado via Chatbot.**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-pink?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Conclu%C3%ADdo-brightgreen?style=for-the-badge)

</div>

---

## 📌 Visão Geral

O **Sorveteria Glacê** é uma aplicação desktop em Python projetada para centralizar a operação diária de uma sorveteria. O sistema alia um painel administrativo financeiro e operacional a uma interface interativa de atendimento ao cliente baseada em chatbot.

A ferramenta foi construída com foco em **usabilidade, responsividade de interface e validação de dados em tempo real**, garantindo que as vendas só sejam processadas se houver saldo e estoque compatíveis.

---

## 🎨 Principais Funcionalidades

### 📊 Dashboard em Tempo Real
- **Caixa Atual:** Exibição dinâmica do saldo total acumulado.
- **Vendas do Dia:** Contador das transações realizadas com sucesso.
- **Itens Vendidos:** Total de unidades comercializadas.
- **Alerta de Estoque:** Monitoramento de produtos com baixa disponibilidade ($\le 5$ unidades).

### 🛒 Ponto de Venda (PDV - Vendas)
- Suporte a múltiplos métodos de pagamento (*Pix, Cartão de Crédito, Cartão de Débito, Dinheiro*).
- Cálculo automático de **troco** para pagamentos em dinheiro.
- Bloqueio automático de vendas caso a quantidade solicitada supere o estoque atual.

### 📦 Controle & Reposição de Estoque
- Visualização em tabela (`Treeview`) com ordenação de itens e indicativos visuais de status:
  - `✓ Normal` (Estoque adequado)
  - `⚠️ Baixo` (5 unidades ou menos)
  - `❌ Esgotado` (0 unidades)
- Formulário rápido para entrada/reposição de produtos no estoque.

### 📋 Extrato & Auditabilidade
- Registro em tempo real de todas as operações (abertura de caixa, vendas diretas, vendas via chat e reposições).
- Exibição em ordem cronológica inversa (operações mais recentes no topo).

### 💬 Chatbot Interativo de Atendimento
- **Reconhecimento de Intenções:** Processa saudações, pedidos de cardápio, suporte e agradecimentos.
- **Extração de Dados via Regex:** Identifica sabores e quantidades digitadas pelo usuário em linguagem natural (ex: *"Quero 3 Pistache"*).
- **Checkout Integrado:** Permite a seleção do método de pagamento diretamente pela interface do chat.

---

## 📐 Arquitetura do Projeto

```text
├── sorveteria_glace.py   # Código-fonte principal (GUI + Lógica de Negócios)
├── README.md             # Documentação do projeto
└── LICENSE               # Licença do repositório (MIT)