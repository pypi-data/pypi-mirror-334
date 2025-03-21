#!/usr/bin/env python
"""
Exemplo de uso do Python Wait-On com múltiplos recursos
"""

import os
import time
import threading
import http.server
import socketserver
from python_wait_on.wait_on import wait_on

def iniciar_servidor_http(porta):
    """Inicia um servidor HTTP simples na porta especificada"""
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", porta), handler)
    print(f"Servidor HTTP iniciado na porta {porta}")
    httpd.serve_forever()

def criar_arquivo_apos_delay(caminho, delay):
    """Cria um arquivo após um delay especificado"""
    print(f"Aguardando {delay} segundos para criar o arquivo {caminho}...")
    time.sleep(delay)
    with open(caminho, 'w') as f:
        f.write("Conteúdo de teste")
    print(f"Arquivo {caminho} criado")

def main():
    # Criar diretório temporário para os arquivos
    os.makedirs("temp", exist_ok=True)
    arquivo1 = "temp/arquivo1.txt"
    arquivo2 = "temp/arquivo2.txt"
    
    # Iniciar servidor HTTP na porta 8001
    servidor_thread = threading.Thread(target=iniciar_servidor_http, args=(8001,))
    servidor_thread.daemon = True
    servidor_thread.start()
    
    # Criar arquivo1 após 2 segundos
    arquivo1_thread = threading.Thread(target=criar_arquivo_apos_delay, args=(arquivo1, 2))
    arquivo1_thread.daemon = True
    arquivo1_thread.start()
    
    # Criar arquivo2 após 4 segundos
    arquivo2_thread = threading.Thread(target=criar_arquivo_apos_delay, args=(arquivo2, 4))
    arquivo2_thread.daemon = True
    arquivo2_thread.start()
    
    # Aguardar por múltiplos recursos
    print("\nAguardando por múltiplos recursos...")
    recursos = [
        "http://localhost:8001",  # Servidor HTTP
        arquivo1,                 # Arquivo 1
        arquivo2,                 # Arquivo 2
        "tcp:localhost:8001"      # Porta TCP
    ]
    
    resultado = wait_on(
        resources=recursos,
        timeout=10000,  # 10 segundos
        interval=500,   # verificar a cada 500ms
        window=1000,    # janela de estabilidade de 1 segundo
        verbose=True
    )
    
    if resultado:
        print("\nTodos os recursos estão disponíveis!")
    else:
        print("\nTimeout ao aguardar pelos recursos")
    
    # Limpar arquivos temporários
    try:
        os.remove(arquivo1)
        os.remove(arquivo2)
        print("Arquivos temporários removidos")
    except:
        pass

if __name__ == "__main__":
    main()
