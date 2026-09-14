import cv2
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import mediapipe as mp

# Opcional para controle de volume no Windows (pycaw)
try:
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_control = interface.QueryInterface(IAudioEndpointVolume)
    HAS_PYCAW = True
except Exception:
    HAS_PYCAW = False

# CONFIGURAÇÕES DE API
WEATHER_API_KEY = "SUA_CHAVE_OPENWEATHER"
CITY_NAME = "Sao Paulo"

SPOTIPY_CLIENT_ID = "SEU_CLIENT_ID_SPOTIFY"
SPOTIPY_CLIENT_SECRET = "SEU_SECRET_SPOTIFY"
SPOTIPY_REDIRECT_URI = "http://localhost:8888/callback"


def obter_clima(cidade, api_key):
    """Consulta a previsão do tempo via OpenWeatherMap com tratamento de erros."""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&lang=pt_br&units=metric"
        resposta = requests.get(url, timeout=5).json()
        if resposta.get("cod") == 200:
            clima = resposta["weather"][0]["main"].lower()
            temp = resposta["main"]["temp"]
            print(f"Clima atual em {cidade}: {clima} ({temp}°C)")
            return clima
        else:
            print(f"Erro na API de Clima: {resposta.get('message')}")
    except Exception as e:
        print(f"Falha na conexão de clima: {e}")
    return "clear"


def mapear_genero_ou_termo(clima, humor):
    termos = {
        "feliz": "happy pop upbeat",
        "triste": "sad acoustic chill",
        "energetico": "rock workout party",
        "calmo": "ambient lofi relax",
        "romantico": "romantic love songs",
        "nostalgico": "80s 90s classics"
    }
    termo_humor = termos.get(humor, "pop")
    
    if "rain" in clima or "drizzle" in clima:
        termo_humor += " rain chill"
    elif "clear" in clima:
        termo_humor += " summer vibe"

    return termo_humor


def criar_playlist_spotify(sp, nome_playlist, termo_busca):
    try:
        user_id = sp.current_user()["id"]
        resultados = sp.search(q=termo_busca, limit=10, type="track")
        faixas_uris = [track["uri"] for track in resultados["tracks"]["items"]]
        
        playlist = sp.user_playlist_create(
            user=user_id, 
            name=nome_playlist, 
            public=True, 
            description="Playlist gerada automaticamente com base no clima e humor!"
        )
        
        if faixas_uris:
            sp.playlist_add_items(playlist_id=playlist["id"], items=faixas_uris)
            print(f"Playlist '{nome_playlist}' criada com sucesso! ({len(faixas_uris)} músicas)")
        else:
            print("Nenhuma música encontrada.")
    except Exception as e:
        print(f"Erro ao interagir com a API do Spotify: {e}")


def iniciar_controle_gestos(sp):
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    mp_draw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    ultimo_comando_tempo = time.time()
    texto_status = "Aguardando gesto..."

    while cap.isOpened():
        success, img = cap.read()
        if not success:
            break

        img = cv2.flip(img, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        resultado = hands.process(img_rgb)

        if resultado.multi_hand_landmarks:
            for hand_lms in resultado.multi_hand_landmarks:
                mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)
                landmarks = hand_lms.landmark
                
                # Identificação simplificada de dedos levantados
                dedos = [
                    landmarks[4].x < landmarks[3].x,  # Polegar (para mão direita espelhada)
                    landmarks[8].y < landmarks[6].y,  # Indicador
                    landmarks[12].y < landmarks[10].y, # Médio
                    landmarks[16].y < landmarks[14].y, # Anelar
                    landmarks[20].y < landmarks[18].y  # Mínimo
                ]

                agora = time.time()
                if agora - ultimo_comando_tempo > 1.5:
                    # Mão Aberta -> Play / Pause
                    if all(dedos):
                        texto_status = "Comando: Play / Pause"
                        try:
                            playback = sp.current_playback()
                            if playback and playback.get('is_playing'):
                                sp.pause_playback()
                            else:
                                sp.start_playback()
                        except Exception as e:
                            texto_status = "Erro: Spotify sem player ativo"
                        ultimo_comando_tempo = agora

                    # Apenas Indicador -> Próxima Faixa
                    elif dedos[1] and not any([dedos[0], dedos[2], dedos[3], dedos[4]]):
                        texto_status = "Comando: Próxima Música"
                        try:
                            sp.next_track()
                        except Exception as e:
                            texto_status = "Erro no controle Spotify"
                        ultimo_comando_tempo = agora

                    # Apenas Polegar -> Aumentar Volume
                    elif dedos[0] and not any(dedos[1:]):
                        texto_status = "Comando: Volume +"
                        if HAS_PYCAW:
                            vol_atual = volume_control.GetMasterVolumeLevelScalar()
                            volume_control.SetMasterVolumeLevelScalar(min(1.0, vol_atual + 0.1), None)
                        ultimo_comando_tempo = agora

        # Exibe o status do comando diretamente na janela de vídeo
        cv2.putText(img, texto_status, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow("Controle por Gestos - Spotify", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def main():
    print("=== ASSISTENTE MUSICAL INTELIGENTE ===")
    
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET,
            redirect_uri=SPOTIPY_REDIRECT_URI,
            scope="playlist-modify-public user-modify-playback-state user-read-playback-state"
        ))
    except Exception as e:
        print(f"Erro de autenticação no Spotify: {e}")
        return

    print("\nEscolha seu humor atual:")
    print("1 - Feliz | 2 - Triste | 3 - Energético | 4 - Calmo | 5 - Romântico | 6 - Nostálgico")
    humores = {"1": "feliz", "2": "triste", "3": "energetico", "4": "calmo", "5": "romantico", "6": "nostalgico"}
    opcao = input("Opção (1-6): ").strip()
    humor_escolhido = humores.get(opcao, "feliz")

    clima = obter_clima(CITY_NAME, WEATHER_API_KEY)
    termo_busca = mapear_genero_ou_termo(clima, humor_escolhido)
    
    nome_playlist = f"Vibe: {humor_escolhido.capitalize()} ({clima.capitalize()})"
    criar_playlist_spotify(sp, nome_playlist, termo_busca)

    input("\nPressione ENTER para iniciar o controle por gestos...")
    iniciar_controle_gestos(sp)


if __name__ == "__main__":
    main()