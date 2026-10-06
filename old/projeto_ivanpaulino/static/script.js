document.addEventListener("DOMContentLoaded", function() {
    carregarDados();

    // Enviar Cadastro de Cliente
    document.getElementById("formCliente").addEventListener("submit", function(e) {
        e.preventDefault();
        const nome = document.getElementById("nomeCliente").value;
        const telefone = document.getElementById("telCliente").value;

        fetch('/api/clientes', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ nome, telefone })
        })
        .then(res => res.json())
        .then(dados => {
            alert(dados.mensagem);
            carregarDados();
            document.getElementById("formCliente").reset();
        });
    });

    // Enviar Agendamento
    document.getElementById("formAgendamento").addEventListener("submit", function(e) {
        e.preventDefault();
        const dados = {
            cliente_id: document.getElementById("selectCliente").value,
            funcionario_id: document.getElementById("selectFuncionario").value,
            servico_id: document.getElementById("selectServico").value,
            dia_semana: document.getElementById("diaSemana").value,
            hora: document.getElementById("hora").value,
            agendado_por: "Recepcionista-Andrei" // Fixo conforme regra de negócio
        };

        fetch('/api/agendamentos', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(dados)
        })
        .then(res => res.json())
        .then(dados => {
            alert(dados.mensagem);
        });
    });
});

// Carregar Dados das Tabelas
function carregarDados() {
    fetch('/api/dados-iniciais')
    .then(res => res.json())
    .then(data => {
        // Preencher Select de Clientes
        const selectC = document.getElementById("selectCliente");
        selectC.innerHTML = '<option value="">Selecione...</option>';
        data.clientes.forEach(c => {
            selectC.innerHTML += `<option value="${c.id}">${c.nome}</option>`;
        });

        // Preencher Select de Funcionários
        const selectF = document.getElementById("selectFuncionario");
        selectF.innerHTML = '';
        data.funcionarios.forEach(f => {
            selectF.innerHTML += `<option value="${f.id}">${f.cargo}-${f.nome}</option>`;
        });

        // Preencher Select de Serviços
        const selectS = document.getElementById("selectServico");
        selectS.innerHTML = '';
        data.servicos.forEach(s => {
            selectS.innerHTML += `<option value="${s.id}">${s.nome} (R$ ${s.preco})</option>`;
        });

        // Renderizar área de edição de Preços
        const areaPrecos = document.getElementById("listaPrecos");
        areaPrecos.innerHTML = '<h3>Serviços</h3>';
        data.servicos.forEach(s => {
            areaPrecos.innerHTML += criarLinhaPreco('servicos', s.id, s.nome, s.preco);
        });
        
        areaPrecos.innerHTML += '<h3>Produtos</h3>';
        data.produtos.forEach(p => {
            areaPrecos.innerHTML += criarLinhaPreco('produtos', p.id, p.nome, p.preco);
        });
    });
}

function criarLinhaPreco(tabela, id, nome, preco) {
    return `
        <div class="item-preco">
            <span>${nome}</span>
            <div>
                <input type="number" step="0.1" id="val-${tabela}-${id}" value="${preco}">
                <button onclick="salvarPreco('${tabela}', ${id})">Salvar</button>
            </div>
        </div>
    `;
}

function salvarPreco(tabela, id) {
    const novoPreco = document.getElementById(`val-${tabela}-${id}`).value;
    fetch('/api/editar-preco', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ tabela, id, preco: novoPreco })
    })
    .then(res => res.json())
    .then(dados => {
        alert(dados.mensagem);
        carregarDados();
    });
}

// Função para Descarregar o JSON diretamente no teu PC!
function exportarBanco() {
    fetch('/api/exportar-json')
    .then(res => res.json())
    .then(dados => {
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(dados, null, 4));
        const downloadAnchor = document.createElement('a');
        downloadAnchor.setAttribute("href", dataStr);
        downloadAnchor.setAttribute("download", "banco_salao_beleza.json");
        document.body.appendChild(downloadAnchor);
        downloadAnchor.click();
        downloadAnchor.remove();
    });
}