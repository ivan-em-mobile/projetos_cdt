import os
from dotenv import load_dotenv
from google import genai


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


try:
    if not GEMINI_API_KEY:
        raise ValueError("A chave GEMINI_API_KEY não foi encontrada. Verifique o arquivo .env.")
        

    client = genai.Client(api_key=GEMINI_API_KEY)
    print("✅ Conexão com a API do Gemini estabelecida com sucesso!")

except Exception as e:
    print(f"❌ Erro ao inicializar o Gemini: {e}")

    client = None 



def testar_conexao_gemini(cliente):
    """Envia um prompt simples para confirmar que a IA está respondendo."""
    if not cliente:
        print("Não foi possível testar a conexão. O cliente Gemini falhou na inicialização.")
        return

    print("\n[TESTE DA IA] Pedindo uma ideia de Pokémon...")
    try:
        response = cliente.models.generate_content(
            model='gemini-2.5-flash',
            contents='Gere uma breve descrição para um Pokémon do tipo Elétrico/Fogo chamado "Volcarona".'
        )
        print("--- Resposta da IA ---")
        
        print(response.text)
        print("----------------------")

    except Exception as e:
        print(f"❌ Erro ao chamar a API: {e}. Verifique se a chave é válida.")


testar_conexao_gemini(client)

