# 🐍 Python — Comandos Essenciais

Guia de referência: do zero até ambiente virtual, pip, requirements.txt e comandos do dia a dia.

---

## 1. Verificando a Instalação

### Ver a versão do Python instalada
```bash
python --version
```
No Windows, às vezes é `py` em vez de `python`:
```bash
py --version
```

### Ver onde o Python está instalado
```bash
python -c "import sys; print(sys.executable)"
```

### Abrir o interpretador interativo (REPL)
```bash
python
```
Sai com `exit()` ou `Ctrl+D` (Linux/macOS) / `Ctrl+Z` + `Enter` (Windows).

### Rodar um script
```bash
python nome_do_arquivo.py
```

---

## 2. Ambiente Virtual (venv)

### Por que usar
Isola as dependências de cada projeto, evitando conflito de versões entre projetos diferentes.

### Criar o ambiente
```bash
python -m venv venv
```
`venv` (o segundo) é o nome da pasta criada — `.venv` e `env` também são comuns.

### Ativar

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

O terminal passa a mostrar `(venv)` no início do prompt quando está ativo.

### Desativar
```bash
deactivate
```

### Confirmar que está usando o Python do venv (não o global)
```bash
where python     # Windows
which python      # Linux/macOS
```
O caminho deve apontar pra dentro da pasta `venv\`.

### Criar venv com uma versão específica do Python (se tiver várias instaladas)
```bash
python3.12 -m venv venv
```

---

## 3. pip — Gerenciador de Pacotes

### Instalar um pacote
```bash
pip install nome-do-pacote
```

### Instalar uma versão específica
```bash
pip install nome-do-pacote==1.2.3
```

### Instalar uma versão mínima
```bash
pip install "nome-do-pacote>=1.0"
```

### Atualizar um pacote já instalado
```bash
pip install --upgrade nome-do-pacote
```

### Desinstalar um pacote
```bash
pip uninstall nome-do-pacote
```

### Ver todos os pacotes instalados
```bash
pip list
```

### Ver pacotes desatualizados
```bash
pip list --outdated
```

### Ver detalhes de um pacote (versão, dependências, local de instalação)
```bash
pip show nome-do-pacote
```

### Atualizar o próprio pip
```bash
python -m pip install --upgrade pip
```

---

## 4. requirements.txt

### Gerar a partir do que está instalado no venv ativo
```bash
pip freeze > requirements.txt
```
⚠️ Sempre com o venv **ativado** antes de rodar isso — senão captura pacotes globais do sistema também.

### Instalar tudo que está listado
```bash
pip install -r requirements.txt
```

### Separar dependências de produção e de desenvolvimento
```bash
pip freeze > requirements.txt          # dependências que o projeto precisa pra rodar
pip freeze > requirements-dev.txt      # + ferramentas de dev (pytest, flake8, black...)
```

---

## 5. Fluxo Completo (clonar e rodar um projeto do zero)

```bash
git clone https://github.com/usuario/projeto.git
cd projeto

python -m venv venv
venv\Scripts\activate            # Windows
source venv/bin/activate          # Linux/macOS

pip install -r requirements.txt

python main.py

deactivate
```

---

## 6. Comandos Úteis do Dia a Dia

### Rodar um arquivo sem ativar o venv (usando o Python de dentro da pasta direto)
```bash
.\venv\Scripts\python.exe main.py     # Windows
./venv/bin/python main.py              # Linux/macOS
```

### Instalar um projeto local em "modo edição" (bom pra bibliotecas em desenvolvimento)
```bash
pip install -e .
```

### Ver o caminho de instalação de um pacote específico
```bash
python -c "import nome_do_pacote; print(nome_do_pacote.__file__)"
```

### Rodar um módulo como script
```bash
python -m nome_do_modulo
```
(É assim que comandos como `python -m venv`, `python -m pip`, `python -m pytest` funcionam — executam um módulo instalado como se fosse um script.)

### Limpar cache de bytecode compilado (`__pycache__`)
```bash
find . -type d -name "__pycache__" -exec rm -rf {} +     # Linux/macOS
Get-ChildItem -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force   # PowerShell
```

---

## 7. Erros Comuns

| Erro | Causa provável | Solução |
|---|---|---|
| `ModuleNotFoundError` mesmo após instalar | venv não estava ativo quando você rodou `pip install` | Ative o venv (`(venv)` deve aparecer no prompt) e instale de novo |
| `pip: command not found` | pip não está no PATH, ou venv não ativado | Ative o venv, ou use `python -m pip` no lugar de `pip` |
| Pacotes globais aparecendo no `pip freeze` | venv criado com `--system-site-packages` | Recrie o venv sem essa flag |
| `SyntaxError` em código que parecia certo | Rodando com uma versão de Python muito antiga (ex: recurso do 3.10+ rodando no 3.8) | Confirme a versão com `python --version` |
| Prompt sem `(venv)` no início | Você esqueceu de ativar, ou ativou e depois fechou/reabriu o terminal | Rode `venv\Scripts\activate` de novo — a ativação não é permanente entre sessões de terminal |

---

## 8. Alternativas ao venv (bom saber que existem)

| Ferramenta | Quando usar |
|---|---|
| `venv` | Nativo do Python, simples, suficiente pra maioria dos projetos |
| `virtualenv` | Similar, com mais recursos extras |
| `pipenv` | Junta pip + venv + lockfile (`Pipfile.lock`) |
| `poetry` | Gerenciamento de dependências + empacotamento + publicação — comum em projetos modernos |
| `conda` | Comum em Data Science, gerencia até bibliotecas não-Python |

Pro seu contexto (automação, scripts, integração com CI/CD da Ford), `venv` + `requirements.txt` continua sendo o padrão mais simples e mais provável de encontrar no ambiente de trabalho.

---

## 9. `.gitignore` para projetos Python (lembrete)

```gitignore
venv/
.venv/
__pycache__/
*.pyc
.env
.pytest_cache/
```

Nunca versione a pasta `venv/` — ela é pesada e específica de cada máquina. Quem clonar o projeto recria o ambiente com `pip install -r requirements.txt`.
