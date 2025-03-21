#!/usr/bin/env python
"""
Exemplo de uso do Python Wait-On com recursos de diretório
"""

import os
import time
import threading
import tempfile
import shutil
from python_wait_on.wait_on import wait_on

def criar_diretorio_apos_delay(caminho, delay):
    """Cria um diretório após um delay especificado"""
    print(f"Aguardando {delay} segundos para criar o diretório {caminho}...")
    time.sleep(delay)
    os.makedirs(caminho, exist_ok=True)
    print(f"Diretório {caminho} criado")

def main():
    # Criar diretório temporário para os testes
    temp_dir = tempfile.mkdtemp()
    diretorio_teste = os.path.join(temp_dir, "diretorio_teste")
    
    # Criar diretório após 3 segundos
    thread = threading.Thread(target=criar_diretorio_apos_delay, args=(diretorio_teste, 3))
    thread.daemon = True
    thread.start()
    
    # Aguardar pelo diretório
    print("\nAguardando pela criação do diretório...")
    resultado = wait_on(
        resources=[f'dir:{diretorio_teste}'],
        timeout=10000,  # 10 segundos
        interval=500,   # verificar a cada 500ms
        verbose=True
    )
    
    if resultado:
        print(f"\nDiretório {diretorio_teste} está disponível!")
    else:
        print(f"\nTimeout ao aguardar pelo diretório {diretorio_teste}")
    
    # Limpar diretórios temporários
    try:
        shutil.rmtree(temp_dir)
        print("Diretórios temporários removidos")
    except:
        pass

if __name__ == "__main__":
    main()
