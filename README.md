testando mudanca readme para forçar conflito
MEU SISTEMA (Exemplo com UV)

Descrição
---------
Este projeto é um sistema simples em Python utilizando a ferramenta UV para 
gerenciamento de dependências e build. 
O objetivo é demonstrar:
- Uso de uma dependência externa (httpx).
- Automação de build para geração de artefatos instaláveis (wheel, tar.gz).
- Boas práticas de empacotamento e versionamento.


Requisitos
----------
- Python 3.10 ou superior
- UV instalado:
  pip install uv


Instalação e configuração
-------------------------
1. Clonar o repositório:
   git clone https://github.com/Murilo-de-Oliveira/C14---Engenharia-de-Software.git
   cd meu_sistema

2. Instalar dependências:
   uv sync


Execução do projeto
-------------------
Para executar o programa principal:
   uv run main.py

Saída esperada:
   Usuário encontrado: {'login': 'octocat', 'name': 'The Octocat', 'public_repos': 8, 'followers': 19208, 'following': 9, 'url': 'https://github.com/octocat'} | Seu IP público é: x.x.x.x


Build automatizado
------------------
Para gerar os pacotes instaláveis:
   uv build

Os artefatos estarão na pasta dist/:
- meu_sistema-0.1.0.tar.gz             -> distribuição do código-fonte
- meu_sistema-0.1.0-py3-none-any.whl   -> pacote binário instalável

Exemplo de instalação do arquivo .whl:
   pip install dist/meu_sistema-0.1.0-py3-none-any.whl