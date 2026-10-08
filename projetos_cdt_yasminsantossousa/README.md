🎯 Projeto Final: Sistema de Reconhecimento Facial - Açaíteria Delírio Roxo

Olá! 👋 Bem-vindo ao repositório do projeto final do curso Código_Transformação. Este sistema foi desenvolvido para automatizar e modernizar a experiência de atendimento na açaíteria "Delírio Roxo", unindo Visão Computacional, Deep Learning e um banco de dados relacional.
O projeto integra reconhecimento facial em tempo real com a recuperação automática dos pedidos favoritos dos clientes cadastrados.

💻 Visão Geral do Projeto

O sistema utiliza a webcam para capturar o rosto do cliente no balcão. Por meio de inteligência artificial, ele verifica se a pessoa já possui cadastro:
* **Cliente Antigo:** Reconhece o rosto, identifica o nome e exibe instantaneamente o seu açaí preferido.
* **Cliente Novo:** Identifica que o rosto não está no sistema e direciona o fluxo para o cadastro de um novo perfil.

🛠️ Tecnologias Utilizadas:

* **Linguagem:** Python 3
* **Visão Computacional & Câmera:** OpenCV (`cv2`)
* **Inteligência Artificial (Reconhecimento Facial):** DeepFace (com modelos de Deep Learning)
* **Banco de Dados:** SQLite3 (Relacional)
* **Interface Gráfica (GUI):** Tkinter (Nativo do Python)

⚙️ Regras de Negócio e Funcionalidades

* **Biometria Real:** Substituição de simulações por verificação facial real utilizando algoritmos de *embeddings* faciais do DeepFace.
* **Modularidade do Código:** Separação clara entre a lógica de inteligência artificial/câmera (`src/camera.py`) e a interface visual para o atendente (`main.py`).
* **Tratamento de Exceções:** Validação de erros caso a webcam esteja indisponível ou o banco de dados esteja vazio.

🗄️ Estrutura do Banco de Dados (`acaiteria.db`)

O banco de dados armazena as informações essenciais dos clientes para o funcionamento da açaíteria:
* `id`: Identificador único do cliente
* `nome`: Nome completo do cliente
* `acai_preferido`: O sabor e os adicionais favoritos do cliente
* `foto_path`: O caminho local da foto salva no momento do cadastro para a comparação biométrica do DeepFace

📂 Estrutura de Arquivos do Repositório

PROJETO_CDT_LARRISASOUZAPY/
│
├── src/
│   └── camera.py       # Módulo de Visão Computacional e DeepFace
├── acaiteria.db        # Banco de dados SQLite com os registros e caminhos das fotos
├── main.py             # Código principal com a Interface Gráfica (GUI - Tkinter)
├── requirements.txt    # Dependências do projeto (OpenCV, DeepFace, etc.)
└── README.md           # Documentação oficial do projeto

🚀 Como Testar e Rodar o Projeto Localmente

Se quiseres clonar e executar este projeto na tua máquina local, segue estes passos simples:

1. Clonar o Repositório
```bash
git clone [https://github.com/larissasouzapy/projeto_cdt.git](https://github.com/larissasouzapy/projeto_cdt.git)
cd projeto_cdt
