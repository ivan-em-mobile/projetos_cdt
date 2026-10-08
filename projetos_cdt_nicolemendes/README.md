
**TamaFoco (Tamagotchi da Produtividade)**.

---

### 1. Compreensão do Objetivo

Analisando o arquivo em Python (`app_tamafoco_nicolemendes.py`) e a documentação original (`README.md`), o objetivo é consolidar a documentação oficial para refletir todas as funcionalidades e evoluções implementadas no código:

* **Atualização do nome do arquivo:** Alterar todas as referências do código-fonte para `app_tamafoco_nicolemendes.py`.


* **Documentação Técnica Completa:** Incluir detalhes sobre os temas visualmente renovados (modo claro/escuro com paleta Microsoft Rewards), cálculo dinâmico de XP/níveis, detecção automática de janelas ativas por sistema, motor de desenho 3D suavizado (sem serrilhamento via Pillow/LANCZOS) e o modo de mascotinho flutuante/transparente.


* **Formatação Pronta para Markdown:** Disponibilizar o código em um bloco de fácil cópia e colagem.

---

### 2. Panorama Geral da Documentação

O novo `README.md` foi estruturado nas seguintes seções:

1. **Cabeçalho & Apresentação:** Título, visão geral e objetivo do projeto.


2. **Funcionalidades Principais:** Destaques como mascotinho 3D, modo flutuante transparente, alternância de temas, lojas, estatísticas e sistema de pontuação.


3. **Requisitos de Sistema e Dependências:** Lista completa de bibliotecas Python (`Pillow`, `psutil`, `pygetwindow`, `plyer`).


4. **Estrutura de Arquivos:** Organização do projeto com o arquivo `app_tamafoco_nicolemendes.py` e a pasta `assets/`.


5. **Como Executar o Código:** Passo a passo para rodar no ambiente Python.


6. **Como Gerar o Executável (`.exe`):** Instruções atualizadas usando PyInstaller para compilar o arquivo correto.


7. **Regras de Produtividade & Persistência:** Como funciona o algoritmo de pontos e onde os dados são salvos (`tamagotchi_state.json`).


8. **Solução de Problemas:** Guia rápido para falhas comuns.



---

### 3. Conteúdo Completo em Markdown

Aqui está o **README.md** atualizado. Podes clicar no botão de cópia no canto superior do bloco abaixo para copiar diretamente para o teu projeto:

```markdown
# 🐣 TamaFoco — Tamagotchi da Produtividade

O **TamaFoco** (Tamagotchi da Produtividade) é uma aplicação desktop desenvolvida em Python e Tkinter que transforma o foco no trabalho e nos estudos em um jogo divertido. O mascote acompanha o teu computador em tempo real, reage aos aplicativos ou sites abertos e recompensa períodos produtivos com pontos, experiência (XP), novos níveis, conquistas e cosméticos.

---

## 🌟 Funcionalidades Principais

- **Mascote 3D Suave e Expressivo:** Desenho tridimensional gerado via código com efeitos de luz, sombra e reamostragens em alta definição (anti-aliasing via LANCZOS).
- **Modo Flutuante e Transparente:** Ao minimizar a aplicação, o mascote flutua sozinho sobre a área de trabalho sem molduras ou barras visíveis. É arrastável com o mouse e possui expressões em tempo real.
- **Monitoramento de Produtividade:** Identificação automática da janela ativa e dos processos no computador (suporte para Windows, macOS e Linux).
- **Temas Claro e Escuro:** Interface visual moderna e limpa inspirada no ecossistema do Microsoft Rewards, com alternância instantânea.
- **Sistema de Pontuação e Progressão:**
  - Felicidade dinâmica do mascote (com alteração de expressão e humor).
  - Experiência (XP) e níveis progressivos.
  - Sequência diária (*streak*) e metas personalizáveis de foco.
- **Central de Recompensas e Personalização:**
  - Desbloqueio de skins de mascotes (Gato, Cachorro, Coelho, Raposa, Panda).
  - Acessórios visuais (Óculos, Boné, Laço, Coroa).
  - Cartões-presente conceituais (Xbox, PlayStation, Centauro, Microsoft, Roblox, etc.).
- **Lembretes de Saúde Digital:** Alertas para pausas recomendadas a cada 25 minutos de foco contínuo.
- **Conquistas Desbloqueáveis:** Sistema de medalhas com recompensas em pontos.
- **Persistência Automática:** Salvamento constante do progresso em arquivo JSON.

---

## 📋 Requisitos e Dependências

Para executar o código-fonte Python, é recomendado o **Python 3.10 ou superior**.

### Bibliotecas Utilizadas
- **`tkinter` / `ttk`:** Interface gráfica nativa.
- **`Pillow` (PIL):** Renderização de artes do catálogo e anti-aliasing em alta definição.
- **`psutil`:** Leitura de processos ativos no sistema operacional.
- **`pygetwindow`:** Identificação do título da janela ativa no Windows.
- **`plyer`:** Envio de notificações nativas do sistema.

Instale todas as dependências necessárias com o comando:

```bash
pip install pillow psutil pygetwindow plyer

