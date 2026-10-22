> **Nota:** este é o roteiro inicial usado para gerar os slides no Genspark. A versão final (`curso-ia-estatistica.pdf`/`.pptx`, 45 slides) reordenou os blocos — os exercícios ficaram na última parte da aula — e acrescentou, para cada exercício, um slide de resultados com tabelas no padrão ABNT (Tabelas 1 a 12), além do slide 5 com a evidência do experimento de Peng et al. (2023) sobre produtividade com IA.

# Roteiro dos slides — IA para Estatística Experimental

Curso Inova Agroflorestal (UFVJM) · 4 horas · público sem experiência em programação.
Total: 38 slides (12a–12c e 28a inseridos depois). Estilo visual: limpo, natural/agroflorestal (verdes, terra, folhagem), fonte grande, pouco texto por slide, ícones simples. Idioma: português do Brasil.

---

## 1. Capa
**IA para Estatística Experimental**
Do campo à ANOVA com Gemini — sem precisar programar
Curso Inova Agroflorestal · UFVJM · Prof. ____

## 2. O que você vai levar hoje
- Saber pedir uma análise estatística para a IA (e conferir!)
- Entender o que a IA faz "por trás" (ela escreve código)
- Organizar sua planilha do jeito certo
- Seu próprio assistente estatístico (Gem) com skills prontas
- Apostila, dados de exemplo e gabarito

## 3. Roteiro da aula (4h)
1. Abertura (15 min) · 2. Como a IA chega no resultado (35) · 3. Formatos (30) · Intervalo (15) · 4. Mão na massa no Gemini (45) · 5. Ecossistema Gemini (25) · 6. Skills portáteis (40) · 7. Fechamento (5)

## 4. Por que IA na pesquisa agroflorestal?
- Experimentos de campo geram muitos dados (mudas, SAF, café sombreado, ILPF)
- Programas estatísticos assustam quem não programa
- IA traduz "português" em análise — mas não substitui o pesquisador

## 5. O que a IA faz bem × faz mal
Bem: escrever código, explicar conceitos, organizar planilhas, redigir texto de resultados.
Mal: fazer conta "de cabeça", lembrar dados que não viu, saber o delineamento se você não disser.
Mensagem: **IA é estagiária muito rápida — você é o orientador.**

## 6. Alucinação
A IA pode inventar números, referências e p-valores com total confiança.
Regra de ouro: **nunca aceite um resultado sem ver o código e conferir.**

---

## 7. A IA não faz conta de cabeça
Diagrama de fluxo: Você pergunta em português → IA escreve um programa (Python/R) → executa o programa → lê o resultado → explica para você.
"Mostre o código que você usou" = sua garantia.

## 8. As linguagens da análise de dados
- **R** — padrão da agronomia (pacotes ExpDes.pt, agricolae)
- **Python** — língua nativa das IAs (pandas, statsmodels)
- **SISVAR / Excel** — clássicos com cliques
A IA fala todas; você não precisa falar nenhuma.

## 9. A mesma ANOVA, três jeitos
Lado a lado (código curto):
R: `dic(d$substrato, d$altura_cm, mcomp = "tukey")`
Python: `ols("altura_cm ~ C(substrato)", data=d).fit()` + `anova_lm`
Gemini: "Faça a ANOVA em DIC e o teste de Tukey a 5% da altura das mudas por substrato."
Mesmo resultado: F = 34,57; p < 0,001; CV = 6,1%.

## 10. Peça para ver o código
Prompt: "Mostre o código que você executou e os valores exatos da saída."
Se a IA não executou código → desconfie.

---

## 11. Formato longo: 1 linha = 1 parcela
Ruim (largo): uma coluna por repetição. Bom (longo): colunas substrato | repeticao | altura_cm.
Imagem: duas tabelas lado a lado, ✗ e ✓.

## 12. Regras de ouro da planilha
- Nomes de colunas sem acento e sem espaço (altura_cm)
- Uma informação por coluna, unidade no nome
- Ponto decimal (ou avise a IA que usa vírgula)
- Parcela perdida = célula vazia, nunca "perdida" ou 0
- CSV para a IA, XLSX para você

## 12a. Qual formato usar no Gemini?
1º CSV UTF-8 (melhor) · 2º XLSX com 1 aba e 1 tabela · 3º colar os dados como texto no chat (até ~100 linhas; funciona em qualquer plano, plano B se o upload falhar) · 4º Google Planilhas via @Google Drive.
Evitar: PDF ou foto de tabela (a IA precisa "ler" a imagem e pode errar números).

## 12b. A armadilha do Excel brasileiro
"CSV" do Excel em português sai com ; e vírgula decimal. Acentos quebrados (Ã§) = arquivo fora de UTF-8.
Solução: Google Planilhas > Arquivo > Fazer download > CSV, ou avisar o Gemini: "o arquivo usa ; como separador e vírgula como decimal".

## 12c. Feche o ciclo: confira a leitura
Prompt: "Antes de analisar, diga quantas linhas e colunas você leu, os níveis de cada fator e mostre as 5 primeiras linhas. Depois rode a análise em Python e mostre o código."
Levando o resultado embora: tabela em CSV/Markdown, exportar para Docs/Planilhas, gráfico como imagem, código em .txt para a metodologia. Envie junto um dicionário de dados.

