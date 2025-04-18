import struct

def extrair_wav(arquivo_entrada):
    with open(arquivo_entrada, "rb") as f:
        posicao = 0
        contador = 1
        total_bytes = len(f.read())  # Gets the total file size for monitoring

       # Reopen the file for reading, since f.read() has already moved the pointer to the end
        f.seek(0) 
        while True:
            f.seek(posicao)
            
            # Read 4 bytes to verify the "RIFF" signature
            header = f.read(4)
            
            if header == b"RIFF":
                print(f"\nAssinatura 'RIFF' encontrada na posição {posicao} ({(posicao / total_bytes) * 100:.2f}% do arquivo processado)")

                tamanho_riff = struct.unpack("<I", f.read(4))[0]
                
                # Read the "WAVE" identifier after the size (4 bytes)
                wave_id = f.read(4)
                
                if wave_id != b"WAVE":
                    print("Erro: Esperado 'WAVE' após RIFF.")
                    break
                
               # The file found has signature "RIFF" and "WAVE", it is a WAV file
                print(f"Arquivo WAV encontrado na posição {posicao}, tamanho: {tamanho_riff + 8} bytes")
          
                dados_inicio = f.tell()
                
                dados_fim = dados_inicio + tamanho_riff - 4
                
               # Read data from the WAV file
                f.seek(dados_inicio)
                dados = f.read(tamanho_riff - 4)
                
               # Save the extracted WAV file
                nome_arquivo_saida = f"audio_{contador}.wav"
                with open(nome_arquivo_saida, "wb") as out:
                    out.write(b"RIFF")
                    out.write(struct.pack("<I", tamanho_riff + 8))
                    out.write(b"WAVE")
                    out.write(dados) 
                
                print(f"Arquivo WAV {nome_arquivo_saida} extraído com sucesso!")
                contador += 1

                # Update the position to search for the next "RIFF"
                posicao = dados_fim
            else:             
                f.seek(posicao + 1)
                posicao = f.tell()

            # If the end of the file is reached, terminate the process
            if f.tell() >= total_bytes:
                print("Fim do arquivo. Extração concluída.")
                break

# Call the function to extract the WAV files
arquivo_entrada = "OLTAUNT.LAB" # REPLACE WITH YOUR FILE NAME (THIS IS AN OUTLAWS FILENAME)
extrair_wav(arquivo_entrada)