```

---

## 📂 Estrutura do Projeto

Mantenha os arquivos e pastas organizados da seguinte forma:

```text
TamaFoco/
├── app_tamafoco_nicolemendes.py   # Código-fonte principal do programa
├── create_catalog_assets.py       # Script utilitário para gerar/restaurar artes
├── tamagotchi_state.json          # Arquivo gerado automaticamente com o seu progresso
├── assets/                        # Pasta de recursos visuais do catálogo
│   ├── accessories/               # Imagens PNG dos acessórios
│   ├── pets/                      # Imagens PNG dos mascotes
│   └── rewards/                   # Imagens PNG das recompensas e cartões
└── README.md                      # Documentação do projeto

```

> **Nota:** Caso a pasta `assets` esteja ausente ou incompleta, execute o script `create_catalog_assets.py` uma vez para gerar automaticamente todas as 23 artes originais em PNG.

---

## 🚀 Como Executar o Código Python

1. Clone ou baixe este repositório para o seu computador.
2. Abra o terminal ou Prompt de Comando na pasta do projeto.
3. Certifique-se de que instalou as dependências informadas acima.
4. Execute o aplicativo com o comando:

```bash
python app_tamafoco_nicolemendes.py

```

---

## 🛠️ Como Gerar a Versão Executável (`.exe` para Windows)

Se desejas criar um arquivo executável standalone (`TamaFoco.exe`) para distribuir sem a necessidade de instalar o Python:

1. Instale o **PyInstaller**:
```powershell
pip install pyinstaller

```


2. Execute o comando de compilação apontando para o arquivo do projeto:
```powershell
py -m PyInstaller --noconfirm --clean --windowed --onedir --contents-directory . --name TamaFoco --add-data "assets;assets" --collect-all plyer app_tamafoco_nicolemendes.py

```


3. Ao finalizar a compilação, a pasta pronta para distribuição estará em:
```text
dist/TamaFoco/

```


> **Importante:** Sempre distribua a pasta `TamaFoco` inteira contendo o `TamaFoco.exe` e a subpasta `assets`.



---

## 🎯 Regras de Classificação e Pontuação

### Classificação de Atividades

* **Produtivas:** Janelas ou processos contendo termos como *Visual Studio Code, VS Code, GitHub Desktop, GitHub*, entre outros.
* **Distrações:** Janelas ou processos contendo *Instagram, TikTok, WhatsApp, YouTube*.
* **Neutras:** Demais aplicativos que não estejam mapeados nas palavras-chave.

### Recompensas por Foco

* A cada *tick* (3 segundos) em atividade produtiva: **+10 XP** e **+2 Pontos**.
* Recuperação contínua de felicidade.
* Conclusão da meta diária: **+50 XP** e **+50 Pontos**.

---

## 💾 Salvamento de Dados e Backup

Todos os dados de perfil, progresso, pontos, itens resgatados, histórico de tempo e configurações de tela são armazenados no arquivo:

```text
tamagotchi_state.json

```

* **Backup:** Para guardar o seu progresso, basta fazer uma cópia de segurança deste arquivo.
* **Restauração:** Coloque o arquivo de backup na pasta do programa antes de iniciá-lo.
* **Reiniciar Perfil:** Se apagar este arquivo, o sistema iniciará uma nova jornada a partir do nível 1.

---

## ❓ Solução de Problemas

* **As imagens do catálogo não aparecem:** Certifique-se de que a pasta `assets/` está no mesmo diretório do arquivo `.py` (ou do `.exe`). Execute `python create_catalog_assets.py` para recriá-las.
* **O mascote não detecta a janela ativa:** Alguns programas executados como Administrador podem bloquear a leitura do título da janela por programas de usuário comum. Tente executar o TamaFoco com permissões equivalentes.
* **Notificações não são exibidas:** Confirme nas **Configurações do Sistema** do seu sistema operacional se as notificações e a Assistência de Foco/Não Perturbe estão permitindo alertas de aplicativos em segundo plano.

---

## 📢 Aviso Legal / Importante

Os cartões-presente (*Gift Cards*) de marcas como Xbox, PlayStation, Centauro, Microsoft e Roblox exibidos na Central de Recompensas são **ilustrativos e conceituais**, destinados exclusivamente para a experiência de gamificação do projeto. Não há compra real, estoque, geração de códigos ou qualquer vínculo/parceria oficial com as empresas citadas.

---

*Desenvolvido para unir produtividade, bem-estar digital, foco e diversão.*

