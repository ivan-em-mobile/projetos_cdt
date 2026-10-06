 # 🛍️ Monitor de Produtos - Mercado Livre (Desktop)

Este é um aplicativo desktop completo para busca automatizada de produtos no **Mercado Livre**, desenvolvido em **Python** utilizando a biblioteca gráfica **Tkinter**. O sistema conta com automação web via **Selenium**, banco de dados local para persistência do histórico de buscas e exportação dos resultados em **Excel** e **JSON**.

---

## 📦 Dependências do Projeto

| Biblioteca | Finalidade |
| :--- | :--- |
| `selenium` | Automação do navegador Chrome para acessar o Mercado Livre e extrair os produtos |
| `pandas` | Manipulação dos dados coletados e geração das planilhas/exportações |
| `openpyxl` | Leitura e escrita de arquivos `.xlsx` (Excel) |
| `ttkbootstrap` | Interface gráfica moderna e temas prontos sobre o Tkinter |
| `sqlite3` | Banco de dados local do histórico de buscas (já vem embutido no Python) |
| `PyInstaller` | Empacotamento do sistema em executável `.exe` (usado só na hora de gerar o .exe) |

---

## 🚀 Funcionalidades do Sistema

* **Busca Automatizada:** o usuário digita o nome do produto e o sistema abre o Chrome automaticamente, acessa o Mercado Livre e extrai **nome, preço e link** dos 10 primeiros resultados.
* **Busca por Enter ou Botão:** a pesquisa pode ser disparada tanto clicando em "Nova Pesquisa" quanto apertando a tecla **Enter** no campo de busca.
* **Exibição da Busca Atual:** ao concluir uma pesquisa, a tabela mostra **apenas os produtos daquela busca** — o histórico completo só é exibido quando solicitado explicitamente.
* **Histórico Completo sob Demanda:** botão dedicado ("Carregar Histórico do Banco") que traz todas as buscas já realizadas, salvas no banco SQLite.
* **Exportação para Excel:** gera um arquivo `.xlsx` com todo o histórico de buscas e produtos.
* **Exportação para JSON:** gera um arquivo `.json` com o mesmo histórico, em formato estruturado.
* **Visualizador de Exportações:** botão "Ver Exportações" lista todos os arquivos `.xlsx` e `.json` já exportados na pasta do projeto, permitindo carregar qualquer um deles de volta na tabela sem precisar navegar manualmente pelo explorador de arquivos.
* **Leitura de Planilha Externa:** permite abrir e visualizar qualquer planilha `.xlsx` selecionada manualmente pelo usuário.
* **Tratamento de Erros:** mensagens claras na interface em caso de falha na busca, no banco de dados ou na leitura de arquivos.

---

## 📂 Estrutura Completa de Caminhos e Arquivos

Abaixo está o mapeamento de como os arquivos ficam organizados no diretório do projeto após a compilação com o PyInstaller:

```text
📁 Área de Trabalho (Desktop)
└── 📁 projetos_cdt-main
    └── 📁 projetos_cdt/                          # Pasta principal do projeto
        │
        ├── 📁 build/                             # Arquivos temporários de compilação
        │   └── 📁 AutomacaoPrecos/               # Subpasta criada pelo PyInstaller
        │       ├── 📁 localpycs/                 # Arquivos Python compilados em bytecode (.pyc)
        │       ├── 📁 base_library.zip           # Biblioteca padrão do Python compactada
        │       ├── 📄 Analysis-00.toc            # Tabela de conteúdos da análise de dependências
        │       ├── 📄 EXE-00.toc                 # Metadados de criação do executável
        │       ├── 📄 PKG-00.toc                 # Metadados do pacote de arquivos
        │       ├── 📄 PYZ-00.pyz & .toc          # Arquivos compactados com scripts Python do sistema
        │       ├── 📄 AutomacaoPrecos.pkg        # Pacote bruto do aplicativo gerado
        │       ├── 📄 warn-AutomacaoPrecos.txt   # Registro de avisos/alertas da compilação
        │       └── 📄 xref-AutomacaoPrecos.html  # Tabela de referências cruzadas do código
        │
        ├── 📁 dist/                              # PASTA DO PROGRAMA PRONTO PARA USO
        │   └── ⚙️ AutomacaoPrecos.exe             # O executável final do sistema
        │
        ├── 🗃️ historico.db                        # Banco de dados com o histórico de buscas
        ├── 📄 historico_exportado_AAAAMMDD_HHMMSS.xlsx  # Exportações em Excel (uma por exportação)
        ├── 📄 historico_exportado_AAAAMMDD_HHMMSS.json  # Exportações em JSON (uma por exportação)
        ├── 🐍 app_MonitorProdutos-version1.py     # Código-fonte original em Python
        ├── 📄 AutomacaoPrecos.spec                # Arquivo de configuração de compilação do PyInstaller
        ├── 📄 build_exe.bat                       # Script para gerar o .exe automaticamente
        └── 📄 README.md                           # Documentação do projeto
```

---

## ⚡ Guia de Instalação e Execução

1. **Instale as dependências:**
   ```bash
   pip install selenium pandas openpyxl ttkbootstrap
   ```

2. **Execute o aplicativo:**
   ```bash
   python app_MonitorProdutos-version1.py
   ```

> **Pré-requisito:** o **Google Chrome** precisa estar instalado na máquina (o Selenium controla ele para fazer as buscas).

---

### Alternativa: usar o executável pronto

Se você já tem o `.exe` gerado, não precisa instalar nada — basta rodar:
```
dist\AutomacaoPrecos.exe
```
(mesmo assim, o Google Chrome precisa estar instalado na máquina).

### Gerar o executável novamente

```bash
build_exe.bat
```