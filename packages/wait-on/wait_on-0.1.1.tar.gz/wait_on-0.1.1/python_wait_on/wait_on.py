"""
Módulo principal do Python Wait-On que implementa a funcionalidade de aguardar recursos

Este módulo contém a função principal wait_on e funções auxiliares para verificar
diferentes tipos de recursos (arquivos, HTTP, TCP, sockets).

Exemplos de uso:
    
    # Aguardar por um arquivo
    result = wait_on(['arquivo.txt'])
    
    # Aguardar por múltiplos recursos com opções personalizadas
    result = wait_on(
        resources=['http://localhost:8000', 'tcp:localhost:5000'],
        delay=1000,       # Atraso inicial de 1 segundo
        interval=500,     # Verificar a cada 0.5 segundos
        timeout=30000,    # Timeout de 30 segundos
        reverse=False,    # Modo normal (não reverso)
        window=1000,      # Janela de estabilidade de 1 segundo
        verbose=True      # Modo verboso
    )
"""

import os
import time
import socket
import logging
import requests
from typing import List, Dict, Any, Tuple, Optional, Union, Callable
from urllib.parse import urlparse

# Configuração de logging
logging.basicConfig(format='%(levelname)s: %(message)s')
logger = logging.getLogger('python-wait-on')

# Tipos de recursos suportados
FILE_TYPE = 'file'
HTTP_TYPE = 'http'
HTTPS_TYPE = 'https'
HTTP_GET_TYPE = 'http-get'
HTTPS_GET_TYPE = 'https-get'
TCP_TYPE = 'tcp'
SOCKET_TYPE = 'socket'
DIRECTORY_TYPE = 'dir'

def wait_on(
    resources: List[str],
    delay: int = 0,
    interval: int = 250,
    reverse: bool = False,
    timeout: int = 0,  # 0 significa infinito
    window: int = 750,
    verbose: bool = False
) -> bool:
    """
    Aguarda por recursos como arquivos, portas, sockets e HTTP(S) ficarem disponíveis.
    
    Args:
        resources: Lista de recursos para aguardar
        delay: Atraso inicial antes de verificar os recursos em ms
        interval: Intervalo para verificar os recursos em ms
        reverse: Operação reversa, aguardar até que os recursos NÃO estejam disponíveis
        timeout: Tempo máximo em ms para aguardar antes de sair com código de falha (1), 0 para infinito
        window: Janela de estabilidade em ms
        verbose: Exibir informações detalhadas durante a execução
        
    Returns:
        bool: True se todos os recursos estiverem disponíveis (ou não disponíveis no modo reverso), False caso contrário
    """
    # Configurar nível de log
    if verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)
    
    # Validar recursos
    if not resources:
        logger.error("Nenhum recurso especificado")
        return False
    
    # Converter tempos de ms para segundos
    delay_sec = delay / 1000.0
    interval_sec = interval / 1000.0
    timeout_sec = timeout / 1000.0 if timeout > 0 else float('inf')
    window_sec = window / 1000.0
    
    # Atraso inicial
    if delay_sec > 0:
        logger.info(f"Aguardando atraso inicial de {delay_sec:.2f} segundos")
        time.sleep(delay_sec)
    
    # Preparar recursos
    resource_checkers = []
    resource_states = {}  # Dicionário para armazenar o estado de cada recurso
    
    for resource in resources:
        checker = _create_resource_checker(resource)
        if checker:
            resource_checkers.append(checker)
            resource_states[checker[0]] = False  # Inicializar estado como False (não disponível)
        else:
            logger.error(f"Tipo de recurso não suportado: {resource}")
            return False
    
    # Iniciar monitoramento
    start_time = time.time()
    last_change_time = start_time
    stable_since = start_time
    
    logger.info(f"Iniciando monitoramento de {len(resource_checkers)} recursos")
    
    while True:
        # Verificar timeout
        elapsed = time.time() - start_time
        if elapsed > timeout_sec and timeout_sec != float('inf'):
            logger.error(f"Timeout após {elapsed:.2f} segundos")
            return False
        
        # Verificar todos os recursos
        all_available = True
        any_changed = False
        
        for resource, check_func in resource_checkers:
            try:
                available = check_func()
                
                # No modo reverso, queremos que o recurso NÃO esteja disponível
                if reverse:
                    available = not available
                
                if not available:
                    all_available = False
                    logger.info(f"Recurso ainda não está {'indisponível' if reverse else 'disponível'}: {resource}")
                else:
                    logger.info(f"Recurso está {'indisponível' if reverse else 'disponível'}: {resource}")
                
                # Se o estado mudou desde a última verificação, atualizar o tempo de mudança
                if available != resource_states[resource]:
                    resource_states[resource] = available  # Atualizar estado
                    any_changed = True
            except Exception as e:
                logger.info(f"Erro ao verificar recurso {resource}: {str(e)}")
                all_available = False
        
        # Se houve mudança, atualizar o tempo da última mudança
        if any_changed:
            last_change_time = time.time()
            stable_since = last_change_time
        
        # Se todos os recursos estão disponíveis e estáveis pelo período da janela
        if all_available and (time.time() - stable_since) >= window_sec:
            logger.info(f"Todos os recursos estão {'indisponíveis' if reverse else 'disponíveis'} e estáveis por {window_sec:.2f} segundos")
            return True
        
        # Aguardar intervalo antes da próxima verificação
        time.sleep(interval_sec)

