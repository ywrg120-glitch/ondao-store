#!/usr/bin/env python3
"""Gera o tema Shopify (layout/, sections/, templates/, assets/, config/, locales/, snippets/)
a partir do site estático index.html.

Uso (na raiz do repositório):  python3 ferramentas/gerar_tema.py

Depois de passar para o Shopify, o tema passa a ser a fonte principal. Este script só serve
para voltar a gerar o tema se alguém mudar o index.html antigo.
"""
import json
import re
import shutil
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
html = (RAIZ / "index.html").read_text(encoding="utf-8")

# ---------- partes do index.html ----------
css = re.search(r"<style>\n?(.*?)</style>", html, re.S).group(1)
js = re.search(r"<body>.*<script>\n?(.*?)</script>\s*</body>", html, re.S).group(1)
corpo = re.search(r"<body>\n?(.*?)<script>", html, re.S).group(1)

anuncio_header = re.search(r'(<div class="anuncio".*?</header>)', corpo, re.S).group(1)
main = re.search(r"<main>\n?(.*?)</main>", corpo, re.S).group(1)
footer = re.search(r"(<footer>.*?</footer>)", corpo, re.S).group(1)
depois_footer = corpo.split("</footer>", 1)[1]  # popup, botão topo, barra fixa

# ---------- imagens: src/x.jpg -> asset_url ----------
usadas = sorted(set(re.findall(r"src/([A-Za-z0-9_.-]+\.(?:jpe?g|png|webp))", html)))


def imagens(t: str) -> str:
    return re.sub(r"src/([A-Za-z0-9_.-]+\.(?:jpe?g|png|webp))", r"{{ '\1' | asset_url }}", t)


def links(t: str) -> str:
    # âncoras da página inicial funcionam em qualquer página
    t = re.sub(r'href="#(produto|ingredientes|historia|faq|vip|topo)"', r'href="{{ routes.root_url }}#\1"', t)
    t = t.replace('href="#" class="logo"', 'href="{{ routes.root_url }}" class="logo"')
    t = t.replace('href="envios.html"', 'href="{{ shop.shipping_policy.url | default: \'/policies/shipping-policy\' }}"')
    t = t.replace('href="devolucoes.html"', 'href="{{ shop.refund_policy.url | default: \'/policies/refund-policy\' }}"')
    t = t.replace('href="privacidade.html"', 'href="{{ shop.privacy_policy.url | default: \'/policies/privacy-policy\' }}"')
    t = t.replace('href="termos.html"', 'href="{{ shop.terms_of_service.url | default: \'/policies/terms-of-service\' }}"')
    return t


def dimensoes(t: str) -> str:
    """Acrescenta width/height às imagens (evita saltos na página enquanto carrega)."""
    from PIL import Image

    def f(m):
        tag = m.group(0)
        if " width=" in tag:
            return tag
        nome = re.search(r"\{\{ '([^']+)' \| asset_url \}\}", tag).group(1)
        with Image.open(RAIZ / "src" / nome) as im:
            w, h = im.size
        return tag.replace("<img ", f'<img width="{w}" height="{h}" ', 1)

    return re.sub(r"<img [^>]*\{\{ '[^']+' \| asset_url \}\}[^>]*>", f, t)


def escrever(caminho: str, conteudo: str):
    p = RAIZ / caminho
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(conteudo, encoding="utf-8")


# ---------- assets ----------
escrever("assets/ondao.css", css.strip() + "\n\n" + (RAIZ / "ferramentas/extra.css").read_text(encoding="utf-8"))
for nome in usadas:
    shutil.copyfile(RAIZ / "src" / nome, RAIZ / "assets" / nome)

# JS: CONFIG passa a vir do Shopify (preço e link do produto); o menu passa para o cabeçalho
cfg_novo = """const CONFIG = Object.assign({
  PRECO: 19.99,          // compra única, 200 ml (o Shopify substitui pelo preço real)
  ML: 200,
  PRE_LANCAMENTO: true,  // true = botões levam à Lista VIP
  FORM_ENDPOINT: "https://formspree.io/f/xqpegzwz",
  INSCRITOS: 0,          // nº real de inscritos na Lista VIP; a partir de 50 aparece como prova social
  LINK_COMPRA: "",       // o Shopify preenche quando o produto está à venda: o site muda sozinho para pré-encomenda
  DIAS_PREPARACAO: 10,   // dias até enviarmos, a contar do pagamento (o transporte é à parte)
  DIAS_DEVOLUCAO: 14     // dias para devolver, a contar da ENTREGA (mínimo legal: 14)
}, window.ONDAO_CONFIG || {});"""
js = re.sub(r"const CONFIG = \{.*?\n\};", cfg_novo, js, count=1, flags=re.S)
js = re.sub(
    r"// menu\nconst btnMenu = .*?\n(?=\n// galeria)",
    '// menu: tratado no cabeçalho (sections/ondao-header.liquid)\n',
    js, count=1, flags=re.S)
js = js.replace('document.getElementById("ano").textContent = new Date().getFullYear();',
                'const ano = document.getElementById("ano"); if (ano) ano.textContent = new Date().getFullYear();')
