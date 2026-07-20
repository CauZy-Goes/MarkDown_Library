# 🌿 Git — Comandos Essenciais 

Guia de referência: do zero até navegar entre branches, voltar commits, e sobreviver à temida tela de merge do Vim.

---

## 1. Criando/Clonando um Repositório

### Iniciar um repositório novo (projeto já existe na sua máquina)
```bash
git init
```

### Clonar um repositório existente
```bash
git clone https://github.com/usuario/projeto.git
```

### Conectar um repositório local a um remoto (quando você fez `git init` na mão)
```bash
git remote add origin https://github.com/usuario/projeto.git
```

### Ver quais remotos estão configurados
```bash
git remote -v
```

### Trocar a URL de um remote já existente
```bash
git remote set-url origin https://github.com/usuario/outro-repo.git
```

---

## 2. O Fluxo Básico (dia a dia)

```bash
git status              # Vê o que mudou desde o último commit
git add arquivo.py       # Adiciona um arquivo específico à "staging area"
git add .                 # Adiciona TUDO que mudou
git commit -m "mensagem"  # Registra o commit com as mudanças adicionadas
git push                  # Envia os commits pro repositório remoto
git pull                  # Traz mudanças do remoto pra sua máquina
```

### Ver o histórico de commits
```bash
git log
```
Versão mais compacta (uma linha por commit):
```bash
git log --oneline
```
Com um "gráfico" visual de branches/merges:
```bash
git log --oneline --graph --all
```

---

## 3. Branches

### Ver todas as branches (locais)
```bash
git branch
```
A branch em que você está aparece marcada com `*`.

### Ver também as branches remotas
```bash
git branch -a
```

### Criar uma branch nova (sem trocar pra ela ainda)
```bash
git branch nome-da-branch
```

### Criar e já trocar pra ela (o mais usado no dia a dia)
```bash
git checkout -b nome-da-branch
```
Versão mais moderna do Git (equivalente):
```bash
git switch -c nome-da-branch
```

### Trocar de branch (navegar entre elas)
```bash
git checkout nome-da-branch
```
ou, no Git mais recente:
```bash
git switch nome-da-branch
```

### Renomear a branch atual
```bash
git branch -m novo-nome
```

### Apagar uma branch (local)
```bash
git branch -d nome-da-branch     # só apaga se já foi mesclada (merge)
git branch -D nome-da-branch     # força a apagar, mesmo sem merge
```

### Apagar uma branch remota
```bash
git push origin --delete nome-da-branch
```

### Enviar uma branch nova pro remoto pela primeira vez
```bash
git push -u origin nome-da-branch
```
O `-u` (upstream) faz o Git lembrar essa ligação, então depois basta `git push` sem precisar especificar de novo.

---

## 4. Juntando Branches (Merge)

### Trazer as mudanças de outra branch para a atual
```bash
git checkout main          # vai pra branch que vai RECEBER as mudanças
git merge nome-da-branch    # traz o conteúdo da outra branch pra cá
```

---

## 5. Voltando no Tempo (desfazer mudanças/commits)

Essa é a parte que mais gera confusão — cada comando desfaz de um jeito diferente. Resumo:

| Comando | O que faz | Quando usar |
|---|---|---|
| `git checkout <commit> -- arquivo` | Restaura **um arquivo específico** para como estava em outro commit | Só quer voltar um arquivo, não tudo |
| `git restore arquivo.py` | Descarta mudanças não commitadas em um arquivo | Bagunçou um arquivo e quer voltar ao último commit |
| `git reset --soft HEAD~1` | Desfaz o **último commit**, mas mantém as mudanças "prontas" (staged) | Quer refazer a mensagem do commit ou juntar com outro |
| `git reset --mixed HEAD~1` | Desfaz o commit e tira do staging, mas mantém as mudanças no arquivo | Quer editar mais antes de commitar de novo |
| `git reset --hard HEAD~1` | Desfaz o commit **e apaga as mudanças** — ⚠️ perde tudo | Tem certeza que quer descartar tudo daquele commit |
| `git revert <commit>` | Cria um **novo commit** que desfaz as mudanças de um commit antigo | Preferível quando já tem push feito e outras pessoas usam o repositório — não reescreve histórico |

### Ver o hash dos commits (necessário pra maioria desses comandos)
```bash
git log --oneline
```
Exemplo de saída:
```
a1b2c3d Corrige bug no listener
e4f5g6h Adiciona persistência no banco
```

### Voltar (sem perder nada, só "olhando") um commit específico
```bash
git checkout a1b2c3d
```
Isso te deixa em um estado de **"detached HEAD"** — só olhando aquele ponto do histórico, sem estar em nenhuma branch. Pra voltar pra sua branch normal:
```bash
git checkout main
```

### Desfazer o último commit, mantendo as mudanças no seu editor
```bash
git reset --soft HEAD~1
```

### Desfazer TUDO do último commit (perigoso, apaga o trabalho)
```bash
git reset --hard HEAD~1
```

---

## 6. 🆘 A Tela Chata do Merge (Vim)

Essa é a pegadinha clássica de quem está começando. Quando você roda um `git merge`, `git rebase`, ou às vezes até um `git commit` sem `-m`, o Git abre o **Vim** (um editor de texto de terminal) pra você escrever a mensagem do commit de merge — e se você nunca usou Vim, parece que o terminal "travou".

### Como sair

1. Aperte `Esc` (garante que você não está em modo de edição de texto).
2. Digite:
   ```
   :wq
   ```
   e aperte `Enter`.

- `:wq` = **w**rite (salva) + **q**uit (sai) → salva a mensagem padrão e conclui o merge.
- Se quiser sair **sem salvar nada** (cancelar o commit de merge): `:q!` (mais raro de precisar, porque geralmente você só quer aceitar a mensagem padrão).

### Resumo rápido
```
Esc  →  :wq  →  Enter
```
Isso resolve 95% dos casos — a mensagem de merge padrão já vem pronta, você só precisa "confirmar e sair".

### Como evitar essa tela pra sempre (recomendado)

Trocar o editor padrão do Git pro **Nano** (bem mais simples, mostra os atalhos na tela):
```bash
git config --global core.editor "nano"
```

Ou, já que você usa VS Code, pode configurar ele como editor padrão do Git:
```bash
git config --global core.editor "code --wait"
```
Com isso, toda vez que o Git precisar que você escreva uma mensagem, ele abre o VS Code em vez do Vim — bem mais confortável.

---

## 7. Comandos Úteis Extras

### Ver as diferenças antes de commitar
```bash
git diff
```

### Ver o que está no staging, pronto pra commit
```bash
git diff --staged
```

### Renomear a branch principal (ex: de `master` pra `main`)
```bash
git branch -m master main
```

### Guardar mudanças temporariamente sem commitar (útil pra trocar de branch no meio de um trabalho)
```bash
git stash          # guarda as mudanças
git stash pop       # traz de volta
git stash list      # vê o que está guardado
```

### Ver quem mudou cada linha de um arquivo (e quando)
```bash
git blame arquivo.py
```
