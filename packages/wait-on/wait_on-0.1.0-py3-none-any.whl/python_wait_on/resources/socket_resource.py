"""
Módulo para verificação de recursos de socket de domínio
"""

import socket
from typing import Dict, Any, Optional

class SocketResource:
    """Classe para verificar recursos de socket de domínio"""
    
    def __init__(self, path: str):
        """
        Inicializa um recurso de socket de domínio
        
        Args:
            path: Caminho para o socket
        """
        self.path = path
    
    def is_available(self) -> bool:
        """
        Verifica se o socket de domínio está disponível
        
        Returns:
            bool: True se o socket estiver disponível, False caso contrário
        """
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(self.path)
            sock.close()
            return True
        except (socket.timeout, socket.error, FileNotFoundError):
            return False
