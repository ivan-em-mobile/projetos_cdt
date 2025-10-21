// --- Seleção de Elementos HTML ---
// Seleciona o elemento HTML com o ID 'memory-game' (onde as cartas serão exibidas)
const memoryGame = document.getElementById('memory-game');
// Seleciona o elemento 'span' com o ID 'moves-count' (onde o número de movimentos é mostrado)
const movesCountElement = document.getElementById('moves-count');
// Seleciona o botão com o ID 'restart-button'
const restartButton = document.getElementById('restart-button');

// --- Variáveis de Controle do Jogo ---
let cardsArray = []; // Um array vazio que vai guardar as informações de todas as cartas (ID e imagem)
const numPairs = 18; // Define o número de pares de cartas. Para uma grade 6x6, temos 36 cartas no total, então 18 pares.

let hasFlippedCard = false; // Sinaliza se uma carta já foi virada (true) ou se é o primeiro clique (false)
let lockBoard = false; // Uma "trava" para impedir que o jogador clique em mais cartas enquanto as duas cartas viradas estão sendo comparadas ou virando de volta
let firstCard, secondCard; // Variáveis para armazenar as duas cartas que foram viradas
let matchesFound = 0; // Contador de quantos pares já foram encontrados
let moves = 0; // Contador de quantos movimentos o jogador fez

// --- Imagens das Cartas ---
// Lista de URLs das imagens que serão usadas nas cartas.
// IMPORTANTE: Certifique-se de que os caminhos para as imagens estão corretos em seu projeto.
const cardImages = [
    './assets/img/img1.png', './assets/img/img2.png', './assets/img/img3.png', './assets/img/img4.png',
    './assets/img/img5.png', './assets/img/img6.png', './assets/img/img7.png', './assets/img/img8.png',
    './assets/img/img9.png', './assets/img/img10.png', './assets/img/img11.png', './assets/img/img12.png',
    './assets/img/img13.png', './assets/img/img14.png', './assets/img/img15.png', './assets/img/img16.png',
    './assets/img/img17.png', './assets/img/img18.png'
];

// --- Função Principal: Inicializa o Jogo ---
function initializeGame() {
    cardsArray = []; // Limpa o array de cartas para um novo jogo
    matchesFound = 0; // Reseta o contador de pares encontrados
    moves = 0; // Reseta o contador de movimentos
    movesCountElement.textContent = moves; // Atualiza o placar na tela para 0
    memoryGame.innerHTML = ''; // Limpa qualquer carta que possa estar no tabuleiro de um jogo anterior

    // --- Cria os Pares de Cartas ---
    // Para cada imagem na lista 'cardImages', cria duas entradas no 'cardsArray'
    // Cada entrada tem um 'id' (para identificar o par) e a 'image' (o caminho da imagem)
    for (let i = 0; i < numPairs; i++) {
        cardsArray.push({ id: i, image: cardImages[i] }); // Adiciona a primeira carta do par
        cardsArray.push({ id: i, image: cardImages[i] }); // Adiciona a segunda carta do par
    }

    shuffleCards(cardsArray); // Chama a função para embaralhar as cartas recém-criadas

    // --- Cria os Elementos HTML das Cartas no DOM ---
    // Para cada item no 'cardsArray' (que já está embaralhado):
    cardsArray.forEach(card => {
        // Cria um novo elemento 'div' que será a carta
        const memoryCard = document.createElement('div');
        memoryCard.classList.add('memory-card'); // Adiciona a classe CSS 'memory-card' para estilização
        memoryCard.dataset.id = card.id; // Armazena o ID do par na carta usando 'dataset' (útil para comparar)

        // Cria a imagem da "frente" da carta
        const frontFace = document.createElement('img');
        frontFace.classList.add('front-face'); // Adiciona a classe CSS 'front-face'
        frontFace.src = card.image; // Define o caminho da imagem para a frente da carta
        frontFace.alt = 'Card Front'; // Texto alternativo para acessibilidade

        // Cria a imagem do "verso" da carta
        const backFace = document.createElement('img');
        backFace.classList.add('back-face'); // Adiciona a classe CSS 'back-face'
        // IMPORTANTE: Defina o caminho para a imagem do verso da carta.
        backFace.src = './assets/img/card_back.jpg';
        backFace.alt = 'Card Back';

        // Adiciona as faces (frente e verso) como "filhos" dentro da div da carta
        memoryCard.appendChild(frontFace);
        memoryCard.appendChild(backFace);

        // Remove quaisquer classes 'flip' ou 'match' que a carta possa ter tido de um jogo anterior
        memoryCard.classList.remove('flip', 'match');
        // Adiciona um "ouvinte de evento" (event listener) de clique a cada carta.
        // Quando a carta for clicada, a função 'flipCard' será executada.
        memoryCard.addEventListener('click', flipCard);
        // Adiciona a carta completa (memoryCard) ao elemento 'memory-game' no HTML
        memoryGame.appendChild(memoryCard);
    });
}

