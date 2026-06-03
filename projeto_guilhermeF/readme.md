# Sistema de Cadastro e Gestão de Clientes 🚀

Este é um sistema simples em linha de comando (CLI) desenvolvido em Python para o gerenciamento, cadastro e exportação de dados de clientes, contando com um sistema seguro de login de acesso.

## 📋 Funcionalidades

- **Sistema de Autenticação Seguro**: Proteção por senha com limite de até 5 tentativas e ocultação de caracteres no terminal durante a digitação.
- **Alteração de Senha**: Opção interna no menu para reconfigurar a credencial de acesso.
- **Gestão de Planos**: Cadastro de clientes atrelados a três categorias de planos (Gratuito, Básico e Premium).
- **Controle de Carimbo de Data/Hora**: Armazenamento automático da data e hora exata em que o cliente foi cadastrado.
- **Listagem e Relatórios**: Visualização detalhada de clientes salvos e contador em tempo real do total de registros.
- **Exportação de Dados**: Geração automática de um arquivo estruturado em formato `.json`.

## 🛠️ Pré-requisitos e Tecnologias

O projeto utiliza apenas bibliotecas nativas do ecossistema Python, não sendo necessária a instalação de dependências externas.

- **Python 3.x** instalado.
- Módulos nativos utilizados:
  - `getpass` (para mascaramento seguro de senhas)
  - `json` (para manipulação e exportação de dados)
  - `datetime` (para manipulação de datas)

## 🚀 Como Executar o Projeto

1. Certifique-se de ter o Python instalado em sua máquina. Para verificar, execute:
   ```bash
   python --version

python main.py

## ❗ Informaçoes Essenciais

Criadores do projeto: *Guilherme Firmino* => estrutura principal e reestruturaçâo, *Leonardo Santana* => fez a funcionalidades e o sistema visivel.

Esse projeto ira servir de portifolio!

O projeto e simples, mas foi trabalhoso na parte de correção de bugs.