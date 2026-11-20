---
name: ondão
description: Creme finalizador unissexo com óleo de Cacay da Colômbia — loja de um só produto, quente, humana e honesta.
colors:
  verde-floresta: "#1C3327"
  verde-musgo: "#2E5240"
  salvia: "#6B9A7B"
  salvia-clara: "#E4EBE2"
  terracota: "#C55A37"
  terracota-funda: "#A9472A"
  cobre: "#8A4C2D"
  rosa-argila: "#E39A7B"
  creme: "#F7F3EC"
  branco-quente: "#FFFDF9"
  areia: "#ECE3D8"
  linho: "#E3DBD0"
  cinza-produto: "#ECE8E0"
  tinta: "#1E1B18"
  cinza-terra: "#6A625A"
  linha: "#DDD3C6"
  texto-sobre-verde: "#EFE9DF"
  subtexto-sobre-verde: "#BFC9C0"
  linha-sobre-verde: "#4A6B5A"
typography:
  display:
    fontFamily: "Fraunces, Georgia, 'Times New Roman', serif"
    fontSize: "clamp(2.4rem, 9vw, 4.6rem)"
    fontWeight: 500
    lineHeight: 1.02
    letterSpacing: "-0.02em"
    fontVariation: "'SOFT' 100, 'WONK' 0"
  headline:
    fontFamily: "Fraunces, Georgia, 'Times New Roman', serif"
    fontSize: "clamp(2.05rem, 7.6vw, 3.5rem)"
    fontWeight: 400
    lineHeight: 1.02
    letterSpacing: "-0.025em"
    fontVariation: "'SOFT' 100, 'WONK' 0"
  title:
    fontFamily: "Fraunces, Georgia, 'Times New Roman', serif"
    fontSize: "clamp(1.5rem, 5.4vw, 2.4rem)"
    fontWeight: 500
    lineHeight: 1.1
    letterSpacing: "-0.015em"
  price:
    fontFamily: "Fraunces, Georgia, serif"
    fontSize: "2rem"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "-0.01em"
    fontFeature: "'tnum' 1"
  body:
    fontFamily: "'Instrument Sans', system-ui, -apple-system, 'Segoe UI', sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "'Instrument Sans', system-ui, sans-serif"
    fontSize: "0.8rem"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "0.12em"
rounded:
  sm: "12px"
  md: "16px"
  lg: "22px"
  pill: "999px"
spacing:
  gutter: "20px"
  gutter-desktop: "40px"
  max: "1180px"
  section: "72px"
components:
  button-primary:
    backgroundColor: "{colors.verde-floresta}"
    textColor: "{colors.branco-quente}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "18px 30px"
    height: "52px"
  button-primary-hover:
    backgroundColor: "{colors.verde-musgo}"
    textColor: "{colors.branco-quente}"
  button-on-photo:
    backgroundColor: "{colors.creme}"
    textColor: "{colors.verde-floresta}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "14px 34px"
  button-terracota:
    backgroundColor: "{colors.terracota}"
    textColor: "{colors.branco-quente}"
    rounded: "{rounded.pill}"
    padding: "18px 30px"
  button-terracota-hover:
    backgroundColor: "{colors.terracota-funda}"
  button-outline:
    backgroundColor: "transparent"
    textColor: "{colors.verde-floresta}"
    rounded: "{rounded.pill}"
    padding: "14px 22px"
  option-card:
    backgroundColor: "{colors.branco-quente}"
    textColor: "{colors.tinta}"
    rounded: "14px"
    padding: "16px"
  option-card-selected:
    backgroundColor: "{colors.salvia-clara}"
    textColor: "{colors.verde-floresta}"
  input-on-forest:
    backgroundColor: "rgba(255,253,249,.06)"
    textColor: "{colors.branco-quente}"
    rounded: "{rounded.sm}"
    padding: "14px 16px"
    height: "52px"
  summary-card:
    backgroundColor: "{colors.branco-quente}"
    textColor: "{colors.tinta}"
    rounded: "{rounded.md}"
    padding: "22px"
  tag:
    backgroundColor: "{colors.terracota}"
    textColor: "{colors.branco-quente}"
    rounded: "{rounded.pill}"
    padding: "3px 10px"
---

# Design System: ondão

## Overview

**Creative North Star: "Ondas com raízes"**

