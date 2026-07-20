# README.md

Este repositório reúne documentação essencial e comandos chave para três tecnologias fundamentais do desenvolvimento moderno: Git, Python e o uso do Docker/WSL no Windows. Abaixo, você encontra o resumo de cada conteúdo, seus principais conceitos e comandos de terminal (cmd) para uso prático no dia a dia.

---

## GIT.md

### 🌿 Git — Controle de Versão

Git é o sistema de versionamento mais usado para rastrear alterações em arquivos e colaborar em projetos de software. Permite reverter mudanças, gerenciar branches e sincronizar código entre a máquina local e um servidor remoto (ex: GitHub).

#### Comandos chave

- Iniciar/clonar repo:
    - `git init` — Cria um repositório local.
    - `git clone <url>` — Clona um repo remoto para a máquina.

- Fluxo básico:
    - `git status` — Mostra mudanças locais.
    - `git add <arquivo>`/`git add .` — Adiciona arquivos ao staging.
    - `git commit -m "msg"` — Grava alterações definitivas.
    - `git push` — Envia commits ao repo remoto.
    - `git pull` — Traz novas alterações do remoto.

- Branches:
    - `git branch` — Lista branches locais.
    - `git checkout nome-da-branch` ou `git switch nome-da-branch` — Troca de branch.
    - `git checkout -b nome-da-branch` ou `git switch -c nome-da-branch` — Cria e entra em uma branch nova.
    - `git branch -d nome-da-branch` — Apaga uma branch local (se já mesclada).
    - `git push origin --delete nome-da-branch` — Apaga branch remota.

- Merge:
    - `git merge nome-da-branch` — Junta alterações de outra branch na atual.

- "Desfazer" mudanças:
    - `git restore arquivo.py` — Descarta alterações não commitadas.
    - `git reset --soft HEAD~1` — Desfaz último commit, mas mantém alterações no staging.
    - `git reset --hard HEAD~1` — Desfaz commit e apaga alterações.
    - `git revert <commit>` — Cria um commit novo que desfaz alterações de um commit antigo.

- Tela de merge (Vim):
    - Para sair: `Esc`, `:wq`, `Enter`.
    - Definir editor padrão: `git config --global core.editor "nano"` ou `"code --wait"`.

- Extras:
    - `git diff` — Vê diferenças antes do commit.
    - `git stash` — Guarda mudanças temporárias.
    - `git blame arquivo.py` — Mostra quem alterou cada linha.

---

## PYTHON.md

### 🐍 Python — Automação e Desenvolvimento

Python é uma linguagem de programação de fácil leitura e alta produtividade, usada para scripts, automação, integração, web e análise de dados. O gerenciamento de ambientes virtuais e dependências garante projetos isolados e portáveis.

#### Comandos chave

- Instalação/versão:
    - `python --version` — Mostra versão instalada.
    - `python nome_do_arquivo.py` — Executa um script Python.

- Ambiente virtual:
    - `python -m venv venv` — Cria um ambiente virtual.
    - `venv\Scripts\activate` (Windows) / `source venv/bin/activate` (Linux/macOS) — Ativa o ambiente.
    - `deactivate` — Desativa o ambiente.
    - `pip install -r requirements.txt` — Instala dependências listadas.

- pip — Gerenciador de pacotes:
    - `pip install nome-do-pacote` — Instala pacote.
    - `pip uninstall nome-do-pacote` — Remove pacote.
    - `pip list` — Lista pacotes instalados.
    - `pip freeze > requirements.txt` — Gera arquivo de dependências.

- Rodar projetos clonados:
    - Sequência: `git clone ...` → `python -m venv venv` → ativa venv → `pip install -r requirements.txt` → `python main.py` → `deactivate`

- Utilitário:
    - `pip install -e .` — Instala projeto local em modo edição.
    - `python -m nome_do_modulo` — Executa um módulo como script.

- Limpeza:
    - `find . -type d -name "__pycache__" -exec rm -rf {} +` — Remove cache compilado (Linux/macOS).
    - `Get-ChildItem -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force` — (PowerShell).

- Erros comuns:
    - Ative sempre o venv antes de instalar pacotes.
    - Use `python -m pip` se `pip` não funcionar.

- `.gitignore` recomendado:
    - Excluir `venv/`, `.venv/`, `__pycache__/`, `*.pyc`, `.env` — não versionar ambientes e arquivos gerados.

---

## WSL_Docker.md

### 🐳 Docker + WSL no Windows — Gerenciamento de Contêineres e Memória

Docker permite criar ambientes isolados para rodar aplicações. No Windows, funciona em cima do WSL2, consumindo memória mesmo parado. Saber desligar corretamente é essencial para liberar recursos.

#### Comandos chave

- Containers do projeto atual:
    - `docker compose stop` — Para containers.
    - `docker compose ps` — Lista containers atuais.
    - `docker compose start`/`docker compose up -d` — Religa containers.

- Para containers de toda a máquina:
    - `docker stop $(docker ps -q)` — Para todos os containers.
    - No PowerShell: `docker stop (docker ps -q)`

- Fechar Docker Desktop:
    - Via ícone do sistema ("Quit Docker Desktop").

- Desligar o WSL (libera RAM de verdade):
    - `wsl --list --verbose` — Lista distribuições WSL ligadas.
    - `wsl --shutdown` — Desliga todas as distros WSL.
    - `wsl --terminate docker-desktop` — Desliga distro específica.

- Confirmar memória liberada:
    - No Gerenciador de Tarefas, veja o processo `Vmmem/Vmmemwsl`.

- Religar o ambiente:
    - `Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"` — Religa Docker.
    - `docker compose up -d` — Sobe containers.

- Resumo para "desligar tudo":
    ```powershell
    docker compose stop      # Para containers do projeto
    # Quit Docker Desktop via bandeja
    wsl --shutdown           # Derruba todas as distros WSL e libera RAM
    ```

- Resumo para "voltar a usar":
    ```powershell
    Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    docker compose up -d
    ```

- Extras:
    - `docker stats` — Mostra uso de CPU/memória por container.
    - `docker system prune` — Limpa containers/imagens não usados (libera espaço).
    - `docker system df` — Mostra uso total de disco.

---

Este compilado serve como referência rápida para comandos essenciais de Git, Python e Docker/WSL, facilitando seu fluxo de trabalho e gerenciamento de recursos no desenvolvimento de software.