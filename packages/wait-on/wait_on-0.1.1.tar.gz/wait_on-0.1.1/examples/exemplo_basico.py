#!/usr/bin/env python
"""
Exemplo básico de uso do Python Wait-On via API Python
"""

import time
import threading
import http.server
import socketserver
from python_wait_on.wait_on import wait_on

def iniciar_servidor_http():
    """Inicia um servidor HTTP simples na porta 8000"""
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", 8000), handler)
    print("Servidor HTTP iniciado na porta 8000")
    httpd.serve_forever()

def main():
    # Iniciar servidor HTTP em uma thread separada
    servidor_thread = threading.Thread(target=iniciar_servidor_http)
    servidor_thread.daemon = True
    servidor_thread.start()
    
    print("Aguardando 2 segundos para o servidor iniciar...")
    time.sleep(2)
    
    # Aguardar pelo servidor HTTP
    print("Verificando se o servidor HTTP está disponível...")
    resultado = wait_on(
        resources=["http://localhost:8000"],
        timeout=5000,  # 5 segundos
        interval=100,  # verificar a cada 100ms
        verbose=True
    )
    
    if resultado:
        print("Servidor HTTP está disponível!")
    else:
        print("Timeout ao aguardar pelo servidor HTTP")
    
    # Aguardar por um arquivo que não existe (deve falhar com timeout)
    print("\nVerificando arquivo inexistente (deve falhar)...")
    resultado = wait_on(
        resources=["arquivo_inexistente.txt"],
        timeout=2000,  # 2 segundos
        interval=100,  # verificar a cada 100ms
        verbose=True
    )
    
    if resultado:
        print("Arquivo está disponível!")
    else:
        print("Timeout ao aguardar pelo arquivo (esperado)")
    
    # Aguardar por um arquivo que não existe no modo reverso (deve ter sucesso)
    print("\nVerificando arquivo inexistente no modo reverso (deve ter sucesso)...")
    resultado = wait_on(
        resources=["arquivo_inexistente.txt"],
        timeout=2000,  # 2 segundos
        interval=100,  # verificar a cada 100ms
        reverse=True,  # modo reverso
        verbose=True
    )
    
    if resultado:
        print("Arquivo não está disponível (modo reverso)!")
    else:
        print("Timeout ao aguardar pelo arquivo no modo reverso")

if __name__ == "__main__":
    main()