def _create_resource_checker(resource: str) -> Optional[Tuple[str, Callable[[], bool]]]:
    """
    Cria uma função de verificação para o recurso especificado.
    
    Args:
        resource: String do recurso a ser verificado
        
    Returns:
        Tupla contendo (recurso, função_verificação) ou None se o tipo não for suportado
    """
    # Determinar o tipo de recurso
    if resource.startswith(('http://', 'https://')):
        return (resource, lambda: _check_http(resource, 'HEAD'))
    elif resource.startswith(('http-get://', 'https-get://')):
        url = resource.replace('http-get://', 'http://').replace('https-get://', 'https://')
        return (resource, lambda: _check_http(url, 'GET'))
    elif resource.startswith('tcp:'):
        parts = resource[4:].split(':')
        if len(parts) == 1:
            host, port = 'localhost', parts[0]
        else:
            host, port = parts
        return (resource, lambda: _check_tcp(host, int(port)))
    elif resource.startswith('socket:'):
        socket_path = resource[7:]
        return (resource, lambda: _check_socket(socket_path))
    elif resource.startswith('dir:'):
        dir_path = resource[4:]
        return (resource, lambda: _check_directory(dir_path))
    elif ':' not in resource or resource.startswith('file:'):
        # Se não tiver prefixo ou começar com file:, assume que é um arquivo
        path = resource[5:] if resource.startswith('file:') else resource
        return (resource, lambda: _check_file(path))
    
    return None

def _check_file(path: str) -> bool:
    """Verifica se um arquivo existe."""
    return os.path.exists(path)

def _check_http(url: str, method: str = 'HEAD') -> bool:
    """Verifica se um recurso HTTP/HTTPS está disponível."""
    try:
        if method == 'HEAD':
            response = requests.head(url, timeout=5, allow_redirects=True)
        else:  # GET
            response = requests.get(url, timeout=5, allow_redirects=True)
        
        return 200 <= response.status_code < 300
    except Exception:  # Captura qualquer exceção, não apenas RequestException
        return False

def _check_tcp(host: str, port: int) -> bool:
    """Verifica se uma porta TCP está aberta."""
    try:
        with socket.create_connection((host, port), timeout=5):
            return True
    except (socket.timeout, socket.error):
        return False

def _check_socket(socket_path: str) -> bool:
    """Verifica se um socket de domínio está disponível."""
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(socket_path)
        sock.close()
        return True
    except (socket.timeout, socket.error, FileNotFoundError):
        return False

def _check_directory(path: str) -> bool:
    """Verifica se um diretório existe."""
    return os.path.isdir(path)
