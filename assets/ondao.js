/* ============ CONFIG — edite aqui ============ */
const CONFIG = Object.assign({
  PRECO: 19.99,          // compra única, 200 ml (o Shopify substitui pelo preço real)
  ML: 200,
  PRE_LANCAMENTO: true,  // true = botões levam à Lista VIP
  FORM_ENDPOINT: "https://formspree.io/f/xqpegzwz",
  INSCRITOS: 0,          // nº real de inscritos na Lista VIP; a partir de 50 aparece como prova social
  LINK_COMPRA: "",       // o Shopify preenche quando o produto está à venda: o site muda sozinho para pré-encomenda
  DIAS_PREPARACAO: 10,   // dias até enviarmos, a contar do pagamento (o transporte é à parte)
  DIAS_DEVOLUCAO: 14     // dias para devolver, a contar da ENTREGA (mínimo legal: 14)
}, window.ONDAO_CONFIG || {});
/* ============================================ */

const eur = v => v.toLocaleString("pt-PT",{style:"currency",currency:"EUR"});
const btnComprar = document.getElementById("comprar");
const por100 = document.getElementById("por100");
por100.textContent = eur(CONFIG.PRECO / CONFIG.ML * 100) + " / 100 ml";
document.querySelectorAll('#comprar-preco, .preco-vip').forEach(e => e.innerHTML = '<b>' + eur(CONFIG.PRECO) + '</b> · compra única');
function atualizarPlano(){}

function irParaVip(){
  document.getElementById("vip").scrollIntoView({behavior:"smooth"});
  setTimeout(() => document.getElementById("email").focus({preventScroll:true}), 650);
}
btnComprar.addEventListener("click", () => {
  if (CONFIG.PRE_LANCAMENTO) irParaVip();
  else if (typeof window.ondaoAddToCart === "function") window.ondaoAddToCart("unica");
});

// tipo de caracol: escolhe no formulário e leva à Lista VIP
document.querySelectorAll(".tipos-rapidos button").forEach(b => b.addEventListener("click", () => {
  const r = document.querySelector('input[name="cabelo"][value="' + b.dataset.tipo + '"]');
  if (r) r.checked = true;
  irParaVip();
}));

// menu: tratado no cabeçalho (sections/ondao-header.liquid)

// galeria
const slides = document.getElementById("slides"), pontos = document.getElementById("pontos");
[...slides.children].forEach((s, i) => {
  const b = document.createElement("button");
  b.type = "button"; b.setAttribute("aria-label", "Imagem " + (i + 1));
  b.addEventListener("click", () => slides.scrollTo({left: s.offsetLeft, behavior: "smooth"}));
  pontos.appendChild(b);
});
const galNum = document.getElementById("gal-num"), galNome = document.getElementById("gal-nome"), contador = document.querySelector(".contador");
document.getElementById("gal-total").textContent = "/ " + String(slides.children.length).padStart(2, "0");
let galUltimo = -1;
function marcarPonto(){
  const i = Math.round(slides.scrollLeft / slides.clientWidth);
  [...pontos.children].forEach((b, k) => b.setAttribute("aria-current", k === i));
  if (i === galUltimo) return; galUltimo = i;
  contador.classList.add("troca");
  setTimeout(() => {
    galNum.textContent = String(i + 1).padStart(2, "0");
    galNome.textContent = slides.children[i] ? (slides.children[i].dataset.legenda || "") : "";
    contador.classList.remove("troca");
  }, 200);
}
function irSlide(d){
  const n = slides.children.length, i = (Math.round(slides.scrollLeft / slides.clientWidth) + d + n) % n;
  slides.dispatchEvent(new Event("pointerdown"));
  slides.scrollTo({left: slides.children[i].offsetLeft, behavior: "smooth"});
}
document.getElementById("gal-ant").addEventListener("click", () => irSlide(-1));
document.getElementById("gal-seg").addEventListener("click", () => irSlide(1));
slides.addEventListener("scroll", () => requestAnimationFrame(marcarPonto), {passive:true});
marcarPonto();

