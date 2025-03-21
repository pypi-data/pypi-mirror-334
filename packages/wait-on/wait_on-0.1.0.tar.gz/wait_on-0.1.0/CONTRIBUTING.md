# Contribuindo para o Python Wait-On

Obrigado pelo seu interesse em contribuir para o Python Wait-On! Este documento fornece diretrizes para contribuir com o projeto.

## Configuração do Ambiente de Desenvolvimento

1. Clone o repositório:
   ```bash
   git clone https://github.com/yourusername/python-wait-on.git
   cd python-wait-on
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências de desenvolvimento:
   ```bash
   pip install -e ".[dev]"
   ```

## Executando os Testes

Execute os testes unitários com:

```bash
python -m unittest discover tests
```

## Diretrizes de Contribuição

1. Crie uma branch para sua contribuição:
   ```bash
   git checkout -b feature/sua-feature
   ```

2. Faça suas alterações e adicione testes para cobrir seu código.

3. Certifique-se de que todos os testes passam.

4. Atualize a documentação conforme necessário.

5. Envie um pull request com uma descrição clara das alterações.

## Estilo de Código

- Siga o PEP 8 para estilo de código Python.
- Use docstrings no formato do Google para documentar funções e classes.
- Mantenha o código limpo e bem documentado.

## Relatando Problemas

Se você encontrar um bug ou tiver uma sugestão de melhoria, por favor, abra uma issue no GitHub com os seguintes detalhes:

- Descrição clara do problema ou sugestão
- Passos para reproduzir o problema (se aplicável)
- Ambiente (sistema operacional, versão do Python, etc.)
- Comportamento esperado vs. comportamento atual

## Licença

Ao contribuir para este projeto, você concorda que suas contribuições serão licenciadas sob a mesma licença MIT que cobre o projeto.
