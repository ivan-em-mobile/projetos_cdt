import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

try:
    if not GEMINI_API_KEY:
        raise ValueError("A chave GEMINI_API_KEY não foi encontrada.")
        
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    print(f"Erro ao inicializar o Gemini: {e}")
    client = None 

def iniciar_chat_pokedex():
    if not client:
        return None
        
    system_instruction = (
        "Você é um Professor Pokémon e Consultor Estratégico. Sua tarefa é analisar o pedido do usuário "
        "e sugerir times de 6 Pokémon válidos (incluindo Megas/Lendários se apropriado), "
        "justificando a sinergia de tipos, habilidades e estatísticas. Sua resposta deve ser sempre focada em ajudar na formação do time."
    )

    chat = client.chats.create(
        model='gemini-2.5-flash',
        system_instruction=system_instruction
    )
    return chat

def enviar_mensagem_chat(chat_session, mensagem_usuario):
    if not chat_session:
        return "Erro: Chat da IA não inicializado."
    
    try:
        response = chat_session.send_message(mensagem_usuario)
        return response.text
    except Exception as e:
        return f"Erro na comunicação com a IA: {e}"