// galeria passa sozinha, em fundido suave (crossfade) com zoom lento; pára quando a pessoa mexe ou sai do ecrã
(function(){
  const reduz = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const lista = [...slides.children];
  const atual = () => Math.round(slides.scrollLeft / slides.clientWidth);
  function marcarAtivo(){ const i = atual(); lista.forEach((sl, k) => sl.classList.toggle("ativo", k === i && !reduz)); }
  slides.addEventListener("scrollend", marcarAtivo); slides.addEventListener("scroll", () => { clearTimeout(slides._t); slides._t = setTimeout(marcarAtivo, 120); }, {passive:true});
  marcarAtivo();
  if (reduz || lista.length < 2) return;
  const INTERVALO = 5000, FUNDE = 1100;
  pontos.style.setProperty("--intervalo", INTERVALO + "ms");
  const camada = document.createElement("div"); camada.className = "fundir"; camada.setAttribute("aria-hidden", "true");
  slides.parentNode.insertBefore(camada, slides.nextSibling);
  let visivel = false, pausaAte = 0, timer = null, aFundir = false;
  function reiniciarBarra(){ pontos.classList.remove("auto"); void pontos.offsetWidth; pontos.classList.add("auto"); }
  function fundirPara(prox){
    aFundir = true;
    const copia = lista[prox].cloneNode(true); copia.classList.remove("ativo"); copia.classList.add("ativo");
    camada.innerHTML = ""; camada.appendChild(copia); camada.style.height = slides.offsetHeight + "px";
    requestAnimationFrame(() => camada.classList.add("ver"));
    setTimeout(() => {
      slides.style.scrollSnapType = "none";
      slides.scrollTo({left: lista[prox].offsetLeft, behavior: "auto"});
      slides.style.scrollSnapType = "";
      marcarPonto(); marcarAtivo();
      requestAnimationFrame(() => { camada.classList.remove("ver"); camada.style.transition = "none"; camada.style.opacity = 0;
        requestAnimationFrame(() => { camada.style.transition = ""; camada.style.opacity = ""; camada.innerHTML = ""; aFundir = false; agendar(); }); });
    }, FUNDE);
  }
  function agendar(){
    clearTimeout(timer);
    if (aFundir) return;
    if (!visivel || document.hidden) { pontos.classList.remove("auto"); return; }
    const espera = Math.max(0, pausaAte - Date.now());
    if (espera) { pontos.classList.add("pausa"); timer = setTimeout(agendar, espera); return; }
    pontos.classList.remove("pausa"); reiniciarBarra();
    timer = setTimeout(() => fundirPara((atual() + 1) % lista.length), INTERVALO - FUNDE);
  }
  function pausar(ms){ pausaAte = Date.now() + ms; agendar(); }
  ["pointerdown","touchstart","wheel","keydown"].forEach(ev => slides.addEventListener(ev, () => pausar(9000), {passive:true}));
  pontos.addEventListener("click", () => pausar(9000));
  slides.addEventListener("mouseenter", () => pausar(60000));
  slides.addEventListener("mouseleave", () => pausar(1500));
  new IntersectionObserver(es => { visivel = es[0].isIntersecting; agendar(); }, {threshold: .6}).observe(slides);
  document.addEventListener("visibilitychange", agendar);
})();

// origem do visitante
const qs = new URLSearchParams(location.search);
document.getElementById("origem").value = qs.get("utm_source") || document.referrer || "direto";

