# README.md

Este repositório traz guias de referência rápida para as principais tecnologias utilizadas na documentação do projeto, incluindo comandos essenciais de Alembic, Git, Python e Docker/WSL. O objetivo é facilitar a consulta e o uso das ferramentas necessárias para desenvolvimento, versionamento, gerenciamento de dependências e administração de ambientes.



## Índice

- [Alembic.md](#alembicmd)
- [GIT.md](#gitmd)
- [PYTHON.md](#pythonmd)
- [WSL_Docker.md](#wsldockermd)


---

## Alembic.md

### Conceito

Alembic é uma ferramenta de migração de banco de dados para projetos que utilizam SQLAlchemy. Permite versionar mudanças estruturais no banco (como criação/modificação de tabelas e colunas) através de arquivos de "migration" registrados no Git, garantindo a mesma estrutura entre ambientes de desenvolvimento, teste e produção.

### Principais comandos/fluxo:

- `alembic init alembic`: Cria a estrutura de pastas do Alembic (uma vez no projeto).
- `alembic revision --autogenerate -m "descrição"`: Gera um arquivo de migration comparando modelos Python com o banco, sem aplicar o SQL.
- `alembic upgrade head`: Aplica todas as migrations pendentes ao banco.
- `alembic downgrade -1`: Desfaz a última migration aplicada.
- `alembic current`: Mostra qual revision está aplicada no banco atualmente.
- `alembic history`: Lista todas as migrations geradas.
- `alembic upgrade head --sql`: Mostra o SQL gerado pelas migrations, sem executar.

Estes comandos controlam a evolução do esquema do banco, garantindo histórico, reversão e rastreabilidade. O Alembic depende do SQLAlchemy — os modelos são importados no `env.py` para serem processados nas migrations.

---

## GIT.md

### Conceito

Git é um sistema de controle de versões distribuído, usado para rastrear mudanças em código e facilitar colaboração entre desenvolvedores. Permite criar repositórios, branches, integrar e reverter mudanças, além de controlar histórico de arquivos de projetos.

### Principais comandos/fluxo:

- `git init`: Inicia um novo repositório.
- `git clone url`: Clona um repositório existente.
- `git status`: Mostra arquivos modificados e prontos (staged) para commit.
- `git add .`/`git add arquivo`: Adiciona arquivos ao staging para commit.
- `git commit -m "msg"`: Registra mudanças com uma mensagem.
- `git push`: Envia commits para o repositório remoto.
- `git pull`: Sincroniza mudanças do repositório remoto.
- `git branch`: Lista branches locais.
- `git checkout -b nome`: Cria e troca para uma nova branch.
- `git merge nome`: Mescla outro branch na branch atual.
- `git reset --soft/mixed/hard HEAD~1`: Desfaz commits (diferentes níveis de reversão).
- `git revert commit`: Cria novo commit revertendo mudanças de um commit antigo.
- `git stash`: Guarda mudanças não commitadas de forma temporária.
- `git config --global core.editor nano/code --wait`: Altera o editor padrão do Git.
- `git log`, `git diff`, `git blame`, `git remote add/set-url`, etc.: Diversos comandos para histórico, comparação, remotos.

Git fornece controle total sobre o histórico de alterações, branchs, merges e reversão de mudanças.

---

## PYTHON.md

### Conceito

Python é uma linguagem de programação amplamente utilizada para automação, scripts, data science e desenvolvimento web. O gerenciamento de ambiente virtual (venv) e pacotes (pip) é essencial para isolamento e controle das dependências de cada projeto.

### Principais comandos/fluxo:

#### Python/venv

- `python --version`: Verifica a versão instalada.
- `python -m venv venv`: Cria um ambiente virtual isolado.
- `venv\Scripts\activate` ou `source venv/bin/activate`: Ativa venv (Windows ou Linux/macOS).
- `deactivate`: Desativa o ambiente virtual.
- `where python`/`which python`: Verifica se está usando o Python do venv.

#### pip

- `pip install pacote`: Instala pacotes.
- `pip install pacote==versão`: Instala versão específica.
- `pip freeze > requirements.txt`: Gera lista de dependências instaladas.
- `pip install -r requirements.txt`: Instala todas as dependências do projeto.
- `pip uninstall pacote`: Remove um pacote.
- `pip list`, `pip show pacote`, `pip list --outdated`: Consulta pacotes instalados/detalhes.

#### Fluxo comum para clonar e rodar um projeto

- `git clone ...`
- `cd projeto`
- `python -m venv venv`
- `venv\Scripts\activate` ou `source ...`
- `pip install -r requirements.txt`
- `python main.py`
- `deactivate`

Python + venv + pip garantem reprodutibilidade dos ambientes e controle de dependências.

---

## WSL_Docker.md

### Conceito

Docker permite a criação e gerenciamento de containers — ambientes isolados para rodar aplicações. No Windows, o Docker Desktop funciona via WSL2, que utiliza uma VM Linux (processo `Vmmem`/`Vmmemwsl`) que consome memória, mesmo com containers parados. Saber desligar o Docker e o WSL libera recursos da máquina.

### Principais comandos/fluxo:

- `docker compose stop`: Para containers de um projeto, mantendo dados/volumes.
- `docker compose ps`: Lista containers ativos no projeto.
- `docker compose start` ou `docker compose up -d`: Religa containers do projeto.
- `docker stop $(docker ps -q)`: Para todos containers rodando na máquina.
- Fechar Docker Desktop na bandeja: Libera parte da memória.
- `wsl --shutdown`: Desliga completamente o WSL2 e libera RAM.
- `wsl --terminate nome`: Termina distribuição WSL específica.
- `Start-Process ...`: Religa o Docker Desktop através do PowerShell.
- `docker stats`: Monitoramento de uso de recursos dos containers.
- `docker system prune`: Limpa containers parados, imagens não usadas, cache de build.

O gerenciamento de containers e do WSL2 é fundamental para liberar recursos e otimizar o ambiente de desenvolvimento no Windows com Docker.

---

**Para mais detalhes em cada tópico, consulte os arquivos individuais deste repositório!**