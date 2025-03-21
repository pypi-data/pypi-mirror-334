"""
Python Wait-On - Utilitário para aguardar recursos como arquivos, portas, sockets e HTTP(S)

Este pacote fornece uma implementação em Python do utilitário wait-on, inspirada na 
versão Node.js. Ele permite aguardar por recursos como arquivos, portas TCP, sockets 
de domínio e endpoints HTTP(S) ficarem disponíveis (ou indisponíveis no modo reverso).

Exemplos de uso:
    
    # Via linha de comando
    python-wait-on arquivo.txt && echo "Arquivo disponível!"
    python-wait-on http://localhost:8000 && echo "API disponível!"
    python-wait-on tcp:5000 && echo "Porta disponível!"
    
    # Via API Python
    from python_wait_on.wait_on import wait_on
    result = wait_on(['arquivo.txt', 'http://localhost:8000'])
"""

__version__ = "0.1.0"
__author__ = "Devin AI"
__email__ = "devin-ai-integration[bot]@users.noreply.github.com"
__license__ = "MIT"
