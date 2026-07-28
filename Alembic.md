# Guia do Alembic — Node-Registry

Guia de referência em português sobre o Alembic, escrito para o contexto deste projeto
(FastAPI + SQLAlchemy sync + PostgreSQL local).

---

## 1. O problema que o Alembic resolve

Hoje a tabela `nodes` tem seis colunas. Semana que vem você vai querer adicionar
`scan_date`, ou aumentar o `pc_info` de 16 para 255 caracteres.

No seu banco de desenvolvimento, você pode apagar tudo e recriar. Mas quando existir
um banco de teste, e depois um de produção, aparece a pergunta:

> Como garantir que os três bancos têm **exatamente** a mesma estrutura?

A resposta ingênua é "eu rodo o comando de alterar tabela em cada um". Funciona até
alguém esquecer, ou até você precisar descobrir por que a coluna X existe e quando
foi criada.

**Migration** é a ideia de tratar mudanças de estrutura como **arquivos versionados no
Git**, aplicados em ordem. Cada mudança é um passo registrado. Qualquer banco vazio
pode ser levado até o estado atual rodando os passos em sequência.

O **Alembic** é a ferramenta que faz isso para o SQLAlchemy.

---

## 2. Como ele se encaixa nas três camadas

| Camada | Papel |
|---|---|
| **PostgreSQL** | Guarda os dados. Não sabe nada de Python. |
| **SQLAlchemy** | Traduz classe Python em SQL. Descreve as tabelas. |
| **Alembic** | Lê o SQLAlchemy e gera os passos de evolução da estrutura. |

O ponto que mais confunde no início:

> **O Alembic não substitui o SQLAlchemy — ele lê o SQLAlchemy.**

Você **nunca** descreve a tabela duas vezes. A classe `Node` é a fonte da verdade.
O Alembic apenas compara essa classe com o banco real e escreve a diferença.

---

## 3. Estrutura de arquivos

```
alembic.ini              configuração geral
alembic/
  ├── env.py             o único arquivo que você precisa entender
  ├── script.py.mako     template usado para gerar migrations
  └── versions/          as migrations ficam aqui (vão para o Git)
```

E dentro do banco, uma tabela extra:

```
alembic_version          uma única linha, guarda qual migration foi aplicada
```

É por essa tabela que o Alembic sabe o que falta aplicar. **Não mexa nela na mão.**

---

## 4. O `env.py` — as três coisas que ele precisa saber

### 4.1 Onde está o projeto

```python
import os, sys
sys.path.append(os.getcwd())
```

Sem isso o Alembic não consegue importar `core` e `models`.

### 4.2 Onde está o banco

```python
from core.config import settings
config.set_main_option("sqlalchemy.url", settings.database_url)
```

A URL vem do `.env`, não do `alembic.ini`. Motivo: o `alembic.ini` vai para o Git
e não deve conter senha.

### 4.3 Quais são as tabelas

```python
from core.database import Base
from models.node import Node        # ← import essencial, ver abaixo

target_metadata = Base.metadata
```

`Base.metadata` é o catálogo de tabelas. Cada classe que herda de `Base` se registra
nele — **mas só quando o módulo é importado**.

> ### A pegadinha mais comum
>
> `from models.node import Node` parece um import inútil: nada usa a variável `Node`.
> Mas sem ele a classe não se registra, o `Base.metadata` fica vazio, e o Alembic
> gera uma **migration vazia** sem reclamar de nada.
>
> **Cada modelo novo precisa ser importado no `env.py`.**

---

## 5. Os comandos principais

### `alembic init alembic`

Cria a estrutura de pastas. Roda **uma vez só** na vida do projeto.

---

### `alembic revision --autogenerate -m "descrição"`

Compara suas classes Python com o banco e **escreve um arquivo** de migration.

- **Não altera o banco.** Só cria o arquivo.
- Precisa que o banco esteja acessível (ele lê o estado atual para comparar).
- A descrição vira parte do nome do arquivo — escreva algo útil.

```powershell
alembic revision --autogenerate -m "create nodes table"
alembic revision --autogenerate -m "add scan_date to nodes"
```

---

### `alembic upgrade head`

Aplica ao banco todas as migrations pendentes.

`head` = a migration mais recente. Outras formas:

```powershell
alembic upgrade head        # até a última
alembic upgrade +1          # avança um passo
alembic upgrade abc123      # até uma revisão específica
```

---

### `alembic downgrade -1`

Desfaz a última migration aplicada.

```powershell
alembic downgrade -1        # volta um passo
alembic downgrade base      # desfaz tudo, banco volta ao vazio
```

⚠️ Downgrade que remove coluna **apaga os dados daquela coluna**. Em desenvolvimento,
sem problema. Em produção, pense duas vezes.

---

### `alembic current`

Mostra em que revisão o banco está agora. O primeiro comando a rodar quando algo
parece estranho.

---

### `alembic history`

Lista todas as migrations em ordem. Útil para entender a linha do tempo.

```powershell
alembic history --verbose    # com mais detalhe
```

---

### `alembic upgrade head --sql`

Em vez de aplicar, **imprime o SQL** que seria executado.

Excelente para aprender: mostra exatamente o que o Alembic faria no banco. Também é
o que se usa quando um DBA precisa revisar a mudança antes de aplicar em produção.

---

## 6. Tabela de referência rápida

| Comando | O que faz | Toca o banco? |
|---|---|---|
| `alembic init alembic` | cria a estrutura | não |
| `alembic revision --autogenerate -m "..."` | gera arquivo de migration | não |
| `alembic revision -m "..."` | gera migration **vazia**, para escrever à mão | não |
| `alembic upgrade head` | aplica tudo que está pendente | **sim** |
| `alembic upgrade +1` | aplica um passo | **sim** |
| `alembic downgrade -1` | desfaz um passo | **sim** |
| `alembic downgrade base` | desfaz tudo | **sim** |
| `alembic current` | mostra a revisão atual | não |
| `alembic history` | lista o histórico | não |
| `alembic upgrade head --sql` | mostra o SQL sem aplicar | não |

