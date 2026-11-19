# Navi AI
 
Assistente de terminal, feito em Python, que orienta **universitários e estudantes de baixa renda** sobre bolsas, financiamento estudantil, cadastros do governo, isenção do Enem e transporte estudantil.
 
Ele só responde com o que está na base de conhecimento (`data/base_conhecimento.json`). Toda resposta mostra a fonte, a data em que a informação foi conferida e o aviso de que o assistente **não é um canal oficial**. O assistente nunca pede dados pessoais e recusa perguntas que tenham.

## Integrantes
- Giulliana Maistro Brasolin - RM 569381
- Lara Dos Santos Cândido Alves - RM 573827
- Mikaella Mirela Dos Santos Lucindo - RM 573775

## Público alvo e problema

**Público alvo:** universitários e estudantes de baixa renda.
 
**Problema:** as informações sobre ProUni, Fies, CadÚnico, isenção do Enem e passe de estudante estão espalhadas, em linguagem técnica e misturadas com sites que parecem oficiais e não são. Muita gente perde tempo (ou até o prazo de inscrição) tentando descobrir o que fazer, o que levar e onde ir.

## ODS relacionados
- **ODS 4 – Educação de Qualidade:** facilita o acesso a bolsas, financiamento e outros apoios para estudar.
- **ODS 10 – Redução das Desigualdades:** a orientação é voltada a quem tem menor renda.

## Como executar
Precisa de Python 3 e não usa bibliotecas externas. Na pasta do projeto:
 
```
python main.py
```
 
O repositório já vem com os atendimentos do teste com usuários em `data/historico.json` e `data/atendimentos.csv` (17 atendimentos), então a opção 3 do menu já mostra os indicadores do teste. Novos atendimentos são acrescentados a esses arquivos. Para começar do zero, apague os dois: o programa cria o histórico no primeiro atendimento e o CSV ao sair.
 
Os atendimentos de cada teste estão separados em `data/testes/`.
 
## Como usar
Ao abrir, o programa mostra o objetivo do assistente, avisa que ele não é um canal oficial e explica que perguntas com 8 ou mais números ou com `@` são recusadas. Depois mostra o menu:
 
| Opção | O que faz |
|---|---|
| 1 | Fazer uma pergunta |
| 2 | Navegar por categorias |
| 3 | Ver indicadores |
| 4 | Exportar atendimentos para CSV |
| 0 | Sair do programa |
 
**Ao sair:**
- Se houve atendimento na sessão, o assistente pede uma **nota de facilidade de 1 a 5**, exporta o CSV automaticamente (já com a nota) e se despede agradecendo a avaliação.
- Se não houve atendimento, ele só diz "Até mais!", sem pedir nota e sem exportar. Fizemos essa escolha pois achamos que não faz sentido receber uma nota sem atendimento.
Se a opção 4 for escolhida sem nenhum atendimento novo na sessão, o assistente avisa que não há o que exportar (o CSV é exportado automaticamente ao sair).

## Regra de pontuação
Antes de comparar, a pergunta, as palavras-chave e o título passam pelo `normalizar()`: minúsculas, sem acentos e sem pontuação. Depois, cada orientação recebe pontos:
 
| Regra | Pontos |
|---|---|
| Palavra-chave da orientação que aparece na pergunta | +3 |
| Palavra da pergunta (4 letras ou mais) que aparece no título | +1 |
 
| Melhor pontuação | Resultado |
|---|---|
| 6 ou mais | Confiança **ALTA** |
| 3 a 5 | Confiança **MÉDIA** |
| menos de 3 | "Não encontrei": sugere outras palavras e as categorias |
 
- A comparação é por **palavra inteira**.
- Cada palavra da pergunta conta uma vez só no título.
- O `buscar()` devolve uma lista de tuplas `(pontos, orientacao)`, da maior para a menor pontuação. Em caso de empate, vale a ordem da base.
- O assistente mostra a melhor orientação e **até duas alternativas** (título, categoria e pontos).
**Exemplo:** a pergunta `bilhete unico gratuito` recebe +3 por `gratuito`, +3 por `bilhete unico gratuito` e +1 por `bilhete` e +1 por `unico` no título da orientação 12 (as palavras do título também contam): **8 pontos, confiança ALTA**.

## Regras de atendimento
- **Dados pessoais:** perguntas com 8 ou mais dígitos ou com `@` são recusadas e **não são registradas**.
- **Entradas inválidas:** opção fora da lista, letras, resposta vazia ou `s/n` inválido pedem de novo, sem fechar o programa.
- **Arquivos:** base de conhecimento ou histórico ausente ou com JSON inválido não trava o programa. Sem a base, o assistente avisa e funciona sem orientações.
- **Transparência:** toda resposta mostra fonte, data de verificação e o aviso de que o assistente não é um canal oficial.

## Fontes consultadas
- Portal Acesso Único do MEC (ProUni e Fies): https://acessounico.mec.gov.br
- Ministério do Desenvolvimento e Assistência Social (CadÚnico): https://www.gov.br/mds/pt-br/acoes-e-programas/cadastro-unico
- Cadastro Único (comprovante): https://cadunico.dataprev.gov.br
- Inep (Enem): https://www.gov.br/inep/pt-br
- SPTrans (Bilhete Único de Estudante): https://bilheteunico.sptrans.com.br
- gov.br: https://www.gov.br
  