A ondão vive entre duas casas: a terra da Orinoquía colombiana, de onde vem o Cacay e o fundador, e a luz das casas de Lisboa, onde a marca nasceu. O sistema visual traduz isso num chão de verde-floresta com acentos de terracota, sobre papel creme quente, e em fotografia de filme de 35 mm com luz natural: pessoas reais, pele com textura, caracóis com frizz, o tubo verdadeiro. Nada parece de estúdio.

A sensação é **quente e tátil**: botões em pílula cheia, cantos suaves, cartões de papel, sombras quase invisíveis. A página respira; uma só ação principal por ecrã ("Quero o meu ondão"), e cada secção tem um só trabalho. O título serifado (Fraunces, macio) fala com voz humana; a sans (Instrument Sans) trata dos factos.

Rejeitamos dois mundos: o **clínico de farmácia** (branco frio, azul, cara de laboratório) e o **luxo distante** (preto e dourado, modelos frias, preço inacessível). A ondão é próxima, honesta e de casa.

**Key Characteristics:**
- Verde-floresta como chão das ações e das secções escuras; terracota como sotaque raro.
- Fundo creme quente, nunca branco puro nem preto puro.
- Títulos em Fraunces com uma palavra em itálico terracota.
- Fotografia de filme, luz natural, pessoas e tubo reais.
- Pílulas cheias, cantos de 12 a 22 px, sombras difusas e raras.
- Telemóvel primeiro; botão de compra fixo no fundo do ecrã.

## Colors

Uma paleta de terra: floresta, musgo e sálvia para a base; terracota e argila para o calor; creme, areia e linho como papel.

### Primary
- **Verde-floresta** (`verde-floresta`): o chão da marca. Botões principais, secções escuras (fundador, ingredientes, newsletter), logótipo, ícones e o fundo da barra de avisos.
- **Verde-musgo** (`verde-musgo`): o estado de hover dos botões verdes, o texto de estado ("Pré-encomenda · envio em até 10 dias") e o traço dos ícones de confiança.

### Secondary
- **Terracota** (`terracota`): o sotaque. A palavra em itálico nos títulos ("onda?", "raízes.", "Zero enchimento."), etiquetas como "Portes grátis", o contador do carrinho, o anel de foco e os pontos da linha do tempo. Também é a cor do próprio tubo.
- **Terracota-funda** (`terracota-funda`): o hover dos botões terracota e o texto terracota pequeno sobre fundo claro (origem dos ingredientes, lugares dos capítulos), onde a terracota normal não chega ao contraste AA.
- **Rosa-argila** (`rosa-argila`): o itálico e o contorno sobre fundo verde-floresta (citação do fundador, newsletter), onde a terracota perde força.

### Tertiary
- **Sálvia** (`salvia`) e **sálvia-clara** (`salvia-clara`): calma e confirmação. A cor da tampa do tubo. Usada na opção escolhida, na caixa de portes do carrinho, nas bolinhas de lista e nos pontos de estado. A sálvia nunca é usada em texto pequeno sobre creme (contraste baixo).
- **Cobre** (`cobre`): reservado para pormenores do tubo e ilustrações; não é cor de interface.

### Neutral
- **Creme** (`creme`): o fundo geral das páginas.
- **Branco-quente** (`branco-quente`): o "branco" da marca: texto sobre verde, cartões, resumo do carrinho, opções.
- **Areia** (`areia`), **linho** (`linho`) e **cinza-produto** (`cinza-produto`): superfícies secundárias, fundos de imagens a carregar e o bloco do produto.
- **Tinta** (`tinta`): texto principal; um quase-preto quente.
- **Cinza-terra** (`cinza-terra`): texto secundário, notas e legendas.
- **Linha** (`linha`): divisórias, contornos de controlos inativos, trilho da linha do tempo.
- **Texto, subtexto e linha sobre verde** (`texto-sobre-verde`, `subtexto-sobre-verde`, `linha-sobre-verde`): as versões destas três funções para secções verde-floresta.

### Named Rules
**The Forest Floor Rule.** Toda a ação principal é verde-floresta sobre claro, ou creme sobre fotografia. A terracota não é cor de botão de compra; aparece no máximo em cerca de 10% de um ecrã.

**The Warm Paper Rule.** Nada de `#FFFFFF` nem `#000000`. O claro é creme ou branco-quente; o escuro é tinta ou verde-floresta. O texto secundário sobre verde é tingido de verde (`subtexto-sobre-verde`), nunca cinzento.

## Typography

