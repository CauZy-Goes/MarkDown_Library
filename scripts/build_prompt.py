"""
build_prompt.py
----------------
Percorre o repositório, lê o conteúdo de todos os arquivos .md
(exceto o próprio README.md), e monta um único arquivo prompt.txt
para ser enviado à IA gerar o README.
"""

from pathlib import Path

REPO_ROOT = Path(".")
OUTPUT_FILE = Path("prompt.txt")
IGNORAR = {"README.md"}

partes = [
    "Gere um README.md para este repositório, esse readME sera a junção de todos os arquivos md desse repo"
    "O readME gerado deve conter o nome do conteúdo. um breve resumo sobre e os comandos cmd chave\n"
    "quero que o markdown tenha índice/sumário navegável adicionado no topo (usando âncoras de markdown, que funcionam como atalhos para cada conteúdo)"
]

arquivos_md = sorted(
    p for p in REPO_ROOT.rglob("*.md")
    if p.name not in IGNORAR and ".git" not in p.parts
)

for arquivo in arquivos_md:
    conteudo = arquivo.read_text(encoding="utf-8", errors="ignore")
    partes.append(f"\n---\nArquivo: {arquivo}\n\n{conteudo}\n")

OUTPUT_FILE.write_text("".join(partes), encoding="utf-8")
print(f"Prompt montado com {len(arquivos_md)} arquivo(s) .md")
print(REPO_ROOT)
print("".join(partes))

