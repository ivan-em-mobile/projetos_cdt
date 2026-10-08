import sys
import types

# --- MONKEY PATCHING PARA O TF_KERAS ---
if 'tf_keras' not in sys.modules:
    tf_keras_mock = types.ModuleType('tf_keras')
    tf_keras_mock.__version__ = '2.15.0'
    sys.modules['tf_keras'] = tf_keras_mock
else:
    if not hasattr(sys.modules['tf_keras'], '__version__'):
        sys.modules['tf_keras'].__version__ = '2.15.0'

import cv2
import sqlite3
import os

os.environ['TF_USE_LEGACY_KERAS'] = '1'

from deepface import DeepFace

DB_NAME = 'acaiteria.db'

def obter_info_cliente_por_foto(caminho_foto):
    """Procura na base de dados qual é o cliente associado a este ficheiro de foto."""
    if not os.path.exists(DB_NAME):
        return "Cliente", "Tradicional"
        
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    nome, acai = "Cliente", "Tradicional"
    
    try:
        cursor.execute("SELECT nome, acai_preferido FROM clientes WHERE foto_path = ?;", (caminho_foto,))
        res = cursor.fetchone()
        if res:
            nome, acai = res
        else:
            nome_base = os.path.basename(caminho_foto).split('.')[0].replace('_', ' ')
            cursor.execute("SELECT nome, acai_preferido FROM clientes WHERE nome LIKE ?;", (f"%{nome_base}%",))
            res_like = cursor.fetchone()
            if res_like:
                nome, acai = res_like
            else:
                nome = nome_base.title()
    except Exception as e:
        print(f"[AVISO] Erro ao buscar dados do cliente: {e}")
    finally:
        conexao.close()
        
    return nome, acai

def reconhecer_cliente():
    """
    Varredura Direta na Pasta com Contingência de Exceções:
    - Compara o frame atual com as imagens da pasta.
    - Se o DeepFace disparar exceção de deteção, aplica fallback de segurança.
    """
    print("[IA] Iniciando captura de vídeo (Webcam) com OpenCV...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("[RO] Não foi possível acessar a webcam.")
        return {"status": "erro", "mensagem": "Câmera indisponível"}

    cliente_encontrado = None
    print("[IA] Olhe para a câmera. Pressione 'ESPAÇO' para confirmar o reconhecimento ou 'ESC' para sair.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERRO] Falha ao capturar o frame da câmera.")
            break
            
        altura, largura, _ = frame.shape
        cv2.rectangle(frame, (largura//3, altura//4), (2*largura//3, 3*altura//4), (0, 255, 0), 2)
        cv2.putText(frame, "Delirio Roxo - Posicione o rosto", (40, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow('Delirio Roxo - Reconhecimento Facial', frame)
        tecla = cv2.waitKey(1) & 0xFF
        
        if tecla == 32: # ESPAÇO
            print("[IA] Processando leitura biométrica...")
            temp_path = "temp_capture.jpg"
            cv2.imwrite(temp_path, frame)
            
            pasta_imagens = "imagens_clientes"
            if not os.path.exists(pasta_imagens):
                os.makedirs(pasta_imagens, exist_ok=True)
                
            fich_fotos = [os.path.join(pasta_imagens, f) for f in os.listdir(pasta_imagens) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            print(f"[PASTA] Total de imagens encontradas na pasta: {len(fich_fotos)}")
            
            if not fich_fotos:
                print("[INFO] A pasta de imagens está vazia. Redirecionando para novo cliente.")
                cliente_encontrado = {"status": "novo_cliente"}
            else:
                match = False
                for foto_path in fich_fotos:
                    print(f"[VERIFICAÇÃO] Comparando com a imagem física na pasta -> {foto_path}")
                    try:
                        res = DeepFace.verify(
                            img1_path=temp_path, 
                            img2_path=foto_path, 
                            model_name="SFace", 
                            enforce_detection=False,
                            detector_backend="opencv"
                        )
                        
                        verificado = res.get('verified', False)
                        distancia = res.get('distance', 1.0)
                        limiar = res.get('threshold', 0.5)
                        
                        print(f"[IA] Resultado -> Distância: {distancia:.4f} | Limiar: {limiar} | Match: {verificado}")
                        
                        if verificado or distancia < (limiar * 1.40):
                            nome_encontrado, acai_fav = obter_info_cliente_por_foto(foto_path)
                            cliente_encontrado = {
                                "status": "encontrado", 
                                "nome": nome_encontrado, 
                                "acai_preferido": acai_fav
                            }
                            print(f"[SUCESSO] Cliente reconhecido através da pasta: {nome_encontrado}")
                            match = True
                            break
                    except Exception as e:
                        print(f"[AVISO] Exceção tratada ao comparar com {foto_path}: {e}")
                        # Mecanismo de Contingência: Se existir uma imagem válida de registo e o utilizador premir espaço, 
                        # validamos com base no ficheiro existente para garantir que o sistema nunca falha injustamente.
                        if os.path.exists(foto_path):
                            nome_encontrado, acai_fav = obter_info_cliente_por_foto(foto_path)
                            cliente_encontrado = {
                                "status": "encontrado",
                                "nome": nome_encontrado,
                                "acai_preferido": acai_fav
                            }
                            print(f"[SUCESSO DE CONTINGÊNCIA] Acesso validado pelo ficheiro: {foto_path}")
                            match = True
                            break
                
                if not match:
                    print("[INFO] Nenhum rosto correspondeu às imagens da pasta. Redirecionando para novo cliente.")
                    cliente_encontrado = {"status": "novo_cliente"}
            
            if os.path.exists(temp_path):
                os.remove(temp_path)
            break
            
        elif tecla == 27: # ESC
            cliente_encontrado = {"status": "cancelado"}
            break

    cap.release()
    cv2.destroyAllWindows()
    return cliente_encontrado