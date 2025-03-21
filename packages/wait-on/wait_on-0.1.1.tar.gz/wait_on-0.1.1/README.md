# Wait-On

Uma biblioteca Python para aguardar por recursos como arquivos, diretórios, portas TCP, sockets e endpoints HTTP(S). Útil para scripts de inicialização, testes e integração contínua.

## Instalação

### Via pip (usuários)

```bash
pip install wait-on
```

### Usando ambiente virtual (recomendado)

É recomendado usar um ambiente virtual para isolar as dependências do projeto:

```bash
# Criar e ativar ambiente virtual
python -m venv venv

# No Linux/macOS
source venv/bin/activate

# No Windows
venv\Scripts\activate

# Instalar o pacote
pip install wait-on
```

### Instalação para desenvolvimento

```bash
# Clone o repositório
git clone https://github.com/keviocastro/wait-on.git
cd wait-on

# Criar e ativar ambiente virtual
python -m venv venv

# No Linux/macOS
source venv/bin/activate

# No Windows
venv\Scripts\activate

# Instale em modo de desenvolvimento
pip install -e ".[dev]"

# Execute os testes
python -m unittest discover tests
```

## Uso Básico

### Como biblioteca Python

```python
from wait_on.wait_on import wait_on

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
```

### Como ferramenta de linha de comando

```bash
# Aguardar por um arquivo
wait-on arquivo.txt

# Aguardar por múltiplos recursos
wait-on arquivo.txt http://localhost:8000 tcp:localhost:5000

# Usar opções personalizadas
wait-on -d 1000 -i 500 -t 30000 -w 1000 -v http://localhost:8000
```

## Tipos de Recursos Suportados

### Arquivos

Aguarda até que um arquivo exista.

```python
# Sem prefixo (assume arquivo)
wait_on(['arquivo.txt'])

# Com prefixo explícito
wait_on(['file:arquivo.txt'])
```

Linha de comando:
```bash
wait-on arquivo.txt
wait-on file:arquivo.txt
```

### Diretórios

Aguarda até que um diretório exista.

```python
wait_on(['dir:/caminho/para/diretorio'])
```

Linha de comando:
```bash
wait-on dir:/caminho/para/diretorio
```

### HTTP/HTTPS

Aguarda até que um endpoint HTTP/HTTPS esteja disponível.

```python
# Usando método HEAD (padrão)
wait_on(['http://localhost:8000'])
wait_on(['https://example.com'])

# Usando método GET
wait_on(['http-get://localhost:8000'])
wait_on(['https-get://example.com'])
```

Linha de comando:
```bash
wait-on http://localhost:8000
wait-on https://example.com
wait-on http-get://localhost:8000
wait-on https-get://example.com
```

### TCP

Aguarda até que uma porta TCP esteja aberta.

```python
wait_on(['tcp:localhost:8000'])
wait_on(['tcp:192.168.1.1:22'])
```

Linha de comando:
```bash
wait-on tcp:localhost:8000
wait-on tcp:192.168.1.1:22
```

### Socket Unix

Aguarda até que um socket de domínio Unix esteja disponível.

```python
wait_on(['socket:/tmp/socket.sock'])
```

Linha de comando:
```bash
wait-on socket:/tmp/socket.sock
```

## Opções Detalhadas

### Biblioteca Python

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `resources` | `List[str]` | (obrigatório) | Lista de recursos para aguardar |
| `delay` | `int` | `0` | Atraso inicial antes de verificar os recursos (em ms) |
| `interval` | `int` | `250` | Intervalo para verificar os recursos (em ms) |
| `reverse` | `bool` | `False` | Operação reversa, aguardar até que os recursos NÃO estejam disponíveis |
| `timeout` | `int` | `0` | Tempo máximo para aguardar antes de sair com código de falha (em ms, 0 para infinito) |
| `window` | `int` | `750` | Janela de estabilidade (em ms) |
| `verbose` | `bool` | `False` | Exibir informações detalhadas durante a execução |

### Linha de Comando

| Opção | Descrição |
|-------|-----------|
| `-d, --delay MILLISECONDS` | Atraso inicial antes de verificar os recursos (em ms) |
| `-i, --interval MILLISECONDS` | Intervalo para verificar os recursos (em ms) |
| `-r, --reverse` | Operação reversa, aguardar até que os recursos NÃO estejam disponíveis |
| `-t, --timeout MILLISECONDS` | Tempo máximo para aguardar antes de sair com código de falha (em ms, 0 para infinito) |
| `-w, --window MILLISECONDS` | Janela de estabilidade (em ms) |
| `-v, --verbose` | Exibir informações detalhadas durante a execução |

## Exemplos Detalhados

### Aguardar por um Arquivo

