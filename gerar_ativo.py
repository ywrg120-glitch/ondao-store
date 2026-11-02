import os
import argparse
from google import genai

def main():
    parser = argparse.ArgumentParser(description="Gerar imagens com Gemini API")
    parser.add_argument("--prompt", required=True, help="Prompt para a geração da imagem")
    parser.add_argument("--output", required=True, help="Caminho do ficheiro de saída")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("A variável de ambiente GEMINI_API_KEY não está definida.")

    client = genai.Client(api_key=api_key)
    
    print(f"A gerar imagem com o prompt: {args.prompt}")
    response = client.models.generate_images(
        model='imagen-3.0-generate-002',
        prompt=args.prompt,
        config=dict(
            number_of_images=1,
            output_mime_type="image/jpeg",
            aspect_ratio="1:1",
            person_generation="ALLOW_ADULT"
        )
    )

    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    for generated_image in response.generated_images:
        image = generated_image.image
        image.save(args.output)
        print(f"Imagem guardada com sucesso em: {args.output}")

if __name__ == "__main__":
    main()
