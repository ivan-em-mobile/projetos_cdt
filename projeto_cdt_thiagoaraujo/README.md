# TamaFoco — Versão executável para Windows

Eu e meu grupo decidimos cria o : **TamagotchiProdutividade** é um tamagotchi de produtividade para Windows. O mascote acompanha as atividades realizadas no computador, reage ao tipo de aplicativo aberto e recompensa períodos produtivos com pontos, experiência, níveis e conquistas.

Esta documentação é destinada à versão executável `TamagotchiProdutividade.exe`.

## Requisitos

- Windows 10 ou Windows 11, preferencialmente em 64 bits.
- Aproximadamente 200 MB de espaço livre.
- Permissão para executar aplicativos baixados.
- Notificações do Windows ativadas, caso queira receber lembretes.

Depois que o executável estiver pronto, não será necessário instalar Python para utilizá-lo.

## Estrutura da versão executável

Mantenha todos os arquivos dentro da mesma pasta:

```text
TamaFoco/
├── TamaFoco.exe
├── assets/
│   ├── accessories/
│   ├── pets/
│   └── rewards/
└── README_EXE.md
```

Não mova apenas o `TamaFoco.exe` para outro local. A pasta `assets` contém as imagens dos mascotes, acessórios e recompensas utilizadas pelo programa.

Para criar um atalho, clique com o botão direito no executável e escolha **Enviar para → Área de trabalho (criar atalho)**.

## Como abrir

1. Extraia todo o conteúdo do arquivo ZIP.
2. Abra a pasta extraída.
3. Clique duas vezes em `TamaFoco.exe`.
4. Aguarde alguns segundos durante a primeira inicialização.

Caso o Windows SmartScreen mostre um aviso, confirme que o arquivo veio de uma fonte confiável, clique em **Mais informações** e depois em **Executar assim mesmo**.

## Primeira configuração

Na primeira execução, informe:

- nome do responsável;
- apelido;
- nome do mascote;
- meta diária de foco.

As informações e o progresso são salvos automaticamente no arquivo `tamagotchi_state.json`.

## Funcionalidades

- Detecção do aplicativo ativo no computador.
- Mudança de humor conforme atividades produtivas ou distrações.
- Sistema de felicidade, pontos, experiência e níveis.
- Cronômetro e registro do tempo de foco.
- Meta diária e lembretes de pausa.
- Conquistas desbloqueáveis.
- Central de recompensas inspirada no Microsoft Rewards.
- Gift cards conceituais e cosméticos com imagens.
- Skins de mascotes e acessórios.
- Temas claro e escuro.
- Pet flutuante, transparente e sem caixa ao minimizar.
- Pet arrastável com o mouse.
- Salvamento automático do progresso.

## Pet flutuante

Ao minimizar a janela principal, somente o mascote permanecerá flutuando sobre a tela.

- Segure o botão esquerdo do mouse e arraste para mudar o pet de lugar.
- Dê dois cliques no mascote para abrir novamente o programa.
- Clique com o botão direito para acessar as opções de abrir ou fechar.
- O pet poderá mudar de expressão conforme o aplicativo utilizado.

Também é possível ativar esse modo pelo botão **Modo flutuante** na tela inicial.

## Aplicativos produtivos e distrações

O programa possui uma lista inicial de aplicativos e palavras-chave:

- Produtivos: Visual Studio Code, GitHub e ferramentas relacionadas.
- Distrações: Instagram, TikTok, WhatsApp e YouTube.
- Neutros: programas que não correspondem às listas anteriores.

Essas listas podem ser alteradas no início do arquivo `tamagotchi_produtividade_completo.py` antes de gerar uma nova versão do executável.

## Dados e backup

O progresso é armazenado no arquivo:

```text
tamagotchi_state.json
```

Para criar um backup:

1. Feche o TamaFoco.
2. Copie o arquivo `tamagotchi_state.json`.
3. Guarde a cópia em uma pasta segura.

Para restaurar o progresso, coloque o arquivo novamente na pasta do programa antes de abrir o executável.

Apagar esse arquivo fará o aplicativo iniciar com um novo perfil.

## Solução de problemas

### O programa não abre

- Extraia o ZIP antes de executar.
- Não abra o executável diretamente de dentro do ZIP.
- Verifique se o antivírus colocou o arquivo em quarentena.
- Tente executar como administrador somente para diagnóstico.

### As imagens não aparecem

- Confirme que a pasta `assets` está ao lado de `TamaFoco.exe`.
- Não altere os nomes das pastas ou das imagens.
- Extraia novamente o pacote completo.

### O pet não identifica o aplicativo aberto

- Alguns aplicativos protegidos podem impedir a leitura da janela ativa.
- Execute o TamaFoco e o aplicativo monitorado com o mesmo nível de permissão.
- Feche e abra novamente o TamaFoco.

### As notificações não aparecem

Abra **Configurações do Windows → Sistema → Notificações** e confirme que as notificações estão ativadas.

### O progresso desapareceu

Procure pelo arquivo `tamagotchi_state.json`. Se ele tiver sido removido, restaure uma cópia de segurança.

## Gift cards e recompensas

Os cartões presente exibidos no programa são artes ilustrativas. Ainda não existe compra, estoque, código de resgate ou parceria oficial com Xbox, PlayStation, Centauro, Microsoft, Roblox ou outras marcas citadas.

## Como gerar o executável

Esta etapa é necessária somente para quem possui o código-fonte e deseja criar o `TamaFoco.exe`.

### 1. Instale o Python

Instale o Python 3.11 ou mais recente e marque a opção **Add Python to PATH**.

### 2. Instale as dependências

Abra o Prompt de Comando na pasta do projeto e execute:

```powershell
py -m pip install pyinstaller psutil pygetwindow plyer pillow
```

### 3. Gere o executável

Execute o comando:

```powershell
py -m PyInstaller --noconfirm --clean --windowed --onedir --contents-directory . --name TamaFoco --add-data "assets;assets" --collect-all plyer tamagotchi_produtividade_completo.py
```

Ao finalizar, a versão executável estará em:

```text
dist/TamaFoco/TamaFoco.exe
```

Distribua a pasta completa `dist/TamaFoco`. Não envie somente o arquivo `.exe`.

## Arquivos do código-fonte

- `tamagotchi_produtividade_completo.py`: aplicativo principal.
- `assets`: imagens utilizadas na interface.
- `create_catalog_assets.py`: recria as imagens do catálogo.
- `LEIA-ME.txt`: instruções da versão em Python.
- `README_EXE.md`: instruções da versão executável.

---

O TamaFoco foi criado para unir produtividade, bem-estar digital, personalização e recompensas em uma experiência simples e divertida.
