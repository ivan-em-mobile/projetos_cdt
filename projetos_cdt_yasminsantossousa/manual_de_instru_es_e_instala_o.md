# 🍇 Guia Completo: Instalação, Execução e Empacotamento - Delírio Roxo

Este documento reúne todas as instruções necessárias para preparar o ambiente, instalar as bibliotecas corretas, executar o sistema de reconhecimento facial da açaíteria e esclarecer a viabilidade do uso do **PyInstaller**.

---

## 1. Pré-requisitos e Estrutura de Pastas

Certifica-te de que o teu projeto está organizado da seguinte forma no teu computador (dentro da pasta `projeto_cdt_larissarios`):

```text
projeto_cdt_larissarios/
│
├── main.py                 # Ficheiro principal (Interface Gráfica Tkinter)
├── acaiteria.db            # Base de dados SQLite com os clientes
├── requirements.txt        # Lista de dependências do projeto
└── src/
    ├── __init__.py         # Módulo vazio para reconhecimento de pacotes
    └── camera.py           # Módulo de visão computacional (OpenCV e DeepFace)
```

---

## 2. Passo a Passo: Instalação das Bibliotecas

Para garantir que o ambiente Python está limpo e preparado (especialmente se estiveste a lidar com conflitos anteriores), abre o terminal na pasta raiz do projeto e executa os seguintes comandos:

### Passo A: Atualizar o gestor de pacotes (pip)
```bash
py -m pip install --upgrade pip
```

### Passo B: Instalar as dependências essenciais
Instala o DeepFace com suporte ao TensorFlow, juntamente com o OpenCV e o Pandas:
```bash
py -m pip install "deepface[tensorflow]" opencv-python pandas
```

*Nota: O `tkinter` e o `sqlite3` já vêm integrados por defeito na grande maioria das instalações oficiais do Python.*

---

## 3. Como Executar o Aplicativo

Com todas as dependências instaladas com sucesso, podes iniciar a aplicação executando o ficheiro principal (`main.py`):

```bash
py main.py
```

Isto irá abrir a janela gráfica com o tema da açaíteria *"Delírio Roxo"*. Ao clicares em **"Iniciar Reconhecimento Facial"**, o sistema ativará a webcam para detetar o rosto do cliente.

---

## 4. É possível usar o PyInstaller para criar um executável (.exe)?

**Sim, é possível, mas com fortes ressalvas e dificuldades técnicas importantes.**

O **PyInstaller** é uma ferramenta fantástica para transformar scripts Python em ficheiros `.exe` portáteis. Contudo, quando o projeto envolve bibliotecas de Inteligência Artificial e Visão Computacional de grande porte como o **DeepFace**, **TensorFlow** e **OpenCV**, o processo de empacotamento apresenta grandes desafios:

### ⚠️ Principais Desafios ao usar o PyInstaller com DeepFace / TensorFlow:
1. **Ficheiros de Modelos de IA:** O DeepFace descarrega automaticamente pesos de redes neuronais (como `Facenet`, `VGG-Face`, etc.) na primeira execução para uma pasta oculta (`.deepface` no diretório de utilizador do Windows). O PyInstaller não consegue incluir estes ficheiros pesados automaticamente dentro do `.exe`, o que fará com que o executável falhe se for corrido num computador sem acesso à internet ou sem os pesos previamente descarregados.
2. **Tamanho Gigantesco:** As bibliotecas do TensorFlow e do OpenCV contêm centenas de megabytes em binários e dependências C++. O ficheiro `.exe` gerado poderá facilmente ultrapassar 1 GB ou mais.
3. **Erros de Caminhos Dinâmicos (Hidden Imports):** O TensorFlow faz muitas importações dinâmicas que o PyInstaller frequentemente falha em detetar automaticamente, exigindo a criação manual de ficheiros de especificação (`.spec`) complexos cheios de correções.

### 💡 Recomendação do Parceiro de Programação:
Para fins educacionais, de desenvolvimento ou testes locais, **a forma mais recomendada e estável de executar o projeto é através do próprio interpretador Python** (correndo `py main.py`), tal como tens feito até agora. 

Se o objetivo final for distribuir a aplicação para computadores de clientes ou funcionários sem Python instalado, métodos alternativos como criar um instalador com o **Inno Setup** contendo o ambiente Python comprimido costumam ser muito mais estáveis do que forçar um executável direto via PyInstaller para projetos de Deep Learning.