// formulário VIP
const form = document.getElementById("form-vip"), msg = document.getElementById("msg");
form.addEventListener("submit", async e => {
  e.preventDefault();
  const email = form.email.value.trim();
  if (!/^\S+@\S+\.\S+$/.test(email)) { msg.textContent = "Confirme o seu email."; return; }
  if (!form.consent.checked) { msg.textContent = "Precisamos do seu consentimento para enviar emails."; return; }
  msg.textContent = "A guardar o seu lugar…";
  try {
    const r = await fetch(CONFIG.FORM_ENDPOINT, {method:"POST", body:new FormData(form), headers:{Accept:"application/json"}});
    if (!r.ok) throw 0;
    form.reset(); atualizarPlano();
    msg.textContent = "Está dentro. Vai ser dos primeiros a saber quando abrirmos.";
    marcarInscrito(); contar("inscricao-formulario");
  } catch { msg.textContent = "Algo falhou. Tente de novo dentro de momentos."; }
});

// prova social: só mostra números reais
if (CONFIG.INSCRITOS >= 50) {
  document.getElementById("prova-txt").textContent = "Junte-se a " + CONFIG.INSCRITOS.toLocaleString("pt-PT") + "+ pessoas na Lista VIP";
  document.getElementById("prova").hidden = false;
}

// hero: muda suavemente ao fazer scroll
const heroEl = document.getElementById("topo");
if (!matchMedia("(prefers-reduced-motion: reduce)").matches) {
  let pend = false;
  addEventListener("scroll", () => {
    if (pend) return; pend = true;
    requestAnimationFrame(() => {
      const p = Math.min(1, Math.max(0, scrollY / (heroEl.offsetHeight || 1)));
      heroEl.style.setProperty("--p", p.toFixed(3));
      pend = false;
    });
  }, {passive:true});
}
document.getElementById("cta-hero").addEventListener("click", e => { e.preventDefault(); irParaVip(); });

// botão fixo no telemóvel
const fixa = document.getElementById("fixa");
let depoisHero = false, naVip = false;
const topoBtn = document.getElementById("topo-btn");
const mostrarFixa = () => fixa.classList.toggle("on", depoisHero && (!naVip || !!CONFIG.LINK_COMPRA));
new IntersectionObserver(([e]) => { depoisHero = !e.isIntersecting && e.boundingClientRect.top < 0; mostrarFixa(); topoBtn.classList.toggle("on", depoisHero); }).observe(document.querySelector(".hero"));
topoBtn.addEventListener("click", () => {
  const suave = !matchMedia("(prefers-reduced-motion: reduce)").matches;
  window.scrollTo({top: 0, behavior: suave ? "smooth" : "auto"});
  contar("voltar-ao-topo");
});
new IntersectionObserver(([e]) => { naVip = e.isIntersecting; mostrarFixa(); }).observe(document.getElementById("vip"));

// estatísticas (GoatCounter): eventos sem cookies
function contar(nome){ try { window.goatcounter && window.goatcounter.count && window.goatcounter.count({path: nome, title: nome, event: true}); } catch(e){} }
document.querySelectorAll('a[href="#vip"], #comprar, #cta-hero').forEach(el => el.addEventListener("click", () => contar("clique-cta-" + (el.id || "vip"))));

