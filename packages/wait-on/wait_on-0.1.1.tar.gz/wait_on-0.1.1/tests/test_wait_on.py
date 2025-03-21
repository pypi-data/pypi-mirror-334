"""
Testes unitários para o módulo wait_on
"""

import os
import time
import socket
import unittest
import threading
import http.server
import socketserver
from tempfile import NamedTemporaryFile, mkdtemp
from shutil import rmtree
from unittest.mock import patch, MagicMock

from python_wait_on.wait_on import wait_on, _check_file, _check_http, _check_tcp, _check_socket, _check_directory

class TestWaitOn(unittest.TestCase):
    """Testes para a função wait_on e funções auxiliares"""
    
    def setUp(self):
        """Configuração para os testes"""
        self.temp_dir = mkdtemp()
        self.temp_file = os.path.join(self.temp_dir, 'test_file.txt')
        
        # Criar arquivo temporário
        with open(self.temp_file, 'w') as f:
            f.write('test content')
    
    def tearDown(self):
        """Limpeza após os testes"""
        rmtree(self.temp_dir)
    
    def test_check_file(self):
        """Testa a função _check_file"""
        # Arquivo existente
        self.assertTrue(_check_file(self.temp_file))
        
        # Arquivo não existente
        non_existent_file = os.path.join(self.temp_dir, 'non_existent.txt')
        self.assertFalse(_check_file(non_existent_file))
    
    @patch('requests.head')
    def test_check_http_head(self, mock_head):
        """Testa a função _check_http com método HEAD"""
        # Resposta de sucesso
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_head.return_value = mock_response
        
        self.assertTrue(_check_http('http://example.com', 'HEAD'))
        mock_head.assert_called_with('http://example.com', timeout=5, allow_redirects=True)
        
        # Resposta de erro
        mock_response.status_code = 404
        self.assertFalse(_check_http('http://example.com', 'HEAD'))
    
    @patch('requests.head')
    def test_check_http_head_exception(self, mock_head):
        """Testa a função _check_http com método HEAD quando ocorre uma exceção"""
        # Exceção
        mock_head.side_effect = Exception('Connection error')
        self.assertFalse(_check_http('http://example.com', 'HEAD'))
    
    @patch('requests.get')
    def test_check_http_get(self, mock_get):
        """Testa a função _check_http com método GET"""
        # Resposta de sucesso
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        self.assertTrue(_check_http('http://example.com', 'GET'))
        mock_get.assert_called_with('http://example.com', timeout=5, allow_redirects=True)
        
        # Resposta de erro
        mock_response.status_code = 500
        self.assertFalse(_check_http('http://example.com', 'GET'))
    
    @patch('requests.get')
    def test_check_http_get_exception(self, mock_get):
        """Testa a função _check_http com método GET quando ocorre uma exceção"""
        # Exceção
        mock_get.side_effect = Exception('Connection error')
        self.assertFalse(_check_http('http://example.com', 'GET'))
    
    @patch('socket.create_connection')
    def test_check_tcp(self, mock_create_connection):
        """Testa a função _check_tcp"""
        # Conexão bem-sucedida
        mock_socket = MagicMock()
        mock_create_connection.return_value = mock_socket
        
        self.assertTrue(_check_tcp('localhost', 8000))
        mock_create_connection.assert_called_with(('localhost', 8000), timeout=5)
        
        # Falha na conexão
        mock_create_connection.side_effect = socket.error('Connection refused')
        self.assertFalse(_check_tcp('localhost', 8000))
    
    @patch('socket.socket')
    def test_check_socket(self, mock_socket_class):
        """Testa a função _check_socket"""
        # Conexão bem-sucedida
        mock_socket = MagicMock()
        mock_socket_class.return_value = mock_socket
        
        self.assertTrue(_check_socket('/tmp/test.sock'))
        mock_socket.connect.assert_called_with('/tmp/test.sock')
        
        # Falha na conexão
        mock_socket.connect.side_effect = socket.error('Connection refused')
        self.assertFalse(_check_socket('/tmp/test.sock'))
    
    def test_wait_on_file(self):
        """Testa wait_on com arquivo"""
        # Arquivo existente
        result = wait_on([self.temp_file], timeout=1000)
        self.assertTrue(result)
        
        # Arquivo não existente
        non_existent_file = os.path.join(self.temp_dir, 'non_existent.txt')
        result = wait_on([non_existent_file], timeout=1000)
        self.assertFalse(result)
    
    def test_wait_on_reverse(self):
        """Testa wait_on no modo reverso"""
        # Arquivo existente, modo reverso (deve falhar)
        result = wait_on([self.temp_file], reverse=True, timeout=1000)
        self.assertFalse(result)
        
        # Arquivo não existente, modo reverso (deve ter sucesso)
        non_existent_file = os.path.join(self.temp_dir, 'non_existent.txt')
        result = wait_on([non_existent_file], reverse=True, timeout=1000)
        self.assertTrue(result)
    
    def test_wait_on_delay(self):
        """Testa wait_on com atraso"""
        start_time = time.time()
        result = wait_on([self.temp_file], delay=100, timeout=2000)
        elapsed = time.time() - start_time
        
        self.assertTrue(result)
        self.assertGreaterEqual(elapsed, 0.1)  # Pelo menos 100ms de atraso
    
    def test_wait_on_timeout(self):
        """Testa wait_on com timeout"""
        non_existent_file = os.path.join(self.temp_dir, 'non_existent.txt')
        
        start_time = time.time()
        # Usar valores muito pequenos para o teste ser rápido
        result = wait_on([non_existent_file], timeout=50, interval=5, window=5)
        elapsed = time.time() - start_time
        
        self.assertFalse(result)
        self.assertGreaterEqual(elapsed, 0.05)  # Pelo menos 50ms de timeout
        self.assertLess(elapsed, 0.5)  # Não deve demorar muito mais que o timeout
    
    def test_wait_on_multiple_resources(self):
        """Testa wait_on com múltiplos recursos"""
        # Criar segundo arquivo temporário
        second_temp_file = os.path.join(self.temp_dir, 'second_test_file.txt')
        with open(second_temp_file, 'w') as f:
            f.write('test content')
        
        # Ambos os arquivos existem
        result = wait_on([self.temp_file, second_temp_file], timeout=1000)
        self.assertTrue(result)
        
        # Um arquivo não existe
        non_existent_file = os.path.join(self.temp_dir, 'non_existent.txt')
        result = wait_on([self.temp_file, non_existent_file], timeout=1000)
        self.assertFalse(result)
        
    def test_check_directory(self):
        """Testa a função _check_directory"""
        # Diretório existente
        temp_dir = mkdtemp()
        self.assertTrue(_check_directory(temp_dir))
        
        # Diretório não existente
        non_existent_dir = os.path.join(self.temp_dir, 'non_existent_dir')
        self.assertFalse(_check_directory(non_existent_dir))
        
        # Limpar
        rmtree(temp_dir)
        
    def test_wait_on_directory(self):
        """Testa wait_on com diretório"""
        # Criar diretório temporário
        temp_dir = mkdtemp()
        
        # Diretório existente
        result = wait_on([f'dir:{temp_dir}'], timeout=1000)
        self.assertTrue(result)
        
        # Limpar
        rmtree(temp_dir)

class TestHTTPServer(unittest.TestCase):
    """Testes com um servidor HTTP real"""
    
    def setUp(self):
        """Inicia um servidor HTTP para testes"""
        # Configurar servidor HTTP
        self.port = 8888
        handler = http.server.SimpleHTTPRequestHandler
        
        class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
            allow_reuse_address = True
        
        self.httpd = ThreadedHTTPServer(("", self.port), handler)
        
        # Iniciar servidor em uma thread separada
        self.server_thread = threading.Thread(target=self.httpd.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        # Aguardar um pouco para o servidor iniciar
        time.sleep(0.5)
    
    def tearDown(self):
        """Para o servidor HTTP"""
        self.httpd.shutdown()
        self.httpd.server_close()
        self.server_thread.join(1)
    
    def test_wait_on_http(self):
        """Testa wait_on com um servidor HTTP real"""
        result = wait_on([f'http://localhost:{self.port}'], timeout=2000)
        self.assertTrue(result)
    
    def test_wait_on_tcp(self):
        """Testa wait_on com uma porta TCP real"""
        result = wait_on([f'tcp:localhost:{self.port}'], timeout=2000)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
