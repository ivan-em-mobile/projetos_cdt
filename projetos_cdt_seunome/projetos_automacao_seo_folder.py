import os
import shutil

# A nossa pasta principal onde as imagens vão ficar reunidas
pasta_principal = r"C:\Users\ivsilva\Documents\fotosnov2026"

# Um contador para numerar as imagens de forma progressiva (1, 2, 3...)
contador = 1

# O nosso robozinho vai olhar a pasta principal e todas as subpastas dentro dela
for pasta_atual, subpastas, arquivos in os.walk(pasta_principal):
    
    # Para evitar que o robô tente mexer na própria pasta principal de forma confusa,
    # nós dizemos para ele só mexer nas pastas que estão *dentro* dela.
    if pasta_atual == pasta_principal:
        continue

    for arquivo in arquivos:
        
        # Deixamos o nome em letras minúsculas para não errar o formato
        nome_minusculo = arquivo.lower()
        
        # Verificamos se o arquivo é uma imagem (termina com .png, .jpg ou .jpeg)
        if nome_minusculo.endswith(('.png', '.jpg', '.jpeg')):
            
            # Descobrimos o formato original da imagem (ex: .jpg ou .png)
            extensao = os.path.splitext(arquivo)[1]
            
            # Criamos o novo nome bonitinho: 2026-NOV-1.jpg, 2026-NOV-2.jpg...
            novo_nome = f"2026-NOV-{contador}{extensao}"
            
            # Onde a imagem está agora (dentro da subpasta)
            caminho_antigo = os.path.join(pasta_atual, arquivo)
            
            # Para onde a imagem vai (direto na pasta principal)
            caminho_novo = os.path.join(pasta_principal, novo_nome)
            
            # O robozinho move a imagem e já muda o nome dela!
            shutil.move(caminho_antigo, caminho_novo)
            print(f"Oba! A imagem '{arquivo}' foi retirada da subpasta e virou '{novo_nome}' na pasta principal!")
            
            # Aumentamos o número do contador para a próxima imagem
            contador += 1

print("Prontinho! Todas as imagens foram resgatadas e organizadas com sucesso! 🎉")