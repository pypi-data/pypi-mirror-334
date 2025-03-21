"""
Módulo para verificação de recursos de diretório
"""

import os
import time
from typing import Dict, Any, Optional

class DirectoryResource:
    """Classe para verificar recursos de diretório"""
    
    def __init__(self, path: str):
        """
        Inicializa um recurso de diretório
        
        Args:
            path: Caminho para o diretório
        """
        self.path = path
        self.last_modified = None
        self.last_check_time = None
    
    def is_available(self) -> bool:
        """
        Verifica se o diretório existe
        
        Returns:
            bool: True se o diretório existir, False caso contrário
        """
        return os.path.isdir(self.path)
    
    def has_changed(self) -> bool:
        """
        Verifica se o diretório mudou desde a última verificação
        
        Returns:
            bool: True se o diretório mudou, False caso contrário
        """
        if not self.is_available():
            changed = self.last_modified is not None
            self.last_modified = None
            return changed
        
        try:
            # Verificar a data de modificação do diretório
            current_modified = os.path.getmtime(self.path)
            current_time = time.time()
            
            if self.last_modified is None:
                self.last_modified = current_modified
                self.last_check_time = current_time
                return True
            
            changed = current_modified != self.last_modified
            self.last_modified = current_modified
            self.last_check_time = current_time
            
            return changed
        except (OSError, IOError):
            return True