// popup do quiz: aparece uma vez, ao fim de 8 s, a quem ainda não se inscreveu
function ler(k){ try { return localStorage.getItem(k); } catch(e){ return null; } }
function guardar(k,v){ try { localStorage.setItem(k,v); } catch(e){} }
function marcarInscrito(){ guardar("ondao_vip","1"); }
const pop = document.getElementById("pop");
const popForm = document.getElementById("pop-form");
let ultimoFoco = null;
function abrirPop(){
  if (ler("ondao_vip") || ler("ondao_pop") || !pop.hidden) return;
  if (document.getElementById("vip").getBoundingClientRect().top < innerHeight) return;
  guardar("ondao_pop","1");
  ultimoFoco = document.activeElement;
  pop.hidden = false; document.body.style.overflow = "hidden";
  pop.querySelector(".pop-opcoes button").focus({preventScroll:true});
  contar("popup-aberto");
}
function fecharPop(){ pop.hidden = true; document.body.style.overflow = ""; if (ultimoFoco) ultimoFoco.focus({preventScroll:true}); }
setTimeout(abrirPop, 8000);
document.getElementById("pop-fechar").addEventListener("click", fecharPop);
pop.addEventListener("click", e => { if (e.target === pop) fecharPop(); });
document.addEventListener("keydown", e => { if (e.key === "Escape" && !pop.hidden) fecharPop(); });
pop.querySelectorAll(".pop-opcoes button").forEach(b => b.addEventListener("click", () => {
  document.getElementById("pop-cabelo").value = b.dataset.tipo;
  document.getElementById("pop-tipo-txt").textContent = b.dataset.tipo === "nao-sei" ? "ondulado ou cacheado" : b.textContent.toLowerCase();
  document.getElementById("pop-passo1").hidden = true; popForm.hidden = false; popForm.style.display = "grid";
  document.getElementById("pop-email").focus();
  contar("popup-tipo-" + b.dataset.tipo);
}));
document.getElementById("pop-origem").value = "popup · " + (qs.get("utm_source") || document.referrer || "direto");
popForm.addEventListener("submit", async e => {
  e.preventDefault();
  const pm = document.getElementById("pop-msg");
  const email = document.getElementById("pop-email").value.trim();
  if (!/^\S+@\S+\.\S+$/.test(email)) { pm.textContent = "Confirme o seu email."; return; }
  if (!document.getElementById("pop-consent").checked) { pm.textContent = "Precisamos do seu consentimento para enviar emails."; return; }
  pm.textContent = "A guardar o seu lugar…";
  try {
    const r = await fetch(CONFIG.FORM_ENDPOINT, {method:"POST", body:new FormData(popForm), headers:{Accept:"application/json"}});
    if (!r.ok) throw 0;
    marcarInscrito(); contar("inscricao-popup");
    popForm.innerHTML = '<p class="pop-titulo" style="margin-top:28px;font-size:2rem;text-align:center">Está dentro.</p><p class="pop-sub" style="text-align:center">A sua rotina chega-lhe por email. Avisamos quando abrirmos.</p>';
    setTimeout(fecharPop, 3500);
  } catch { pm.textContent = "Algo falhou. Tente de novo dentro de momentos."; }
});

const ano = document.getElementById("ano"); if (ano) ano.textContent = new Date().getFullYear();

