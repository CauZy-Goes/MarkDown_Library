# README.md

Este repositório contém documentação essencial para uso de Python, ambientes virtuais, gerenciamento de dependências e procedimentos eficientes para Docker + WSL no Windows. Abaixo estão os tópicos principais, conceitos breves e comandos chave de cada tecnologia que te ajudarão no dia a dia.

---

## PYTHON.md

### Conceito
Refere-se ao uso prático do Python: desde instalação, ambiente virtual (venv), uso do pip para pacotes, gerenciamento de requirements.txt, comandos de rotina e dicas para evitar erros comuns.

### Comandos CMD Essenciais

- **Verificar instalação e versão**
  ```bash
  python --version
  py --version
  ```
  Mostra a versão instalada do Python.

- **Local do Python instalado**
  ```bash
  python -c "import sys; print(sys.executable)"
  ```
  Mostra caminho do executável Python atual.

- **Rodar scripts**
  ```bash
  python