# Fluxo de email da Lista VIP — Lote 001

## Objetivo e âmbito

Registar pedidos de adesão à Lista VIP para a abertura do Lote 001 e comunicar
com os fundadores por email. A inscrição na lista é uma manifestação de
interesse; não reserva uma unidade, não confirma uma compra e não garante
disponibilidade de stock.

## Estado técnico

O formulário está em [`src/index.html`](./src/index.html). O atributo
`data-endpoint` do formulário `#vip-email-form` está vazio por omissão. Enquanto
estiver vazio, o site não envia nem guarda o email e apresenta uma mensagem a
informar que o registo ainda não está ativo.

Para ativar o envio:

1. Criar uma lista/audiência para o Lote 001 num serviço aprovado e configurar a
   confirmação de subscrição e as regras aplicáveis.
2. Configurar o endpoint HTTPS do formulário em `data-endpoint`. O envio atual
   usa `POST` com `FormData` e o cabeçalho `Accept: application/json`, adequado
   a endpoints que aceitem submissões de formulário, como um formulário
   Formspree configurado para aceitar pedidos cross-origin.
3. Fazer um teste de ponta a ponta com um endereço de teste e verificar a
   receção, os erros, a confirmação de subscrição e a remoção/descadastro.
4. Atualizar o aviso de privacidade da página com o responsável pelo tratamento,
   serviço/subcontratante, finalidade, base legal, conservação, transferências
   eventualmente aplicáveis e forma de exercer direitos antes de recolher dados.

O formulário também exige confirmação explícita para receber novidades por
email e envia esse consentimento junto com o endereço. Manter essa prova no
serviço e processá-la de acordo com a política de privacidade publicada.

Não colocar chaves privadas, tokens ou credenciais no HTML/JavaScript público.
Uma integração Mailchimp que não aceite pedidos cross-origin exige o formulário
de incorporação oficial ou um endpoint intermédio protegido no servidor; não
substituir `data-endpoint` por uma chave privada.

## Sequência recomendada

| Momento | Gatilho | Mensagem | Objetivo |
| --- | --- | --- | --- |
| Imediato | O serviço aceita o email e, quando configurado, a confirmação de subscrição é concluída | Boas-vindas à Lista VIP | Confirmar a adesão e explicar o que a lista significa |
| Antes da abertura | A data e as condições de abertura estão aprovadas | Abertura próxima do Lote 001 | Avisar a lista, sem prometer stock ou benefícios não confirmados |
| Abertura | Checkout publicado e testado; stock e condições aprovados | O checkout do Lote 001 está aberto | Dar acesso ao checkout e explicar que a compra só se conclui no checkout |
| Após a abertura | De acordo com o estado real do checkout/stock | Atualização de disponibilidade | Comunicar apenas estado verificado; parar envios quando a oferta terminar |

Enviar apenas a pessoas com base legal e consentimentos adequados. Respeitar
preferências, descadastros e limites de frequência. Não inferir que os primeiros
100 emails correspondem a 100 compras ou a 100 vagas de produto.

## Template — email de boas-vindas

**Assunto:** Bem-vinda/o à Lista VIP do Lote 001

**Preheader:** Vamos avisar-te quando houver novidades sobre o Lote 001.

**Corpo:**

Olá,

Obrigado pelo teu interesse no Lote 001 da Ondão. O teu endereço foi adicionado
à Lista VIP **[após aceitação pelo serviço e confirmação, quando aplicável]**.

A lista serve para receberes novidades e um aviso quando o checkout estiver
disponível. A inscrição não é uma encomenda nem reserva uma unidade; a compra,
o preço final e a disponibilidade só serão confirmados no checkout, de acordo
com as condições publicadas nessa altura.

**[Ver o Lote 001]** — [URL pública da página]

Recebeste esta mensagem porque pediste para receber comunicações sobre o Lote
001. Podes deixar de receber estes emails a qualquer momento através de
**[ligação de descadastro do serviço]**.

Ondão
**[Dados de contacto e identificação do responsável pelo tratamento]**

**Nota de preparação:** substituir os campos entre parênteses retos, validar o
conteúdo legal e incluir a ligação para a política de privacidade publicada.
Não afirmar que o destinatário é um dos 100 compradores, nem prometer desconto,
prioridade de compra ou disponibilidade enquanto essas condições não estiverem
confirmadas.
