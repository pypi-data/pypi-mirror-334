"""
Módulo para verificação de recursos HTTP/HTTPS
"""

import requests
from typing import Dict, Any, Optional

class HttpResource:
    """Classe para verificar recursos HTTP/HTTPS"""
    
    def __init__(self, url: str, method: str = 'HEAD'):
        """
        Inicializa um recurso HTTP/HTTPS
        
        Args:
            url: URL do recurso
            method: Método HTTP a ser usado (HEAD ou GET)
        """
        self.url = url
        self.method = method.upper()
        if self.method not in ('HEAD', 'GET'):
            raise ValueError("Método HTTP deve ser HEAD ou GET")
    
    def is_available(self) -> bool:
        """
        Verifica se o recurso HTTP/HTTPS está disponível
        
        Returns:
            bool: True se o recurso estiver disponível, False caso contrário
        """
        try:
            if self.method == 'HEAD':
                response = requests.head(self.url, timeout=5, allow_redirects=True)
            else:  # GET
                response = requests.get(self.url, timeout=5, allow_redirects=True)
            
            return 200 <= response.status_code < 300
        except Exception:  # Captura qualquer exceção, não apenas RequestException
            return False
