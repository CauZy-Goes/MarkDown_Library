# README

## Índice

- [GIT.md](#gitmd)
- [PYTHON.md](#pythonmd)
- [WSL_Docker.md](#wsl_dockermd)

---

## GIT.md

### Conceito

Git é um sistema de controle de versão distribuído, usado para rastrear alterações em arquivos, gerenciar branches e colaborar em projetos de software. Suporta operações como criação de repositórios, commit, merge e revert, além de facilitar colaboração com repositórios remotos.

### Principais Comandos

| Comando | O que faz |
|---|---|
| `git init` | Cria um novo repositório Git no diretório atual |
| `git clone <url>` | Clona um repositório remoto |
| `git remote add origin <url>` | Conecta o repositório local ao remoto |
| `git status` | Mostra o estado atual dos arquivos |
| `git add <arquivo>` | Adiciona arquivos para o próximo commit |
| `git commit -m "msg"` | Cria um commit com mensagem |
| `git push` | Envia commits para o repositório remoto |
| `git pull` | Atualiza o repositório local com mudanças do remoto |
| `git log --oneline` | Exibe histórico compacto dos commits |
| `git branch` | Lista branches locais |
| `git branch -a` | Lista branches locais e remotas |
| `git checkout -b <branch>` | Cria e troca para uma nova branch |
| `git switch -c <branch>` | Cria e troca para uma nova branch (moderno) |
| `git branch -d <branch>` | Deleta uma branch local (se já foi merged) |
| `git push origin --delete <branch>` | Deleta branch remota |
| `git merge <branch>` | Junta outra branch na atual |
| `git reset --soft HEAD~1` | Desfaz último commit, preservando mudanças |
| `git reset --hard HEAD~1` | Desfaz commit e apaga mudanças (perigoso) |
| `git revert <commit>` | Cria commit que desfaz mudanças |
| `git stash` | Guarda mudanças temporariamente |
| `git blame <arquivo>` | Mostra quem editou cada linha de um arquivo |

#### Comandos para sair do editor Vim após merges:
- `Esc` → `:wq` → `Enter` — salva e sai
- `Esc` → `:q!` → `Enter` — sai sem salvar

#### Para trocar o editor padrão:
```bash
git config --global core.editor "nano"
git config --global core.editor "code --wait"
```

---

## PYTHON.md

### Conceito

Python é uma linguagem de programação versátil e utilizada desde scripts automação até aplicações completas. Para projetos profissionais, usa-se ambientes virtuais (venv) para isolar dependências, além do gerenciador de pacotes pip e arquivos requirements.txt.

### Principais Comandos

| Comando | O que faz |
|---|---|
| `python --version` | Mostra a versão instalada do Python |
| `python -m venv venv` | Cria um ambiente virtual |
| `venv\Scripts\activate` | Ativa venv no Windows |
| `source venv/bin/activate` | Ativa venv no Linux/macOS |
| `deactivate` | Desativa ambiente virtual |
| `pip install <pacote>` | Instala um pacote |
| `pip uninstall <pacote>` | Remove um pacote |
| `pip list` | Lista pacotes instalados |
| `pip freeze > requirements.txt` | Gera arquivo de dependências do projeto |
| `pip install -r requirements.txt` | Instala todos pacotes listados |
| `python nome_do_arquivo.py` | Executa um script |
| `pip install -e .` | Instala projeto local em modo edição |
| `python -m <modulo>` | Roda um módulo como script |
| `where python` / `which python` | Mostra caminho do Python usado pelo terminal |

#### Comandos úteis para limpar e depurar:
- Limpar `__pycache__`:  
  - Linux/macOS: `find . -type d -name "__pycache__" -exec rm -rf {} +`
  - PowerShell: `Get-ChildItem -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force`

#### Fluxo para iniciar um projeto:
```bash
git clone <url>
cd <projeto>
python -m venv venv
venv\Scripts\activate    # ou source venv/bin/activate
pip install -r requirements.txt
python main.py
deactivate
```

---

## WSL_Docker.md

### Conceito

No Windows, Docker Desktop utiliza o WSL2 (Subsistema do Windows para Linux) para rodar containers, consumindo memória mesmo sem containers ativos. Comandos permitem parar containers, liberar RAM e religar o ambiente conforme a necessidade.

### Principais Comandos

| Comando | O que faz |
|---|---|
| `docker compose stop` | Para containers do projeto atual |
| `docker compose start` / `docker compose up -d` | Religa containers do projeto |
| `docker stop $(docker ps -q)` | Para todos containers rodando |
| `docker compose ps` | Exibe status dos containers do projeto |
| `docker stats` | Mostra consumo de recursos dos containers em tempo real |
| `docker system prune` | Remove containers/paradas, imagens não usadas, libera espaço no disco |
| `docker system df` | Exibe consumo total de espaço em disco pelo docker |

#### Comandos para controlar WSL:
- Listar distribuições WSL:  
  `wsl --list --verbose` ou `wsl -l -v`
- Desligar todas distribuições:  
  `wsl --shutdown`
- Desligar uma distribuição específica:  
  `wsl --terminate <distro>`

#### Reiniciando o Docker/WSL:
```powershell
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
docker compose up -d
```

#### Sequência para liberar memória RAM:
```powershell
docker compose stop            # 1. Para containers
# Quit Docker Desktop via bandeja
wsl --shutdown                 # 2. Desliga a VM do WSL (libera RAM)
```

#### Confirmar liberação:
- Abrir Gerenciador de Tarefas e conferir processos `Vmmem` ou `Vmmemwsl`.

---

_Fim do resumo das tecnologias e principais comandos deste repositório._