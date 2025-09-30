# Gerenciador de Tarefas
Este projeto é um exemplo de aplicação de gerenciamento de tarefas (To-Do List) desenvolvido em Python, utilizando FastAPI para a API e pytest para testes automatizados.

## Pré-Requisitos
 - Python 3.11 ou superior
 - UV (Gerenciador de dependências): pip install uv

## Instalação
1. Clone o repositório:
`git clone https://github.com/Murilo-de-Oliveira/C14---Engenharia-de-Software.git`
`cd C14---Engenharia-de-Software/github-actions`

2. Instale as dependências:
`uv sync`

3. Ative o ambiente virtual:
Windows: `.venv\Scripts\activate`
Linux: `source .venv/bin/activate`

## Configurações
1. pyproject.toml: Define as dependências e configurações do projeto.
2. pyproject.unit.toml: Configurações específicas para testes unitários.
3. .flake8: Configurações do linter.

## Execução
Para executar a API localmente:
`uv run uvicorn app.main:app --reload`

A documentação interativa estará presente em `http://localhost:8000/docs`

## Testes
`uv run pytest tests/{nome_do_arquivo}.py`

## Criador
Criado por Murilo de Oliveira Domingos Figueiredo