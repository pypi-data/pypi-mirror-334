#!/usr/bin/env python
"""
Demonstração de um cenário real de uso do Python Wait-On
"""

import os
import time
import threading
import subprocess
import tempfile
from python_wait_on.wait_on import wait_on

def iniciar_servidor_http(porta):
    """Inicia um servidor HTTP simples na porta especificada"""
    print(f"Iniciando servidor HTTP na porta {porta}...")
    # Usar subprocess para iniciar o servidor em um processo separado
    return subprocess.Popen(
        ["python", "-m", "http.server", str(porta)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

def criar_arquivo_apos_delay(caminho, delay):
    """Cria um arquivo após um delay especificado"""
    print(f"Arquivo {caminho} será criado após {delay} segundos...")
    time.sleep(delay)
    with open(caminho, 'w') as f:
        f.write(f"Arquivo criado em {time.time()}")
    print(f"Arquivo {caminho} criado!")

def main():
    """Função principal que demonstra um cenário real de uso"""
    print("=== Demonstração de Cenário Real do Python Wait-On ===\n")
    
    # Criar diretório temporário
    temp_dir = tempfile.mkdtemp()
    print(f"Diretório temporário criado: {temp_dir}")
    
    # Definir caminhos de arquivos
    arquivo1 = os.path.join(temp_dir, "config.json")
    arquivo2 = os.path.join(temp_dir, "data.txt")
    
    # Iniciar servidor HTTP na porta 8765
    servidor = iniciar_servidor_http(8765)
    
    # Criar threads para gerar arquivos com delays diferentes
    thread1 = threading.Thread(target=criar_arquivo_apos_delay, args=(arquivo1, 3))
    thread2 = threading.Thread(target=criar_arquivo_apos_delay, args=(arquivo2, 5))
    
    # Iniciar threads
    thread1.start()
    thread2.start()
    
    print("\n=== Simulando um pipeline de inicialização ===")
    
    # Etapa 1: Aguardar pelo servidor HTTP
    print("\nEtapa 1: Aguardando servidor HTTP iniciar...")
    resultado = wait_on(
        resources=["http://localhost:8765"],
        timeout=10000,
        interval=500,
        verbose=True
    )
    
    if resultado:
        print("✓ Servidor HTTP está disponível!")
    else:
        print("✗ Timeout ao aguardar pelo servidor HTTP")
        return
    
    # Etapa 2: Aguardar pelo arquivo de configuração
    print("\nEtapa 2: Aguardando arquivo de configuração ser gerado...")
    resultado = wait_on(
        resources=[arquivo1],
        timeout=10000,
        interval=500,
        verbose=True
    )
    
    if resultado:
        print(f"✓ Arquivo de configuração disponível: {arquivo1}")
    else:
        print("✗ Timeout ao aguardar pelo arquivo de configuração")
        return
    
    # Etapa 3: Aguardar pelo arquivo de dados
    print("\nEtapa 3: Aguardando arquivo de dados ser gerado...")
    resultado = wait_on(
        resources=[arquivo2],
        timeout=10000,
        interval=500,
        verbose=True
    )
    
    if resultado:
        print(f"✓ Arquivo de dados disponível: {arquivo2}")
    else:
        print("✗ Timeout ao aguardar pelo arquivo de dados")
        return
    
    # Etapa 4: Aguardar por múltiplos recursos simultaneamente
    print("\nEtapa 4: Verificando todos os recursos novamente...")
    resultado = wait_on(
        resources=[
            "http://localhost:8765",
            arquivo1,
            arquivo2,
            "tcp:localhost:8765"
        ],
        timeout=2000,
        interval=500,
        verbose=True
    )
    
    if resultado:
        print("✓ Todos os recursos estão disponíveis!")
    else:
        print("✗ Nem todos os recursos estão disponíveis")
    
    # Encerrar o servidor HTTP
    print("\nEncerrando servidor HTTP...")
    servidor.terminate()
    servidor.wait()
    
    # Etapa 5: Aguardar pelo servidor ser encerrado (modo reverso)
    print("\nEtapa 5: Aguardando servidor HTTP encerrar (modo reverso)...")
    resultado = wait_on(
        resources=["tcp:localhost:8765"],
        timeout=5000,
        interval=500,
        reverse=True,
        verbose=True
    )
    
    if resultado:
        print("✓ Servidor HTTP foi encerrado com sucesso!")
    else:
        print("✗ Timeout ao aguardar pelo encerramento do servidor")
    
    # Limpar arquivos temporários
    print(f"\nLimpando arquivos temporários em {temp_dir}...")
    try:
        os.remove(arquivo1)
        os.remove(arquivo2)
        os.rmdir(temp_dir)
        print("✓ Arquivos temporários removidos com sucesso!")
    except Exception as e:
        print(f"✗ Erro ao remover arquivos temporários: {e}")
    
    print("\n=== Demonstração concluída com sucesso! ===")

if __name__ == "__main__":
    main()
