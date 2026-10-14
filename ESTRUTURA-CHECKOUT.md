# Transição da Lista VIP para o checkout — Lote 001

## Princípio

A Lista VIP recolhe manifestações de interesse; o checkout é o fluxo que permite
consultar condições e tentar comprar uma unidade. Inscrição, lugar na lista,
acesso ao link e compra confirmada são estados distintos. Só o sistema de
checkout pode confirmar uma encomenda e a disponibilidade real.

## Fluxo operacional

1. **Preparar a lista:** configurar o endpoint de recolha, o serviço de email,
   a confirmação de subscrição, o aviso de privacidade e o processo de
   descadastro. Testar o registo e o tratamento de falhas.
2. **Recolher interesse:** o CTA abre o modal; o visitante fornece um email
   válido. O site envia o formulário apenas quando `data-endpoint` está
   configurado. Resposta de sucesso significa que o endpoint aceitou o registo,
   não que uma unidade ficou reservada.
3. **Aguardar preparação comercial e operacional:** aprovar preço final,
   condições do desconto de fundador (se aplicável), termos, política de
   privacidade, stock efetivo, expedição, devoluções, impostos e apoio ao cliente.
   Não abrir o checkout com campos essenciais por confirmar.
4. **Preparar o checkout:** configurar o produto do Lote 001, preço, quantidade
   máxima por pedido, stock, pagamentos, impostos, expedição, confirmação de
   encomenda e políticas. Definir como a plataforma impede vendas acima do stock.
5. **Testar antes do lançamento:** percorrer a ligação a partir do email em
   mobile e desktop; testar disponibilidade, pagamento de teste, erros,
   abandono, confirmação, emails transacionais e limites de stock. Não usar uma
   lista de emails de clientes reais em testes.
6. **Abrir para a Lista VIP:** quando checkout, stock e condições estiverem
   aprovados, enviar o email de abertura com a ligação direta para o produto no
   checkout. A ligação não deve incluir dados pessoais no URL.
7. **Confirmar a compra:** o checkout mostra preço e condições finais antes do
   pagamento. Só a confirmação emitida pela plataforma marca a encomenda como
   concluída; atualizar stock e enviar confirmação/transação através da
   plataforma.
8. **Encerrar ou atualizar:** ao esgotar o stock, desativar a compra e atualizar
   a página e os emails. Não continuar a comunicar uma vaga/unidade disponível
   sem confirmação operacional.

## Estados e mensagens

| Estado | Significado | Mensagem/ação |
| --- | --- | --- |
| Email inválido | Formato não aceite pelo navegador | Pedir correção; não enviar |
| Endpoint não configurado | Lista ainda não ativa | Informar que o registo não foi enviado |
| Pedido em envio | Pedido submetido, sem resposta ainda | Mostrar estado de envio e impedir submissões duplicadas |
| Endpoint rejeita ou falha | Inscrição não confirmada | Mostrar erro e permitir nova tentativa |
| Endpoint aceita | Email aceite para a Lista VIP | Agradecer pela vaga na lista; não alegar reserva de produto |
| Checkout aberto | Produto disponível para compra segundo stock/preço publicados | Enviar link de abertura à lista, respeitando consentimentos |
| Encomenda confirmada | Plataforma de checkout confirma pagamento/encomenda | Mostrar/enviar confirmação da encomenda |
| Stock esgotado/checkout fechado | Não aceitar novas compras | Fechar CTA de compra e atualizar comunicações |

## Responsabilidades de integração

- O formulário está em [`src/index.html`](./src/index.html); o atributo
  `data-endpoint` permanece vazio até ser configurado.
- O endpoint deverá aceitar `POST` com os campos do formulário e responder com
  um status HTTP de sucesso apenas depois de aceitar o registo. A página não
  persiste emails localmente.
- A integração de checkout, a gestão de stock e a confirmação de encomendas não
  estão implementadas nesta página estática; devem ser fornecidas pela
  plataforma de comércio eletrónico ou por serviços de backend apropriados.
- Não incluir segredos no frontend, não passar emails em URLs e não comunicar
  que uma inscrição VIP é uma reserva, compra ou garantia de stock.

## Critérios para ativação

- [ ] Endpoint de email configurado e testado com respostas de sucesso e erro.
- [ ] Aviso de privacidade e mecanismo de descadastro publicados e revistos.
- [ ] Preço, condições, stock, expedição e políticas aprovados.
- [ ] Checkout e emails transacionais testados em mobile e desktop.
- [ ] Ligação do email de abertura aponta para produto/checkout ativos.
- [ ] Processo de fecho por esgotamento ou indisponibilidade testado.