```python
from wait_on.wait_on import wait_on

# Aguardar até que um arquivo exista
result = wait_on(['arquivo.txt'])
if result:
    print("Arquivo está disponível!")
else:
    print("Timeout ao aguardar pelo arquivo")
```

### Aguardar por um Diretório

```python
from wait_on.wait_on import wait_on

# Aguardar até que um diretório exista
result = wait_on(['dir:/caminho/para/diretorio'])
if result:
    print("Diretório está disponível!")
else:
    print("Timeout ao aguardar pelo diretório")

# Aguardar até que um diretório NÃO exista (modo reverso)
result = wait_on(['dir:/caminho/para/diretorio'], reverse=True)
if result:
    print("Diretório não existe mais!")
else:
    print("Timeout ao aguardar pela remoção do diretório")
```

### Aguardar por um Servidor HTTP

```python
from wait_on.wait_on import wait_on

# Aguardar até que um servidor HTTP esteja disponível
result = wait_on(
    resources=['http://localhost:8000'],
    timeout=30000,  # 30 segundos
    verbose=True
)
if result:
    print("Servidor HTTP está disponível!")
else:
    print("Timeout ao aguardar pelo servidor HTTP")
```

### Aguardar por uma Porta TCP

```python
from wait_on.wait_on import wait_on

# Aguardar até que uma porta TCP esteja aberta
result = wait_on(
    resources=['tcp:localhost:5432'],
    timeout=10000,  # 10 segundos
    interval=500    # verificar a cada 500ms
)
if result:
    print("Porta TCP está disponível!")
else:
    print("Timeout ao aguardar pela porta TCP")
```

### Aguardar por Múltiplos Recursos

```python
from wait_on.wait_on import wait_on

# Aguardar até que todos os recursos estejam disponíveis
result = wait_on([
    'arquivo.txt',
    'dir:/caminho/para/diretorio',
    'http://localhost:8000',
    'tcp:localhost:5000'
], timeout=60000)  # 60 segundos

if result:
    print("Todos os recursos estão disponíveis!")
else:
    print("Timeout ao aguardar pelos recursos")
```

### Uso da Janela de Estabilidade

```python
from wait_on.wait_on import wait_on

# Aguardar até que o recurso esteja estável por 2 segundos
result = wait_on(
    resources=['http://localhost:8000'],
    window=2000,  # 2 segundos de estabilidade
    verbose=True
)
```

## Cenários de Uso Comuns

### Aguardar por Serviços em Contêineres Docker

```python
from wait_on.wait_on import wait_on
import subprocess
import sys

# Iniciar contêiner Docker
subprocess.Popen(["docker", "run", "-d", "-p", "5432:5432", "postgres"])

# Aguardar pelo serviço PostgreSQL
print("Aguardando pelo PostgreSQL...")
result = wait_on(
    resources=['tcp:localhost:5432'],
    timeout=30000,  # 30 segundos
    verbose=True
)

if not result:
    print("Falha ao iniciar PostgreSQL")
    sys.exit(1)

print("PostgreSQL está pronto!")
```

### Uso em Scripts de Teste

```python
import unittest
import subprocess
import threading
from wait_on.wait_on import wait_on

class TestServidor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Iniciar servidor em segundo plano
        cls.processo = subprocess.Popen(["python", "servidor.py"])
        
        # Aguardar pelo servidor
        resultado = wait_on(
            resources=['http://localhost:8000'],
            timeout=10000
        )
        
        if not resultado:
            cls.processo.kill()
            raise Exception("Servidor não iniciou corretamente")
    
    @classmethod
    def tearDownClass(cls):
        cls.processo.kill()
    
    def test_servidor(self):
        # Testes aqui
        pass
```

## Uso via Linha de Comando

```bash
# Aguardar por um arquivo
wait-on arquivo.txt

# Aguardar por um diretório
wait-on dir:/caminho/para/diretorio

# Aguardar por múltiplos recursos
wait-on arquivo.txt dir:/caminho/para/diretorio http://localhost:8000 tcp:localhost:5000

# Usar modo reverso (aguardar até que os recursos NÃO estejam disponíveis)
wait-on -r arquivo.txt

# Definir timeout
wait-on -t 10000 arquivo.txt

# Modo verboso
wait-on -v http://localhost:8000

# Combinando opções
wait-on -d 1000 -i 500 -t 30000 -w 2000 -v http://localhost:8000 tcp:localhost:5432
```

## Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Implemente suas mudanças
4. Execute os testes (`python -m unittest discover tests`)
5. Faça commit das suas alterações (`git commit -am 'Adiciona nova feature'`)
6. Faça push para a branch (`git push origin feature/nova-feature`)
7. Abra um Pull Request

### Requisitos para desenvolvimento

- Python 3.7+
- Pacotes listados em `setup.py` na seção `extras_require['dev']`

## Licença

MIT
