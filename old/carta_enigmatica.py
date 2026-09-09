import string

# --- Configurações da Cifra ---
ZENIT = "ZENIT"
POLAR = "POLAR"

def criar_mapa_substituicao(chave1, chave2):
    """Cria um dicionário de mapeamento de substituição bi-direcional."""
    mapa = {}
    
    # Mapeamento Z <-> P, E <-> O, N <-> L, I <-> A, T <-> R
    for i in range(len(chave1)):
        letra_chave1 = chave1[i]
        letra_chave2 = chave2[i]
        
        # Mapeamento bi-direcional
        mapa[letra_chave1] = letra_chave2
        mapa[letra_chave2] = letra_chave1
        
    return mapa

def processar_cifra(texto, mapa):
    """Cifra ou decifra o texto usando o mapa de substituição, preservando o caso."""
    texto_processado = ""
    for char in texto:
        if char.isalpha():
            char_maiuscula = char.upper()
            
            if char_maiuscula in mapa:
                substituto_maiusculo = mapa[char_maiuscula]
                
                # Preserva o caso original
                if char.isupper():
                    char_substituido = substituto_maiusculo
                else:
                    char_substituido = substituto_maiusculo.lower()
                    
                texto_processado += char_substituido
            else:
                texto_processado += char
        else:
            texto_processado += char
            
    return texto_processado

# --- Função Principal com Loop de Repetição ---

def menu_principal():
    """
    Controla o fluxo do programa, permitindo múltiplas operações de cifragem/decifragem.
    """
    mapa_zenit_polar = criar_mapa_substituicao(ZENIT, POLAR)
    
    continuar_rodando = True
    
    while continuar_rodando:
        print("\n===========================================")
        print("      🔑 Cifra Enigmática ZENIT POLAR 🔑")
        print("===========================================")
        print(f"Chaves de Substituição: {ZENIT} <-> {POLAR}")
        
        # 1. Entrada de Texto do Usuário
        texto_original = input("\n➡️ Por favor, digite o texto que deseja processar: \n> ")
        
        # 2. Loop para Forçar a Escolha Válida (Cifrar/Decifrar)
        while True:
            escolha = input("\n❓ Deseja **Cifrar** (C) ou **Decifrar** (D) a mensagem? Digite C ou D: ").upper()
            
            if escolha == 'C':
                acao = "Cifrado"
                resultado = processar_cifra(texto_original, mapa_zenit_polar)
                break
            elif escolha == 'D':
                acao = "Decifrado"
                resultado = processar_cifra(texto_original, mapa_zenit_polar)
                break
            else:
                print("❌ Opção inválida. Por favor, digite apenas 'C' para Cifrar ou 'D' para Decifrar.")
                
        # 3. Exibir Resultados
        print("\n-------------------------------------------")
        print(f"Texto Original:   {texto_original}")
        print(f"Texto {acao}: {resultado}")
        print("-------------------------------------------")

        # 4. Loop de Continuação (Pergunta se quer repetir)
        while True:
            continuar = input("\n🔁 Deseja cifrar/decifrar **outra** mensagem? (S/N): ").upper()
            
            if continuar == 'N':
                continuar_rodando = False # Seta a variável de controle para FALSE
                break # Sai do loop interno
            elif continuar == 'S':
                break # Sai do loop interno e continua o loop principal (while continuar_rodando)
            else:
                print("❌ Opção inválida. Por favor, digite 'S' para Sim ou 'N' para Não.")
                
    print("\nEncerrando o programa. Até a próxima! 👋")


if __name__ == "__main__":
    menu_principal()