## Resultado do teste com usuários
O assistente foi testado com **3 pessoas de fora da equipe**, uma de cada vez, em **17 atendimentos** (6 por pergunta em texto livre e 11 pela navegação por categorias), todos em 18/11/2026. Nenhum nome ou dado das pessoas que testaram foi registrado. Os atendimentos de cada teste estão em `data/testes/`([atendimentos_teste1.csv](data/testes/atendimentos_teste1.csv), [atendimentos_teste2.csv](data/testes/atendimentos_teste2.csv), [atendimentos_teste3.csv](data/testes/atendimentos_teste3.csv)) e juntos em `historico_testes.json` e `atendimentos_testes.csv`.
 
### Indicadores por teste
| Indicador | Teste 1 | Teste 2 | Teste 3 | **Geral** |
|---|---|---|---|---|
| Atendimentos | 7 | 6 | 4 | **17** |
| Resposta encontrada | 100% | 66,7% | 100% | **88,2%** |
| Taxa de acerto (ajudou) | 85,7% | 50% | 75% | **70,6%** |
| Tempo médio para encontrar | 6,5 s | 24,2 s | 14,1 s | **13,2 s** |
| Tentativas por atendimento | 1,0 | 1,0 | 1,0 | **1,0** |
| Facilidade de uso (1 a 5) | 5,0 | 4,0 | 5,0 | **4,6** |
 
Os valores são os da opção 3 do menu. O geral é calculado sobre os 17 atendimentos juntos. O tempo inclui a digitação e a leitura da pessoa.
 
### Dúvidas sem solução
- "o Enem da acesso a entrar na UFABC?" (não encontrada)
- "Me fala sobre o Enem" (não encontrada)
- "Quais são os critérios para pedir isenção da taxa do Enem?" (encontrada, mas a pessoa respondeu que não ajudou)
### O que o teste mostrou
- As duas perguntas que não foram encontradas são gerais sobre o Enem. A base só tem orientações específicas sobre o Enem (isenção da taxa e nota mínima para o ProUni), então perguntas amplas não casam com nenhuma palavra-chave.
- A orientação de isenção da taxa do Enem foi marcada como "não ajudou" em 2 das 4 vezes em que apareceu, e a de gratuidade do Bilhete Único em 1 das 3.
- A busca em texto livre foi usada em 6 atendimentos, e em 4 deles encontrou uma orientação (as outras 2 são as perguntas sobre o Enem acima).

### Feedback dos usuários de teste

- "No final eu não sabia como dar a nota, de 0 a 10 eu sempre vejo 10 como melhor, de 3 a 1 eu vejo 1 como melhor. No sistema de vocês é de 1 a 5, não sei se seria algo como 5 estrelas ou 1 de melhor colocação." - Por conta disso adicionamos "(1 = muito difícil, 5 = muito fácil)" na linha onde o assistente pede a nota.
- "Senti falta de uma função que pegue caso eu escreva alguma coisa errado, como errar alguma letra de uma palavra específica, por exemplo escrever "favuldade" em vez de "faculdade." - Nesse caso decidimos não implementar isso no código, mas adicionamos um aviso sobre isso na seção "Limitações" do README.

### Melhoria feita a partir do teste
**Problema:** duas perguntas gerais sobre o Enem ("Me fala sobre o Enem" e "o Enem da acesso a entrar na UFABC?") não foram encontradas, porque a base só tinha orientações específicas sobre o Enem (isenção da taxa e nota mínima do ProUni).
 
**O que foi feito:** a nova orientação **13**, "Enem: o que é e onde usar a nota" (categoria Enem), explica o que é o Enem e onde a nota pode ser usada (Sisu, ProUni, Fies e seleções próprias das instituições). As palavras-chave são gerais: `enem`, `sobre o enem`, `o que e o enem`, `que serve o enem`, `como funciona o enem` e `usar o enem`. A base passou de 12 para 13 orientações.
 
**Resultado:** as duas perguntas agora são encontradas (7 e 4 pontos). As perguntas específicas do teste continuam indo para a mesma orientação de antes: como a nova é a última da base, em caso de empate vale a ordem anterior. Os indicadores acima são de **antes** da melhoria, e os testes não foram refeitos.

## Limitações
- A busca compara palavra inteira: se a pessoa escrever "bolsas" no plural e a palavra-chave estiver no singular, não encontra. A solução seria incluir as variações na base.
- Não corrige erros de digitação.
- Palavras comuns do título (como "fazer") podem somar pontos sozinhas.
- A regra de dados pessoais conta só os dígitos: uma pergunta com datas e anos (ex.: "13 a 24 de abril de 2026") passa de 8 dígitos e é recusada.
- Valores, prazos e regras mudam a cada edital. O assistente mostra a data da última conferência de cada orientação.
- As informações de transporte são sobre a cidade de São Paulo.
- O tempo registrado inclui o tempo de digitação e leitura da pessoa, não só o da busca.

## Vídeo técnico
