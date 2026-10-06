
### Panorama Geral da Solução

Para organizar este `README.md` de forma clara e profissional, dividiremos a documentação em **6 secções principais**:

1. **Título e Descrição Geral do Projeto:** Uma breve apresentação sobre o propósito do robô (automação da reavaliação/aprovação de atividades de alunos no EAD).
2. **Funcionalidades:** Lista dos recursos do robô (pesquisa automática, atribuição de nota 0,75, ciclo contínuo em `while` e tratamento de pendências).
3. **Pré-requisitos e Dependências:** O que precisa de estar instalado no computador (Python 3.x, biblioteca `selenium` e o navegador Google Chrome).
4. **Configuração do Ambiente:** Instruções passo a passo de como abrir o Chrome na porta de depuração (`9222`) para reaproveitar a sessão logada.
5. **Como Executar o Script:** Como iniciar o script via VS Code ou linha de comandos.
6. **Estrutura e Explicação do Código:** Um resumo didático do fluxo do código Python e dos seus parâmetros (como a variável com o nome do jovem).

---

### Apresentação da Documentação `README.md`

Abaixo encontras o conteúdo completo formatado em **Markdown**. Podes copiar diretamente o bloco abaixo e colá-lo num novo ficheiro chamado `README.md` na mesma pasta onde está o teu ficheiro Python.

```markdown
# 🤖 Automador de Aprovação de Atividades - Plataforma EAD

Este projeto consiste numa automação em Python desenvolvida com **Selenium WebDriver** para otimizar o processo de lançamento de notas e aprovação de atividades pendentes de alunos numa plataforma EAD.

O robô conecta-se a uma sessão ativa do Google Chrome, pesquisa o aluno desejado e processa continuamente todas as suas atividades com o status **Pendente**, atribuindo a nota **0,75** e retornando à listagem até que todas as pendências daquele aluno sejam concluídas.

---

## 📌 Funcionalidades

- **Conexão com Sessão Ativa:** Conecta-se ao navegador Google Chrome já aberto, evitando a necessidade de realizar login e resolver *captchas* a cada execução.
- **Busca Dinâmica:** Localiza o campo de pesquisa e filtra as atividades pelo nome do jovem informado.
- **Atribuição Automática de Nota:** Acessa a prova e seleciona automaticamente a opção de nota **0,75**.
- **Processamento Contínuo (Loop `while`):** Repete o ciclo automaticamente para todas as atividades pendentes do aluno até que a fila seja zerada.
- **Navegação Segura:** Utiliza comandos via JavaScript (`scrollIntoView` e `click`) para garantir a interação correta com os elementos visuais da página.

---

## 🛠️ Pré-requisitos

Antes de executar o projeto, certifique-se de ter instalado no seu computador:

1. **Python 3.x**: [Download do Python](https://www.python.org/downloads/)
2. **Google Chrome**: Navegador instalado.
3. **Biblioteca Selenium**: Instalada via terminal.

```bash
pip install selenium

```

---

## 🚀 Passo a Passo de Configuração e Execução

### Passo 1: Abrir o Google Chrome na Porta de Depuração (`9222`)

Para que o script controle a sua janela aberta do Chrome com o login já efetuado, é necessário iniciar o navegador através do **Prompt de Comando (CMD)** do Windows:

1. Feche todas as janelas abertas do Google Chrome.
2. Abra o **Prompt de Comando (CMD)** do Windows.
3. Cole e execute o seguinte comando:

```cmd
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\selenium\AutomationProfile"

```

### Passo 2: Acessar a Plataforma EAD

1. Na janela do Chrome que acabou de abrir, aceda à plataforma EAD.
2. Faça o seu login normalmente e navegue até a página de **Listagem de Provas/Atividades**.

### Passo 3: Executar o Script Python

1. Abra a pasta do projeto no **VS Code**.
2. Abra o ficheiro do script Python (ex: `automacao_provas.py`).
3. No final do ficheiro, defina o nome do aluno na variável `jovem_para_aprovar`:

```python
if __name__ == "__main__":
    # Insira aqui o nome do aluno que deseja processar:
    jovem_para_aprovar = "Leandro do Carmo Xavier"
    
    aprovar_todas_pendencias_aluno(jovem_para_aprovar)

```

4. Execute o ficheiro no terminal:

```bash
python automacao_provas.py

```

---

## 🧠 Como o Código Funciona (Estrutura)

1. **`Options.debuggerAddress = "127.0.0.1:9222"`**: Conecta o Selenium à janela do Chrome já aberta.
2. **`while True`**: Inicia um ciclo infinito para verificar e processar pendências.
3. **`campo_busca.send_keys(nome_aluno)`**: Pesquisa o nome do jovem na tabela.
4. **`espera_curta.until(...)`**: Tenta encontrar o texto *"Pendente"*. Se não encontrar mais nenhum registro, o laço é encerrado (`break`).
5. **`botao_nota` (0,75)**: Clica na nota desejada.
6. **`navegador.back()`**: Retorna para a página anterior para iniciar a próxima verificação.

---

## 📄 Licença e Uso

Projeto desenvolvido para fins educacionais e de automação de tarefas administrativas repetitivas.

```

---

### Instruções Detalhadas de Implementação

1. **Criar o Ficheiro no VS Code:**
   * No VS Code, clica no ícone de **Novo Ficheiro** na barra lateral esquerda.
   * Dá-lhe o nome exato: `README.md`.
2. **Colar o Conteúdo:**
   * Copia todo o código Markdown do bloco acima e cola dentro desse novo ficheiro `README.md`.
3. **Guardar o Ficheiro:**
   * Pressiona `Ctrl + S` para guardar.
4. **Visualizar a Formatação (Opcional):**
   * No VS Code, podes clicar com o botão direito no ficheiro `README.md` e selecionar **"Abrir Pré-visualização"** (ou usar o atalho `Ctrl + Shift + V`) para ver o resultado visual formatado com os ícones e blocos de código estilizados.
