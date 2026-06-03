let nomeUsuario = "";

const subMenus = {
    1: ["O que é o Credo?", "1° Artigo", "2° Artigo", "3° Artigo", "4° Artigo", "5° Artigo", "6° Artigo", "7° Artigo", "8° Artigo", "9° Artigo", "10° Artigo", "11° Artigo", "12° Artigo"],
    2: ["O que é Sacramento?", "Batismo", "Confirmação", "Eucaristia", "Penitência", "Unção dos Enfermos", "Ordem", "Matrimônio"],
    3: ["O que é O Decálogo?", "1° Mandamento", "2° Mandamento", "3° Mandamento", "4° Mandamento", "5° Mandamento", "6° Mandamento", "7° Mandamento", "8° Mandamento", "9° e 10° Mandamentos"],
    4: ["O que é Oração?", "Introdução", "1ª Petição", "2ª Petição", "3ª Petição", "4ª Petição", "5ª Petição", "6ª Petição", "7ª Petição", "Última Palavra", "Outras Orações"],
    5: ["O que é Dogma?", "Santíssima Trindade", "Divindade de Cristo", "Imaculada Conceição", "Virgindade de Maria"],
    6: ["O que é Tradição?", "As Escrituras", "O Magistério", "Importâncias"],
    7: ["Definição da Igreja", "Notas da Igreja", "Membros da Igreja"]
};

document.addEventListener("DOMContentLoaded", () => {
    const btnLogin = document.getElementById("btn-login");
    const btnCadastro = document.getElementById("btn-cadastro");
    const usuarioInput = document.getElementById("input-usuario");
    const senhaInput = document.getElementById("input-senha");
    const feedback = document.getElementById("mensagem-feedback");
    
    const painelLogin = document.getElementById("painel-identificacao");
    const painelPrincipal = document.getElementById("painel-principal");
    const saudacao = document.getElementById("saudacao-usuario");

    function mostrarMensagem(texto, erro = false) {
        feedback.innerText = texto;
        feedback.className = `text-xs text-center font-medium mt-1 ${erro ? 'text-red-400' : 'text-green-400'}`;
        feedback.classList.remove("hidden");
    }

    if (btnLogin) {
        btnLogin.addEventListener("click", () => {
            const usuario = usuarioInput.value.trim();
            const senha = senhaInput.value;

            if (!usuario || !senha) {
                mostrarMensagem("Por favor, preencha todos os campos.", true);
                return;
            }

            fetch("/api/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ usuario: usuario, senha: senha })
            })
            .then(res => res.json().then(data => ({ status: res.status, data })))
            .then(({ status, data }) => {
                if (status === 200) {
                    nomeUsuario = data.usuario;
                    
                    painelLogin.classList.add("hidden");
                    painelPrincipal.classList.remove("hidden");
                    saudacao.innerText = `Salve Maria, ${nomeUsuario}! O que deseja aprender hoje?`;
                } else {
                    mostrarMensagem(data.erro, true);
                }
            })
            .catch(err => {
                console.error(err);
                mostrarMensagem("Erro ao conectar com o servidor.", true);
            });
        });
    }

    if (btnCadastro) {
        btnCadastro.addEventListener("click", () => {
            const usuario = usuarioInput.value.trim();
            const senha = senhaInput.value;

            if (!usuario || !senha) {
                mostrarMensagem("Por favor, defina um usuário e senha para cadastrar.", true);
                return;
            }

            fetch("/api/cadastro", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ usuario: usuario, senha: senha })
            })
            .then(res => res.json().then(data => ({ status: res.status, data })))
            .then(({ status, data }) => {
                if (status === 201) {
                    mostrarMensagem("Conta criada com sucesso! Agora clique em 'Entrar'.", false);
                    senhaInput.value = "";
                } else {
                    mostrarMensagem(data.erro, true);
                }
            })
            .catch(err => {
                console.error(err);
                mostrarMensagem("Erro ao conectar com o servidor.", true);
            });
        });
    }
});

function carregarSubMenu(categoriaId) {
    const container = document.getElementById("sub-menu-container");
    container.innerHTML = ""; 
    
    if (!subMenus[categoriaId]) return;

    subMenus[categoriaId].forEach((nomeSub, index) => {
        const btn = document.createElement("button");
        btn.innerText = nomeSub;
        btn.className = "bg-slate-700 hover:bg-amber-700 text-slate-100 px-3 py-1.5 text-xs font-medium rounded transition cursor-pointer shadow-sm border border-slate-600 hover:text-white";
        
        btn.onclick = () => buscarDadosDoServidor(categoriaId, index + 1);
        container.appendChild(btn);
    });

    buscarDadosDoServidor(categoriaId, 1);
}

async function buscarDadosDoServidor(categoriaId, opcaoId) {
    try {
        const url = `/api/conteudo/${categoriaId}/${opcaoId}`;
        console.log("Tentando acessar a rota:", url);

        const resposta = await fetch(url);
        
        if (!resposta.ok) {
            throw new Error(`O servidor respondeu com status ${resposta.status}`);
        }

        const dados = await resposta.json();
        
        const elementoTitulo = document.getElementById("texto-titulo");
        const elementoConteudo = document.getElementById("texto-conteudo");

        if (dados.erro) {
            elementoTitulo.innerText = "Aviso do Banco de Dados";
            elementoConteudo.innerText = `Erro: ${dados.erro} (Categoria: ${categoriaId}, Opção: ${opcaoId})`;
        } else {
            elementoTitulo.innerText = dados.titulo;
            elementoConteudo.innerHTML = dados.texto;
        }

    } catch (erro) {
        console.error("Erro na requisição:", erro);
        
        document.getElementById("texto-titulo").innerText = "Erro de Conexão/Rota";
        document.getElementById("texto-conteudo").innerText = 
            `Não foi possível carregar os dados.\nDetalhes do erro: ${erro.message}\n\nSe estiver testando localmente, garanta que o Flask está rodando. Se for na Vercel, verifique os Logs de Implantação.`;
    }
}

function mostrarConsideracoes() {
    document.getElementById("sub-menu-container").innerHTML = "";
    
    const elementoTitulo = document.getElementById("texto-titulo");
    const elementoConteudo = document.getElementById("texto-conteudo");
    
    elementoTitulo.innerText = "--- CONSIDERAÇÕES FINAIS ---";
    elementoConteudo.innerHTML = `
        <p class='mb-2 text-justify w-full'>Este sistema de aprendizado foi projetado para fornecer uma visão clara, fiel e ortodoxa da Doutrina Católica.</p>
        <p class='font-semibold mt-4 text-amber-500'>As fontes teológicas utilizadas foram:</p>
        <ul class='list-disc pl-5 mt-2 space-y-1 text-sm text-slate-300 text-justify'>
            <li>O Catecismo Romano (Promulgado por ordem do Concílio de Trento e do Papa São Pio V, 1566).</li>
            <li>Atas e Decretos Dogmáticos do Sacrossanto Concílio de Trento.</li>
            <li>Encíclicas Papais de relevância dogmática (como <i>Ineffabilis Deus</i> de Pio IX e <i>Mystici Corporis Christi</i> de Pio XII).</li>
        </ul>
        <p class='mt-4 font-light text-xs italic text-slate-500'>Obrigado por utilizar este roteiro de estudos teológicos!</p>
    `;
}