// --- Função para Embaralhar as Cartas (Algoritmo de Fisher-Yates) ---
// Este algoritmo garante que as cartas sejam embaralhadas de forma realmente aleatória
function shuffleCards(array) {
    // Percorre o array de trás para frente
    for (let i = array.length - 1; i > 0; i--) {
        // Gera um índice aleatório 'j' entre 0 e 'i'
        const j = Math.floor(Math.random() * (i + 1));
        // Troca os elementos nas posições 'i' e 'j'
        [array[i], array[j]] = [array[j], array[i]];
    }
}

// --- Função para Virar a Carta (Chamada ao Clicar) ---
function flipCard() {
    if (lockBoard) return; // Se o tabuleiro estiver "travado" (aguardando comparação), sai da função e não faz nada
    if (this === firstCard) return; // Evita que o jogador clique na mesma carta duas vezes seguidas

    // Adiciona a classe 'flip' à carta clicada. Esta classe, definida no CSS, faz a carta girar.
    this.classList.add('flip');

    if (!hasFlippedCard) {
        // Se esta é a PRIMEIRA carta a ser virada:
        hasFlippedCard = true; // Marca que uma carta já foi virada
        firstCard = this; // Armazena a referência para esta carta como a 'firstCard'
        return; // Sai da função, aguardando o segundo clique
    }

    // Se chegou aqui, é a SEGUNDA carta a ser virada:
    secondCard = this; // Armazena a referência para esta carta como a 'secondCard'
    moves++; // Incrementa o contador de movimentos
    movesCountElement.textContent = moves; // Atualiza o placar na tela

    checkForMatch(); // Chama a função para verificar se as duas cartas formam um par
}

// --- Função para Verificar se as Cartas Formam um Par ---
function checkForMatch() {
    // Compara o 'dataset.id' (que armazenamos o ID do par) das duas cartas
    let isMatch = firstCard.dataset.id === secondCard.dataset.id;

    if (isMatch) {
        disableCards(); // Se for um par, "desativa" as cartas
    } else {
        unflipCards(); // Se não for um par, vira as cartas de volta
    }
}

// --- Função para Desativar Cartas que Formaram um Par ---
function disableCards() {
    // Remove o "ouvinte de clique" das duas cartas. Isso impede que elas sejam clicadas novamente.
    firstCard.removeEventListener('click', flipCard);
    secondCard.removeEventListener('click', flipCard);

    // Adiciona a classe 'match'. O CSS usa essa classe para garantir que a carta não seja clicável.
    firstCard.classList.add('match');
    secondCard.classList.add('match');

    matchesFound++; // Incrementa o contador de pares encontrados
    // Verifica se todos os pares foram encontrados
    if (matchesFound === numPairs) {
        // Se sim, espera um pouco (500ms) e então exibe um alerta de vitória
        setTimeout(() => {
            alert(`Parabéns! Você encontrou todos os pares em ${moves} movimentos!`);
        }, 500);
    }

    resetBoard(); // Reseta as variáveis de controle para o próximo turno
}

// --- Função para Virar as Cartas de Volta (se não for um par) ---
function unflipCards() {
    lockBoard = true; // "Trava" o tabuleiro para que o jogador não clique em outras cartas enquanto estas viram

    // Espera um tempo (1000ms = 1 segundo) antes de virar as cartas de volta
    setTimeout(() => {
        firstCard.classList.remove('flip'); // Remove a classe 'flip', fazendo a primeira carta virar de volta
        secondCard.classList.remove('flip'); // Remove a classe 'flip', fazendo a segunda carta virar de volta
        resetBoard(); // Reseta as variáveis de controle do tabuleiro após as cartas virarem
    }, 1000);
}

// --- Função para Resetar as Variáveis de Controle do Tabuleiro ---
// Prepara o jogo para o próximo par de cliques
function resetBoard() {
    [hasFlippedCard, lockBoard] = [false, false]; // Reseta 'hasFlippedCard' e 'lockBoard' para 'false'
    [firstCard, secondCard] = [null, null]; // Limpa as referências das cartas viradas
}

// --- Event Listener para o Botão de Reiniciar ---
// Quando o botão de reiniciar for clicado, a função 'initializeGame' é chamada novamente
restartButton.addEventListener('click', initializeGame);

// --- Início do Jogo ---
// Chama a função 'initializeGame' quando a página é carregada pela primeira vez,
// para montar o tabuleiro e começar o jogo.
initializeGame();