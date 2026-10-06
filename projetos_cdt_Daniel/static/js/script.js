'use strict';

const CONFIG = {
    storageKey: 'rh_alunos',
    adminUser: 'root',
    adminPassword: 'master',
    feedbackDuration: 4800,
    botDelay: 500
};

const alunosPadrao = [
    {
        id: 1,
        nome: 'Carlos Silva',
        cpf: '123.456.789-00',
        plano: 'Plano Semestral (R$ 150,00/mês)',
        pagamento: 'Cartão (Débito Automático)',
        status: 'ativo'
    },
    {
        id: 2,
        nome: 'Ana Souza',
        cpf: '987.654.321-11',
        plano: 'Plano Mensal (R$ 90,00/mês)',
        pagamento: 'Boleto Bancário',
        status: 'pendente'
    }
];

let listaAlunos = carregarAlunos();

const $ = (selector) => document.querySelector(selector); const $$ = (selector) => document.querySelectorAll(selector);

function carregarAlunos() {
    try {
        const dados = localStorage.getItem(CONFIG.storageKey);
        return dados ? JSON.parse(dados) : [...alunosPadrao];
    } catch (error) {
        console.error('Erro ao carregar alunos:', error);
        return [...alunosPadrao];
    }
}

function salvarAlunos() {
    localStorage.setItem(CONFIG.storageKey, JSON.stringify(listaAlunos));
    atualizarTabelaAdmin();
}

function escaparHTML(valor) {
    return String(valor)
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#039;');
}

function mostrarFeedback(mensagem, badge = 'Matrícula Realizada!', duracao = CONFIG.feedbackDuration) {
    const feedback = $('#feedback-sucesso');
    const badgeText = $('#badgeText');
    const textoFeedback = $('#textoFeedback');

    badgeText.textContent = badge;
    textoFeedback.innerHTML = mensagem;
    feedback.classList.add('mostrar');

    window.clearTimeout(feedback._timer);
    feedback._timer = window.setTimeout(() => {
        feedback.classList.remove('mostrar');
    }, duracao);
}

function normalizarTexto(texto) {
    return texto
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '');
}

// PAINEL ADMINISTRATIVO
const logoAdminTrigger = $('#logoAdminTrigger');
const adminSection = $('#admin-section');
const adminLoginBox = $('#adminLoginBox');
const adminPanel = $('#adminPanel');
const btnLoginAdmin = $('#btnLoginAdmin');
const adminUser = $('#adminUser');
const adminPassword = $('#adminPassword');
const adminLoginError = $('#adminLoginError');
const btnLogoutAdmin = $('#btnLogoutAdmin');

logoAdminTrigger.addEventListener('dblclick', (event) => {
    event.preventDefault();
    adminSection.style.display = 'block';
    adminSection.scrollIntoView({ behavior: 'smooth' });
});

btnLoginAdmin.addEventListener('click', () => {
    const acessoValido =
        adminUser.value === CONFIG.adminUser &&
        adminPassword.value === CONFIG.adminPassword;

    if (!acessoValido) {
        adminLoginError.style.display = 'block';
        return;
    }

    adminLoginBox.style.display = 'none';
    adminPanel.style.display = 'block';
    adminLoginError.style.display = 'none';
    atualizarTabelaAdmin();
});

adminPassword.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') btnLoginAdmin.click();
});

btnLogoutAdmin.addEventListener('click', () => {
    adminPanel.style.display = 'none';
    adminLoginBox.style.display = 'block';
    adminUser.value = '';
    adminPassword.value = '';
    adminSection.style.display = 'none';

    mostrarFeedback('Até breve! O painel administrativo foi ocultado com segurança.', 'Sessão Encerrada', 4200);

    window.setTimeout(() => {
        $('#badgeText').textContent = 'Matrícula Realizada!';
    }, 4600);
});