## 13. A estrutura do bom prompt
**Papel + Contexto + Dados + Tarefa + Formato de saída**
Ex.: "Você é estatístico agrícola. Experimento em DIC com 5 substratos e 4 repetições (arquivo anexo). Faça ANOVA, verifique pressupostos e aplique Tukey 5%. Entregue tabela da ANOVA, médias com letras e um parágrafo de interpretação."

## 14. Prompt ruim × prompt bom
Ruim: "analisa isso aí".
Bom: o exemplo do slide anterior. Resultado: análise correta na primeira tentativa.

---

## 15. Intervalo (15 min) ☕

---

## 16. Mão na massa — nossos dados
6 experimentos fictícios realistas:
DIC mudas de ipê · DBC milho em aleias · Fatorial espécie × adubação · Parcela subdividida café sombreado · Doses de N no eucalipto · Contagem de pragas em SAF

## 17. Exercício 1 — DIC: substratos para mudas de ipê
F = 34,57 (p < 0,001), CV = 6,1%. Tukey: composto orgânico (37,4 cm) a, terra+esterco (36,4) a, comercial (33,2) a; terra (26,5) b, terra+areia (25,0) b.
Gráfico de barras com letras.

## 18. Exercício 2 — DBC: milho em aleias
Bloco entra no modelo! Se o resíduo tiver 15 GL, a IA esqueceu o bloco (o certo é 12).
F cultivar = 34,69; CV = 5,0%.

## 19. Exercício 3 — Fatorial: espécie × adubação
Interação significativa → **desdobrar** antes de interpretar.
Mogno responde ao adubo mineral; aroeira quase não responde.
Gráfico de interação (linhas cruzando).

## 20. Exercício 4 — Parcela subdividida: café sombreado
Dois erros: erro (a) para sombreamento, erro (b) para cultivar.
Certo: F sombreamento = 6,48. Se a IA usar um erro só: F ≈ 17,7 (errado!).

## 21. Exercício 5 — Regressão: doses de nitrogênio
Fator quantitativo → regressão, não Tukey.
Modelo quadrático, R² = 0,99. Dose de máxima eficiência técnica = 171 kg/ha de N (≈ 60 m³/ha).
Gráfico de curva com ponto máximo.

## 22. Exercício 6 — Quando os pressupostos falham
Contagem de pragas: variâncias diferentes (Bartlett p = 0,02), CV = 52%.
Solução: transformação √(x + 0,5) → OK, ou Kruskal-Wallis (p = 0,002).
A IA tem que avisar — se não avisou, pergunte.

## 23. Checklist: conferindo a IA
- Delineamento certo? GL do resíduo batem?
- Pressupostos testados?
- Tukey só para fator qualitativo; regressão para quantitativo
- Interação desdobrada?
- CV razoável?
- Código mostrado e executado?

---

## 24. Ecossistema Gemini
Mapa: Gemini app · Gems · Canvas · Deep Research · @Google Drive · NotebookLM · Colab · Planilhas.

## 25. Quem tem acesso a quê
- Grátis (conta pessoal/@ufvjm.edu.br): Gemini app, Gems, Canvas, NotebookLM, Colab + Data Science Agent
- Pago: Gemini dentro do Planilhas/Docs (painel lateral, =AI())
Atenção: disponibilidade muda — confira antes.

## 26. Colab + Data Science Agent
Você pede em português → ele escreve e roda o notebook inteiro.
É o "código por trás" ao vivo.

## 27. NotebookLM, Canvas e Deep Research
NotebookLM: pergunte aos seus PDFs (artigos, normas) com citação da fonte.
Canvas: relatório e gráfico editáveis.
Deep Research: revisão de literatura rápida — confira as referências!

---

## 28. O que é uma skill?
Um "manual de instruções" em texto que transforma a IA em especialista.
Mesmo arquivo funciona em Gemini (Gem), ChatGPT (GPT/Projeto) e Claude (Skill/Projeto).

## 28a. Anatomia de uma skill
Arquivo .md (texto puro). Cabeçalho: name + description. Seções: Quando usar · Perguntas antes de analisar · Passo a passo · Código de referência · Formato da resposta · Regras de segurança.
Exemplo: skill 02 + dic_mudas.csv → Gemini devolve F = 34,57 e as mesmas letras do gabarito.

## 29. Nossas 6 skills
00 Assistente estatístico (roteador) · 01 Planejamento do experimento · 02 DIC/DBC + ANOVA + Tukey · 03 Fatorial e parcela subdividida · 04 Regressão e doses · 05 Interpretação e relatório

## 30. Criando seu Gem em 4 passos
1. gemini.google.com → Gems → Novo Gem
2. Nome: "Estatístico Agroflorestal"
3. Cole o conteúdo de gem-unico.md nas instruções
4. Anexe os arquivos das skills como conhecimento → Salvar → testar com um CSV

## 31. Exercício final: planeje seu experimento
Use a skill de planejamento: descreva sua pergunta de pesquisa → a IA sugere delineamento, nº de repetições, croqui casualizado e planilha modelo.

---

## 32. Ética e boas práticas
- Nunca invente ou "complete" dados
- Confira cada resultado
- Declare o uso de IA na metodologia
- Cuidado com dados sensíveis/inéditos

## 33. Materiais para levar
Apostila (PDF) · Dados de exemplo + gabarito · Pacote de skills · Notebook do Colab

## 34. Obrigado!
Perguntas? · Contato: ____
