'''Definindo os nossos serviços'''
class FinanceService:
    @staticmethod
    def recomendar_investimento(banco, meta):
        # Base de dados de recomendações
        dados = {
            "Nubank": {
                "Investir": ["Caixinha de Reserva de Emergência", "CDB NuInvest", "RDB Planejado"],
                "Organizar": ["Função 'Guardar Dinheiro'", "Alerta de Gastos", "NuLimite Garantido"]
            },
            "Inter": {
                "Investir": ["CDB Meu Porquinho", "LCI Isento de IR", "Inter Invest Ações"],
                "Organizar": ["Gerenciador Financeiro Inter", "Débito Automático", "CDB Mais Limite"]
            }
        }
        
        # Tenta buscar a recomendação, se não achar, dá uma dica geral
        banco_selecionado = dados.get(banco, {})
        return banco_selecionado.get(meta, ["Tesouro Selic (Dica Geral)"])



'''class FinanceService:
    @staticmethod
    def recomendar_investimento(banco, perfil):

        recomendacoes = {
            "Nubank": [
                "Caixinhas do Nubank (Reserva de Emergência)",
                "Tesoura Direto via App",
                "CDB com liquidez diária"
            ],
            "inter": [
                "CDB Porquinho",
                "LCI/LCA (Isento de Imposto de Renda)",
                "INter Invest (Ações e FIIS)"
            ]
        }
        return recomendacoes.get(banco, ["Poupança (Não recomendado)"])
    
class FinanceService:
    @staticmethod
    def recomendar_investimento(banco, meta):
        # Dicionário de estratégias básicas por banco
        estrategias = {
            "Nubank": {
                "Investir": ["Caixinha de Reserva de Emergência", "RDB Planejado", "Nu Reserva Imediata (Fundo)"],
                "Organizar": ["Uso do 'Guardar Dinheiro'", "Organização por subcontas", "Cartão com limite garantido"]
            },
            "Inter": {
                "Investir": ["CDB Meu Porquinho", "LCI Diária (Isento de IR)", "Plataforma Inter Invest"],
                "Organizar": ["Débito Automático de Contas", "Gráfico de Gastos Inter", "CDB Mais Limite"]
            }
        }
        
        # Retorna a lista baseada no Banco e na Meta (Investir ou Organizar)
        return estrategias.get(banco, {}).get(meta, ["Opção geral: Tesouro Selic"])'''