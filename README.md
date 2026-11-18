# ondao-store
Repositório oficial da marca Ondão (E-commerce &amp; Automações)

## Tema Shopify (loja online)

A loja online da Shopify usa o tema que está nas pastas `layout/`, `sections/`, `templates/`, `assets/`, `config/` e `locales/` deste repositório. O tema está ligado à Shopify pela integração oficial com o GitHub: cada commit no `main` atualiza a loja, e as alterações feitas no editor da Shopify voltam como commits.

- Página principal e página do produto: `sections/ondao-landing.liquid`
- Estilos: `assets/ondao.css` · Comportamento: `assets/ondao.js`
- O preço e o botão de compra vêm do produto na Shopify. Enquanto o produto não está à venda, o site mostra a Lista VIP; quando o produto fica ativo, muda sozinho para pré-encomenda, com checkout direto e botões de pagamento num toque (Apple Pay, Shop Pay, Google Pay, PayPal).
- `ferramentas/gerar_tema.py` volta a gerar o tema a partir do `index.html` antigo, se for preciso.

O `index.html` e as páginas `.html` na raiz são o site antigo (GitHub Pages) e continuam a funcionar até o domínio passar para a Shopify.
