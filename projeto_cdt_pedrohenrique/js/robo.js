/*
=========================================================
ROBO ASSISTENTE - BURGER HOUSE 🍔🤖
Assistente virtual para montar pedidos
=========================================================
*/

let pedido = [];
let etapa = "inicio";
let produtoSelecionado = null;

let dadosCliente = {
    nome: "",
    entrega: "",
    endereco: "",
    pagamento: ""
};


// ======================================================
// ELEMENTOS DA PÁGINA
// ======================================================

const mensagens = document.getElementById("mensagens");
const entrada = document.getElementById("entradaUsuario");


// ======================================================
// ADICIONAR MENSAGEM
// ======================================================

function adicionarMensagem(texto, tipo = "robo") {

    if (!mensagens) {
        return;
    }

    const div = document.createElement("div");

    div.className =
        tipo === "cliente"
            ? "mensagem-cliente"
            : "mensagem-robo";

    div.innerHTML = escapar(texto);

    mensagens.appendChild(div);

    mensagens.scrollTop = mensagens.scrollHeight;
}


// ======================================================
// ESCAPAR TEXTO
// ======================================================

function escapar(txt) {

    const div = document.createElement("div");

    div.textContent = String(
        txt == null ? "" : txt
    );

    return div.innerHTML.replace(/\n/g, "<br>");
}


// ======================================================
// NORMALIZAR TEXTO
// ======================================================

function normalizar(texto) {

    return String(texto)
        .toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .trim();
}


// ======================================================
// ENVIAR MENSAGEM
// ======================================================

function enviarMensagem() {

    if (!entrada) {
        return;
    }

    const texto = entrada.value.trim();

    if (!texto) {
        return;
    }

    adicionarMensagem(texto, "cliente");

    entrada.value = "";

    responderCliente(texto);
}


// ======================================================
// RESPONDER CLIENTE
// ======================================================