escrever("assets/ondao.js", js.strip() + "\n")

# ---------- layout ----------
head_meta = re.search(r"(<meta name=\"viewport\".*?)\n<style>", html, re.S).group(1)
head_meta = re.sub(r"<title>.*?</title>\n", "", head_meta)
head_meta = re.sub(r'<meta name="description"[^>]*>\n', "", head_meta)
head_meta = imagens(head_meta)

escrever("layout/theme.liquid", f"""<!doctype html>
<html lang="{{{{ request.locale.iso_code | default: 'pt-PT' }}}}">
<head>
<meta charset="utf-8">
<title>{{%- if template.name == 'index' -%}}ondão — Creme Finalizador para Pentear{{%- else -%}}{{{{ page_title }}}} · ondão{{%- endif -%}}</title>
<meta name="description" content="{{{{ page_description | default: 'Creme finalizador para pentear ondas e caracóis, feito à volta do óleo de Cacay da Colômbia. Define sem pesar e controla o frizz. Para ela e para ele.' | escape }}}}">
<link rel="canonical" href="{{{{ canonical_url }}}}">
{head_meta}
{{{{ 'ondao.css' | asset_url | stylesheet_tag }}}}
{{{{ content_for_header }}}}
</head>
<body class="tpl-{{{{ template.name }}}}">
{{% section 'ondao-header' %}}
<main>
{{{{ content_for_layout }}}}
</main>
{{% section 'ondao-footer' %}}
</body>
</html>
""")

escrever("layout/password.liquid", """<!doctype html>
<html lang="pt-PT">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ondão — Em breve</title>
<meta name="theme-color" content="#1C3327">
{{ 'ondao.css' | asset_url | stylesheet_tag }}
{{ content_for_header }}
</head>
<body class="tpl-password">
{{ content_for_layout }}
</body>
</html>
""")

# ---------- secções ----------
menu_js = """<script>
(function(){
  var btn = document.getElementById("btn-menu"), menu = document.getElementById("menu");
  if (!btn || !menu) return;
  btn.addEventListener("click", function(){
    var aberto = menu.classList.toggle("aberto");
    btn.setAttribute("aria-expanded", aberto);
  });
  menu.querySelectorAll("a").forEach(function(a){ a.addEventListener("click", function(){ menu.classList.remove("aberto"); btn.setAttribute("aria-expanded", false); }); });
})();
</script>"""

escrever("sections/ondao-header.liquid", links(imagens(anuncio_header)) + "\n" + menu_js + """

{% schema %}
{"name": "Cabeçalho ondão", "settings": []}
{% endschema %}
""")

footer_l = links(footer).replace('<span id="ano"></span>', '<span id="ano">{{ "now" | date: "%Y" }}</span>')
escrever("sections/ondao-footer.liquid", footer_l + """

{% schema %}
{"name": "Rodapé ondão", "settings": []}
{% endschema %}
""")

express = """
      {%- if p != blank and v.available -%}
      <div class="express" id="express">
        <p class="express-ou"><span>ou pague num toque</span></p>
        {%- form 'product', p, id: 'ondao-express-form' -%}
          <input type="hidden" name="id" value="{{ v.id }}">
          <input type="hidden" name="quantity" value="1">
          {{ form | payment_button }}
        {%- endform -%}
      </div>
      {%- endif -%}"""

landing = dimensoes(links(imagens(main + depois_footer)))
# corrige um </span> a mais no botão de compra do index.html original
landing = landing.replace('compra única</span></span></button>', 'compra única</span></button>').replace('compra única</span></span></a>', 'compra única</span></a>')
# botões de pagamento expresso (Apple Pay, Shop Pay, Google Pay, PayPal) logo a seguir ao botão de compra
landing = re.sub(r'(<button class="btn btn-verde btn-full btn-preco" id="comprar".*?</button>)', lambda m: m.group(1) + express, landing, count=1, flags=re.S)

topo_liquid = """{%- liquid
  if product
    assign p = product
  elsif section.settings.produto != blank
    assign p = section.settings.produto
  else
    assign p = all_products['creme-finalizador-para-pentear-com-oleo-de-cacay']
  endif
  if p != blank
    assign v = p.selected_or_first_available_variant
  endif
-%}
<script>
  window.ONDAO_CONFIG = {
    {%- if p != blank %}
    PRECO: {{ v.price | divided_by: 100.0 | json }},
    {%- if v.available %}
    LINK_COMPRA: {{ request.origin | append: '/cart/' | append: v.id | append: ':1' | json }},
    {%- endif %}
    {%- endif %}
    DIAS_PREPARACAO: {{ section.settings.dias_preparacao | json }},
    DIAS_DEVOLUCAO: {{ section.settings.dias_devolucao | json }}
  };
</script>
"""