**Display Font:** Fraunces (com Georgia), eixos `SOFT 100` e `WONK 0`
**Body Font:** Instrument Sans (com system-ui)

**Character:** Uma serifa macia e humana, quase escrita à mão nos itálicos, com uma sans limpa e direta. A Fraunces é a voz; a Instrument Sans são os factos.

### Hierarchy
- **Display** (500, clamp(2.4rem, 9vw, 4.6rem), 1.02): o título do topo ("Defina a sua *onda* com **ondão.**"). Uma vez por página.
- **Headline** (400, clamp(2.05rem, 7.6vw, 3.5rem), 1.02): títulos das páginas e do fecho "Pronto para a sua *onda?*".
- **Title** (500, clamp(1.5rem, 5.4vw, 2.4rem), 1.1): títulos de secção, o nome do produto e os títulos dos cartões (1.2–1.55rem).
- **Price** (600, 2rem, números tabulares): o preço junto ao nome do produto.
- **Body** (400, 1rem, 1.6): texto corrido, com no máximo 65–75 caracteres por linha. As notas e legendas usam 0.82–0.9rem em cinza-terra.
- **Label** (700, 0.8rem, espaçamento 0.12em, MAIÚSCULAS): só nos botões e na barra de avisos.

### Named Rules
**The Italic Wave Rule.** Um título pode ter uma, e só uma, palavra ou expressão em Fraunces itálico terracota (ou rosa-argila sobre verde). É a "onda" do título.

**The No Eyebrow Rule.** Não há etiquetas pequenas em maiúsculas por cima dos títulos. Uma informação que precise de existir (origem de um ingrediente, lugar de um capítulo) vai por baixo do título, em texto normal de frase.

## Layout

Telemóvel primeiro, com uma só coluna e margens de 20 px. A partir de 900 px as margens passam a 40 px, o conteúdo fica limitado a 1180 px e aparecem as duas colunas: galeria e compra no produto, foto e passos no "Como se usa", foto e lista nos ingredientes, itens e resumo fixo no carrinho.

As secções têm cerca de 72 px de respiração vertical (110 px nas secções verdes no computador). Há mais espaço acima de um título do que abaixo dele. O topo ocupa no máximo 78% da altura do ecrã no computador, para o produto aparecer cedo.

Os carrosséis do telemóvel (cartões e retratos) deslizam lateralmente com encaixe e mantêm as margens laterais (`scroll-padding`).

O botão de compra fica fixo no fundo do ecrã no telemóvel e flutua centrado no computador. O rodapé reserva espaço para ele não tapar nada.

## Elevation & Depth

Um sistema plano, com camadas de tom: a profundidade vem da mudança de superfície (creme → cinza-produto → branco-quente → verde-floresta) e da fotografia, não de sombras. As sombras são raras, difusas e quentes (tingidas de verde-floresta), e aparecem só em elementos que flutuam ou respondem ao toque.

### Shadow Vocabulary
- **Flutuante** (`box-shadow: 0 10px 30px rgba(28,51,39,.3)`): o botão fixo de compra.
- **Toque** (`box-shadow: 0 12px 28px -18px rgba(28,51,39,.5)`): hover dos cartões de ingredientes, com subida de 3 px.
- **Pousado** (`box-shadow: 0 2px 8px rgba(0,0,0,.15)`): o pequeno botão "+" sobre fotografias.

### Named Rules
**The Flat-By-Default Rule.** Superfícies paradas não têm sombra. Ou há contorno, ou há sombra, nunca os dois no mesmo cartão.

## Shapes

Formas suaves e orgânicas, como o tubo. Pílulas cheias (999 px) para tudo o que se carrega: botões, etiquetas, controlo de quantidade, seletor de país. Cartões e fotografias com 16 px (12 px nas miniaturas e campos; 22 px nas imagens grandes do topo). Os círculos são para retratos pequenos (fundador, assinatura) e ícones. Não há cantos retos nem formas geométricas duras, e nenhuma barra colorida num só lado de uma caixa.

## Components

### Buttons
- **Shape:** pílula cheia (999 px), com pelo menos 52 px de altura e texto numa só linha.
- **Primary:** verde-floresta com texto branco-quente, label em maiúsculas. Diz sempre a ação: "Quero o meu ondão", "Finalizar compra".
- **Hover / Focus:** o hover passa a verde-musgo e sobe 1 px; ao carregar, encolhe para 0.98. O foco tem anel terracota de 2 px a 3 px de distância.
- **Sobre fotografia:** creme com texto verde-floresta.
- **Terracota:** só na newsletter e em ofertas pontuais; nunca na compra principal.
- **Contorno:** transparente, com contorno verde de 1.5 px, para ações secundárias ("Juntar 1 tubo", "Ver o creme").