function responderCliente(texto) {

    const mensagem = normalizar(texto);


    // --------------------------------------------------
    // NOVO PEDIDO
    // --------------------------------------------------

    if (
        mensagem.includes("novo pedido") ||
        mensagem.includes("comecar de novo")
    ) {

        novoPedido();

        return;
    }


    // --------------------------------------------------
    // PEDIDO JÁ FINALIZADO
    // --------------------------------------------------

    if (etapa === "finalizado") {

        adicionarMensagem(
            "Seu pedido anterior já foi confirmado. 😄"
        );

        adicionarMensagem(
            'Digite "novo pedido" para fazer outro.'
        );

        return;
    }


    // --------------------------------------------------
    // SAUDAÇÕES
    // --------------------------------------------------

    if (
        mensagem === "oi" ||
        mensagem === "ola" ||
        mensagem === "oii" ||
        mensagem === "oie" ||
        mensagem.includes("bom dia") ||
        mensagem.includes("boa tarde") ||
        mensagem.includes("boa noite")
    ) {

        adicionarMensagem(
            "Olá! 😄🍔 Sou o atendente virtual da Burger House!"
        );

        adicionarMensagem(
            'Posso ajudar você a montar seu pedido. Digite "cardápio" para ver os produtos.'
        );

        return;
    }


    // --------------------------------------------------
    // CARDÁPIO
    // --------------------------------------------------

    if (
        mensagem.includes("cardapio") ||
        mensagem.includes("menu") ||
        mensagem.includes("produtos")
    ) {

        mostrarCardapio();

        return;
    }


    // --------------------------------------------------
    // VER PEDIDO
    // --------------------------------------------------

    if (
        mensagem.includes("meu pedido") ||
        mensagem.includes("meu carrinho") ||
        mensagem === "pedido" ||
        mensagem === "carrinho"
    ) {

        mostrarPedido();

        return;
    }


    // --------------------------------------------------
    // LIMPAR PEDIDO
    // --------------------------------------------------

    if (
        mensagem.includes("limpar pedido") ||
        mensagem.includes("limpar carrinho") ||
        mensagem.includes("apagar pedido") ||
        mensagem.includes("zerar pedido")
    ) {

        pedido = [];
        produtoSelecionado = null;

        etapa = "escolhendo";

        adicionarMensagem(
            "🧹 Pronto! Seu pedido foi limpo."
        );

        adicionarMensagem(
            'Digite "cardápio" para escolher novamente.'
        );

        return;
    }


    // --------------------------------------------------
    // REMOVER PRODUTO
    // --------------------------------------------------

    if (
        mensagem.includes("remover") ||
        mensagem.includes("tirar")
    ) {

        removerProduto(texto);

        return;
    }


    // --------------------------------------------------
    // FINALIZAR PEDIDO
    // --------------------------------------------------

    if (
        mensagem.includes("finalizar") ||
        mensagem.includes("terminar") ||
        mensagem.includes("concluir")
    ) {

        iniciarFinalizacao();

        return;
    }


    // ==================================================
    // ETAPA: QUANTIDADE
    // ==================================================

    if (etapa === "quantidade") {

        processarQuantidade(texto);

        return;
    }


    // ==================================================
    // ETAPA: MAIS PRODUTOS
    // ==================================================

    if (etapa === "mais") {

        if (
            mensagem === "sim" ||
            mensagem === "s" ||
            mensagem.includes("quero mais") ||
            mensagem.includes("mais um") ||
            mensagem.includes("mais uma")
        ) {

            etapa = "escolhendo";

            adicionarMensagem(
                "Perfeito! 😄🍔 Qual outro produto você deseja?"
            );

            return;
        }


        if (
            mensagem === "nao" ||
            mensagem === "n" ||
            mensagem.includes("nao quero")
        ) {

            iniciarFinalizacao();

            return;
        }


        adicionarMensagem(
            'Digite "sim" para adicionar mais produtos ou "não" para finalizar.'
        );

        return;
    }


    // ==================================================
    // ETAPA: NOME
    // ==================================================

    if (etapa === "nome") {

        if (texto.length < 2) {

            adicionarMensagem(
                "Por favor, digite seu nome."
            );

            return;
        }

        dadosCliente.nome = texto;

        etapa = "entrega";

        adicionarMensagem(
            "Prazer, " + dadosCliente.nome + "! 😄"
        );

        adicionarMensagem(
            'Você deseja receber o pedido por "entrega" ou fazer "retirada"?'
        );

        return;
    }


    // ==================================================
    // ETAPA: ENTREGA OU RETIRADA
    // ==================================================

    if (etapa === "entrega") {

        if (
            mensagem.includes("entrega") ||
            mensagem.includes("delivery")
        ) {

            dadosCliente.entrega = "Entrega";

            etapa = "endereco";

            adicionarMensagem(
                "🏠 Certo! Digite o endereço de entrega."
            );

            return;
        }


        if (
            mensagem.includes("retirada") ||
            mensagem.includes("buscar")
        ) {

            dadosCliente.entrega = "Retirada";

            etapa = "pagamento";

            adicionarMensagem(
                "👍 Beleza! Você fará a retirada na Burger House."
            );

            adicionarMensagem(
                "Agora escolha a forma de pagamento: dinheiro, pix, débito ou crédito."
            );

            return;
        }


        adicionarMensagem(
            'Digite apenas "entrega" ou "retirada".'
        );

        return;
    }


    // ==================================================
    // ETAPA: ENDEREÇO
    // ==================================================

    if (etapa === "endereco") {

        if (texto.length < 5) {

            adicionarMensagem(
                "Por favor, digite um endereço válido."
            );

            return;
        }

        dadosCliente.endereco = texto;

        etapa = "pagamento";

        adicionarMensagem(
            "📍 Endereço registrado!"
        );

        adicionarMensagem(
            "Agora escolha a forma de pagamento: dinheiro, pix, débito ou crédito."
        );

        return;
    }


    // ==================================================
    // ETAPA: PAGAMENTO
    // ==================================================

    if (etapa === "pagamento") {

        if (mensagem.includes("dinheiro")) {

            dadosCliente.pagamento = "Dinheiro";

        } else if (mensagem.includes("pix")) {

            dadosCliente.pagamento = "Pix";

        } else if (mensagem.includes("debito")) {

            dadosCliente.pagamento = "Débito";

        } else if (mensagem.includes("credito")) {

            dadosCliente.pagamento = "Crédito";

        } else {

            adicionarMensagem(
                "Escolha uma opção: dinheiro, pix, débito ou crédito."
            );

            return;
        }

        etapa = "confirmacao";

        mostrarResumo();

        return;
    }


    // ==================================================
    // ETAPA: CONFIRMAÇÃO
    // ==================================================

    if (etapa === "confirmacao") {

        if (
            mensagem === "sim" ||
            mensagem === "s" ||
            mensagem.includes("confirmo") ||
            mensagem.includes("confirmar")
        ) {

            confirmarPedido();

            return;
        }


        if (
            mensagem === "nao" ||
            mensagem === "n"
        ) {

            adicionarMensagem(
                "Tudo bem! 😄 Seu pedido ainda não foi confirmado."
            );

            adicionarMensagem(
                'Digite "pedido" para consultar ou "limpar pedido" para começar novamente.'
            );

            etapa = "escolhendo";

            return;
        }


        adicionarMensagem(
            'Deseja confirmar o pedido? Digite "sim" ou "não".'
        );

        return;
    }


    // ==================================================
    // PROCURAR PRODUTO
    // ==================================================

    const produto = encontrarProduto(texto);

    if (produto) {

        produtoSelecionado = produto;

        const quantidade = extrairQuantidade(texto);

        if (quantidade !== null) {

            adicionarAoPedido(
                produto,
                quantidade
            );

            produtoSelecionado = null;

            perguntarMais();

            return;
        }


        etapa = "quantidade";

        adicionarMensagem(
            produto.nome +
            " — " +
            formatarDinheiro(
                converterPreco(produto.preco)
            )
        );

        adicionarMensagem(
            "Quantas unidades você deseja?"
        );

        return;
    }


    // ==================================================
    // MENSAGENS GENÉRICAS
    // ==================================================

    if (
        mensagem.includes("comprar") ||
        mensagem.includes("quero") ||
        mensagem.includes("pedir")
    ) {

        adicionarMensagem(
            'Claro! 🍔 Digite o nome do produto ou escreva "cardápio" para ver as opções.'
        );

        return;
    }


    adicionarMensagem(
        '🤔 Não consegui entender. Digite "cardápio", "pedido" ou o nome de um produto.'
    );
}