function atualizarTabelaAdmin() {
    const tbody = $('#adminTableBody');
    if (!tbody) return;

    const estatisticas = listaAlunos.reduce(
        (acc, aluno) => {
            acc.total++;
            if (aluno.status === 'ativo') acc.ativos++;
            if (aluno.status === 'pendente') acc.pendentes++;
            if (aluno.pagamento.includes('Débito Automático')) acc.debitoAuto++;
            return acc;
        },
        { total: 0, ativos: 0, pendentes: 0, debitoAuto: 0 }
    );

    $('#statTotal').textContent = estatisticas.total;
    $('#statAtivos').textContent = estatisticas.ativos;
    $('#statPendentes').textContent = estatisticas.pendentes;
    $('#statDebito').textContent = estatisticas.debitoAuto;

    tbody.innerHTML = listaAlunos.map((aluno) => {
        const statusInfo = {
            ativo: { classe: 'ativo', texto: 'Ativo' },
            pendente: { classe: 'pendente', texto: 'Pendente' },
            cancelado: { classe: 'cancelado', texto: 'Cancelado' }
        }[aluno.status] || { classe: 'cancelado', texto: 'Cancelado' };

        const acao = aluno.status !== 'cancelado'
            ? `<button class="btn-acao btn-cancelar" type="button" data-id="${aluno.id}"><i class="fa-solid fa-ban"></i> Cancelar</button>`
            : '<span style="color:var(--gray); font-size:11px;">Encerrado</span>';

        return `
            <tr>
                <td><strong>${escaparHTML(aluno.nome)}</strong></td>
                <td>${escaparHTML(aluno.cpf)}</td>
                <td>${escaparHTML(aluno.plano)}</td>
                <td>${escaparHTML(aluno.pagamento)}</td>
                <td><span class="badge ${statusInfo.classe}">${statusInfo.texto}</span></td>
                <td>${acao}</td>
            </tr>
        `;
    }).join('');
}

document.addEventListener('click', (event) => {
    const botao = event.target.closest('.btn-cancelar');
    if (!botao) return;
    const id = Number(botao.dataset.id);
    const aluno = listaAlunos.find((item) => item.id === id);
    if (!aluno) return;

    if (!confirm(`Deseja realmente cancelar a inscrição de ${aluno.nome}?`)) return;
    aluno.status = 'cancelado';
    salvarAlunos();
});

// MENU MOBILE
const menuToggle = $('#menuToggle');
const navMenu = $('#navMenu');  menuToggle.addEventListener('click', (event) => {     event.stopPropagation();     navMenu.classList.toggle('ativo'); });  $$('.nav-link').forEach((link) => {
    link.addEventListener('click', () => navMenu.classList.remove('ativo'));
});

// MATRÍCULA
const contactForm = $('#contactForm');
const selectPlanoMatricula = $('#planoSelecionado');

contactForm.addEventListener('submit', (event) => {
    event.preventDefault();

    const nome = $('#inputNome').value.trim();
    const cpf = $('#inputCpf').value.trim();
    const plano = selectPlanoMatricula.value;
    const formaPagamento = $('#formaPagamento').value;

    const pagamentos = {
        pix: { texto: 'PIX (À vista)', status: 'ativo' },
        cartao: { texto: 'Cartão (Débito Automático)', status: 'ativo' },
        boleto: { texto: 'Boleto (Pendente)', status: 'pendente' }
    };

    const pagamento = pagamentos[formaPagamento];
    if (!pagamento) return;

    listaAlunos.push({
        id: Date.now(),
        nome,
        cpf,
        plano,
        pagamento: pagamento.texto,
        status: pagamento.status
    });

    salvarAlunos();

    const mensagem = pagamento.status === 'ativo'
        ? `Parabéns, ${escaparHTML(nome)}! Sua matrícula está ativa e o acesso liberado.`
        : 'Matrícula registrada! Aguardando compensação do boleto para liberação.';

    mostrarFeedback(mensagem);
    contactForm.reset();
});

$$('.btn-escolher-plano').forEach((botao) => {
    botao.addEventListener('click', (event) => {
        event.preventDefault();
        selectPlanoMatricula.value = botao.dataset.plano;
        $('#contato').scrollIntoView({ behavior: 'smooth' });
    });
});

