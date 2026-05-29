// Função para iniciar a contagem do pinguim
function iniciarContadorPinguim() {
    const themeContainer = document.getElementById('theme-toggle-container');
    const loadingScreen = document.getElementById('loading-screen');
    const resultsScreen = document.getElementById('results-screen');

    if (loadingScreen) {
        if (themeContainer) {
            themeContainer.style.display = 'none';
        }
    }

    // Aguarda os 3 segundos regulamentares (OBS: Descartado por enquanto)
    setTimeout(() => {
        if (loadingScreen && resultsScreen) {
            loadingScreen.style.display = 'none';
            resultsScreen.style.display = 'block';
            
            if (themeContainer) {
                themeContainer.style.display = 'flex';
            }
            
            gerarGraficoDinamico();
        } else {
            console.log("Erro: Elementos da tela não foram encontrados no HTML.");
        }
    }, 3000);
}

// Executa automaticamente
iniciarContadorPinguim();

// ==========================================
// FUNÇÃO DO GRÁFICO (CHART.JS)
// ==========================================
function gerarGraficoDinamico() {
    const ctx = document.getElementById('chartRosquinha');
    if (!ctx) return;

    const renda = typeof rendaMensalUsuario !== 'undefined' ? rendaMensalUsuario : 0;
    
    const essentials = renda * 0.50;
    const lifestyle = renda * 0.30;
    const savings = renda * 0.20;

    const estiloComputado = getComputedStyle(document.documentElement);
    const corAzul = estiloComputado.getPropertyValue('--cor-essencial').trim() || '#38bdf8';
    const corAmarelo = estiloComputado.getPropertyValue('--cor-estilo-vida').trim() || '#ffb800';
    const corVerde = estiloComputado.getPropertyValue('--cor-reserva').trim() || '#10b981';

    // Salva a instância globalmente para o MutationObserver do HTML conseguir atualizar as cores
    window.meuGraficoInstanciado = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Essencial (50%)', 'Estilo de Vida (30%)', 'Investimentos (20%)'],
            datasets: [{
                data: [essentials, lifestyle, savings],
                backgroundColor: [corAzul, corAmarelo, corVerde],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: estiloComputado.getPropertyValue('--texto-principal').trim() || '#ffffff',
                        font: { family: 'Urbanist', size: 12 }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let value = context.raw || 0;
                            return ` R$ ${value.toFixed(2)}`;
                        }
                    }
                }
            }
        }
    });
}

// ==========================================
// FUNÇÃO DOS BOTÕES DE INVESTIMENTO
// ==========================================
function selecionarInvestimento(tipo) {
    const campoDica = document.getElementById('dica-investimento');
    if (!campoDica) return;

    campoDica.style.opacity = 0;
    
    setTimeout(() => {
        if (tipo === 'Imóveis') {
            campoDica.innerHTML = `🏠 O Pinguim recomenda: Guardar a reserva em fundos imobiliários (FIIs) ou poupar para uma entrada sólida de consórcio!`;
        } else if (tipo === 'Automóveis') {
            campoDica.innerHTML = `🚗 O Pinguim recomenda: Investir em títulos de renda fixa com liquidez na data planejada para a compra do veículo.`;
        } else if (tipo === 'Compras Futuras') {
            campoDica.innerHTML = `🛍️ O Pinguim recomenda: Usar as 'Caixinhas' ou objetivos digitais de rendimento 100% CDI para compras de curto prazo!`;
        }
        campoDica.style.opacity = 1;
        campoDica.style.transition = "opacity 0.3s ease";
    }, 500);
}