/* Ingredientes: tocar num cartão troca-o com o painel grande */
const INGS={
  cacay:{nome:"Cacay.",card:"Óleo de Cacay",origem:"Orinoquía colombiana",img:"src/IMG_4142.jpeg",alt:"Nozes de Cacay abertas e óleo dourado sobre ardósia",
    latim:"Caryodendron orinocense · bacia do Orinoco, Colômbia",
    corpo:"O óleo de uma noz que as comunidades da Orinoquía conhecem há gerações. Rico em vitamina E e ácido linoleico: nutre a fibra e dá brilho sem deixar o caracol pesado.",
    funcao:"O ativo principal. Nutre e dá brilho com um toque seco, sem efeito oleoso.",curto:"Nutre a fibra e dá brilho sem pesar."},
  "sacha-inchi":{nome:"Sacha Inchi.",card:"Óleo de Sacha Inchi",origem:"Amazónia colombiana",img:"src/ing-sacha-inchi.jpg",alt:"Cápsulas em estrela de Sacha Inchi, sementes e óleo claro sobre ardósia",
    latim:"Plukenetia volubilis · Amazónia colombiana",
    corpo:"A \u201cnoz-estrela\u201d da Amazónia. As sementes escondem-se dentro de cápsulas em forma de estrela e dão um óleo muito leve, rico em ómega-3 e ómega-6.",
    funcao:"Amacia e dá brilho com uma textura ultraleve, que é absorvida depressa e não deixa resíduo.",curto:"Ultraleve e rico em ómega-3. Brilho sem peso."},
  ungurahui:{nome:"Ungurahui.",card:"Óleo de Ungurahui",origem:"Amazónia colombiana",img:"src/ing-ungurahui.jpg",alt:"Frutos roxos de Ungurahui e óleo verde-dourado sobre ardósia",
    latim:"Oenocarpus bataua · conhecido na Colômbia como seje",
    corpo:"O fruto de uma palmeira amazónica que as comunidades indígenas usam há gerações para cuidar do cabelo. O óleo, rico em ácido oleico, é parecido com o azeite, mas mais leve.",
    funcao:"Suaviza a fibra, ajuda a desembaraçar e deixa os caracóis com brilho e toque macio.",curto:"Usado há gerações no cuidado do cabelo. Brilho e suavidade."},
  quinoa:{nome:"Quinoa.",card:"Proteína de Quinoa",origem:"Andes",img:"src/ing-quinoa.jpg",alt:"Grãos de quinoa, espiga seca e proteína em pó sobre ardósia",
    latim:"Chenopodium quinoa · Andes",
    corpo:"O grão dos Andes, cultivado também no sul da Colômbia. A proteína é hidrolisada, ou seja, partida em fragmentos pequenos que conseguem aderir à superfície do cabelo.",
    funcao:"Dá estrutura e elasticidade ao caracol e ajuda a protegê-lo da quebra ao pentear.",curto:"Estrutura e elasticidade para o caracol."},
  poliglutamico:{nome:"Ácido Poliglutâmico.",card:"Ácido Poliglutâmico",origem:"Biotecnologia",img:"src/ing-poliglutamico.jpg",alt:"Gel transparente a escorrer de uma pipeta para uma taça de cerâmica",
    latim:"γ-PGA · obtido por fermentação natural",
    corpo:"Um ativo de biotecnologia, produzido por fermentação. Funciona como um íman de água: atrai e segura a hidratação dentro e à volta do fio.",
    funcao:"Forma um filme leve e invisível que mantém o caracol hidratado e ajuda a controlar o frizz da humidade.",curto:"Retém a hidratação. Menos frizz."}
};
(function(){
  const heroi=document.getElementById('ing-heroi'); if(!heroi) return;
  let atual='cacay';
  const reduz=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function pintarHeroi(k){
    const d=INGS[k], img=heroi.querySelector('.foto img');
    img.src=d.img; img.alt=d.alt; img.loading='eager';
    const pal=heroi.querySelector('.palavra'); pal.textContent=d.nome; pal.classList.toggle('longa',d.nome.length>12);
    heroi.querySelector('.latim').textContent=d.latim;
    heroi.querySelector('.corpo').textContent=d.corpo;
    heroi.querySelector('.funcao span').textContent=d.funcao;
  }
  function pintarCard(b,k){
    const d=INGS[k]; b.dataset.ing=k;
    const img=b.querySelector('img'); img.src=d.img; img.alt=d.alt;
    b.querySelector('.origem').textContent=d.origem;
    b.querySelector('h4').textContent=d.card;
    b.querySelector('p').textContent=d.curto;
    b.setAttribute('aria-label','Saber mais sobre '+d.card);
  }
  document.querySelectorAll('.ing[data-ing]').forEach(b=>{
    pintarCard(b,b.dataset.ing);
    b.addEventListener('click',()=>{
      const novo=b.dataset.ing, antigo=atual; atual=novo;
      contar('ingrediente-'+novo);
      const top=heroi.getBoundingClientRect().top;
      if(top<0||top>window.innerHeight*0.5) heroi.scrollIntoView({behavior:reduz?'auto':'smooth',block:'start'});
      if(reduz){pintarHeroi(novo);pintarCard(b,antigo);return;}
      heroi.classList.add('troca');
      setTimeout(()=>{pintarHeroi(novo);pintarCard(b,antigo);heroi.classList.remove('troca');},280);
    });
  });
  Object.values(INGS).forEach(d=>{const i=new Image();i.src=d.img;});
})();

