"""Corre um agente da ondão com o Gemini e escreve o relatório em relatorio.md.

Variáveis de ambiente: GEMINI_API_KEY, AGENTE, TAREFA, MODELO (opcional).
"""
import glob
import os
import subprocess
import sys
from pathlib import Path

from google import genai
from google.genai import errors, types

RAIZ = Path(__file__).resolve().parent.parent
AGENTES = ["copy", "cro", "pdp", "css", "qa", "liquid", "git"]


def ler(caminho: Path, limite: int = 120_000) -> str:
    try:
        return caminho.read_text(encoding="utf-8")[:limite]
    except FileNotFoundError:
        return ""


def contexto(agente: str) -> str:
    partes = []
    if agente in ("copy", "cro", "pdp", "css", "qa"):
        partes.append("## index.html\n```html\n" + ler(RAIZ / "index.html") + "\n```")
    if agente == "qa":
        existentes = sorted(p.name for p in RAIZ.iterdir() if p.suffix == ".html")
        partes.append("## Páginas HTML existentes\n" + ", ".join(existentes))
    if agente == "liquid":
        for f in sorted(glob.glob(str(RAIZ / "src" / "sections" / "*.liquid")) + glob.glob(str(RAIZ / "src" / "snippets" / "*.liquid"))):
            partes.append(f"## {Path(f).relative_to(RAIZ)}\n```liquid\n{ler(Path(f), 40_000)}\n```")
    if agente == "git":
        ficheiros = subprocess.run(["git", "ls-files"], cwd=RAIZ, capture_output=True, text=True).stdout
        historico = subprocess.run(["git", "log", "--stat", "-15", "--date=short", "--format=%h %ad %s"],
                                   cwd=RAIZ, capture_output=True, text=True).stdout
        partes.append("## Ficheiros no repositório\n```\n" + ficheiros + "\n```")
        partes.append("## Últimos commits\n```\n" + historico[:30_000] + "\n```")
    return "\n\n".join(partes)


def main() -> int:
    agente = os.environ.get("AGENTE", "").strip().lower()
    tarefa = os.environ.get("TAREFA", "").strip()
    modelo = os.environ.get("MODELO", "").strip() or "gemini-3.8-flash"
    saida = RAIZ / "relatorio.md"

    if agente not in AGENTES:
        saida.write_text(f"Agente desconhecido: `{agente}`. Opções: {', '.join(AGENTES)}.", encoding="utf-8")
        return 2
    if not os.environ.get("GEMINI_API_KEY"):
        saida.write_text("Falta o segredo `GEMINI_API_KEY` em Settings → Secrets and variables → Actions.", encoding="utf-8")
        return 2

    sistema = ler(RAIZ / "agentes" / "marca.md") + "\n\n" + ler(RAIZ / "agentes" / "papeis" / f"{agente}.md")
    pedido = f"# Tarefa\n{tarefa or 'Faz a tua revisão habitual do estado atual.'}\n\n# Material\n{contexto(agente)}"

    print(f"Agente: {agente} | modelo: {modelo} | tarefa: {tarefa[:120]}")
    cliente = genai.Client()  # guardar numa variável: se não, o cliente fecha antes do pedido
    try:
        r = cliente.models.generate_content(
            model=modelo,
            contents=pedido,
            config=types.GenerateContentConfig(system_instruction=sistema, temperature=0.4),
        )
        texto = (r.text or "").strip() or "_O modelo não devolveu texto._"
    except errors.APIError as e:
        dica = {404: "O modelo não existe ou foi descontinuado: corre de novo com outro valor em 'modelo'.",
                429: "Quota esgotada no plano gratuito: espera uns minutos ou tenta amanhã.",
                403: "A chave não tem acesso a este modelo."}.get(e.code, "")
        saida.write_text(f"**Erro da API Gemini ({e.code}):** {e.message}\n\n{dica}", encoding="utf-8")
        print(f"ERRO {e.code}: {e.message}")
        return 1
    except Exception as e:  # qualquer outra falha também fica no relatório
        saida.write_text(f"**O agente falhou:** `{type(e).__name__}: {e}`", encoding="utf-8")
        print(f"ERRO: {e!r}")
        return 1

    cabecalho = f"> Agente **{agente}** · modelo `{modelo}`\n> Tarefa: {tarefa or '(revisão habitual)'}\n\n"
    saida.write_text(cabecalho + texto, encoding="utf-8")
    print("Relatório escrito.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
