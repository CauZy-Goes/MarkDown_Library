# 🐳 Docker + WSL — Comandos e Como Liberar Memória

Guia de referência rápida pra ligar, desligar e liberar recursos do Docker/WSL quando não estiver usando.

---

## 1. Por que isso consome tanta memória

No Windows, o Docker Desktop roda por cima de uma **VM Linux dentro do WSL2**. Mesmo sem nenhum container ativo, essa VM (`Vmmem`/`Vmmemwsl` no Gerenciador de Tarefas) fica reservando memória RAM o tempo todo enquanto está ligada — por isso "só fechar a janela do Docker Desktop" nem sempre libera tudo.

---

## 2. Parar os containers de um projeto específico

Na pasta onde está o `docker-compose.yml`:
```bash
docker compose stop
```
Desliga os containers, mas mantém tudo criado (dados, volumes) pra religar rápido depois.

### Ver se realmente parou
```bash
docker compose ps
```

### Voltar a usar depois
```bash
docker compose start
```
ou
```bash
docker compose up -d
```

---

## 3. Parar TODOS os containers da máquina (não só de um projeto)

```bash
docker stop $(docker ps -q)
```
`docker ps -q` lista só os IDs dos containers rodando; `docker stop` recebe essa lista e para todos de uma vez.

No PowerShell, a sintaxe equivalente:
```powershell
docker stop (docker ps -q)
```

---

## 4. Fechar o Docker Desktop

Pela bandeja do sistema (ícone da baleia, perto do relógio):
1. Botão direito no ícone.
2. **Quit Docker Desktop**.

Isso já libera bastante memória, mas o WSL pode continuar rodando em segundo plano.

---

## 5. 🛑 Desligar o WSL (o que mais libera memória)

### Ver quais distribuições WSL estão ligadas
```powershell
wsl --list --verbose
```
ou:
```powershell
wsl -l -v
```
Saída típica:
```
  NAME                   STATE           VERSION
* docker-desktop         Running         2
  docker-desktop-data    Running         2
```

### Desligar TUDO do WSL de uma vez (o comando que você quer)
```powershell
wsl --shutdown
```
Esse é **o botão de desligar** que libera a memória de verdade — derruba todas as distribuições WSL rodando (incluindo as do Docker), como se desligasse uma máquina virtual por completo.

### Desligar só uma distribuição específica
```powershell
wsl --terminate docker-desktop
wsl --terminate docker-desktop-data
```

---

## 6. Confirmar que a memória foi liberada

Abra o **Gerenciador de Tarefas** (`Ctrl + Shift + Esc`) → aba **Detalhes** ou **Processos** → procure por:
- `Vmmem` ou `Vmmemwsl`

Depois do `wsl --shutdown`, esse processo deve sumir ou cair drasticamente de consumo de RAM.

---

## 7. Religando depois (pra voltar a estudar/trabalhar)

```powershell
# Abre o Docker Desktop normalmente — ele já religa o WSL sozinho
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"

# Espera o engine ficar pronto (opcional, evita erro de "engine não encontrado")
do { Start-Sleep -Seconds 2 } until (docker info 2>$null)

# Sobe os containers do projeto
docker compose up -d
```

Não precisa ligar o WSL manualmente antes — o Docker Desktop cuida disso sozinho ao abrir.

---

## 8. Resumo — Sequência pra "desligar tudo e liberar memória"

```powershell
docker compose stop      # 1. Para os containers do projeto atual
# Fecha o Docker Desktop pela bandeja (Quit Docker Desktop)
wsl --shutdown             # 2. Derruba o WSL por completo — aqui é que a memória volta
```

## 9. Resumo — Sequência pra "voltar a usar"

```powershell
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
docker compose up -d
```

---

## 10. Comandos Extras Úteis

### Ver quanto de recurso o Docker está usando agora
```bash
docker stats
```
Mostra CPU/memória em tempo real de cada container ativo (`Ctrl+C` pra sair).

### Limpar containers parados, imagens não usadas, cache de build (libera espaço em disco, não RAM)
```bash
docker system prune
```
⚠️ Isso apaga containers parados e imagens "soltas" (não usadas por nenhum container). Não apaga volumes por padrão — pra incluir volumes também: `docker system prune --volumes` (mais destrutivo, cuidado com dados que você queira manter).

### Ver quanto espaço em disco o Docker está usando no total
```bash
docker system df
```
