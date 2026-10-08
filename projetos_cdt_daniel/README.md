# 🏋️‍♂️ Academia RH Fitness — Sistema de Gestão Integrado & Plataforma Web

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Framework-black?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![HTML5](https://img.shields.io/badge/HTML5-Modern-orange?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow?style=for-the-badge&logo=javascript&logoColor=white)](https://developer.mozilla.org/)
[![Status](https://img.shields.io/badge/Status-Concluído-success?style=for-the-badge)]()

*Uma plataforma web completa e moderna desenvolvida para a **Academia RH Fitness**, unindo uma landing page interativa de alto desempenho com um sistema back-end em Python que gerencia matrículas e dados de forma automatizada em um banco JSON.*

</div>

---

## 📋 Sumário
- [Sobre o Projeto](#-sobre-o-projeto)
- [Detalhes e Funcionalidades da Academia](#-detalhes-e-funcionalidades-da-academia)
- [Funcionalidades do Sistema & Back-end](#-funcionalidades-do-sistema--back-end)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Estrutura de Pastas](#-estrutura-de-pastas)
- [Como Executar o Projeto](#-como-executar-o-projeto)
- [Acesso ao Painel Administrativo](#-acesso-ao-painel-administrativo)
- [Autor](#-autor)

---

## 🎯 Sobre o Projeto

A **Academia RH Fitness** foi concebida para atender tanto os alunos quanto a administração de um centro de treinamento. O projeto integra uma interface visual atraente focada em conversão e experiência do usuário (UX) com uma arquitetura back-end leve em **Python (Flask)**. 

O grande diferencial técnico é a persistência inteligente: todas as interações e cadastros realizados no site comunicam-se via API com o servidor local, gravando e atualizando automaticamente o arquivo **`banco.json`** diretamente na estrutura de diretórios do Visual Studio Code.

---

## 🏋️‍♂️ Detalhes e Funcionalidades da Academia

O site da academia foi estruturado seções estratégicas para engajar o público e otimizar conversões:

* **Início & Apresentação (Hero Section):** 
  * Mensagem de impacto focada em superação de limites e alta performance.
  * Botões de chamada para ação (*CTA*) direcionados para o formulário de matrícula.
* **Seção Institucional (Sobre):** 
  * Apresentação da proposta estrutural da academia, com foco em excelência e acompanhamento profissional individualizado.
* **Modalidades de Treino:**
  * Vitrine visual detalhando as áreas de atendimento, destacando setores como a **Musculação**, equipada com pesos livres e máquinas de última geração para hipertrofia e condicionamento físico.
* **Planos e Assinaturas:**
  * **Plano Mensal (R$ 90,00/mês):** Focado em flexibilidade, oferecendo acesso livre à musculação.
  * **Plano Semestral (R$ 150,00/mês):** Destacado como o melhor custo-benefício, garantindo acesso total à academia e suporte avançado.
* **Ferramenta de Avaliação (Calculadora de IMC):**
  * Utilitário interativo onde o aluno insere o seu peso (kg) e altura (m) para calcular instantaneamente o seu Índice de Massa Corporal e obter um diagnóstico preliminar.
* **Assistente Virtual / Chatbot:**
  * Mini chat integrado no canto da tela para tirar dúvidas rápidas dos visitantes de maneira automatizada e amigável ("Fala, maromba!").
* **Formulário de Matrícula Dinâmico:**
  * Coleta de nome completo, CPF, e-mail, escolha de plano e método de pagamento (PIX ou Cartão de Crédito).
  * Exibição de um feedback visual imersivo pós-cadastro, acompanhado de uma animação temática de supino/musculação.
* **Localização e Contato:**
  * Endereço físico estruturado (Rua Antônio José Bastos, 238 - Parque Regina, São Paulo - SP) e canais de atendimento direto.

---

## 💻 Funcionalidades do Sistema & Back-end

* **🗄️ Persistência Automatizada em JSON:** Comunicação via requisições assíncronas (*Fetch API / Async-Await*) para ler e salvar dados diretamente no arquivo `banco.json` no servidor Python.
* **🔒 Painel Administrativo Restrito:**
  * Área de gestão oculta, ativada por duplo clique no logotipo da marca.
  * Tela de autenticação protegida por usuário e senha.
  * **Métricas em Tempo Real:** Cards dinâmicos exibindo o total de alunos cadastrados, alunos ativos, matrículas pendentes e quantidade de adesões por débito automático.
  * **Tabela de Gestão de Alunos:** Listagem completa com status visuais coloridos (*ativo*, *pendente*, *cancelado*).
  * **Ações de Controle:** Opção interativa para cancelar inscrições de alunos diretamente pelo painel, atualizando o banco instantaneamente.
  * **Exportação de Dados:** Botão dedicado para exportar o arquivo JSON de backup de forma manual a qualquer momento.

---

## 🛠️ Tecnologias Utilizadas

O ecossistema do projeto emprega as seguintes ferramentas e linguagens:

* **Front-end:** 
  * HTML5 Semântico
  * CSS3 Avançado (Flexbox, CSS Grid, Variáveis Customizadas, Animações e Glassmorphism)
  * JavaScript Moderno (ES6+, Manipulação de DOM, Fetch API)
  * [FontAwesome](https://fontawesome.com/) (Biblioteca de ícones)
* **Back-end:** 
  * [Python 3.x](https://www.python.org/)
  * [Flask](https://flask.palletsprojects.com/) (Micro-framework web para criação de rotas e APIs)
  * Módulos nativos do Python (`json`, `os`)

---

## 📁 Estrutura de Pastas

Organize os arquivos na raiz do seu projeto no Visual Studio Code da seguinte maneira:

```text
seu-projeto-academia/
│
├── app.py              # Servidor Python responsável pelas rotas, API e escrita no JSON
├── index.html          # Front-end unificado (Landing Page, Painel Admin e Lógica JS)
└── banco.json          # Arquivo de banco de dados gerado e atualizado em tempo real