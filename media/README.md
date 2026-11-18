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

## Ou: colar só o link da imagem

Em vez de carregar o ficheiro, crie em `media/entrada` um ficheiro de texto com o nome do lugar e a extensão `.url` (ex.: `03-cartao-1.url`) e cole lá dentro o link da imagem ou vídeo (Higgsfield, Midjourney, etc.). O GitHub descarrega e publica. Nomes começados por `elenco-` ficam guardados em `media/elenco/` como referência.

## Ou: criar a imagem com IA diretamente no GitHub (Gemini)

1. GitHub → separador **Actions** → **Criar imagem para o site (IA)** → **Run workflow**.
2. Escolha o **lugar**, cole o **prompt** do guia visual e, se quiser a mesma pessoa ou o tubo, indique uma **referência** (ex.: `assets/ondao-02-galeria-1.jpg` para o tubo).
3. Em 1–2 minutos a imagem é gerada, cortada e publicada no site.

Precisa do segredo `GEMINI_API_KEY` (GitHub → Settings → Secrets and variables → Actions).

## Para o Shopify atualizar sozinho (uma vez só)

O Shopify ignora as alterações feitas pelo robô do GitHub. Para que as imagens processadas apareçam logo no site, dê ao robô uma chave em seu nome:

1. GitHub → foto de perfil → **Settings** → **Developer settings** → **Personal access tokens** → **Fine-grained tokens** → **Generate new token**.
2. Nome: `ondao-media`. Repositório: só `ondao-store`. Permissão: **Contents: Read and write**. Validade: 1 ano.
3. Copie o token. No repositório: **Settings** → **Secrets and variables** → **Actions** → **New repository secret** → nome `GH_PUSH_TOKEN` → cole → **Add secret**.

Sem isto, o site só atualiza no próximo envio seu, ou em Shopify → Temas → menu do GitHub → **Reset to latest commit**.

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