// ======================================================
// MOSTRAR CARDÁPIO
// ======================================================

function mostrarCardapio() {

    if (
        typeof ITENS === "undefined" ||
        !Array.isArray(ITENS)
    ) {

        adicionarMensagem(
            "⚠️ Não consegui carregar o cardápio."
        );

        return;
    }


    let textoCardapio =
        "🍔 ===== CARDÁPIO BURGER HOUSE =====\n\n";


    ITENS.forEach(function (item, index) {

        textoCardapio +=
            (index + 1) +
            ". " +
            item.nome +
            " — " +
            formatarDinheiro(
                converterPreco(item.preco)
            ) +
            "\n" +
            item.descricao +
            "\n\n";
    });


    textoCardapio +=
        "Digite o nome do produto que deseja pedir.";


    adicionarMensagem(
        textoCardapio
    );


    etapa = "escolhendo";
}


// ======================================================
// ENCONTRAR PRODUTO
// ======================================================

function encontrarProduto(texto) {

    if (
        typeof ITENS === "undefined" ||
        !Array.isArray(ITENS)
    ) {

        return null;
    }


    const mensagem = normalizar(texto);


    // Primeiro tenta pelo nome completo
    for (const item of ITENS) {

        const nome = normalizar(item.nome);

        if (mensagem.includes(nome)) {

            return item;
        }
    }


    // Depois procura por palavras do produto
    for (const item of ITENS) {

        const nome = normalizar(item.nome)
            .replace(/[🍔🍟🥤🧃]/g, "")
            .trim();


        const palavras = nome
            .split(/\s+/)
            .filter(function (palavra) {

                return palavra.length >= 3;

            });


        for (const palavra of palavras) {

            if (mensagem.includes(palavra)) {

                return item;
            }
        }
    }


    return null;
}


// ======================================================
// EXTRAIR QUANTIDADE
// ======================================================

