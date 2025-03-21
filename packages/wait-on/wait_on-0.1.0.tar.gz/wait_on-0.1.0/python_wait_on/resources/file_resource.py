"""
Módulo para verificação de recursos de arquivo
"""

import os
import time
from typing import Dict, Any, Optional

class FileResource:
    """Classe para verificar recursos de arquivo"""
    
    def __init__(self, path: str):
        """
        Inicializa um recurso de arquivo
        
        Args:
            path: Caminho para o arquivo
        """
        self.path = path
        self.last_size = None
        self.last_check_time = None
    
    def is_available(self) -> bool:
        """
        Verifica se o arquivo existe
        
        Returns:
            bool: True se o arquivo existir, False caso contrário
        """
        return os.path.exists(self.path)
    
    def has_changed(self) -> bool:
        """
        Verifica se o arquivo mudou desde a última verificação
        
        Returns:
            bool: True se o arquivo mudou, False caso contrário
        """
        if not self.is_available():
            changed = self.last_size is not None
            self.last_size = None
            return changed
        
        try:
            current_size = os.path.getsize(self.path)
            current_time = time.time()
            
            if self.last_size is None:
                self.last_size = current_size
                self.last_check_time = current_time
                return True
            
            changed = current_size != self.last_size
            self.last_size = current_size
            self.last_check_time = current_time
            
            return changed
        except (OSError, IOError):
            return True
