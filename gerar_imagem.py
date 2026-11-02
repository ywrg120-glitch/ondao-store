"""Gera uma imagem com o Gemini (Nano Banana) e guarda-a no repositório.

Uso local:
    GEMINI_API_KEY=... python gerar_imagem.py --prompt "..." --output src/gerado/teste.jpg
Opcional:
    --aspect 4:5            proporção (1:1, 3:4, 4:5, 9:16, 16:9, ...)
    --referencia src/hero-modelo.jpg   imagem de referência (mesma cara, mesmo tubo)
    --modelo gemini-nano-banana-2.1    modelo de imagem a usar
"""
import argparse
import io
import os
import sys

from google import genai
from google.genai import errors, types

MODELO_PADRAO = "gemini-nano-banana-2.1"


def main() -> int:
    p = argparse.ArgumentParser(description="Gerar imagens com a API do Gemini")
    p.add_argument("--prompt", default=os.environ.get("PROMPT", ""), help="Descrição da imagem")
    p.add_argument("--output", default=os.environ.get("OUTPUT", ""), help="Caminho do ficheiro (.jpg, .png ou .webp)")
    p.add_argument("--aspect", default=os.environ.get("ASPECT", "4:5"), help="Proporção, ex.: 4:5")
    p.add_argument("--referencia", default=os.environ.get("REFERENCIA", ""), help="Imagem de referência opcional")
    p.add_argument("--modelo", default=os.environ.get("MODELO") or MODELO_PADRAO)
    a = p.parse_args()

    if not a.prompt.strip() or not a.output.strip():
        print("ERRO: faltam o prompt e/ou o caminho de saída.")
        return 2
    if not os.environ.get("GEMINI_API_KEY"):
        print("ERRO: o segredo GEMINI_API_KEY não está definido (GitHub → Settings → Secrets and variables → Actions).")
        return 2

    conteudo = [a.prompt]
    if a.referencia:
        if not os.path.isfile(a.referencia):
            print(f"ERRO: a imagem de referência '{a.referencia}' não existe no repositório.")
            return 2
        from PIL import Image
        conteudo.append(Image.open(a.referencia))

    cliente = genai.Client()
    print(f"Modelo: {a.modelo} | proporção: {a.aspect} | referência: {a.referencia or 'nenhuma'}")
    try:
        resposta = cliente.models.generate_content(
            model=a.modelo,
            contents=conteudo,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                image_config=types.ImageConfig(aspect_ratio=a.aspect),
            ),
        )
    except errors.APIError as e:
        print(f"ERRO da API Gemini ({e.code}): {e.message}")
        if e.code == 404:
            print("O modelo não existe ou foi descontinuado. Corre de novo com outro valor em 'modelo'.")
        elif e.code in (403, 429):
            print("Sem acesso ou sem quota: os modelos de imagem podem exigir faturação ativa no Google AI Studio.")
        return 1

    imagem = None
    for parte in resposta.parts or []:
        if parte.inline_data is not None:
            imagem = parte.as_image()
            break
        if parte.text:
            print("Gemini:", parte.text.strip()[:500])
    if imagem is None:
        print("ERRO: o Gemini não devolveu nenhuma imagem (pode ter recusado o pedido).")
        return 1

    pasta = os.path.dirname(a.output)
    if pasta:
        os.makedirs(pasta, exist_ok=True)
    imagem.save(a.output)
    print(f"Imagem guardada em: {a.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
