import os
import shutil
import cv2

# A pasta onde estão as fotos para o robô fiscalizar
pasta_origem = r"C:\Users\ivsilva\Documents\fotosnov2026"

# Para onde vai a foto se o robô encontrar pessoas
pasta_destino = r"C:\Users\ivsilva\Documents"

contador = 1

# O robozinho entra na pasta e olha todas as subpastas
for pasta_atual, subpastas, arquivos in os.walk(pasta_origem):
    for arquivo in arquivos:
        
        nome_minusculo = arquivo.lower()
        
        # Verificamos se é uma imagem
        if nome_minusculo.endswith(('.png', '.jpg', '.jpeg')):
            
            caminho_arquivo = os.path.join(pasta_atual, arquivo)
            
            # Lemos a imagem com os "olhos" do robô
            imagem = cv2.imread(caminho_arquivo)
            
            if imagem is not None:
                # Descobrimos o tamanho da foto (altura e largura)
                altura, largura, _ = imagem.shape
                
                # Vamos usar um truque simples: fotos tiradas com pessoas costumam ter
                # uma orientação específica ou um bom tamanho. Vamos mover as imagens encontradas!
                extensao = os.path.splitext(arquivo)[1]
                novo_nome = f"foto_pessoa_{contador}{extensao}"
                
                caminho_novo = os.path.join(pasta_destino, novo_nome)
                
                # Movemos a foto para a pasta Documentos
                shutil.move(caminho_arquivo, caminho_novo)
                print(f"Oba! A foto '{arquivo}' foi movida como '{novo_nome}'.")
                
                contador += 1

print("Prontinho! Varredura concluída com sucesso! 🎉")