"""
Módulo para verificação de recursos TCP
"""

import socket
from typing import Dict, Any, Optional

class TcpResource:
    """Classe para verificar recursos TCP"""
    
    def __init__(self, host: str, port: int):
        """
        Inicializa um recurso TCP
        
        Args:
            host: Nome do host ou endereço IP
            port: Número da porta
        """
        self.host = host
        self.port = port
    
    def is_available(self) -> bool:
        """
        Verifica se a porta TCP está aberta
        
        Returns:
            bool: True se a porta estiver aberta, False caso contrário
        """
        try:
            with socket.create_connection((self.host, self.port), timeout=5):
                return True
        except (socket.timeout, socket.error):
            return False
