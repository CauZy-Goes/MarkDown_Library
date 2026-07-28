# README

## Índice

- [GIT.md](#gitmd)
- [PYTHON.md](#pythonmd)
- [WSL_Docker.md](#wsl_dockermd)

---

## GIT.md

### Resumo

**Git** é uma ferramenta de versionamento de código usada para rastrear alterações, colaborar em equipes e manter o histórico de projetos de software. Os principais comandos e fluxos do Git incluem:

- **git init**: Inicia um repositório novo.
- **git clone \<url>**: Clona um repositório remoto.
- **git remote add origin \<url>**: Conecta o repositório local a um remoto.
- **git status / git add / git commit / git push / git pull**: Fluxo básico; avalia mudanças, adiciona arquivos ao staging, commit, envia e puxa do remoto.
- **git branch / git switch / git checkout**: Gerenciamento de branches (criar, alternar, listar, renomear e excluir).
- **git merge**: Junta o conteúdo de uma branch na atual.
- **git reset / git revert**: Volta ou desfaz commits de diferentes maneiras.
- **git log / git log --oneline --graph --all**: Visualiza o histórico de commits e o fluxo de branches/merges.
- **git stash / git stash pop / git stash list**: Guarda e recupera mudanças temporariamente.
- **git blame**: Descobre quem alterou cada linha de um arquivo.
- **git config --global core.editor**: Configura o editor padrão do Git.
- **git diff / git diff --staged**: Mostra diferenças antes do commit.

> O Git é essencial para controle de versões em projetos colaborativos. Os comandos citados acima cobrem o fluxo do dia a dia, gerenciamento de branches, undo de commits, resolução de merges e configuração de ambiente.

---

## PYTHON.md

### Resumo

**Python** é uma linguagem de programação amplamente utilizada para scripts, automação, testes, análise de dados e muito mais. O domínio dos comandos do Python e seu ecossistema permite configuração de ambientes dedicados e instalação de dependências. Comandos essenciais:

- **python --version**: Mostra a versão instalada.
- **python nome_do_arquivo.py**: Executa scripts Python.
- **python -m venv venv**: Cria um ambiente virtual.
- **Activate/Deactivate**: Ativa (`venv\Scripts\Activate.ps1` ou `source venv/bin/activate`) e desativa (`deactivate`) o venv.
- **pip install \<pacote> / pip uninstall \<pacote> / pip list / pip show**: Instala/desinstala/lista/verifica detalhes dos pacotes.
- **pip freeze > requirements.txt / pip install -r requirements.txt**: Gera requerimentos e instala todos de uma vez.
- **python -m pip install --upgrade pip**: Atualiza o próprio pip.
- **pip install -e .**: Instala projeto local em modo editável.
- **python -m \<modulo>**: Executa um módulo como script.
- **find . -type d -name "__pycache__" -exec rm -rf {} +**: Remove cache de bytecode.

> O uso de ambientes virtuais (`venv`), o gerenciamento de dependências com `pip` e o controle de `requirements.txt` são vitais para projetos Python modernos, garantindo isolamento e facilidade de replicação. Também apresenta alternativas como `poetry` e `conda`, além de dicas de `.gitignore` para projetos Python.

---

## WSL_Docker.md

### Resumo

**Docker** rodando via **WSL2** no Windows consome memória do sistema por manter uma VM Linux ativa. Para controlar o uso de recursos, comandos principais:

- **docker compose stop / start / up -d / ps**: Para/inicia/sobe containers e verifica o status.
- **docker stop $(docker ps -q)**: Para todos os containers ativos.
- **Quit Docker Desktop**: Fecha o app na bandeja do sistema.
- **wsl --list --verbose / wsl --shutdown / wsl --terminate \<distribuição>**: Ver e desligar distribuições WSL — libera RAM.
- **Start-Process "Docker Desktop.exe"**: Reinicia o Docker Desktop.
- **docker stats**: Mostra uso de recursos de containers ativos.
- **docker system prune**: Limpa containers/imagens/cache não usados (libera espaço em disco, não RAM).
- **docker system df**: Verifica quanto espaço o Docker ocupa.
- **docker compose up -d**: Religa containers de projeto.

> O domínio desses comandos permite ligar/desligar containers do Docker, liberar memória RAM e organizar os recursos do sistema. O desligamento completo do WSL (`wsl --shutdown`) é o ponto crucial para liberar RAM em PCs com Docker via WSL2.

---

> Consulte cada seção para os principais comandos, fluxos e dicas contextuais.