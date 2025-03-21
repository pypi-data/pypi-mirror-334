"""
Módulo de interface de linha de comando para o Python Wait-On

Este módulo fornece a interface de linha de comando para o Python Wait-On,
permitindo que o utilitário seja usado diretamente do terminal.

Exemplos de uso:
    
    # Aguardar por um arquivo
    python-wait-on arquivo.txt
    
    # Aguardar por múltiplos recursos
    python-wait-on arquivo.txt http://localhost:8000 tcp:5000
    
    # Usar opções personalizadas
    python-wait-on -d 1000 -i 500 -t 30000 -w 1000 -v http://localhost:8000
    
    # Modo reverso
    python-wait-on -r http://localhost:8000
"""

import sys
import click
from .wait_on import wait_on

@click.command()
@click.argument('resources', nargs=-1, required=True)
@click.option('-d', '--delay', type=int, default=0, help='Atraso inicial antes de verificar os recursos em ms')
@click.option('-i', '--interval', type=int, default=250, help='Intervalo para verificar os recursos em ms')
@click.option('-r', '--reverse', is_flag=True, help='Operação reversa, aguardar até que os recursos NÃO estejam disponíveis')
@click.option('-t', '--timeout', type=int, default=0, help='Tempo máximo em ms para aguardar antes de sair com código de falha (1), 0 para infinito')
@click.option('-w', '--window', type=int, default=750, help='Janela de estabilidade em ms')
@click.option('-v', '--verbose', is_flag=True, help='Exibir informações detalhadas durante a execução')
def main(resources, delay, interval, reverse, timeout, window, verbose):
    """
    Aguarda por recursos como arquivos, portas, sockets e HTTP(S) ficarem disponíveis.
    
    RESOURCES: Lista de recursos para aguardar, como arquivos, URLs HTTP(S), portas TCP ou sockets.
    
    Exemplos:
    
    python-wait-on arquivo.txt
    
    python-wait-on http://localhost:8000
    
    python-wait-on tcp:4000
    
    python-wait-on socket:/caminho/para/socket
    """
    try:
        result = wait_on(
            resources=resources,
            delay=delay,
            interval=interval,
            reverse=reverse,
            timeout=timeout,
            window=window,
            verbose=verbose
        )
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        click.echo("\nOperação interrompida pelo usuário", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Erro: {str(e)}", err=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
