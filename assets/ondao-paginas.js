/* ondão: ingredientes e história (página inicial e páginas próprias) */
if (typeof window.contar !== "function") {
  window.contar = function (nome) { try { window.goatcounter && window.goatcounter.count && window.goatcounter.count({path: nome, title: nome, event: true}); } catch (e) {} };
}
var contar = window.contar;
/* Ingredientes: tocar num cartão troca-o com o painel grande */
const INGS={
  cacay:{nome:"Cacay.",card:"Óleo de Cacay",origem:"Orinoquía colombiana",img:(window.ONDAO_ASSET_BASE||"")+"IMG_4142.jpeg",alt:"Nozes de Cacay abertas e óleo dourado sobre ardósia",
    latim:"Caryodendron orinocense · bacia do Orinoco, Colômbia",
    corpo:"O óleo de uma noz que as comunidades da Orinoquía conhecem há gerações. Rico em vitamina E e ácido linoleico: nutre a fibra e dá brilho sem deixar o caracol pesado.",
    funcao:"O ativo principal. Nutre e dá brilho com um toque seco, sem efeito oleoso.",curto:"Nutre a fibra e dá brilho sem pesar."},
  "sacha-inchi":{nome:"Sacha Inchi.",card:"Óleo de Sacha Inchi",origem:"Amazónia colombiana",img:(window.ONDAO_ASSET_BASE||"")+"ing-sacha-inchi.jpg",alt:"Cápsulas em estrela de Sacha Inchi, sementes e óleo claro sobre ardósia",
    latim:"Plukenetia volubilis · Amazónia colombiana",
    corpo:"A \u201cnoz-estrela\u201d da Amazónia. As sementes escondem-se dentro de cápsulas em forma de estrela e dão um óleo muito leve, rico em ómega-3 e ómega-6.",
    funcao:"Amacia e dá brilho com uma textura ultraleve, que é absorvida depressa e não deixa resíduo.",curto:"Ultraleve e rico em ómega-3. Brilho sem peso."},
  ungurahui:{nome:"Ungurahui.",card:"Óleo de Ungurahui",origem:"Amazónia colombiana",img:(window.ONDAO_ASSET_BASE||"")+"ing-ungurahui.jpg",alt:"Frutos roxos de Ungurahui e óleo verde-dourado sobre ardósia",
    latim:"Oenocarpus bataua · conhecido na Colômbia como seje",
    corpo:"O fruto de uma palmeira amazónica que as comunidades indígenas usam há gerações para cuidar do cabelo. O óleo, rico em ácido oleico, é parecido com o azeite, mas mais leve.",
    funcao:"Suaviza a fibra, ajuda a desembaraçar e deixa os caracóis com brilho e toque macio.",curto:"Usado há gerações no cuidado do cabelo. Brilho e suavidade."},
  quinoa:{nome:"Quinoa.",card:"Proteína de Quinoa",origem:"Andes",img:(window.ONDAO_ASSET_BASE||"")+"ing-quinoa.jpg",alt:"Grãos de quinoa, espiga seca e proteína em pó sobre ardósia",
    latim:"Chenopodium quinoa · Andes",
    corpo:"O grão dos Andes, cultivado também no sul da Colômbia. A proteína é hidrolisada, ou seja, partida em fragmentos pequenos que conseguem aderir à superfície do cabelo.",
    funcao:"Dá estrutura e elasticidade ao caracol e ajuda a protegê-lo da quebra ao pentear.",curto:"Estrutura e elasticidade para o caracol."},
  poliglutamico:{nome:"Ácido Poliglutâmico.",card:"Ácido Poliglutâmico",origem:"Biotecnologia",img:(window.ONDAO_ASSET_BASE||"")+"ing-poliglutamico.jpg",alt:"Gel transparente a escorrer de uma pipeta para uma taça de cerâmica",
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
