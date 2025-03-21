"""
Testes unitários para os módulos de recursos
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

from python_wait_on.resources.file_resource import FileResource
from python_wait_on.resources.http_resource import HttpResource
from python_wait_on.resources.tcp_resource import TcpResource
from python_wait_on.resources.socket_resource import SocketResource
from python_wait_on.resources.directory_resource import DirectoryResource

class TestFileResource(unittest.TestCase):
    """Testes para a classe FileResource"""
    
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
    
    def test_is_available(self):
        """Testa o método is_available"""
        # Arquivo existente
        resource = FileResource(self.temp_file)
        self.assertTrue(resource.is_available())
        
        # Arquivo não existente
        non_existent_file = os.path.join(self.temp_dir, 'non_existent.txt')
        resource = FileResource(non_existent_file)
        self.assertFalse(resource.is_available())
    
    def test_has_changed(self):
        """Testa o método has_changed"""
        resource = FileResource(self.temp_file)
        
        # Primeira verificação
        self.assertTrue(resource.has_changed())
        
        # Segunda verificação sem alterações
        self.assertFalse(resource.has_changed())
        
        # Modificar o arquivo
        time.sleep(0.1)  # Pequeno atraso para garantir timestamp diferente
        with open(self.temp_file, 'a') as f:
            f.write('additional content')
        
        # Verificar novamente
        self.assertTrue(resource.has_changed())
        
        # Remover o arquivo
        os.remove(self.temp_file)
        self.assertTrue(resource.has_changed())
        
        # Verificar novamente após remoção
        self.assertFalse(resource.has_changed())

class TestHttpResource(unittest.TestCase):
    """Testes para a classe HttpResource"""
    
    def test_init(self):
        """Testa a inicialização"""
        # Método válido
        resource = HttpResource('http://example.com', 'HEAD')
        self.assertEqual(resource.url, 'http://example.com')
        self.assertEqual(resource.method, 'HEAD')
        
        resource = HttpResource('https://example.com', 'GET')
        self.assertEqual(resource.url, 'https://example.com')
        self.assertEqual(resource.method, 'GET')
        
        # Método inválido
        with self.assertRaises(ValueError):
            HttpResource('http://example.com', 'POST')
    
    @patch('requests.head')
    def test_is_available_head(self, mock_head):
        """Testa o método is_available com HEAD"""
        resource = HttpResource('http://example.com', 'HEAD')
        
        # Resposta de sucesso
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_head.return_value = mock_response
        
        self.assertTrue(resource.is_available())
        mock_head.assert_called_with('http://example.com', timeout=5, allow_redirects=True)
        
        # Resposta de erro
        mock_response.status_code = 404
        self.assertFalse(resource.is_available())
    
    @patch('requests.head')
    def test_is_available_head_exception(self, mock_head):
        """Testa o método is_available com HEAD quando ocorre uma exceção"""
        resource = HttpResource('http://example.com', 'HEAD')
        
        # Exceção
        mock_head.side_effect = Exception('Connection error')
        self.assertFalse(resource.is_available())
    
    @patch('requests.get')
    def test_is_available_get(self, mock_get):
        """Testa o método is_available com GET"""
        resource = HttpResource('http://example.com', 'GET')
        
        # Resposta de sucesso
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        self.assertTrue(resource.is_available())
        mock_get.assert_called_with('http://example.com', timeout=5, allow_redirects=True)
        
        # Resposta de erro
        mock_response.status_code = 500
        self.assertFalse(resource.is_available())
    
    @patch('requests.get')
    def test_is_available_get_exception(self, mock_get):
        """Testa o método is_available com GET quando ocorre uma exceção"""
        resource = HttpResource('http://example.com', 'GET')
        
        # Exceção
        mock_get.side_effect = Exception('Connection error')
        self.assertFalse(resource.is_available())

class TestTcpResource(unittest.TestCase):
    """Testes para a classe TcpResource"""
    
    def test_init(self):
        """Testa a inicialização"""
        resource = TcpResource('localhost', 8000)
        self.assertEqual(resource.host, 'localhost')
        self.assertEqual(resource.port, 8000)
    
    @patch('socket.create_connection')
    def test_is_available(self, mock_create_connection):
        """Testa o método is_available"""
        resource = TcpResource('localhost', 8000)
        
        # Conexão bem-sucedida
        mock_socket = MagicMock()
        mock_create_connection.return_value = mock_socket
        
        self.assertTrue(resource.is_available())
        mock_create_connection.assert_called_with(('localhost', 8000), timeout=5)
        
        # Falha na conexão
        mock_create_connection.side_effect = socket.error('Connection refused')
        self.assertFalse(resource.is_available())

class TestSocketResource(unittest.TestCase):
    """Testes para a classe SocketResource"""
    
    def test_init(self):
        """Testa a inicialização"""
        resource = SocketResource('/tmp/test.sock')
        self.assertEqual(resource.path, '/tmp/test.sock')
    
    @patch('socket.socket')
    def test_is_available(self, mock_socket_class):
        """Testa o método is_available"""
        resource = SocketResource('/tmp/test.sock')
        
        # Conexão bem-sucedida
        mock_socket = MagicMock()
        mock_socket_class.return_value = mock_socket
        
        self.assertTrue(resource.is_available())
        mock_socket.connect.assert_called_with('/tmp/test.sock')
        
        # Falha na conexão
        mock_socket.connect.side_effect = socket.error('Connection refused')
        self.assertFalse(resource.is_available())

class TestHTTPServer(unittest.TestCase):
    """Testes com um servidor HTTP real"""
    
    def setUp(self):
        """Inicia um servidor HTTP para testes"""
        # Configurar servidor HTTP
        self.port = 8889
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
    
    def test_http_resource_real_server(self):
        """Testa HttpResource com um servidor HTTP real"""
        resource = HttpResource(f'http://localhost:{self.port}', 'HEAD')
        self.assertTrue(resource.is_available())
        
        resource = HttpResource(f'http://localhost:{self.port}', 'GET')
        self.assertTrue(resource.is_available())
    
    def test_tcp_resource_real_server(self):
        """Testa TcpResource com uma porta TCP real"""
        resource = TcpResource('localhost', self.port)
        self.assertTrue(resource.is_available())

class TestDirectoryResource(unittest.TestCase):
    """Testes para a classe DirectoryResource"""
    
    def setUp(self):
        """Configuração para os testes"""
        self.temp_dir = mkdtemp()
        self.sub_dir = os.path.join(self.temp_dir, 'test_dir')
        os.makedirs(self.sub_dir, exist_ok=True)
    
    def tearDown(self):
        """Limpeza após os testes"""
        rmtree(self.temp_dir)
    
    def test_is_available(self):
        """Testa o método is_available"""
        # Diretório existente
        resource = DirectoryResource(self.sub_dir)
        self.assertTrue(resource.is_available())
        
        # Diretório não existente
        non_existent_dir = os.path.join(self.temp_dir, 'non_existent_dir')
        resource = DirectoryResource(non_existent_dir)
        self.assertFalse(resource.is_available())
    
    def test_has_changed(self):
        """Testa o método has_changed"""
        resource = DirectoryResource(self.sub_dir)
        
        # Primeira verificação
        self.assertTrue(resource.has_changed())
        
        # Segunda verificação sem alterações
        self.assertFalse(resource.has_changed())
        
        # Modificar o diretório criando um arquivo dentro dele
        time.sleep(0.1)  # Pequeno atraso para garantir timestamp diferente
        with open(os.path.join(self.sub_dir, 'test_file.txt'), 'w') as f:
            f.write('test content')
        
        # Verificar novamente
        self.assertTrue(resource.has_changed())
        
        # Remover o diretório
        rmtree(self.sub_dir)
        self.assertTrue(resource.has_changed())
        
        # Verificar novamente após remoção
        self.assertFalse(resource.has_changed())

if __name__ == '__main__':
    unittest.main()