$('#inputCpf').addEventListener('input', (event) => {
    let valor = event.target.value.replace(/\D/g, '').slice(0, 11);
    if (valor.length > 9) {
        valor = valor.replace(/^(\d{3})(\d{3})(\d{3})(\d{2}).*/, '$1.$2.$3-$4');
    } else if (valor.length > 6) {
        valor = valor.replace(/^(\d{3})(\d{3})(\d{3}).*/, '$1.$2.$3');
    } else if (valor.length > 3) {
        valor = valor.replace(/^(\d{3})(\d{3}).*/, '$1.$2');
    }
    event.target.value = valor;
});

// CALCULADORA IMC
$('#btnCalcularIMC').addEventListener('click', () => {
    const peso = Number.parseFloat($('#peso').value);
    const altura = Number.parseFloat($('#altura').value);
    const resultado = $('#resultado-imc');

    if (!peso || !altura || peso <= 0 || altura <= 0) {
        resultado.textContent = 'Insira peso e altura válidos!';
        resultado.style.color = 'var(--primary)';
        return;
    }

    const imc = peso / (altura * altura);
    const classificacao =
        imc < 18.5 ? 'Abaixo do peso' :
        imc < 25 ? 'Peso normal' :
        imc < 30 ? 'Sobrepeso' :
        'Obesidade';

    resultado.textContent = `Seu IMC é ${imc.toFixed(2)} (${classificacao})`;
    resultado.style.color = 'white';
});

// CHATBOT
const chatContainer = $('#chatContainer');
const chatBtnToggle = $('#chatBtnToggle');
const chatCloseBtn = $('#chatCloseBtn');
const chatInput = $('#chatInput');
const chatSendBtn = $('#chatSendBtn');
const chatMessages = $('#chatMessages');

function alternarChat(abrir) {
    chatContainer.classList.toggle('ativo', abrir);
    chatContainer.setAttribute('aria-hidden', String(!abrir));
    if (abrir) chatInput.focus();
}

chatBtnToggle.addEventListener('click', () => alternarChat(!chatContainer.classList.contains('ativo')));
chatCloseBtn.addEventListener('click', () => alternarChat(false));

function obterRespostaBot(mensagem) {
    const texto = normalizarTexto(mensagem);
    const permitidas = [
        'treino', 'exercicio', 'musculacao', 'funcional', 'cardio',
        'peso', 'massa', 'hipertrofia', 'emagrecimento', 'plano',
        'preco', 'valor', 'mensalidade', 'horario', 'funciona',
        'abre', 'endereco', 'onde', 'local', 'matricula', 'suplemento',
        'academia', 'imc', 'pagamento', 'pix', 'cartao', 'boleto', 'ola', 'oi'
    ];

    const assuntoValido = permitidas.some((termo) => texto.includes(termo));
    if (!assuntoValido) {
        return 'Opa, foco no treino! Só consigo responder dúvidas referentes à <strong>Academia RH Fitness</strong>, planos, horários ou exercícios.';
    }

    if (texto.includes('treino') || texto.includes('exercicio')) {
        return 'Para ótimos resultados, foque em uma execução perfeita. Nossa área de musculação está completa!';
    }
    if (texto.includes('plano') || texto.includes('preco') || texto.includes('valor')) {
        return 'Temos o Plano Mensal (R$ 90,00), Semestral (R$ 150,00/mês) e Anual VIP (R$ 250,00/mês).';
    }
    if (texto.includes('horario') || texto.includes('funciona') || texto.includes('abre')) {
        return 'Atendemos de segunda a sexta das 06h às 22h, e aos sábados das 08h às 14h.';
    }
    return 'Perfeito, maromba! Se precisar de detalhes sobre nossos planos ou valores, é só mandar aqui.';
}

function adicionarMensagem(texto, remetente) {
    const mensagem = document.createElement('div');
    mensagem.className = `message ${remetente}`;
    mensagem.innerHTML = texto;
    chatMessages.appendChild(mensagem);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function enviarMensagem() {
    const texto = chatInput.value.trim();
    if (!texto) return;

    adicionarMensagem(escaparHTML(texto), 'user');
    chatInput.value = '';

    window.setTimeout(() => {
        adicionarMensagem(obterRespostaBot(texto), 'bot');
    }, CONFIG.botDelay);
}

chatSendBtn.addEventListener('click', enviarMensagem);
chatInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') enviarMensagem();
});

atualizarTabelaAdmin();