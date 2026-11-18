# Imagens e vídeos do site ondão

Cada imagem e vídeo do site tem um **lugar** com um nome fixo (lista em `slots.json`).
Para trocar uma imagem não é preciso mexer em código.

## Trocar uma imagem ou vídeo (telemóvel ou computador)

1. Crie a imagem/vídeo com IA (prompts no guia visual).
2. Dê ao ficheiro o **nome do lugar**, por exemplo `01-topo-telemovel.png` ou `04-como-usar-video.mp4`.
   - Qualquer tamanho e formato serve (png, jpg, webp, heic, mp4, mov).
3. No GitHub: abra a pasta `media/entrada` → **Add file** → **Upload files** → arraste o ficheiro → **Commit changes**.
4. Espere cerca de 2 minutos. O GitHub corta para o tamanho certo, comprime, publica em `assets/` e o Shopify atualiza o site.
5. Atualize o site (F5).

O original fica guardado em `media/originais/`.

## Vídeos

Os vídeos estão desligados até os ligar:
Shopify → Loja online → Temas → **Personalizar** → Definições do tema → **Imagens e vídeos ondão**.

| Lugar | Para quê |
|---|---|
| 01-topo-video-telemovel / 01-topo-video-computador | Vídeo de fundo no topo (sem som, 6–10 s, em loop) |
| 02-galeria-video | Último slide da galeria do produto |
| 04-como-usar-video + 04-como-usar-capa | Secção "Como se usa" (vertical 9:16) |
| 05-fundador | Foto real do fundador na citação |

## Lugares e tamanhos finais

| Lugar | Tamanho | Onde aparece |
|---|---|---|
| 01-topo-telemovel | 1080×1350 (4:5) | Topo, no telemóvel |
| 01-topo-computador | 1920×1080 (16:9) | Topo, no computador |
| 02-galeria-1 … 5 | 1080×1350 (4:5) | Galeria do produto |
| 03-cartao-1, 03-cartao-2 | 1080×1350 (4:5) | "Para ela e para ele" |
| 04-como-usar-capa | 1080×1920 (9:16) | Capa do vídeo "Como se usa" |
| 05-fundador | 1080×1350 | Foto redonda do fundador |
| 06-banner-telemovel / 06-banner-computador | 1080×1350 / 1920×1080 | Banner "Da Orinoquía para o seu cabelo" |
| 07-retrato-1 … 4 | 1080×1440 (3:4) | "Ondas com raízes" |

Se o nome não for reconhecido, o ficheiro fica na pasta e a Action (separador **Actions** no GitHub) diz qual foi.