---

## 7. Anatomia de uma migration

Cada arquivo em `alembic/versions/` tem esta forma:

```python
revision = "a1b2c3d4e5f6"        # identificador desta migration
down_revision = None            # a anterior (None = é a primeira)

def upgrade():
    # o caminho "para frente"
    op.create_table("nodes", ...)

def downgrade():
    # o caminho "para trás" — desfaz o upgrade
    op.drop_table("nodes")
```

O par `revision` / `down_revision` é o que forma a **corrente**: cada migration aponta
para a anterior. É assim que o Alembic sabe a ordem.

Operações mais comuns dentro do `upgrade()`:

```python
op.create_table(...)                        # cria tabela
op.drop_table("nodes")                      # remove tabela
op.add_column("nodes", sa.Column(...))      # adiciona coluna
op.drop_column("nodes", "pc_info")          # remove coluna
op.alter_column("nodes", "pc_info", ...)    # altera tipo/nulidade
op.create_index(...)                        # cria índice
op.create_unique_constraint(...)            # cria constraint UNIQUE
```

---

## 8. O que o autogenerate acerta e o que ele erra

### Detecta bem

- tabela nova / tabela removida
- coluna nova / coluna removida
- mudança de tipo e de nulidade
- índices e constraints `UNIQUE`

### Não detecta ou erra

| Situação | O que acontece |
|---|---|
| **Renomear coluna** | Interpreta como "apagou a antiga, criou uma nova" → **perde os dados** |
| **Renomear tabela** | Mesmo problema |
| Mudança apenas de nome de constraint | Costuma passar batido |
| Alterações em tipos customizados / ENUM | Frequentemente incompleto |

> ### Regra de ouro
>
> **Sempre leia o arquivo gerado antes de rodar `upgrade`.**
>
> O autogenerate é um rascunho muito bom, não uma resposta final. Renomeação é o caso
> clássico: precisa ser corrigido à mão para `op.alter_column(..., new_column_name=...)`.

---

## 9. Situações do dia a dia neste projeto

### Aumentar o `pc_info` de 16 para 255

1. Edite `String(16)` → `String(255)` em `models/node.py`
2. `alembic revision --autogenerate -m "widen pc_info"`
3. Leia o arquivo: deve ter um `op.alter_column` com o tipo novo
4. `alembic upgrade head`

Ampliar um `VARCHAR` é seguro. **Reduzir** falha se algum dado existente não couber.

### Adicionar `scan_date` e `registry_date`

Cuidado com coluna `NOT NULL` em tabela que já tem dados: o Postgres não sabe o que
colocar nas linhas antigas e recusa. Duas saídas:

- criar como opcional (`Mapped[datetime | None]`), ou
- definir um `server_default` na migration

### Ativar o `unique=True` no `serial_id`

1. Troque `unique=False` → `unique=True` no modelo
2. Gere e aplique a migration

⚠️ **Falha se já existirem seriais duplicados no banco.** Limpe as duplicatas antes.
Enquanto a tabela estiver vazia, é de graça.

---

## 10. Problemas comuns

| Sintoma | Causa provável |
|---|---|
| `upgrade()` gerado **vazio** | Faltou importar o modelo no `env.py` |
| `ModuleNotFoundError: core` | Faltou o `sys.path.append(os.getcwd())`, ou rodou de outra pasta |
| `Target database is not up to date` | Existe migration pendente — rode `alembic upgrade head` |
| `Can't locate revision identified by '...'` | A `alembic_version` aponta para arquivo que não existe mais |
| `Multiple head revisions` | Dois branches criaram migrations paralelas — precisa de merge |
| `password authentication failed` | `.env` com senha errada, ou não foi carregado |

---

## 11. Boas práticas

1. **Uma migration por mudança lógica.** Facilita ler o histórico e desfazer.
2. **Sempre revise o arquivo gerado.** Especialmente em renomeações.
3. **Migrations vão para o Git.** Elas são parte do código, não artefato temporário.
4. **Nunca edite migration já aplicada e compartilhada.** Crie uma nova por cima.
5. **Teste o `downgrade`.** Se ele não funciona, você não tem volta.
6. **Senha nunca no `alembic.ini`.** Sempre via `.env` pelo `env.py`.
7. **Mensagens descritivas.** `add_scan_date` ajuda; `update` não ajuda ninguém.

---

## 12. Fluxo completo, do zero

```powershell
# uma vez na vida do projeto
alembic init alembic
# ...ajustar o env.py (seção 4)...

# a cada mudança de modelo
alembic revision --autogenerate -m "descrição da mudança"
#    ...ABRIR E LER o arquivo em alembic/versions/...
alembic upgrade head

# conferir
alembic current
```

---

## 13. Glossário

| Termo | Significado |
|---|---|
| **migration** | Um arquivo que descreve uma mudança na estrutura do banco |
| **revision** | O identificador de uma migration |
| **head** | A migration mais recente da corrente |
| **base** | O estado anterior a qualquer migration (banco vazio) |
| **upgrade** | Aplicar migrations, avançando |
| **downgrade** | Desfazer migrations, retrocedendo |
| **autogenerate** | Gerar a migration comparando modelos com o banco |
| **metadata** | O catálogo de tabelas do SQLAlchemy (`Base.metadata`) |
| **DDL** | Comandos SQL de estrutura (`CREATE`, `ALTER`, `DROP`) |