function extrairQuantidade(texto) {

    const mensagem = normalizar(texto);


    const numero = mensagem.match(/\b(\d+)\b/);


    if (numero) {

        const quantidade = parseInt(
            numero[1],
            10
        );


        if (
            quantidade >= 1 &&
            quantidade <= 20
        ) {

            return quantidade;
        }
    }


    const numerosPorExtenso = {

        "um": 1,
        "uma": 1,
        "dois": 2,
        "duas": 2,
        "tres": 3,
        "quatro": 4,
        "cinco": 5,
        "seis": 6,
        "sete": 7,
        "oito": 8,
        "nove": 9,
        "dez": 10

    };


    for (const palavra in numerosPorExtenso) {

        if (
            mensagem.includes(palavra)
        ) {

            return numerosPorExtenso[palavra];
        }
    }


    return null;
}


// ======================================================
// PROCESSAR QUANTIDADE
// ======================================================

function processarQuantidade(texto) {

    if (!produtoSelecionado) {

        etapa = "escolhendo";

        adicionarMensagem(
            "Escolha primeiro um produto. 🍔"
        );

        return;
    }


    const quantidade = extrairQuantidade(texto);


    if (
        quantidade === null ||
        quantidade < 1 ||
        quantidade > 20
    ) {

        adicionarMensagem(
            "Digite uma quantidade entre 1 e 20."
        );

        return;
    }


    adicionarAoPedido(
        produtoSelecionado,
        quantidade
    );


    produtoSelecionado = null;

    perguntarMais();
}


// ======================================================
// ADICIONAR AO PEDIDO
// ======================================================

function adicionarAoPedido(produto, quantidade) {

    const existente = pedido.find(function (item) {

        return item.nome === produto.nome;

    });


    if (existente) {

        existente.quantidade += quantidade;

    } else {

        pedido.push({

            nome: produto.nome,
            descricao: produto.descricao,
            preco: produto.preco,
            quantidade: quantidade

        });
    }


    adicionarMensagem(
        "✅ Adicionado: " +
        quantidade +
        "x " +
        produto.nome
    );
}


// ======================================================
// PERGUNTAR SE QUER MAIS
// ======================================================

function perguntarMais() {

    etapa = "mais";

    adicionarMensagem(
        '🛒 Quer adicionar mais alguma coisa? Digite "sim" ou "não".'
    );
}


// ======================================================
// CONVERTER PREÇO
// ======================================================

function converterPreco(preco) {

    if (typeof preco === "number") {

        return preco;
    }


    return parseFloat(
        String(preco)
            .replace("R$", "")
            .replace(/\./g, "")
            .replace(",", ".")
            .trim()
    ) || 0;
}


// ======================================================
// FORMATAR DINHEIRO
// ======================================================

function formatarDinheiro(valor) {

    return Number(valor).toLocaleString(
        "pt-BR",
        {
            style: "currency",
            currency: "BRL"
        }
    );
}


// ======================================================
// CALCULAR TOTAL
// ======================================================

function calcularTotal() {

    let total = 0;


    pedido.forEach(function (item) {

        total +=
            converterPreco(item.preco) *
            item.quantidade;

    });


    return total;
}


// ======================================================
// MOSTRAR PEDIDO
// ======================================================

function mostrarPedido() {

    if (pedido.length === 0) {

        adicionarMensagem(
            "🛒 Seu pedido está vazio."
        );

        adicionarMensagem(
            'Digite "cardápio" para escolher alguma coisa.'
        );

        return;
    }


    adicionarMensagem(
        "🛒 ===== SEU PEDIDO ====="
    );


    pedido.forEach(function (item) {

        const subtotal =
            converterPreco(item.preco) *
            item.quantidade;


        adicionarMensagem(
            item.quantidade +
            "x " +
            item.nome +
            " — " +
            formatarDinheiro(subtotal)
        );
    });


    adicionarMensagem(
        "💰 TOTAL: " +
        formatarDinheiro(
            calcularTotal()
        )
    );
}


// ======================================================
// REMOVER PRODUTO
// ======================================================

function removerProduto(texto) {

    if (pedido.length === 0) {

        adicionarMensagem(
            "🛒 Seu pedido está vazio."
        );

        return;
    }


    const mensagem = normalizar(texto);


    const indice = pedido.findIndex(function (item) {

        const nome = normalizar(item.nome);

        if (mensagem.includes(nome)) {

            return true;
        }


        const palavras = nome
            .replace(/[🍔🍟🥤🧃]/g, "")
            .split(/\s+/)
            .filter(function (palavra) {

                return palavra.length >= 3;

            });


        return palavras.some(function (palavra) {

            return mensagem.includes(palavra);

        });

    });


    if (indice === -1) {

        adicionarMensagem(
            "Não encontrei esse produto no seu pedido."
        );

        return;
    }


    const removido = pedido.splice(
        indice,
        1
    )[0];


    adicionarMensagem(
        "❌ Removi " +
        removido.nome +
        " do seu pedido."
    );


    if (pedido.length > 0) {

        mostrarPedido();

    } else {

        adicionarMensagem(
            "Seu pedido ficou vazio."
        );
    }
}


