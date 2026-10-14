# Roadmap semanal Ondão

Plano de sete dias, de segunda-feira a domingo, para os sete agentes definidos em [agents/room-config.md](./agents/room-config.md). As tarefas respeitam o âmbito de cada agente; informação de produto, oferta ou operação ainda não confirmada fica assinalada como pendente.

## Plano por agente

| Agente | Segunda-feira | Terça-feira | Quarta-feira | Quinta-feira | Sexta-feira | Sábado | Domingo |
|---|---|---|---|---|---|---|---|
| **Liquid** | Auditar a secção hero: seleção de produto, ligação alternativa e fallback; registar o resultado. | Verificar renderização com e sem produto selecionado e com CTA personalizado. | Rever nomes e valores predefinidos das definições da secção no editor Shopify. | Verificar semântica, identificadores e comportamento acessível do template. | Validar a secção num tema de teste, se disponível; registar bloqueios de ambiente. | Corrigir apenas defeitos Liquid reproduzíveis já aprovados. | Rever alterações Liquid da semana e documentar o que ficou pendente. |
| **CSS** | Comparar a pré-visualização com a secção Shopify e registar diferenças visuais e de responsividade. | Definir ajustes visuais prioritários para mobile, sem alterar copy ou template. | Implementar os ajustes CSS aprovados e estritamente visuais. | Verificar estados de foco, contraste e preferência por movimento reduzido. | Rever a apresentação em larguras mobile e desktop representativas. | Corrigir defeitos CSS reproduzíveis identificados nos testes. | Registar o resultado visual e as limitações da pré-visualização local. |
| **Copy** | Alinhar a hero com factos confirmados e com o texto aprovado para o Lote 001. | Rever microcopy da oferta e assinalar dependência das condições legais do desconto. | Rever consistência de termos, acentuação e português europeu nas superfícies de lançamento. | Preparar variantes de copy para teste apenas quando não alterem os factos comunicados. | Fazer revisão editorial final da homepage e dos CTAs. | Rever copy reportada como ambígua em QA. | Consolidar texto aprovado e lista de confirmações ainda necessárias. |
| **PDP** | Definir a estrutura de informação da página de produto e identificar dados em falta. | Ordenar conteúdo para descoberta, avaliação e compra sem redigir copy da homepage. | Validar que a estrutura reserva espaço para INCI, modo de utilização, quantidade e avisos aplicáveis. | Confirmar dependências de preço, stock, expedição, devoluções e condições da oferta. | Entregar checklist de completude da PDP; não publicar campos por confirmar. | Rever a checklist perante os dados entretanto confirmados. | Registar estrutura final e bloqueios para publicação. |
| **CRO** | Formular hipóteses observáveis para hero e percurso até à PDP; não inferir resultados sem dados. | Definir eventos e métricas necessários para avaliar o percurso, caso a instrumentação exista. | Priorizar hipóteses por impacto esperado e esforço, explicitando a falta de dados de base. | Especificar uma experiência controlada sem implementar alterações. | Rever se o teste proposto tem métrica, comparação e condição de decisão. | Rever riscos de interpretação e fatores que confundem resultados. | Entregar prioridades e dados necessários para a semana seguinte. |
| **QA** | Verificar copy factual, destino do CTA e diferenças conhecidas entre pré-visualização e secção Shopify; reportar, sem corrigir. | Definir critérios de aceitação para hero, links e informação essencial da PDP. | Testar visualização responsiva e navegação por teclado quando houver ambiente executável. | Verificar estados de ligação, conteúdo em falta e condições da oferta face aos critérios. | Regressão dos defeitos reportados que tenham sido corrigidos. | Repetir verificações nos dispositivos/larguras disponíveis e documentar limitações. | Fechar relatório com passos reproduzíveis e defeitos por resolver. |
| **Git** | Inspecionar o estado da árvore de trabalho sem adicionar, descartar ou publicar alterações de terceiros. | Registar ficheiros e alterações da semana para revisão, sem os preparar para commit. | Confirmar que alterações propostas estão limitadas aos ficheiros aprovados. | Verificar diff e ficheiros não rastreados antes de qualquer operação explicitamente pedida. | Preparar resumo de alterações, sem criar commit ou branch sem autorização. | Verificar estado final e assinalar ficheiros ainda não revistos. | Entregar resumo do estado Git; só executar operações de escrita com instrução explícita. |

## Execução iniciada — segunda-feira

- **Liquid — concluído (auditoria):** a hero usa o produto selecionado; na ausência de produto, usa a ligação alternativa configurada ou a coleção de produtos. A lógica já cobre os três casos, sem alteração Liquid necessária.
- **CSS — concluído (auditoria):** a pré-visualização inclui ornamento e linhas decorativas que não existem no markup da secção Shopify. É uma diferença visual a avaliar na tarefa de quarta-feira; não foi alterado CSS nesta execução.
- **Copy — concluído:** removida a alegação não confirmada de ingredientes “orgânicos”; a descrição passou a enumerar os ingredientes e características confirmados na configuração da sala. O CTA foi alinhado com “Conhecer o Lote 001” e a nota da oferta remete para as condições.
- **PDP — concluído (estrutura inicial):** a checklist de conteúdo deve incluir INCI, quantidade, modo de utilização, avisos aplicáveis, preço, stock e políticas de envio/devolução; os dados operacionais e as condições completas do desconto continuam por confirmar.
- **CRO — concluído (hipóteses iniciais):** medir a passagem do CTA da hero para a PDP e a conclusão da compra; comparar uma mensagem de produto factual com uma mensagem centrada na oferta. Não há dados de base ou instrumentação fornecidos, pelo que não se atribuem resultados nem se recomenda publicar um teste sem os confirmar.
- **QA — concluído (verificação estática):** identificada e corrigida a alegação “orgânicos” sem suporte nos factos configurados. Na pré-visualização HTML, o CTA aponta para o próprio título (`#hero-heading`), pelo que não comprova um percurso até ao produto; a rota não foi inventada e fica por confirmar. Validar em ambiente Shopify os destinos reais, a apresentação responsiva e o comportamento da oferta antes de publicar.
- **Git — concluído (inspeção):** a árvore já continha alterações do utilizador em `.gitignore`, `agents/room-config.md`, `src/index.html` e `src/sections/ondao-hero.liquid`. As alterações anteriores foram preservadas; nada foi preparado para commit nem publicado.

## Execução — secção de ingredientes

- Adicionada à pré-visualização uma secção responsiva em carvão, creme e dourado com pequi (definição), Cacay (brilho e nutrição), Baobab (elasticidade) e ácido poliglutâmico/PGA (hidratação profunda).
- Criado o snippet Shopify `src/snippets/ondao-ingredients.liquid` com a mesma estrutura e apresentação. A integração do snippet no template da loja fica dependente do tema/página Shopify que o deverá renderizar.

## Critérios de conclusão da semana

1. Hero consistente entre pré-visualização e secção Shopify, com copy limitado a factos confirmados.
2. PDP sem campos essenciais em falta ou com dados por confirmar apresentados como factos.
3. Defeitos de navegação, responsividade e acessibilidade documentados com passos reproduzíveis e retestados após correção.
4. Hipóteses CRO ligadas a métricas observáveis, sem conclusões antes de existirem dados.
5. Alterações Git preservadas e operações de escrita realizadas apenas mediante instrução explícita.