escrever("sections/ondao-landing.liquid", topo_liquid + landing + """
<script src="{{ 'ondao.js' | asset_url }}" defer></script>

{% schema %}
{
  "name": "Página ondão",
  "settings": [
    {"type": "product", "id": "produto", "label": "Produto à venda", "info": "O preço e o botão de compra vêm deste produto. Quando o produto está ativo, o site muda sozinho de Lista VIP para pré-encomenda."},
    {"type": "number", "id": "dias_preparacao", "label": "Dias até enviar (a contar do pagamento)", "default": 10},
    {"type": "number", "id": "dias_devolucao", "label": "Dias para devolver (a contar da entrega)", "default": 14}
  ],
  "presets": [{"name": "Página ondão"}]
}
{% endschema %}
""")

escrever("sections/ondao-pagina.liquid", """<section class="secao pagina">
  <div class="wrap estreito">
    {%- case template.name -%}
      {%- when 'page' -%}
        <h1 class="h2">{{ page.title }}</h1>
        <div class="texto">{{ page.content }}</div>
      {%- when 'cart' -%}
        <h1 class="h2">O seu carrinho</h1>
        {%- if cart.item_count > 0 -%}
          <ul class="carrinho">
            {%- for item in cart.items -%}
              <li><span>{{ item.quantity }} × {{ item.product.title }}</span><b>{{ item.final_line_price | money }}</b></li>
            {%- endfor -%}
          </ul>
          <p class="total">Total: <b>{{ cart.total_price | money }}</b></p>
          <form action="{{ routes.cart_url }}" method="post"><button class="btn btn-verde" type="submit" name="checkout">Finalizar compra</button></form>
        {%- else -%}
          <p>O carrinho está vazio.</p>
          <a class="btn btn-verde" href="{{ routes.root_url }}#produto">Ver o creme</a>
        {%- endif -%}
      {%- when '404' -%}
        <h1 class="h2">Página não encontrada</h1>
        <p>Esta página não existe ou mudou de sítio.</p>
        <a class="btn btn-verde" href="{{ routes.root_url }}">Voltar à loja</a>
      {%- when 'article' -%}
        <h1 class="h2">{{ article.title }}</h1>
        <div class="texto">{{ article.content }}</div>
      {%- else -%}
        <h1 class="h2">ondão</h1>
        <p>Por agora temos um só produto: o Creme Finalizador para Pentear.</p>
        <a class="btn btn-verde" href="{{ routes.root_url }}#produto">Ver o creme</a>
    {%- endcase -%}
  </div>
</section>

{% schema %}
{"name": "Página simples", "settings": []}
{% endschema %}
""")

escrever("sections/ondao-password.liquid", """<section class="pagina-pw">
  <div class="wrap estreito">
    <span class="logo">ondão</span>
    <h1 class="h2">Ondas com <em class="it">raízes.</em></h1>
    <p>A loja abre em breve.</p>
    {%- form 'storefront_password' -%}
      {{ form.errors | default_errors }}
      <label for="pw" class="sr">Palavra-passe</label>
      <input type="password" name="password" id="pw" placeholder="Palavra-passe da loja" autocomplete="current-password">
      <button class="btn btn-verde" type="submit">Entrar</button>
    {%- endform -%}
  </div>
</section>

{% schema %}
{"name": "Palavra-passe", "settings": []}
{% endschema %}
""")

# ---------- templates ----------
def tpl(seccao: str, settings: dict | None = None) -> str:
    return json.dumps({"sections": {"main": {"type": seccao, "settings": settings or {}}}, "order": ["main"]},
                      ensure_ascii=False, indent=2) + "\n"


escrever("templates/index.json", tpl("ondao-landing"))
escrever("templates/product.json", tpl("ondao-landing"))
for nome in ["page", "cart", "404", "collection", "list-collections", "search", "blog", "article"]:
    escrever(f"templates/{nome}.json", tpl("ondao-pagina"))
escrever("templates/password.json", json.dumps({"layout": "password", "sections": {"main": {"type": "ondao-password", "settings": {}}}, "order": ["main"]}, indent=2) + "\n")
escrever("templates/gift_card.liquid", """{% layout none %}
<!doctype html>
<html lang="pt-PT"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Cartão-presente · ondão</title>{{ 'ondao.css' | asset_url | stylesheet_tag }}</head>
<body><section class="secao pagina"><div class="wrap estreito">
<h1 class="h2">Cartão-presente</h1>
<p>Valor: <b>{{ gift_card.balance | money }}</b></p>
<p>Código: <b>{{ gift_card.code | format_code }}</b></p>
<a class="btn btn-verde" href="{{ shop.url }}">Ir para a loja</a>
</div></section></body></html>
""")

# ---------- config e locales ----------
escrever("config/settings_schema.json", json.dumps([
    {"name": "theme_info", "theme_name": "ondão", "theme_version": "1.0.0", "theme_author": "ondão",
     "theme_documentation_url": "https://github.com/ywrg120-glitch/ondao-store",
     "theme_support_url": "https://github.com/ywrg120-glitch/ondao-store"}
], ensure_ascii=False, indent=2) + "\n")
if not (RAIZ / "config/settings_data.json").exists():
    escrever("config/settings_data.json", json.dumps({"current": {}}, indent=2) + "\n")
escrever("locales/pt-PT.default.json", json.dumps({"geral": {"loja": "ondão"}}, ensure_ascii=False, indent=2) + "\n")

print("Tema gerado:", len(usadas), "imagens")
