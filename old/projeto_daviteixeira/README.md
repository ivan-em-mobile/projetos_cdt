📘 README - Sistema de Concessionária com SQLite e Tkinter
Este projeto implementa um sistema simples de concessionária utilizando SQLite para persistência de dados e Tkinter para interface gráfica. Ele permite cadastrar carros, clientes e vendas, além de visualizar os carros disponíveis em uma interface amigável.

🚗 Funcionalidades
Banco de Dados SQLite (concessionaria.db)

Tabela carros: modelo, marca, ano e preço.

Tabela clientes: nome, telefone e e-mail.

Tabela vendas: relacionamento entre cliente e carro, com data e valor da venda.

Exportação de dados

Os registros são exportados para um arquivo JSON (dados_concessionaria.json).

Interface Gráfica (Tkinter)

Exibição dos carros cadastrados em uma tabela (Treeview).

Botão para carregar os carros do banco de dados.

Estilo personalizado com cores e destaque para seleção.

🛠️ Tecnologias Utilizadas
SQLite3 → Banco de dados leve e embutido.

Tkinter → Biblioteca padrão para interfaces gráficas em Python.

JSON → Exportação dos dados em formato estruturado.

📂 Estrutura do Projeto

Código
concessionaria/
│── concessionaria.db        # Banco de dados SQLite
│── dados_concessionaria.json # Exportação dos dados
│── main.py                   # Código principal
▶️ Como Executar
Clone ou copie o código para sua máquina.

Certifique-se de ter Python 3.x instalado.

Execute o script:

bash
python main.py
A janela da aplicação será aberta mostrando os carros cadastrados.

📊 Exemplo de Dados
Carros

json
{
  "id": 1,
  "modelo": "Civic",
  "marca": "Honda",
  "ano": 2022,
  "preco": 120000
}
Clientes

json
{
  "id": 1,
  "nome": "João Silva",
  "telefone": "11999999999",
  "email": "joao@email.com"
}
Vendas

json
{
  "id": 1,
  "carro_id": 1,
  "cliente_id": 1,
  "data_venda": "2026-05-18",
  "valor": 120000
}
🎨 Interface Gráfica
Tabela de carros com colunas: Modelo, Marca, Ano e Preço.

Botão "Carregar Carros" para atualizar os dados.

Estilo customizado com fundo escuro e destaque verde para seleção.

🔮 Possíveis Melhorias
Adicionar CRUD completo (inserir, editar, excluir carros/clientes).

Implementar relatórios de vendas.

Criar filtros de busca por marca, ano ou preço.

Melhorar a interface com menus e abas.

Quer que eu prepare também um guia passo a passo para adicionar novos carros e clientes diretamente pela interface gráfica, em vez de apenas via código? Isso tornaria o sistema mais interativo.