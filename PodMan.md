# Guia de Introdução ao Podman

## Índice
1. [O que é Containerização](#o-que-é-containerização)
2. [Podman vs Docker](#podman-vs-docker)
3. [Conceitos Fundamentais](#conceitos-fundamentais)
4. [Dockerfile](#dockerfile)
5. [Docker Compose / Podman Compose](#docker-compose--podman-compose)
6. [Principais Comandos](#principais-comandos)
7. [Fluxo de Trabalho Típico](#fluxo-de-trabalho-típico)
8. [Referências Rápidas](#referências-rápidas)

---

## O que é Containerização

Containerização é uma tecnologia que empacota uma aplicação junto com **tudo que ela precisa para rodar** (código, dependências, bibliotecas, variáveis de ambiente, configurações de sistema) em uma unidade isolada e portátil chamada **container**.

Diferente de uma máquina virtual (VM), o container **não emula um sistema operacional inteiro** — ele compartilha o kernel do sistema operacional hospedeiro, mas mantém processos, redes e sistemas de arquivos isolados. Isso o torna:

- **Muito mais leve** que uma VM (megabytes em vez de gigabytes)
- **Mais rápido para iniciar** (segundos, às vezes milissegundos)
- **Portátil** — "roda igual" em qualquer máquina com o motor de containers instalado

A analogia clássica: se a aplicação fosse uma mudança de casa, a VM seria levar a casa inteira (fundação, encanamento, tudo), e o container seria levar só as caixas com seus pertences, aproveitando a infraestrutura (kernel) que já existe no novo lugar.

---

## Podman vs Docker

**Docker** foi a tecnologia que popularizou containers e criou o padrão que praticamente toda a indústria usa hoje (formato de imagem OCI — *Open Container Initiative*).

**Podman** é uma alternativa ao Docker, desenvolvida pela **Red Hat**, que implementa a mesma especificação OCI. Isso significa que:

- Imagens criadas com Docker rodam no Podman, e vice-versa
- A sintaxe de comandos é **quase idêntica** (`podman build`, `podman run`, `podman ps`... são espelhos de `docker build`, `docker run`, `docker ps`)
- Um `Dockerfile` funciona sem alterações no Podman
- Um `docker-compose.yml` funciona com o `podman-compose` (ou o `podman compose` nativo, em versões mais recentes)

### Principais diferenças técnicas

| Aspecto | Docker | Podman |
|---|---|---|
| Arquitetura | Usa um **daemon** (processo em segundo plano, `dockerd`) que gerencia tudo | **Sem daemon** (*daemonless*) — cada comando roda como processo independente |
| Permissões | Tradicionalmente exige usuário root ou grupo `docker` | Suporta **rootless** nativamente, mais seguro por padrão |
| Orquestração local | Usa `docker-compose` (ferramenta separada ou plugin) | Usa `podman-compose` (compatível) ou gera *Kubernetes YAML* diretamente com `podman generate kube` |
| Origem/Mantenedor | Docker Inc. / Mirantis | Red Hat (parte do ecossistema OpenShift) |

Na prática, para o dia a dia de quem desenvolve, **os comandos e conceitos são intercambiáveis** — quem sabe Docker já sabe quase tudo de Podman.

---

## Conceitos Fundamentais

### Imagem (Image)

Uma **imagem** é um "molde" ou "receita" somente leitura que contém tudo que a aplicação precisa: sistema de arquivos base, dependências instaladas, código da aplicação e instruções de como executá-la.

- É construída a partir de um `Dockerfile`
- É organizada em **camadas** (layers) — cada instrução do Dockerfile gera uma camada, o que permite cache e reuso eficiente
- Fica armazenada localmente ou em um **registry** (repositório de imagens, como Docker Hub, Quay.io, GitHub Container Registry, Azure Container Registry)

### Container

Um **container** é uma **instância em execução** de uma imagem. É o processo real, rodando, isolado, com sua própria rede, sistema de arquivos (baseado na imagem) e recursos.

> Analogia: a **imagem** é a planta/classe (em programação orientada a objetos), o **container** é o objeto instanciado a partir dela. Você pode rodar vários containers a partir da mesma imagem, cada um isolado do outro.

### Volume

Um **volume** é um mecanismo para persistir dados fora do ciclo de vida do container. Como containers são efêmeros (podem ser destruídos e recriados a qualquer momento), dados importantes (como os arquivos de um banco de dados) precisam ser guardados em um volume, para não serem perdidos.

### Rede (Network)

Containers podem se comunicar entre si através de **redes virtuais**. Quando vários containers estão na mesma rede (como acontece automaticamente com Compose), eles conseguem se encontrar **pelo nome do serviço**, sem precisar saber IPs.

---

## Dockerfile

O `Dockerfile` é um arquivo de texto com uma sequência de instruções que descrevem **como construir uma imagem**, passo a passo.

### Exemplo comentado

```dockerfile
# Imagem base: já vem com Python 3.11 instalado
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia apenas o arquivo de dependências primeiro (otimização de cache)
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Documenta (não abre de fato) a porta usada pela aplicação
EXPOSE 8000

# Comando executado quando o container inicia
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Principais instruções

| Instrução | Função |
|---|---|
| `FROM` | Define a imagem base a partir da qual a nova imagem será construída |
| `WORKDIR` | Define o diretório de trabalho dentro do container |
| `COPY` / `ADD` | Copia arquivos do host para dentro da imagem |
| `RUN` | Executa comandos durante a **construção** da imagem (ex: instalar pacotes) |
| `ENV` | Define variáveis de ambiente |
| `EXPOSE` | Documenta qual porta a aplicação usa (informativo) |
| `CMD` | Define o comando padrão executado quando o container **inicia** |
| `ENTRYPOINT` | Similar ao `CMD`, mas menos fácil de sobrescrever — usado quando o container deve sempre rodar um comando fixo |

---

## Docker Compose / Podman Compose

Enquanto o `Dockerfile` descreve **como construir uma imagem**, o `docker-compose.yml` (ou `compose.yml`) descreve **como orquestrar múltiplos containers juntos** — bancos de dados, APIs, caches, filas de mensagens, etc. — como se fossem um único ambiente.

### Exemplo comentado

```yaml
version: "3.9"

services:
  db:
    image: postgres:16          # usa imagem pronta, sem precisar de Dockerfile próprio
    environment:
      POSTGRES_PASSWORD: "123123"
    volumes:
      - db_data:/var/lib/postgresql/data   # persiste os dados do banco
    networks:
      - minha_rede

  api:
    build: .                     # constrói a imagem a partir do Dockerfile local
    depends_on:
      - db                       # só sobe depois do banco
    ports:
      - "8000:8000"
    networks:
      - minha_rede

volumes:
  db_data:

networks:
  minha_rede:
```

### Por que usar Compose

- Sobe **múltiplos containers com um único comando**
- Cria automaticamente uma **rede interna**, permitindo que os serviços se enxerguem pelo nome (`db`, `api`, etc.)
- Gerencia dependências de inicialização (`depends_on`)
- Centraliza configuração de portas, variáveis de ambiente e volumes em um único arquivo versionável

---

## Principais Comandos

### Imagens

| Comando | Descrição |
|---|---|
| `podman build -t nome-imagem .` | Constrói uma imagem a partir do Dockerfile no diretório atual |
| `podman images` | Lista as imagens disponíveis localmente |
| `podman rmi nome-imagem` | Remove uma imagem |
| `podman pull nome-imagem` | Baixa uma imagem de um registry |
| `podman push nome-imagem` | Envia uma imagem para um registry |
| `podman tag origem destino` | Cria uma nova referência (tag) para uma imagem existente |

### Containers

| Comando | Descrição |
|---|---|
| `podman run -p 8000:8000 nome-imagem` | Cria e inicia um container a partir de uma imagem |
| `podman ps` | Lista containers **em execução** |
| `podman ps -a` | Lista **todos** os containers (incluindo parados) |
| `podman stop nome-container` | Para um container em execução |
| `podman start nome-container` | Inicia um container parado |
| `podman restart nome-container` | Reinicia um container |
| `podman rm nome-container` | Remove um container (precisa estar parado) |
| `podman logs nome-container` | Mostra os logs de um container |
| `podman logs -f nome-container` | Acompanha os logs em tempo real (*follow*) |
| `podman exec -it nome-container bash` | Abre um terminal interativo **dentro** do container |
| `podman inspect nome-container` | Mostra detalhes técnicos completos do container |

### Compose

| Comando | Descrição |
|---|---|
| `podman-compose up -d` | Sobe todos os serviços definidos no `docker-compose.yml`, em segundo plano |
| `podman-compose up -d --build` | Sobe os serviços, reconstruindo as imagens antes |
| `podman-compose down` | Para e remove os containers (mantém volumes) |
| `podman-compose down -v` | Para e remove containers **e volumes** (⚠️ apaga dados persistidos) |
| `podman-compose ps` | Lista o status dos serviços do compose |
| `podman-compose logs` | Mostra logs de todos os serviços |
| `podman-compose logs -f nome-servico` | Acompanha logs de um serviço específico em tempo real |
| `podman-compose restart nome-servico` | Reinicia um serviço específico |
| `podman-compose exec nome-servico bash` | Abre terminal dentro de um serviço específico |

### Limpeza e manutenção

| Comando | Descrição |
|---|---|
| `podman system prune` | Remove containers parados, imagens não usadas e redes órfãs |
| `podman volume ls` | Lista volumes existentes |
| `podman volume rm nome-volume` | Remove um volume específico |
| `podman network ls` | Lista redes existentes |

---

## Fluxo de Trabalho Típico

1. **Escrever o `Dockerfile`** — definir como a imagem da aplicação deve ser construída
2. **Escrever o `docker-compose.yml`** — definir todos os serviços necessários (API, banco, cache, etc.) e como eles se conectam
3. **Construir e subir o ambiente**
   ```bash
   podman-compose up -d --build
   ```
4. **Verificar se está tudo rodando**
   ```bash
   podman-compose ps
   podman-compose logs -f
   ```
5. **Desenvolver normalmente**, com o ambiente isolado e reprodutível
6. **Ao final do trabalho, derrubar o ambiente** (se desejar)
   ```bash
   podman-compose down
   ```

---

## Referências Rápidas

- **Imagem** → molde/receita somente leitura, base para criar containers
- **Container** → instância em execução de uma imagem, isolada e efêmera
- **Dockerfile** → receita de como construir **uma** imagem
- **Docker Compose** → orquestração de **múltiplos** containers como um único ambiente
- **Volume** → mecanismo de persistência de dados fora do ciclo de vida do container
- **Rede** → permite que containers se comuniquem entre si pelo nome do serviço
- **Registry** → repositório remoto de imagens (Docker Hub, Quay.io, GHCR, Azure Container Registry)

> **Resumo mental:** Podman e Docker são motores diferentes, mas falam a mesma língua (padrão OCI). Se você aprender um, já sabe 95% do outro — a principal diferença no dia a dia é que o Podman não depende de um daemon rodando em segundo plano e é rootless por padrão, tornando-o uma escolha comum em ambientes corporativos e Red Hat/OpenShift.