/* História: rota desenha-se ao entrar no ecrã; capítulos acendem com o scroll */
(function(){
  const rota=document.getElementById('rota'), caps=document.getElementById('capitulos');
  if(!rota||!caps) return;
  if(!('IntersectionObserver' in window)){rota.classList.add('ver');caps.querySelectorAll('.capitulo').forEach(c=>c.classList.add('ver'));return;}
  new IntersectionObserver((es,o)=>es.forEach(e=>{if(e.isIntersecting){rota.classList.add('ver');contar('historia-vista');o.disconnect();}}),{threshold:.5}).observe(rota);
  const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('ver');io.unobserve(e.target);}}),{rootMargin:'0px 0px -30% 0px'});
  caps.querySelectorAll('.capitulo').forEach(c=>io.observe(c));
  const linha=caps.querySelector('.linha');
  let pedido=false;
  function atualizar(){
    pedido=false;
    const r=caps.getBoundingClientRect(), alvo=window.innerHeight*0.7;
    const h=Math.max(0,Math.min(r.height-16,alvo-r.top));
    linha.style.height=h+'px';
  }
  window.addEventListener('scroll',()=>{if(!pedido){pedido=true;requestAnimationFrame(atualizar);}},{passive:true});
  atualizar();
})();

// ===== MODO PRÉ-ENCOMENDA: ativa-se quando CONFIG.LINK_COMPRA tem um link do Shopify =====
(function(){
  const link = (CONFIG.LINK_COMPRA || "").trim();
  if (!/^https:\/\//.test(link)) return;
  const D = CONFIG.DIAS_PREPARACAO, R = CONFIG.DIAS_DEVOLUCAO;
  let destino = link;
  const preco = CONFIG.PRECO;
  const seta = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
  const ok = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>';
  const linhaPreco = '<b>' + eur(preco) + '</b> · envio em até ' + D + ' dias';
  document.body.classList.add("modo-pre");
  const olho = document.querySelector(".prod-olho"); if (olho) olho.textContent = "ondão · Pré-encomenda";
  CONFIG.PRE_LANCAMENTO = false;
  // barra de avisos
  document.querySelectorAll(".anuncio .trilho span").forEach(sp => {
    if (/Pré-venda/.test(sp.textContent)) sp.textContent = "Pré-encomenda aberta · envio em até " + D + " dias";
    else if (/toda a UE/.test(sp.textContent)) sp.textContent = R + " dias para devolver após a entrega";
  });
  // topo: leva ao produto
  const hero = document.getElementById("cta-hero");
  hero.href = "#produto"; hero.innerHTML = 'Pré-encomendar o meu ondão ' + hero.querySelector("svg").outerHTML;
  // botão do produto e barra fixa: vão direto ao checkout do Shopify
  const comprar = document.getElementById("comprar");
  const novoComprar = comprar.cloneNode(false); comprar.replaceWith(novoComprar);
  novoComprar.innerHTML = '<span class="l1">Pré-encomendar ' + seta + '</span><span class="l2">' + linhaPreco + '</span>';
  novoComprar.addEventListener("click", () => { contar("clique-checkout-produto"); location.href = destino; });
  const fixa = document.getElementById("fixa-btn");
  fixa.href = destino; fixa.innerHTML = '<span class="l1">Quero o meu ondão ' + seta + '</span><span class="l2">' + linhaPreco + '</span>';
  const navCta = document.getElementById("nav-cta");
  if (navCta) { navCta.href = destino; navCta.addEventListener("click", () => contar("clique-checkout-topo")); }
  fixa.addEventListener("click", () => contar("clique-checkout-fixa"));
  // só compra única na pré-encomenda
  // garantias e nota
  const g = document.querySelector(".garantias");
  if (g) g.innerHTML = '<li>' + ok + 'Envio em até ' + D + ' dias</li><li>' + ok + R + ' dias para devolver</li><li>' + ok + 'Pagamento seguro</li>';
  const nota = document.querySelector(".nota-compra");
  if (nota) nota.innerHTML = '<b>Pré-encomenda:</b> paga agora e enviamos em até ' + D + ' dias (mais o tempo de transporte). Os ' + R + ' dias para devolver só começam a contar quando o creme chega a sua casa, por isso a espera não lhe tira prazo.';
})();
