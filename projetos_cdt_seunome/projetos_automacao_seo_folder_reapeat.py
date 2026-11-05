import os
from PIL import Image
import imagehash

# A pasta onde estão as fotos que queremos organizar
pasta_fotos = r"C:\Users\ivsilva\Documents\Fotos WhatsApp Galeria"

# Um "caderno de notas" para guardar as impressões digitais das fotos que já vimos
fotos_vistas = {}

# O robozinho vai olhar todos os arquivos na pasta
for pasta_atual, subpastas, arquivos in os.walk(pasta_fotos):
    for arquivo in arquivos:
        
        nome_minusculo = arquivo.lower()
        
        # Verificamos se é uma imagem
        if nome_minusculo.endswith(('.png', '.jpg', '.jpeg')):
            caminho_arquivo = os.path.join(pasta_atual, arquivo)
            
            try:
                # 1. O robô abre a foto e cria a "impressão digital" dela (o hash)
                imagem = Image.open(caminho_arquivo)
                impressao_digital = imagehash.average_hash(imagem)
                
                # 2. Vimos se essa impressão digital já está no nosso caderno
                if impressao_digital in fotos_vistas:
                    # Se já existe, significa que é uma foto repetida!
                    print(f"Encontrei uma cópia repetida: '{arquivo}' é igual a '{fotos_vistas[impressao_digital]}'. Apagando...")
                    
                    # Fechamos a imagem para o computador não ficar zangado
                    imagem.close()
                    
                    # Apagamos a cópia repetida para sobrar só uma
                    os.remove(caminho_arquivo)
                else:
                    # Se for a primeira vez que vemos essa foto, anotamos no caderno
                    fotos_vistas[impressao_digital] = arquivo
                    imagem.close()
                    
            except Exception as e:
                print(f"Ops, não consegui ler o arquivo {arquivo}. Erro: {e}")

print("Prontinho! Faxina feita e todas as fotos repetidas foram eliminadas! 🎉")