// ======================================================
// INICIAR FINALIZAÇÃO
// ======================================================

function iniciarFinalizacao() {

    if (pedido.length === 0) {

        adicionarMensagem(
            "🛒 Você ainda não adicionou nenhum produto."
        );

        adicionarMensagem(
            'Digite "cardápio" para escolher.'
        );

        return;
    }


    mostrarPedido();


    etapa = "nome";


    adicionarMensagem(
        "👤 Para finalizar, qual é o seu nome?"
    );
}


// ======================================================
// MOSTRAR RESUMO
// ======================================================

function mostrarResumo() {

    adicionarMensagem(
        "📋 ===== RESUMO DO PEDIDO ====="
    );


    pedido.forEach(function (item) {

        const subtotal =
            converterPreco(item.preco) *
            item.quantidade;


        adicionarMensagem(
            item.quantidade +
            "x " +
            item.nome +
            " — " +
            formatarDinheiro(subtotal)
        );
    });


    adicionarMensagem(
        "👤 Nome: " +
        dadosCliente.nome
    );


    adicionarMensagem(
        "🚚 Tipo: " +
        dadosCliente.entrega
    );


    if (
        dadosCliente.entrega === "Entrega"
    ) {

        adicionarMensagem(
            "📍 Endereço: " +
            dadosCliente.endereco
        );
    }


    adicionarMensagem(
        "💳 Pagamento: " +
        dadosCliente.pagamento
    );


    adicionarMensagem(
        "💰 TOTAL: " +
        formatarDinheiro(
            calcularTotal()
        )
    );


    adicionarMensagem(
        '✅ Está tudo certo? Digite "sim" para confirmar ou "não" para cancelar.'
    );
}


// ======================================================
// CONFIRMAR PEDIDO
// ======================================================

function confirmarPedido() {

    const numeroPedido =
        Math.floor(
            1000 +
            Math.random() * 9000
        );


    adicionarMensagem(
        "🎉 PEDIDO CONFIRMADO!"
    );


    adicionarMensagem(
        "🍔 Número do pedido: #" +
        numeroPedido
    );


    adicionarMensagem(
        "💰 Total: " +
        formatarDinheiro(
            calcularTotal()
        )
    );


    adicionarMensagem(
        "Obrigado, " +
        dadosCliente.nome +
        "! 😄🍔"
    );


    adicionarMensagem(
        "Este é um pedido de demonstração do projeto Burger House."
    );


    adicionarMensagem(
        'Se quiser fazer outro pedido, digite "novo pedido".'
    );


    etapa = "finalizado";
}


// ======================================================
// NOVO PEDIDO
// ======================================================

function novoPedido() {

    pedido = [];

    produtoSelecionado = null;


    dadosCliente = {

        nome: "",
        entrega: "",
        endereco: "",
        pagamento: ""

    };


    etapa = "escolhendo";


    adicionarMensagem(
        "🔄 Novo pedido iniciado!"
    );


    adicionarMensagem(
        'Digite "cardápio" para começar.'
    );
}


// ======================================================
// ENTER PARA ENVIAR
// ======================================================

if (entrada) {

    entrada.addEventListener(
        "keydown",
        function (event) {

            if (event.key === "Enter") {

                event.preventDefault();

                enviarMensagem();
            }

        }
    );
}


// ======================================================
// MENSAGEM INICIAL
// ======================================================

if (mensagens) {

    if (
        mensagens.textContent.trim() === ""
    ) {

        adicionarMensagem(
            "🤖 Olá! Sou o atendente virtual da Burger House 🍔"
        );

        adicionarMensagem(
            "Vou ajudar você a escolher os produtos e montar seu pedido!"
        );

        adicionarMensagem(
            'Digite "cardápio" para começar.'
        );
    }
}