### Chips
- **Etiqueta:** pílula terracota com texto branco-quente, 0.72rem negrito, como "Portes grátis" pendurado no canto de uma opção ou o número do carrinho.
- **Escolha de tipo de cabelo:** cantos de 12 px e contorno de 1.5 px sobre verde.

### Cards / Containers
- **Corner Style:** 14–16 px.
- **Background:** branco-quente sobre creme, ou areia para cartões com fotografia.
- **Shadow Strategy:** plano (ver Elevation & Depth).
- **Border:** 1 px linha, ou 1.5 px sálvia/verde-musgo quando escolhido.
- **Internal Padding:** 16–22 px.

### Inputs / Fields
- **Style:** caixa com 52 px de altura, cantos de 12 px, contorno de 1.5 px e letra de 16 px (evita o zoom do iOS). Sobre verde: fundo branco translúcido a 6% e contorno `linha-sobre-verde`.
- **Focus:** anel rosa-argila (sobre verde) ou terracota (sobre claro), de 2 px.
- **Labels:** sempre visíveis, por cima do campo, em texto de frase (0.9rem, 600).
- **Caixa de consentimento:** 20–22 px, em toda a área de 44 px da linha.

### Navigation
- **Barra de avisos:** verde-floresta, label em maiúsculas a correr devagar (para quem prefere "reduzir movimento").
- **Cabeçalho:** creme, com o logótipo "ondão" em Fraunces ao centro, links de texto à esquerda no computador e menu ☰ no telemóvel. À direita, o saco com o contador terracota, que leva ao carrinho.
- **Menu do telemóvel:** lista em Fraunces grande, sem ícones.

### Opção de compra (signature)
Duas linhas de escolha com botão de rádio nativo (1 tubo / 2 tubos), cada uma com nome, nota e preço. A escolhida fica a sálvia-clara com contorno verde-musgo; a etiqueta "Portes grátis" fica no canto. O preço grande em Fraunces aparece por cima, junto ao nome.

### Linha do tempo da história (signature)
Uma linha vertical que se preenche a terracota ao descer a página, com pontos que acendem por capítulo. Cada capítulo tem título em Fraunces, o lugar por baixo em terracota-funda, e uma fotografia real com cantos de 16 px.

## Do's and Don'ts

### Do:
- **Do** usar verde-floresta (`#1C3327`) em todas as ações principais e terracota (`#C55A37`) só como sotaque, em cerca de 10% do ecrã.
- **Do** escrever os títulos em Fraunces com uma só palavra em itálico terracota.
- **Do** usar fotografia de filme de 35 mm com luz natural, pele com textura e cabelo com frizz. Quando aparece o tubo, tem de ser o tubo real: cobre-terracota mate, "Ondão" na vertical em verde escuro, tampa sálvia.
- **Do** dar a cada fotografia e vídeo um fundo areia enquanto carrega, e uma imagem parada como capa de cada vídeo.
- **Do** manter os alvos de toque com pelo menos 44 px e o texto dos campos a 16 px.
- **Do** escrever os preços como "19,99 €" (vírgula, espaço, € no fim).

### Don't:
- **Don't** parecer farmácia ou laboratório: nada de branco frio, azul clínico, fundos assépticos, fotografia de bata ou ícones médicos.
- **Don't** parecer luxo distante: nada de preto com dourado, modelos frias e posadas, letras finíssimas em maiúsculas ou ar de "caro e inacessível".
- **Don't** pôr etiquetas pequenas em maiúsculas por cima de títulos, nem usar maiúsculas fora dos botões e da barra de avisos.
- **Don't** usar branco puro (`#FFFFFF`) nem preto puro (`#000000`).
- **Don't** publicar imagens geradas com erros visíveis: reflexos impossíveis, mãos ou braços errados, objetos que aparecem ou desaparecem, texto ilegível em destaque. É preferível nenhuma imagem a uma imagem que denuncia a IA.
- **Don't** usar emoji ou caracteres como ícones. Os ícones são SVG de traço (1.6–2 px), arredondados e numa só família.
