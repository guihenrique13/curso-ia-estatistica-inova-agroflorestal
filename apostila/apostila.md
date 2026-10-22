---
title: "IA para Estatística Experimental"
subtitle: "Curso Inova Agroflorestal"
author: "Prof. ____"
date: "Outubro de 2026"
lang: pt-BR
toc-title: "Sumário"
---

# Antes de começar {-}

Seja bem-vindo(a)! Esta apostila acompanha o curso **"IA para Estatística Experimental"**, do programa Inova Agroflorestal (UFVJM). Ela foi escrita para quem **nunca programou** e quer usar a inteligência artificial como uma "assistente de estatística" para planejar e analisar experimentos agroflorestais.

**Você só vai precisar de:**

- uma conta Google (pessoal ou `@ufvjm.edu.br`);
- o **Gemini** gratuito, em <https://gemini.google.com>;
- os arquivos de dados do curso (pasta `dados/`) e o pacote de skills (pasta `skills/`), que o professor vai disponibilizar.

**Como usar esta apostila.** Os capítulos seguem a ordem da aula. Os blocos em fonte de máquina de escrever, como este:

```
Isto é um prompt pronto. Copie, cole no Gemini e adapte.
```

são **prompts prontos para copiar e colar**. Sempre que aparecer a seção **"O que esperar"**, ela traz os números corretos (calculados no R com o pacote `ExpDes.pt`), em tabelas no padrão ABNT, para você conferir se a IA acertou. Os exercícios práticos ficam no fim da aula (Capítulo 6), depois que você já conhece os formatos, as ferramentas do Gemini e as skills.

**Os dados do curso são fictícios.** Eles foram simulados por computador (arquivo `dados/gerar_dados.py`) imitando situações reais: mudas de ipê, milho em aleias, café sombreado, eucalipto em ILPF e pragas em SAF. Servem para treinar; não use esses números como resultado de pesquisa.

| Arquivo | Delineamento | O que foi medido |
|---|---|---|
| `dic_mudas.csv` | DIC, 5 substratos × 4 repetições | altura (cm) e diâmetro (mm) de mudas de ipê-amarelo aos 120 dias |
| `dbc_milho.csv` | DBC, 5 cultivares × 4 blocos | produtividade de milho (kg/ha) em aleias de gliricídia |
| `fatorial_adubacao.csv` | Fatorial 3 × 3 em DIC, 4 repetições | massa seca (g) de 3 espécies florestais sob 3 adubações |
| `parcela_sub_cafe_sombra.csv` | Parcela subdividida em DBC, 4 blocos | produtividade de café (sc/ha): sombreamento (parcela) × cultivar (subparcela) |
| `doses_nitrogenio.csv` | DIC com 5 doses × 4 repetições | volume de eucalipto (m³/ha) em função da dose de N (kg/ha) |
| `dic_contagem_pragas.csv` | DIC, 4 manejos × 6 repetições | número de insetos-praga por armadilha |
| `planilha_campo_baguncada.xlsx` | (exercício) | a planilha de mudas "do jeito que veio do campo" |

Todos os `.csv` também existem em versão `.xlsx` (Excel). O arquivo `dados/dicionario_dados.md` descreve cada conjunto: o que significa cada coluna, as unidades, o delineamento e os resultados esperados.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Introdução: o que a IA faz bem, e onde ela erra

## Por que usar IA na pesquisa agroflorestal?

Quem faz experimento no campo conhece bem a rotina: meses de condução, dias de coleta e, no fim, uma planilha que precisa virar **tabela de ANOVA, teste de médias e um parágrafo de resultados**. Para muita gente, essa última etapa é a mais difícil, porque exige um programa estatístico (R, SISVAR, SAS) e algum conhecimento de programação.

As IAs conversacionais, como o Gemini, o ChatGPT e o Claude, mudaram esse cenário. Hoje você pode:

- **descrever o experimento em português** e pedir a análise;
- **enviar a planilha** e receber a ANOVA, o teste de Tukey e o gráfico;
- **pedir ajuda para planejar**: qual delineamento usar, quantas repetições, como sortear as parcelas;
- **pedir o texto** de resultados no estilo de relatório ou TCC.

## O que a IA faz bem

| A IA é ótima para... | Exemplo no experimento |
|---|---|
| Explicar conceitos com paciência | "O que é quadrado médio do resíduo, explicado para quem nunca viu estatística?" |
| Escrever e rodar código | Gerar o script em Python ou R que faz a ANOVA |
| Organizar dados | Transformar a planilha de campo "larga" em formato longo |
| Sugerir o caminho | "Meus dados são contagens; qual análise uso?" |
| Redigir | Rascunho da seção de resultados, legenda de tabela, resumo |
| Revisar | Apontar inconsistências na planilha (valor faltando, nome escrito de dois jeitos) |

## O que a IA faz mal

| A IA pode... | Como isso aparece |
|---|---|
| **Alucinar** | Inventa um número, uma referência bibliográfica ou um pacote do R que não existe, e fala com total segurança |
| Errar o modelo | Analisa um DBC como se fosse DIC (esquece o bloco), ou uma parcela subdividida com um resíduo só |
| "Calcular de cabeça" | Se não rodar código, ela **estima** o resultado em vez de calcular, e erra |
| Ignorar pressupostos | Faz a ANOVA sem testar normalidade e homogeneidade |
| Ler errado a planilha | Confunde vírgula decimal, trata o número do bloco como variável numérica |
| Concordar demais | Se você insistir em uma conclusão, ela tende a concordar com você |

## Alucinação: o que é e por que acontece

Um modelo de linguagem (LLM, do inglês *Large Language Model*) é, no fundo, um sistema que **prevê a próxima palavra** mais provável, com base em tudo o que leu durante o treinamento. Ele não "sabe" as coisas como uma enciclopédia; ele gera texto plausível. Na maior parte do tempo, o texto plausível também é correto. Às vezes, não é. Quando a IA produz algo **convincente, mas falso**, chamamos de **alucinação**.

Exemplos típicos em estatística experimental:

- citar "Gomes (2009), página 245" com um conteúdo que não está lá;
- dizer que o p-valor é 0,03 sem ter feito conta nenhuma;
- recomendar uma função `tukey.dbc()` que não existe em nenhum pacote.

## Por que conferir sempre

> **Regra de ouro do curso:** a IA é uma assistente, não a autora. **Quem assina o trabalho é você.** Todo número que vai para o relatório precisa ter sido calculado por código que você viu e conferido com o checklist do Apêndice B.

Três hábitos que resolvem a maior parte dos problemas:

1. **Peça para a IA rodar código e mostrar o código** (Capítulo 2).
2. **Confira os números-chave**: graus de liberdade, médias, CV, p-valor (Apêndice B).
3. **Desconfie de respostas perfeitas demais** e de referências que você não consegue encontrar.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Como a IA chega no resultado

## A IA não faz conta de cabeça: ela escreve um programa

Quando você envia uma planilha ao Gemini e pede uma ANOVA, um bom resultado segue sempre o mesmo ciclo:

```
  Você (pedido em português)
          |
          v
  1. A IA ESCREVE CÓDIGO   (Python, às vezes R)
          |
          v
  2. A IA EXECUTA O CÓDIGO  (num "computador" na nuvem)
          |
          v
  3. A IA LÊ A SAÍDA        (tabela de ANOVA, p-valores...)
          |
          v
  4. A IA INTERPRETA        (explica em português para você)
```

Os passos 1 a 3 são **cálculo de verdade**, feito por bibliotecas estatísticas consagradas. O passo 4 é **texto gerado pela IA**, e é nele que mora o risco de interpretação errada. Se a IA pular os passos 1 a 3 e for direto para o 4, os números provavelmente foram **inventados**.

No Gemini, quando ele roda código, normalmente aparece um bloco recolhível (algo como "Mostrar código" ou "Análise") acima da resposta. **Se esse bloco não aparecer, peça:**

```
Rode a análise executando código em Python sobre o arquivo que enviei.
Não estime nenhum valor de cabeça. Depois, mostre o código completo
que você usou e a saída original do programa.
```

## Tour rápido pelas ferramentas

Você não precisa aprender a programar, mas vale reconhecer as ferramentas que a IA usa "por trás".

### R: o padrão da agronomia

O R é gratuito e é o programa mais usado em artigos de ciências agrárias no Brasil. Dois pacotes se destacam:

- **`ExpDes.pt`**: análise de experimentos em português. Funções como `dic()`, `dbc()`, `fat2.dic()` e `psub2.dbc()` já entregam ANOVA, pressupostos, Tukey e regressão em uma linha. O gabarito desta apostila foi feito com ele (`notebooks/analise_exemplos.R`).
- **`agricolae`**: testes de médias (`HSD.test` para Tukey, `LSD.test`, `duncan.test`), croquis casualizados (`design.crd`, `design.rcbd`) e muito mais.

### Python: a língua nativa das IAs

O Gemini, quando analisa um arquivo, quase sempre usa **Python**. As bibliotecas principais são:

- **`pandas`**: lê e organiza a planilha (é o "Excel" do Python);
- **`statsmodels`**: ANOVA, regressão e teste de Tukey;
- **`scipy`**: testes de Shapiro-Wilk, Bartlett, Levene e Kruskal-Wallis.

### SISVAR, Excel e outros

- **SISVAR** (UFLA): muito usado em agronomia, com menus e sem programação. Ótimo para conferir os resultados da IA.
- **Excel / Google Planilhas**: fazem ANOVA de um fator (suplemento "Análise de Dados"), mas são limitados para DBC, fatorial e Tukey.
- **SAS, Minitab, Statistica**: comerciais e também comuns em artigos.

O ponto importante: **se o modelo for o mesmo, todos dão o mesmo resultado.** R, Python e SISVAR são apenas "calculadoras" diferentes.

## A mesma ANOVA em R e em Python

Vamos analisar o arquivo `dic_mudas.csv`: altura de mudas de ipê-amarelo em 5 substratos, DIC com 4 repetições.

**Em R (pacote ExpDes.pt):**

```r
library(ExpDes.pt)
d <- read.csv("dic_mudas.csv")
dic(d$substrato, d$altura_cm, quali = TRUE, mcomp = "tukey")
```

**Em Python (pandas + statsmodels):**

```python
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from scipy import stats

d = pd.read_csv("dic_mudas.csv")
modelo = smf.ols("altura_cm ~ C(substrato)", data=d).fit()
print(anova_lm(modelo))                               # ANOVA
print(stats.shapiro(modelo.resid))                    # normalidade
print(stats.bartlett(*[g.altura_cm for _, g in d.groupby("substrato")]))
print(pairwise_tukeyhsd(d.altura_cm, d.substrato))    # Tukey
cv = 100 * modelo.mse_resid ** 0.5 / d.altura_cm.mean()
print(f"CV = {cv:.1f}%")
```

**Comparando linha a linha:**

| Etapa | R (ExpDes.pt) | Python |
|---|---|---|
| Ler a planilha | `read.csv()` | `pd.read_csv()` |
| Definir o modelo | embutido em `dic()` | `smf.ols("altura_cm ~ C(substrato)")` |
| Tabela de ANOVA | embutida em `dic()` | `anova_lm(modelo)` |
| Shapiro-Wilk | embutido | `stats.shapiro()` |
| Bartlett | embutido | `stats.bartlett()` |
| Tukey | `mcomp = "tukey"` | `pairwise_tukeyhsd()` |
| CV% | embutido | calculado à mão: √QMres / média × 100 |

**E o resultado é o mesmo nos dois:**

| FV | GL | SQ | QM | F | p-valor |
|---|---:|---:|---:|---:|---:|
| Substrato | 4 | 515,85 | 128,96 | 34,57 | 2,09 × 10⁻⁷ |
| Resíduo | 15 | 55,95 | 3,73 | | |
| Total | 19 | 571,81 | | | |

CV = 6,1 %. Repare que o R faz tudo em uma linha porque o pacote foi feito para agronomia; o Python exige mais passos, mas a IA escreve esses passos por você.

> **Diferença comum:** no Python, o Tukey aparece como uma lista de **pares** comparados (`reject = True/False`), e não como **letras**. Peça à IA: *"converta o resultado do Tukey em letras, como no SISVAR"*.

## Pedindo para ver o código

Mostrar o código não é para você aprender a programar: é para você **conferir o que foi feito**. Mesmo sem saber programar, dá para checar:

- o **nome do arquivo** lido é o seu?
- a **variável resposta** é a certa (altura ou diâmetro)?
- o **bloco** entrou no modelo (em DBC)?
- os **fatores** aparecem com `C(...)` (como categoria) ou foram tratados como número?

Prompt para usar sempre ao final de uma análise:

```
Mostre o código que você usou, completo, sem resumir. Depois explique
em linguagem simples, linha por linha, o que cada parte faz. Por fim,
escreva o código equivalente em R usando o pacote ExpDes.pt, para eu
conferir no R ou no Colab.
```

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Formatos: como organizar os dados e os pedidos

Metade dos erros da IA vem de **dados mal organizados** ou de **pedidos vagos**. Este capítulo resolve as duas coisas.

## Organizando a planilha

### Formato longo (tidy): 1 linha = 1 parcela

A regra mais importante: **cada linha é uma unidade experimental (parcela), cada coluna é uma variável.**

**Formato largo (evite):** cada repetição em uma coluna.

| Substrato usado | Rep 1 (cm) | Rep 2 (cm) | Rep 3 (cm) | Rep 4 (cm) |
|---|---|---|---|---|
| Terra | 25,9 | 23,1 | 29,7 | 27,2 |
| Composto Orgânico | ... | ... | perdida | ... |

**Formato longo (use):**

| substrato | repeticao | altura_cm | diametro_mm |
|---|---:|---:|---:|
| terra | 1 | 25.9 | 3.20 |
| terra | 2 | 23.1 | 3.26 |
| terra | 3 | 29.7 | 3.46 |
| terra | 4 | 27.2 | 3.37 |

No formato longo, os **fatores** (substrato, bloco, espécie, dose) e a **identificação** (repetição) ficam em colunas próprias, e cada **variável medida** (altura, diâmetro) ganha a sua coluna.

### CSV ou XLSX?

| | CSV (`.csv`) | XLSX (`.xlsx`) |
|---|---|---|
| O que é | texto puro, valores separados por vírgula | planilha do Excel |
| Vantagem | lido por qualquer programa e IA sem surpresa | guarda várias abas, cores, fórmulas |
| Risco | no Excel em português, pode sair com `;` e vírgula decimal | fórmulas, células mescladas e cores confundem a leitura |
| Recomendação | **preferido para enviar à IA** | aceito, se tiver **uma aba só** e sem mesclar células |

Para salvar CSV: no Google Planilhas, *Arquivo → Fazer download → Valores separados por vírgula (.csv)*. No Excel, *Salvar como → CSV UTF-8*.

### Nomes de colunas

| Ruim | Bom | Por quê |
|---|---|---|
| `Substrato usado` | `substrato` | espaço quebra códigos |
| `Rep 1 (cm)` | `repeticao` + `altura_cm` | parênteses e espaço; unidade vai no nome, com `_` |
| `Produção (sc/ha)` | `producao_sc_ha` | acento, barra e parênteses |
| `Ç`, `ã`, `é` | `c`, `a`, `e` | acentos podem virar símbolos estranhos |

**Regra prática:** letras minúsculas, sem acento, sem espaço, palavras ligadas por `_`, unidade no final (`altura_cm`, `dose_n_kg_ha`).

Também padronize os **níveis** dos tratamentos: `Terra`, `terra ` (com espaço no final) e `TERRA` são três tratamentos diferentes para o computador!

### Ponto ou vírgula decimal

O Brasil usa vírgula (25,9); a maioria dos programas usa ponto (25.9). Misturar os dois faz a coluna ser lida como **texto**, e a análise falha ou sai errada.

- Prefira **ponto decimal** nos arquivos enviados à IA (os arquivos do curso já estão assim).
- Se o seu arquivo tem vírgula, **avise no prompt**: *"o arquivo usa vírgula como separador decimal e ponto e vírgula como separador de colunas"*.

### Dados perdidos (parcela perdida)

Planta morreu, formiga atacou, etiqueta sumiu: acontece. Como registrar:

- deixe a célula **vazia** (ou escreva `NA`);
- **nunca** escreva `perdida`, `0`, `-` ou `morreu` na coluna numérica: o zero, por exemplo, será tratado como uma medida real de altura zero;
- se quiser registrar o motivo, crie uma coluna `observacao`;
- **avise a IA** que há parcela perdida: isso deixa o experimento desbalanceado e muda alguns cálculos (GL do resíduo, tipo de soma de quadrados, Tukey com repetições diferentes).

### Exercício rápido: arrumando a planilha de campo

Abra o Gemini, envie o arquivo `planilha_campo_baguncada.xlsx` e cole:

```
Esta planilha veio do campo: experimento em DIC com 5 substratos e 4
repetições, medindo altura de mudas de ipê-amarelo (cm).
1. Liste todos os problemas de organização que você encontrar.
2. Reorganize no formato longo, com as colunas: substrato, repeticao,
   altura_cm. Use ponto decimal, nomes sem acento, minúsculos e com _.
3. Parcelas perdidas devem ficar vazias (NA), nunca zero.
4. Me entregue o resultado como tabela e como arquivo CSV para baixar.
Não invente nenhum valor.
```

**O que esperar:** a IA deve apontar formato largo, nomes de coluna com espaço e parênteses, vírgula decimal, nomes de substrato inconsistentes (`comercial ` com espaço, `Terra c/ esterco`, `terra + areia`, maiúsculas e acentos) e a palavra `perdida` na repetição 3 do composto orgânico, que deve virar `NA`. O resultado deve ter **20 linhas** (5 × 4), com uma delas vazia na altura.

## Trabalhando com arquivos no Gemini

Você já sabe **como** organizar a planilha. Agora falta **entregar** essa planilha ao Gemini sem que nada se perca no caminho, e **trazer o resultado de volta** para o seu relatório. Lembre-se: quem roda a análise é o Gemini; o seu trabalho é garantir que ele leu os dados certos.

### Formatos e quando usar cada um

| Formato | Quando usar | Cuidados | Nota |
|----------------|------------------------|----------------------------|----------------|
| **CSV UTF-8** (`.csv`) | Sempre que puder: é o formato mais simples e seguro para a IA | Confira o separador (`,` ou `;`) e o decimal; salve em UTF-8 | **Melhor opção** |
| **XLSX** (`.xlsx`) | Quando a planilha já está no Excel | **Uma aba só e uma tabela só**; sem células mescladas, cores com significado, fórmulas ou totais no fim | **2ª opção** |
| **Texto colado no chat** | Experimentos pequenos (até ~100 linhas, como os do curso) | Cole com o cabeçalho; diga qual é o separador | **3ª opção** (plano B) |
| **TSV / TXT tabulado** (`.tsv`, `.txt`) | Quando o programa exporta só texto separado por tabulação | Avise que o separador é a tabulação | Aceitável |
| **Google Planilhas** | Quando os dados já estão no Drive do grupo | Use a extensão **@Google Drive** ou baixe como CSV e envie; uma aba só | Aceitável |
| **PDF** | Só quando não existe a planilha original (ex.: tabela de um artigo) | A IA precisa "ler" a página; pode trocar números e colunas | **Evite** (último recurso) |
| **Foto ou print de tabela** | Caderno de campo fotografado, print de tela | Letra, sombra e ângulo geram erros de transcrição | **Evite** (último recurso) |

**Ordem de preferência:** CSV UTF-8 → XLSX com uma aba e uma tabela → dados colados como texto (para experimentos pequenos).

> **PDF e foto são o último recurso.** Nesses casos a IA precisa "ler" a imagem antes de analisar, e **erros de transcrição são possíveis** (um 8 vira 3, uma vírgula some, uma linha pula). **Sempre** peça: *"Antes de analisar, mostre a tabela completa que você leu do arquivo."* Confira linha por linha com o original.

### A armadilha do Excel brasileiro

No Excel em português, a opção **"CSV (separado por vírgulas)"** **não** salva com vírgulas: ela usa **ponto e vírgula (`;`) como separador** e **vírgula como decimal**. O arquivo fica assim:

```
substrato;repeticao;altura_cm;diametro_mm
terra;1;25,9;3,2
terra;2;23,1;3,26
```

Isso não é um erro, mas a IA precisa saber. Você tem duas saídas:

1. **Avise no prompt:** *"o arquivo usa ; como separador de colunas e vírgula como separador decimal."*
2. **Salve no padrão internacional:** no **Google Planilhas**, *Arquivo → Fazer download → Valores separados por vírgula (.csv)*. O arquivo sai com **vírgula como separador** e **ponto como decimal**, que é o padrão que qualquer programa entende. Os arquivos do curso já estão assim.

### Codificação: UTF-8 para os acentos não quebrarem

Todo arquivo de texto tem uma "codificação", o jeito como as letras são gravadas. Use sempre **UTF-8**. No Excel, escolha *Salvar como → **CSV UTF-8 (delimitado por vírgulas)***; o Google Planilhas já salva em UTF-8.

**Sintoma de codificação errada:** aparecem símbolos estranhos no lugar dos acentos, como `Ã§` em vez de `ç` ou `Ã£` em vez de `ã` (`adubaÃ§Ã£o` em vez de `adubação`). Se isso aparecer na resposta da IA, salve de novo em UTF-8, ou use nomes sem acento (veja *Nomes de colunas*, acima).

### Colando os dados como texto

Para experimentos pequenos (até umas **100 linhas**; os do curso têm de 20 a 36), você **não precisa enviar arquivo**: basta colar os dados no chat. Funciona em **qualquer plano** e é o **plano B mais seguro** quando o envio de arquivo falhar.

Duas formas de copiar:

- abra o `.csv` no Bloco de Notas, selecione tudo (`Ctrl + A`), copie e cole no chat; ou
- selecione as células na planilha (Excel ou Google Planilhas), incluindo o cabeçalho, copie e cole. Elas chegam separadas por tabulação, o que também funciona.

As primeiras linhas de `dic_mudas.csv`, como texto, ficam assim:

```
substrato,repeticao,altura_cm,diametro_mm
terra,1,25.9,3.2
terra,2,23.1,3.26
terra,3,29.7,3.46
terra,4,27.2,3.37
terra_esterco,1,35.3,4.16
```

**Prompt completo, com os dados colados:**

```
Atue como estatístico experimental. Experimento em DIC com 5 substratos
e 4 repetições (20 parcelas), mudas de ipê-amarelo aos 120 dias.
Os dados estão abaixo, em CSV (separador vírgula, decimal ponto).
Colunas: substrato (tratamento), repeticao, altura_cm e diametro_mm.

substrato,repeticao,altura_cm,diametro_mm
terra,1,25.9,3.2
terra,2,23.1,3.26
[... cole aqui as 20 linhas do arquivo ...]

1. Antes de analisar, confirme quantas linhas e colunas você leu e
   quais os níveis de substrato.
2. Rode código em Python para a ANOVA da altura_cm, os pressupostos
   (Shapiro-Wilk e Bartlett), o Tukey a 5% e o CV%.
3. Mostre o código e entregue as tabelas em formato que eu possa copiar.
Não invente valores.
```

### Enviando arquivos

**Como anexar:** na caixa de texto do Gemini, clique no **+** (em algumas versões, um **clipe**) → **Enviar arquivo** (ou *Fazer upload*) e escolha o arquivo no computador. Para arquivos do Drive, use a opção **Drive** no mesmo menu ou digite `@Google Drive` no pedido. O arquivo aparece como um "cartão" acima da caixa de texto; depois escreva o pedido normalmente.

> **Os limites mudam.** Em **outubro de 2026**, fontes não oficiais indicam até **10 arquivos por pedido** e até **100 MB por arquivo**. A ajuda do Google, historicamente, já marcou o envio de **planilhas e CSV** como recurso de **plano pago** em alguns casos. Ou seja: **TESTE com a sua conta antes da aula** (envie o `dic_mudas.csv` e veja se ele é aceito e lido).

**Se o envio do CSV falhar:**

1. **cole os dados como texto** (seção anterior); ou
2. **suba o arquivo no Google Drive** e chame com `@Google Drive` (Capítulo 4); ou
3. tente o `.xlsx` no lugar do `.csv` (ou o contrário).

### Feche o ciclo: confirme o que a IA leu

O erro mais perigoso não aparece na resposta: é a IA analisar **outro conjunto de dados** sem você perceber (pulou linhas, leu a vírgula decimal como separador, trocou colunas). Por isso, **sempre** peça que o Gemini:

1. **confirme o que leu:** número de linhas, número de colunas, níveis de cada fator e as **5 primeiras linhas**;
2. **diga se rodou código** (Python) e **mostre o código**;
3. **entregue os resultados como tabela** que você possa copiar.

**Prompt de verificação de leitura** (envie junto com o arquivo, antes da análise):

```
Antes de qualquer análise, confirme a leitura do arquivo:
1. Quantas linhas (sem contar o cabeçalho) e quantas colunas você leu?
2. Qual o nome e o tipo (número ou texto) de cada coluna?
3. Quais são os níveis de cada fator e quantas repetições há em cada
   nível? Há células vazias (NA)?
4. Mostre as 5 primeiras linhas exatamente como você leu.
5. Você leu o arquivo rodando código (Python)? Se sim, mostre o código.
Não faça nenhuma análise ainda. Espere eu confirmar que está correto.
```

Compare com o que você sabe do experimento: o `dic_mudas.csv`, por exemplo, deve ter **20 linhas, 4 colunas, 5 substratos com 4 repetições cada**. Só depois de conferir, peça a ANOVA.

### Levando os resultados para fora do Gemini

| O que você quer | Como pedir ou fazer |
|------------------|-------------------------------------------------|
| Tabela para colar no Excel ou nas Planilhas | *"Entregue a tabela em Markdown"* (copie e cole no Docs) ou *"em texto CSV, num bloco de código"* (cole na planilha e use *Dados → Dividir texto em colunas*) |
| Levar direto para o Google Planilhas ou Docs | Use o botão **Compartilhar e exportar** abaixo da resposta → **Exportar para o Planilhas** (tabelas) ou **Exportar para o Docs** (texto) |
| Gráfico | *"Gere o gráfico como imagem PNG"*; depois clique na imagem para baixar |
| Código, para registro e para a metodologia | *"Mostre o código completo num bloco único"*; copie e salve num arquivo `.txt` (por exemplo, `analise_dic_mudas_codigo.txt`) junto com os dados |

Guardar o código é importante: ele é a prova de **como** a análise foi feita e ajuda a escrever a metodologia (Capítulo 7).

### Skills e arquivos de contexto

As **skills** do curso (Capítulo 5) são arquivos **`.md`**, ou seja, **texto puro** com um pouco de formatação. Um **`.txt`** com o mesmo conteúdo funciona igual. Você pode colar o texto no chat ou anexar o arquivo.

Nos **arquivos de conhecimento** de um Gem, anexe o arquivo da skill (`.md`) **e** o `dados/dicionario_dados.md`, que descreve cada conjunto de dados do curso.

**Dicionário de dados.** Mandar, junto com os dados, um texto curto dizendo **o que cada coluna significa, a unidade e o delineamento** melhora muito a resposta: a IA não precisa adivinhar qual coluna é o bloco, qual é o tratamento e qual é a resposta. O dicionário completo dos dados do curso está em `dados/dicionario_dados.md`. Para o seu experimento, basta algo assim:

```
Dicionário de dados (dic_mudas.csv)
Delineamento: DIC, 5 substratos x 4 repetições = 20 parcelas (viveiro).
- substrato: tratamento (fator, 5 níveis: terra, terra_esterco,
  comercial, composto_organico, terra_areia)
- repeticao: número da repetição (1 a 4), não é bloco
- altura_cm: altura da muda aos 120 dias, em centímetros
- diametro_mm: diâmetro do coleto aos 120 dias, em milímetros
Sem parcelas perdidas.
```

### Checklist "Antes de enviar o arquivo"

- [ ] A planilha está em **formato longo** (1 linha = 1 parcela)?
- [ ] O arquivo tem **uma aba só** e **uma tabela só**, sem células mescladas, cores ou totais?
- [ ] Os nomes de colunas estão **minúsculos, sem acento, sem espaço** e com a unidade (`altura_cm`)?
- [ ] O **separador** e o **decimal** estão claros (vírgula e ponto, ou avisei que é `;` e vírgula)?
- [ ] O arquivo foi salvo em **UTF-8** (sem `Ã§` no lugar de `ç`)?
- [ ] As parcelas perdidas estão **vazias ou como `NA`** (nunca zero)?
- [ ] Vou mandar junto o **dicionário de dados** (colunas, unidades, delineamento)?
- [ ] Vou pedir a **verificação de leitura** (linhas, colunas, níveis, 5 primeiras linhas) antes da análise?

## Organizando o pedido: a estrutura do prompt

Um bom prompt para análise estatística tem cinco partes. Use a sigla **P-C-D-T-F**:

| Parte | Pergunta que responde | Exemplo |
|---|---|---|
| **P**apel | Quem a IA deve ser? | "Atue como estatístico experimental com experiência em ciências agrárias." |
| **C**ontexto | Que experimento é esse? | "Experimento em DBC com 5 cultivares de milho e 4 blocos, em aleias de gliricídia." |
| **D**ados | Onde estão e como estão organizados? | "Arquivo anexo `dbc_milho.csv`; colunas: bloco, cultivar, produtividade_kg_ha." |
| **T**arefa | O que exatamente deve ser feito? | "Teste os pressupostos, faça a ANOVA e o Tukey a 5%." |
| **F**ormato de saída | Como quero receber? | "Tabela de ANOVA, tabela de médias com letras, CV% e um parágrafo para o relatório." |

### Exemplo ruim × exemplo bom

**Ruim:**

```
faz a anova desse arquivo
```

Problemas: não diz o delineamento (a IA pode ignorar o bloco), não diz a variável, não pede pressupostos nem teste de médias, não pede para rodar código.

**Bom:**

```
[Papel] Atue como estatístico experimental especializado em ciências
agrárias.
[Contexto] Experimento em blocos casualizados (DBC) com 5 cultivares de
milho e 4 blocos (faixas de declive), em sistema de aleias.
[Dados] Arquivo anexo dbc_milho.csv. Colunas: bloco (identificação do
bloco, tratar como fator), cultivar (tratamento) e produtividade_kg_ha
(variável resposta).
[Tarefa] Execute código em Python para: (1) ajustar o modelo
produtividade ~ cultivar + bloco; (2) testar normalidade dos resíduos
(Shapiro-Wilk) e homogeneidade (Bartlett); (3) fazer a ANOVA;
(4) aplicar Tukey a 5% e (5) calcular o CV%.
[Formato] Entregue: tabela de ANOVA (FV, GL, SQ, QM, F, p), tabela de
médias com letras, CV%, e um parágrafo curto de resultados no estilo
de relatório técnico. Não invente valores e mostre o código usado.
```

### Mais dicas de prompt

- **Um passo de cada vez.** Em análises longas (fatorial, parcela subdividida), peça primeiro a ANOVA; depois o desdobramento.
- **Peça para a IA perguntar.** *"Antes de analisar, faça as perguntas que precisar sobre o meu experimento."*
- **Fixe o nível de significância** (5%) e o teste de médias (Tukey, Scott-Knott, Duncan).
- **Peça a conferência:** *"Confira se o número de linhas e de repetições por tratamento bate com o delineamento descrito."*

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Ecossistema Gemini

O Gemini não é só a janela de chat. O Google oferece várias ferramentas ligadas a ele, e algumas são muito úteis para quem pesquisa. Nesta parte da aula, o professor faz uma demonstração; esta apostila traz o passo a passo para você testar depois.

## Quem tem acesso a quê

> **Importante:** as informações abaixo foram verificadas em **outubro de 2026**. O Google muda planos, nomes e limites com frequência. **Confira a disponibilidade atual** na página de ajuda do Google antes de planejar uma aula ou um trabalho em cima de uma ferramenta.

| Ferramenta | Conta Google pessoal (grátis) | Conta `@ufvjm.edu.br` (Workspace for Education) | Plano pago (Google AI Pro / complemento Workspace) |
|------------------|----------------|--------------------|----------------|
| Gemini app (chat, envio de arquivos) | Sim, com limites de uso | Sim, incluído em todas as edições Education, **se o administrador tiver liberado** | Sim, limites maiores e modelos mais avançados |
| Gems com arquivos de conhecimento | Sim, com limites | Sim (dentro do Gemini app) | Sim |
| Canvas | Sim, com limites | Sim (dentro do Gemini app) | Sim |
| Deep Research | Sim, poucas pesquisas por mês | Sim (dentro do Gemini app), com limites | Sim, limites maiores |
| Extensão @Google Drive | Sim | Sim (dentro do Gemini app) | Sim |
| NotebookLM | Sim | Sim, incluído em todas as edições Education, **se liberado pelo administrador** | Sim, limites maiores |
| Gemini no Colab (Data Science Agent) | Sim, para maiores de 18 anos em países suportados | Depende de o Colab estar liberado para a conta | Sim |
| Gemini dentro de Docs, Planilhas e Apresentações (painel lateral, "Help me organize", função `=AI()`) | **Não** | **Não**, sem complemento pago | **Sim** |

**Em resumo:** o chat do Gemini (com Gems, Canvas, Deep Research e @Google Drive), o NotebookLM e o Colab são gratuitos. O Gemini **dentro** das Planilhas e do Docs exige plano pago. Se a sua conta `@ufvjm.edu.br` não abrir o Gemini ou o NotebookLM, use a conta pessoal ou peça ao setor de TI que libere o serviço.

## Gemini app: chat com seus dados

**O que é:** o chat em <https://gemini.google.com>, onde você conversa, envia arquivos (CSV, XLSX, PDF, imagens) e o Gemini analisa rodando código.

**Uso no experimento:** tudo o que vamos fazer no Capítulo 6: ANOVA, Tukey, regressão, gráficos, texto de resultados.

**Como usar:**

1. Acesse <https://gemini.google.com> com sua conta Google.
2. Clique no **+** ao lado da caixa de texto e escolha **Enviar arquivo**.
3. Escreva o pedido no formato P-C-D-T-F.
4. Abra o bloco de código da resposta para conferir o que foi feito.

**Prompt de exemplo:**

```
Analise o arquivo anexo (DIC, 5 substratos, 4 repetições, resposta
altura_cm). Rode código em Python, faça ANOVA, pressupostos e Tukey 5%,
e gere um gráfico de barras com as médias, barras de erro e as letras
do Tukey sobre cada barra.
```

## Gems: o seu assistente estatístico personalizado

**O que é:** um Gem é uma "versão personalizada" do Gemini, com **instruções fixas** e **arquivos de conhecimento** anexados. Você configura uma vez e usa sempre.

**Uso no experimento:** criar um "Estatístico Agroflorestal" que já sabe as regras de análise (as skills do curso), sem precisar repetir o prompt longo toda vez. Veja o passo a passo completo no Capítulo 5.

**Prompt de exemplo (dentro do Gem):**

```
Tenho um experimento novo. Anexei a planilha. Faça as perguntas que
precisar antes de analisar.
```

## Canvas: relatório e gráfico editáveis

**O que é:** um espaço de edição ao lado do chat, onde o Gemini escreve um documento ou um pequeno aplicativo/página que você pode editar e pedir ajustes por partes.

**Uso no experimento:** montar o rascunho da seção de resultados com tabela e gráfico, ou uma página interativa com o gráfico da curva de dose.

**Como usar:** na caixa de texto, clique em **Ferramentas** (ou no ícone correspondente) e escolha **Canvas**; depois faça o pedido. Selecione um trecho do texto no Canvas para pedir alterações só naquela parte.

**Prompt de exemplo:**

```
No Canvas, escreva a seção "Resultados e Discussão" do experimento de
doses de nitrogênio em eucalipto, usando SOMENTE os números da análise
que fizemos nesta conversa. Inclua a tabela de ANOVA, a equação de
regressão, a DMET e uma legenda para o gráfico. Marque com [CONFERIR]
qualquer número que não veio da análise.
```

## Deep Research: revisão de literatura rápida

**O que é:** o Gemini faz dezenas de buscas na web, lê as fontes e entrega um relatório com links. Leva alguns minutos.

**Uso no experimento:** levantar o que já se sabe sobre o tema antes de planejar ("doses de N em eucalipto em ILPF"), ou encontrar referências para a discussão.

**Como usar:** em **Ferramentas**, escolha **Deep Research**, escreva o tema, revise o plano de pesquisa que ele propõe e clique em **Iniciar pesquisa**. No plano grátis, há poucas pesquisas por mês.

**Prompt de exemplo:**

```
Faça uma pesquisa sobre a resposta do eucalipto à adubação nitrogenada
em cobertura em sistemas de integração lavoura-pecuária-floresta no
Brasil. Priorize artigos científicos revisados por pares e publicações
da Embrapa. Liste as doses testadas, os delineamentos usados e as doses
recomendadas, sempre com a referência completa e o link.
```

> **Confira cada referência.** Abra os links e veja se o artigo existe e diz o que o relatório afirma. Deep Research reduz, mas não elimina, a alucinação.

## Extensão @Google Drive: chamar a planilha direto no chat

**O que é:** permite que o Gemini acesse arquivos do seu Google Drive sem precisar baixar e enviar.

**Uso no experimento:** analisar a planilha de campo que já está no Drive do grupo de pesquisa.

**Como usar:** na primeira vez, autorize em *Configurações → Apps/Extensões*. Depois, digite `@Google Drive` na caixa de texto, seguido do pedido.

**Prompt de exemplo:**

```
@Google Drive encontre a planilha "dbc_milho" no meu Drive e analise
como DBC: cultivar é o tratamento, bloco é o bloco, resposta
produtividade_kg_ha. ANOVA e Tukey 5%.
```

## NotebookLM: perguntar aos seus próprios PDFs

**O que é:** em <https://notebooklm.google.com>, você cria um "caderno", envia PDFs, links e documentos, e faz perguntas. As respostas vêm **com citação** do trecho exato da fonte. Também gera resumos em áudio e mapas mentais.

**Uso no experimento:** carregar o livro de estatística experimental da disciplina, o manual do `ExpDes.pt`, as normas do programa de pós-graduação ou 10 artigos sobre o tema, e tirar dúvidas com a fonte ao lado.

**Como usar:**

1. Acesse <https://notebooklm.google.com> e clique em **Novo notebook**.
2. Adicione as fontes (PDF, Google Docs, link de site, vídeo do YouTube).
3. Pergunte no chat; clique nos números das citações para ver o trecho original.

**Prompt de exemplo:**

```
Segundo as fontes, quando devo usar parcela subdividida em vez de
fatorial? Quais as vantagens e desvantagens? Cite os trechos.
```

## Gemini no Colab: o código por trás, na prática

**O que é:** o Google Colab (<https://colab.research.google.com>) é um ambiente gratuito para rodar código Python (e R) no navegador. O **Data Science Agent** do Gemini, dentro do Colab, recebe um pedido em português e **escreve e executa um notebook inteiro**, célula por célula.

**Uso no experimento:** ver, de forma transparente, cada passo do código. É ótimo para quem quer guardar a análise reproduzível ou mostrar ao orientador. O notebook do curso (`notebooks/analise_exemplos.ipynb`) traz prompts sugeridos para o agente.

**Como usar:**

1. Abra <https://colab.research.google.com> e crie um **Novo notebook**.
2. Envie o CSV pelo ícone de pasta (barra lateral esquerda) → **Fazer upload**.
3. Abra o painel do Gemini (ícone de estrela/brilho) e descreva a análise.
4. O agente propõe um plano; aceite e acompanhe a execução das células.

**Prompt de exemplo:**

```
Usando o arquivo fatorial_adubacao.csv, faça a análise de um fatorial
3x3 em DIC (especie x adubacao, resposta massa_seca_g): pressupostos,
ANOVA, desdobramento da interação com Tukey 5% e um gráfico de barras
agrupadas. Comente cada célula em português.
```

## Gemini nas Planilhas Google (plano pago)

**O que é:** um painel lateral do Gemini dentro do Google Planilhas, com o recurso "Help me organize" e a função `=AI()`, que aplica um pedido em linguagem natural a cada célula.

**Uso no experimento:** padronizar nomes de tratamentos digitados de formas diferentes, classificar observações de campo, reorganizar a planilha em formato longo.

**Como usar (se você tiver o plano):** abra a planilha, clique no ícone do Gemini no canto superior direito e faça o pedido; ou digite numa célula, por exemplo, `=AI("Padronize o nome do substrato em minúsculas, sem acento e com _", A2)` e arraste para as demais linhas.

**Sem o plano pago:** use o exercício *"Arrumando a planilha de campo"* (Capítulo 3) no Gemini app. O resultado é o mesmo, só que você baixa um CSV em vez de editar a planilha diretamente.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Skills portáteis

## O que é uma skill?

Uma **skill** é um **arquivo de texto com instruções** que ensina a IA a fazer uma tarefa do jeito certo, sempre. Pense nela como um **protocolo de laboratório** para a IA: quais perguntas fazer antes, que passos seguir, que testes rodar, como apresentar o resultado e o que **nunca** fazer.

O pacote do curso fica na pasta `skills/`:

| Arquivo | Para que serve |
|---|---|
| `00-assistente-estatistico/SKILL.md` | Skill "mãe": regras gerais e qual skill usar em cada caso |
| `01-planejamento-experimento/SKILL.md` | Escolher o delineamento, número de repetições, croqui casualizado e planilha modelo |
| `02-dic-dbc-anova-tukey/SKILL.md` | DIC e DBC: pressupostos, ANOVA, Tukey, CV |
| `03-fatorial-parcela-subdividida/SKILL.md` | Fatoriais, desdobramento e parcelas subdivididas |
| `04-regressao-doses/SKILL.md` | Tratamentos quantitativos: regressão e DMET |
| `05-interpretacao-relatorio/SKILL.md` | Texto de resultados, tabela com letras, legendas |
| `gem-unico.md` | **Todas as skills em um arquivo só**, pronto para colar num Gem |
| `README.md` | Como instalar em cada IA |

**Por que "portátil"?** Porque é só texto em Markdown. O mesmo arquivo funciona no Gemini, no ChatGPT, no Claude ou colado no início de qualquer conversa. Você não fica preso a uma empresa.

## Criando o seu Gem "Estatístico Agroflorestal"

1. Acesse <https://gemini.google.com>.
2. No menu lateral, clique em **Explorar Gems** (ou **Gems**) e depois em **Novo Gem**.
3. Em **Nome**, escreva: `Estatístico Agroflorestal`.
4. Abra o arquivo `skills/gem-unico.md` (no computador, use o Bloco de Notas; no Drive, abra com Google Docs), selecione tudo (`Ctrl + A`), copie (`Ctrl + C`) e cole (`Ctrl + V`) no campo **Instruções**.
5. Em **Conhecimento**, clique em **+** / **Adicionar arquivos** e anexe as skills individuais da pasta `skills/` (as que couberem), o dicionário de dados `dados/dicionario_dados.md` e, se quiser, um arquivo de dados de exemplo.
6. Use o painel de **pré-visualização** à direita para testar: envie `dic_mudas.csv` e escreva só *"analise este experimento"*.
7. Clique em **Salvar**. O Gem aparece no menu lateral para todas as próximas conversas.

**O que muda com o Gem:** repare que, com um pedido curto, o Gem **faz perguntas antes** (delineamento, variável resposta, repetições), testa os pressupostos, usa Tukey, mostra o código e avisa se algo estiver errado. É o prompt P-C-D-T-F "embutido".

> Se o campo de instruções reclamar do tamanho, cole apenas o conteúdo de `00-assistente-estatistico/SKILL.md` nas instruções e anexe as demais skills como arquivos de conhecimento.

## O mesmo arquivo em outras IAs

| IA | Onde colocar a skill | Observação |
|---|---|---|
| **Gemini** | Gem → Instruções + Conhecimento | gratuito, com limites |
| **ChatGPT** | Projeto → Instruções do projeto (e arquivos); ou GPT personalizado | criar GPT personalizado pode exigir plano pago |
| **Claude** | Projeto → Instruções e Conhecimento; ou *Configurações → Capacidades → Skills*, enviando a pasta da skill (o `SKILL.md` já está no formato aberto *Agent Skills*) | recursos variam com o plano |
| **Qualquer IA** | Cole o conteúdo de `gem-unico.md` como **primeira mensagem** da conversa e depois envie os dados | funciona em qualquer lugar |

Faça o teste: cole a mesma skill em duas IAs diferentes, envie o mesmo CSV e compare os resultados com o gabarito (as tabelas do Capítulo 6 e o Apêndice C). Se as duas concordarem com o gabarito, ótimo; se discordarem, você descobriu exatamente onde conferir.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Mão na massa no Gemini

Agora é a sua vez. Você já sabe organizar os dados (Capítulo 3), conhece as ferramentas do Gemini (Capítulo 4) e criou o seu Gem com as skills do curso (Capítulo 5). Para cada exercício:

1. Abra uma **conversa nova** no Gemini (<https://gemini.google.com>), clicando em "Nova conversa", ou abra o seu Gem "Estatístico Agroflorestal".
2. Clique no **+** (ou no ícone de clipe) ao lado da caixa de texto e envie o arquivo `.csv` indicado.
3. Cole o prompt, aperte Enter e espere a análise.
4. Compare a resposta com as tabelas de **"O que esperar"** e com o checklist do Apêndice B.

Cada exercício mostra primeiro **como os dados chegam**: as 3 primeiras linhas do arquivo, exatamente como estão no CSV (com **ponto** decimal, porque é assim que o arquivo é gravado). Depois, em **"O que esperar"**, vêm as tabelas de resultado no padrão ABNT/IBGE, com os números corretos calculados no R.

> **Dica:** o Gemini às vezes arredonda de forma diferente (34,57 ou 34,573). Diferenças na terceira casa decimal são normais. Diferenças em **GL, médias ou na conclusão** (significativo ou não) indicam erro.

## Como pedir as tabelas no padrão ABNT ao Gemini

Relatórios, TCCs e artigos brasileiros apresentam as tabelas no padrão da ABNT (NBR 14724), que segue as *Normas de apresentação tabular* do IBGE:

- o **título fica acima** da tabela: "Tabela N – Título descritivo";
- a **fonte e as notas ficam abaixo** ("Fonte: ..." e "Nota: ...");
- a tabela é **aberta nas laterais**: sem linhas verticais e com só **3 linhas horizontais** (acima do cabeçalho, abaixo do cabeçalho e no fim da tabela);
- na ANOVA, o F recebe a legenda de significância: `**` significativo a 1 %, `*` significativo a 5 % e `ns` não significativo;
- **vírgula decimal** e o **mesmo número de casas decimais** em toda a coluna.

Cole este pedido **depois** da análise (ou no fim de qualquer prompt dos exercícios):

```
Agora formate todas as tabelas de resultado no padrão ABNT/IBGE:
- título acima, no formato "Tabela N – Título descritivo (unidade)";
- abaixo da tabela, a linha "Fonte: dados fictícios do curso (2026)." e
  as notas;
- ANOVA com as colunas FV, GL, SQ, QM e F; marque o F com ** (p < 0,01),
  * (0,01 <= p < 0,05) ou ns (p >= 0,05) e explique a legenda na nota;
  informe o CV (%) na nota;
- tabela de médias com a letra do Tukey ao lado de cada média e a nota
  "Médias seguidas pela mesma letra na coluna não diferem entre si pelo
  teste de Tukey a 5 % de probabilidade.";
- vírgula como separador decimal, ponto como separador de milhar e o
  mesmo número de casas decimais em toda a coluna;
- nomes dos tratamentos por extenso, sem "_" (ex.: "Composto orgânico").
Entregue as tabelas em Markdown. Não recalcule nada: use os números da
análise que você já fez nesta conversa.
```

**As bordas no chat não ficam no padrão, e isso é normal.** No chat, toda tabela em Markdown aparece com **todas as bordas** (uma grade). O acabamento final é feito no editor de texto:

1. Na resposta do Gemini, clique em **Compartilhar e exportar** → **Exportar para o app Documentos** (Google Docs).
2. No Google Docs, selecione a tabela inteira e, em **Formatar → Tabela → Propriedades da tabela**, deixe a borda com **0 pt**.
3. Selecione a linha do cabeçalho e, no botão de bordas da barra de ferramentas, aplique borda **superior** e **inferior** (1 pt). Depois selecione a última linha e aplique borda **inferior**.
4. Pronto: sobram só as **3 linhas horizontais** (topo, abaixo do cabeçalho e fim da tabela), como nas tabelas desta apostila.

## Exercício 1: DIC, substratos para mudas de ipê

**Arquivo:** `dic_mudas.csv` (20 linhas)

**Como os dados chegam** (3 primeiras linhas do arquivo):

| `substrato` | `repeticao` | `altura_cm` | `diametro_mm` |
|-------------------|------------------:|------------------:|---------------------:|
| terra | 1 | 25.9 | 3.2 |
| terra | 2 | 23.1 | 3.26 |
| terra | 3 | 29.7 | 3.46 |

```
Atue como estatístico experimental em ciências agrárias.
Contexto: experimento em delineamento inteiramente casualizado (DIC)
com 5 substratos (tratamentos) e 4 repetições, avaliando a altura de
mudas de ipê-amarelo aos 120 dias.
Dados: arquivo anexo dic_mudas.csv, colunas substrato, repeticao,
altura_cm e diametro_mm. Analise apenas altura_cm.
Tarefa: execute código em Python para (1) testar a normalidade dos
resíduos (Shapiro-Wilk) e a homogeneidade de variâncias (Bartlett);
(2) fazer a ANOVA; (3) se F for significativo a 5%, aplicar Tukey a 5%;
(4) calcular o CV%.
Formato: tabela de ANOVA, tabela de médias em ordem decrescente com
letras do Tukey, CV%, e um parágrafo de interpretação.
Não invente valores. Ao final, mostre o código usado.
```

**O que esperar:**

: Tabela 1 – Análise de variância da altura de mudas de ipê-amarelo (cm) aos 120 dias, em função do substrato

| FV | GL | SQ | QM | F |
|--------------------|------------:|------------:|------------:|-------------------:|
| Substrato | 4 | 515,85 | 128,96 | 34,57\*\* |
| Resíduo | 15 | 55,95 | 3,73 | |
| Total | 19 | 571,81 | | |

::: {custom-style="Fonte da tabela"}
Fonte: dados fictícios do curso (2026).

Nota: CV = 6,10 %. \*\* significativo a 1 % de probabilidade pelo teste F.
:::

: Tabela 2 – Altura média de mudas de ipê-amarelo aos 120 dias, em função do substrato

| Substrato | Altura (cm) |
|-----------------------------------------------|------------------------------:|
| Composto orgânico | 37,40 a |
| Terra + esterco | 36,35 a |
| Comercial | 33,23 a |
| Terra | 26,48 b |
| Terra + areia | 24,98 b |

::: {custom-style="Fonte da tabela"}
Fonte: dados fictícios do curso (2026).

Nota: Médias seguidas pela mesma letra na coluna não diferem entre si pelo teste de Tukey a 5 % de probabilidade.
:::

- p-valor do F = 2,09 × 10⁻⁷.
- Shapiro-Wilk p = 0,807 (normal) e Bartlett p = 0,095 (homogêneo): pressupostos atendidos.

**Interpretação esperada:** composto orgânico, terra com esterco e substrato comercial não diferem entre si e produziram mudas mais altas do que terra pura e terra com areia.

**Desafio extra:** peça a mesma análise para `diametro_mm`.

## Exercício 2: DBC, cultivares de milho em aleias

**Arquivo:** `dbc_milho.csv` (20 linhas)

**Como os dados chegam** (3 primeiras linhas do arquivo):

| `bloco` | `cultivar` | `produtividade_kg_ha` |
|-------------:|---------------------|------------------------------------------:|
| 1 | BRS_Caimbe | 5603 |
| 2 | BRS_Caimbe | 5157 |
| 3 | BRS_Caimbe | 4835 |

Use o prompt "bom" do Capítulo 3 (seção *Exemplo ruim × exemplo bom*). Ele já está pronto para este arquivo.

**O que esperar:**

: Tabela 3 – Análise de variância da produtividade de milho (kg ha⁻¹) em aleias de gliricídia, em função da cultivar

| FV | GL | SQ | QM | F |
|---------------|----------:|------------------:|----------------:|----------------:|
| Cultivar | 4 | 10.099.915 | 2.524.979 | 34,69\*\* |
| Bloco | 3 | 1.688.272 | 562.757 | 7,73\*\* |
| Resíduo | 12 | 873.537 | 72.795 | |
| Total | 19 | 12.661.724 | | |

::: {custom-style="Fonte da tabela"}
Fonte: dados fictícios do curso (2026).

Nota: CV = 5,04 %. \*\* significativo a 1 % de probabilidade pelo teste F.
:::

: Tabela 4 – Produtividade média de cultivares de milho em aleias de gliricídia

| Cultivar | Produtividade (kg ha⁻¹) |
|---------------------------------|--------------------------------------------:|
| Híbrido comercial | 6.147 a |
| BRS Gorutuba | 6.130 a |
| BRS Caimbé | 5.213 b |
| AL Bandeirante | 4.974 b |
| Crioulo local | 4.291 c |

::: {custom-style="Fonte da tabela"}
Fonte: dados fictícios do curso (2026).

Nota: Médias seguidas pela mesma letra na coluna não diferem entre si pelo teste de Tukey a 5 % de probabilidade.
:::

- p-valores: cultivar 1,7 × 10⁻⁶; bloco 0,0039. Shapiro-Wilk p = 0,313 (normal).
- O efeito de bloco foi significativo: **o bloqueio foi útil** (as faixas de declive realmente diferiam).

**Atenção:**

- Se a IA mostrar **Resíduo com 15 GL**, ela esqueceu o bloco (analisou como DIC). Corrija: *"o bloco deve entrar no modelo como fator"*.
- O R (`ExpDes.pt`) testou a homogeneidade pelo teste de O'Neill-Mathews (p = 0,50). O Gemini provavelmente usará Bartlett ou Levene, com p-valor diferente; o importante é a conclusão (variâncias homogêneas).

## Exercício 3: fatorial 3 × 3, espécie × adubação

**Arquivo:** `fatorial_adubacao.csv` (36 linhas)

**Como os dados chegam** (3 primeiras linhas do arquivo):

| `especie` | `adubacao` | `repeticao` | `massa_seca_g` |
|----------------|------------------|-------------------:|------------------------:|
| angico | sem_adubo | 1 | 16.2 |
| angico | sem_adubo | 2 | 16.2 |
| angico | sem_adubo | 3 | 16.3 |

```
Atue como estatístico experimental em ciências agrárias.
Contexto: experimento fatorial 3 x 3 em DIC, com 4 repetições. Fator A:
espécie florestal (angico, aroeira, mogno_africano). Fator B: adubação
(sem_adubo, organico, mineral). Resposta: massa seca de mudas aos 6
meses (g).
Dados: arquivo anexo fatorial_adubacao.csv, colunas especie, adubacao,
repeticao, massa_seca_g.
Tarefa: execute código em Python para:
1. ajustar o modelo massa_seca_g ~ especie * adubacao e testar a
   normalidade dos resíduos (Shapiro-Wilk);
2. apresentar a ANOVA com os efeitos de espécie, adubação e interação;
3. se a interação for significativa a 5%, fazer o desdobramento:
   comparar as espécies dentro de cada adubação e as adubações dentro
   de cada espécie, com Tukey a 5%;
4. calcular o CV%.
Formato: tabela de ANOVA; tabela de dupla entrada (espécies nas linhas,
adubações nas colunas) com as médias, letras minúsculas comparando
espécies na coluna e letras maiúsculas comparando adubações na linha;
parágrafo de interpretação. Não invente valores; mostre o código.
```

**O que esperar:**

: Tabela 5 – Análise de variância da massa seca de mudas (g) aos 6 meses, em função da espécie florestal e da adubação

| FV | GL | SQ | QM | F |
|----------------------|----------:|--------------:|----------:|------------------:|
| Espécie (E) | 2 | 769,62 | 384,81 | 111,10\*\* |
| Adubação (A) | 2 | 367,60 | 183,80 | 53,06\*\* |
| E × A | 4 | 217,71 | 54,43 | 15,71\*\* |
| Resíduo | 27 | 93,52 | 3,46 | |
| Total | 35 | 1.448,45 | | |

::: {custom-style="Fonte da tabela"}
Fonte: dados fictícios do curso (2026).

Nota: CV = 8,55 %. \*\* significativo a 1 % de probabilidade pelo teste F.
:::

**A interação é significativa**, então é preciso desdobrar: o efeito da adubação depende da espécie. Shapiro-Wilk p = 0,50 (normal).

: Tabela 6 – Massa seca média de mudas (g) aos 6 meses, por espécie florestal e adubação

| Espécie | Sem adubo | Orgânico | Mineral |
|----------------------------|-----------------:|---------------:|---------------:|
| Angico | 16,03 bB | 26,03 aA | 23,43 bA |
| Aroeira | 15,48 bA | 17,13 bA | 15,58 cA |
| Mogno-africano | 20,23 aC | 28,33 aB | 33,60 aA |

::: {custom-style="Fonte da tabela"}
Fonte: dados fictícios do curso (2026).

Nota: Médias seguidas pela mesma letra minúscula na coluna (espécies dentro de cada adubação) e maiúscula na linha (adubações dentro de cada espécie) não diferem entre si pelo teste de Tukey a 5 % de probabilidade. Para aroeira, o efeito da adubação foi não significativo (F = 0,99; p = 0,385).
:::

**Interpretação esperada:** o mogno-africano respondeu mais à adubação mineral; o angico respondeu igualmente às adubações orgânica e mineral; a **aroeira não respondeu à adubação**.

**Atenção:** a IA às vezes interpreta os efeitos principais ("o mogno é a melhor espécie") **sem desdobrar** a interação. Com interação significativa, essa conclusão é incompleta. Se acontecer, peça o desdobramento.

## Exercício 4: parcela subdividida, café sombreado

**Arquivo:** `parcela_sub_cafe_sombra.csv` (36 linhas)

**Como os dados chegam** (3 primeiras linhas do arquivo):

| `bloco` | `sombreamento_pct` | `cultivar` | `produtividade_sc_ha` |
|---------:|------------------------:|--------------|----------------------------:|
| 1 | 0 | Catuai_144 | 28.6 |
| 1 | 0 | Arara | 30.6 |
| 1 | 0 | Topazio | 23.1 |

Este é o mais difícil, e serve justamente para mostrar onde a IA tropeça.

```
Atue como estatístico experimental em ciências agrárias.
Contexto: experimento em parcelas subdivididas no delineamento em
blocos casualizados (DBC), com 4 blocos. Parcela: sombreamento do
cafezal (0, 30 e 50%). Subparcela: cultivar de café (Catuai_144, Arara,
Topazio). Resposta: produtividade (sacas/ha).
Dados: arquivo anexo parcela_sub_cafe_sombra.csv, colunas bloco,
sombreamento_pct, cultivar, produtividade_sc_ha.
Tarefa: execute código em Python. ATENÇÃO: parcela subdividida tem
DOIS resíduos. O erro (a) = bloco x sombreamento testa o sombreamento;
o erro (b) testa cultivar e a interação.
1. Apresente a ANOVA com: sombreamento, bloco, erro (a), cultivar,
   sombreamento x cultivar, erro (b) e total, com GL, SQ, QM, F e p.
2. Calcule o CV da parcela (CV1) e da subparcela (CV2).
3. Se a interação for significativa, compare as cultivares dentro de
   cada sombreamento (Tukey 5%).
Formato: tabela de ANOVA, tabela de médias e parágrafo de
interpretação. Não invente valores; mostre o código.
```

**O que esperar:**

: Tabela 7 – Análise de variância da produtividade de café (sc ha⁻¹) em parcelas subdivididas, em função do sombreamento (parcela) e da cultivar (subparcela)

| FV | GL | SQ | QM | F |
|-----------------------------|----------:|----------:|----------:|---------------:|
| Sombreamento (S) | 2 | 121,72 | 60,86 | 6,48\* |
| Bloco | 3 | 123,36 | 41,12 | 4,38^ns^ |
| Erro (a) | 6 | 56,38 | 9,40 | |
| Cultivar (C) | 2 | 228,44 | 114,22 | 78,61\*\* |
| S × C | 4 | 34,68 | 8,67 | 5,97\*\* |
| Erro (b) | 18 | 26,15 | 1,45 | |
| Total | 35 | 590,73 | | |

::: {custom-style="Fonte da tabela"}
Fonte: dados fictícios do curso (2026).

Nota: CV1 (parcela) = 9,47 %; CV2 (subparcela) = 3,72 %. \*\* significativo a 1 % e \* significativo a 5 % de probabilidade pelo teste F; ^ns^ não significativo.
:::

: Tabela 8 – Produtividade média de cultivares de café (sc ha⁻¹) em cada nível de sombreamento

| Cultivar | 0 % | 30 % | 50 % |
|------------------------|----------------:|-------------------:|----------------:|
| Arara | 33,15 a | 35,75 a | 36,98 a |
| Catuaí 144 | 31,05 a | 34,63 ab | 32,28 b |
| Topázio | 25,45 b | 32,48 b | 29,50 c |

::: {custom-style="Fonte da tabela"}
Fonte: dados fictícios do curso (2026).

Nota: Médias seguidas pela mesma letra minúscula na coluna (cultivares dentro de cada sombreamento) não diferem entre si pelo teste de Tukey a 5 % de probabilidade. O efeito do sombreamento dentro da cultivar foi não significativo para Arara (p = 0,062) e Catuaí 144 (p = 0,083) e significativo para Topázio (p = 0,002); por ser um fator quantitativo, o sombreamento foi analisado por regressão.
:::

**Sombreamento dentro de Topázio:** resposta quadrática (ŷ = 25,45 + 0,4639x − 0,0077x²), com máxima produtividade perto de 30 % de sombra. Como o sombreamento tem apenas 3 níveis, a curva passa exatamente pelas 3 médias (R² = 1), então interprete com cautela.

**Atenção, o erro clássico:** se a IA fizer uma ANOVA comum, com um resíduo só (24 GL), o F do sombreamento vai dar perto de **17,7** em vez de **6,48**, porque ela testou a parcela com o erro errado. Isso faz o sombreamento parecer muito mais importante do que é. Esse é o tipo de erro que só quem confere percebe.

## Exercício 5: regressão, doses de nitrogênio no eucalipto

**Arquivo:** `doses_nitrogenio.csv` (20 linhas)

**Como os dados chegam** (3 primeiras linhas do arquivo):

| `dose_n_kg_ha` | `repeticao` | `volume_m3_ha` |
|---------------------------:|---------------------:|---------------------------:|
| 0 | 1 | 41.9 |
| 0 | 2 | 42.4 |
| 0 | 3 | 39.6 |

Quando o tratamento é **quantitativo** (doses), não faz sentido usar Tukey ("a dose 100 difere da 150?"). O correto é ajustar uma **curva de resposta**.

```
Atue como estatístico experimental em ciências agrárias.
Contexto: experimento em DIC com 5 doses de nitrogênio em cobertura
(0, 50, 100, 150 e 200 kg/ha) e 4 repetições, em eucalipto num sistema
ILPF. Resposta: volume de madeira (m³/ha).
Dados: arquivo anexo doses_nitrogenio.csv, colunas dose_n_kg_ha,
repeticao, volume_m3_ha.
Tarefa: execute código em Python para:
1. fazer a ANOVA tratando a dose como fator, com Shapiro-Wilk,
   Bartlett e CV%;
2. ajustar regressão linear e quadrática da média em função da dose,
   testar a significância de cada termo e o desvio da regressão;
3. escolher o modelo adequado e, se for quadrático, calcular a dose de
   máxima eficiência técnica (DMET = -b1 / (2*b2)) e o volume máximo.
Formato: tabela de ANOVA, equação ajustada com R², valor da DMET,
gráfico de pontos (médias) com a curva, e parágrafo de interpretação.
Não use teste de Tukey. Não invente valores; mostre o código.
```

**O que esperar:**

: Tabela 9 – Análise de variância, com desdobramento em regressão, do volume de madeira de eucalipto (m³ ha⁻¹) em função da dose de nitrogênio em cobertura

| FV | GL | SQ | QM | F |
|-------------------------------|--------:|-----------:|--------:|---------------:|
| Doses | 4 | 985,30 | 246,33 | 32,55\*\* |
| Efeito linear | 1 | 834,48 | 834,48 | 110,27\*\* |
| Efeito quadrático | 1 | 143,04 | 143,04 | 18,90\*\* |
| Desvios da regressão | 2 | 7,78 | 3,89 | 0,51^ns^ |
| Resíduo | 15 | 113,52 | 7,57 | |
| Total | 19 | 1.098,82 | | |

::: {custom-style="Fonte da tabela"}
Fonte: dados fictícios do curso (2026).

Nota: CV = 5,14 %. \*\* significativo a 1 % de probabilidade pelo teste F; ^ns^ não significativo.
:::

: Tabela 10 – Volume médio de madeira de eucalipto em função da dose de nitrogênio em cobertura

| Dose de N (kg ha⁻¹) | Volume (m³ ha⁻¹) |
|-----------------------------------------:|-----------------------------------:|
| 0 | 41,4 |
| 50 | 50,4 |
| 100 | 56,0 |
| 150 | 60,8 |
| 200 | 59,0 |

::: {custom-style="Fonte da tabela"}
Fonte: dados fictícios do curso (2026).

Nota: Por ser um fator quantitativo, as doses não foram comparadas por teste de médias; a resposta está descrita pela equação de regressão (Figura 1).
:::

::: {custom-style="Table Caption"}
Figura 1 – Volume de madeira de eucalipto (m³ ha⁻¹) em função da dose de nitrogênio em cobertura (kg ha⁻¹)
:::

> **O que o gráfico deve mostrar:** os 5 pontos das médias da Tabela 10 e a curva ajustada **ŷ = 41,16 + 0,2192x − 0,000639x²** (R² = 0,99), que sobe até a **DMET = 171,4 kg ha⁻¹** de N, onde o volume máximo estimado é **ŷmax ≈ 59,95 m³ ha⁻¹**, e cai levemente depois. Eixo x: "Dose de N (kg ha⁻¹)"; eixo y: "Volume (m³ ha⁻¹)"; equação e R² escritos dentro da área do gráfico. No padrão ABNT, o título vai **acima** da figura e **fora** da imagem, e a fonte vai abaixo.

::: {custom-style="Fonte da tabela"}
Fonte: dados fictícios do curso (2026).
:::

- p-valor do F das doses = 3,1 × 10⁻⁷. Shapiro-Wilk p = 0,569 e Bartlett p = 0,563: pressupostos atendidos.
- O modelo linear sozinho é significativo, mas deixa um **desvio da regressão significativo** (p = 0,0045): a reta não basta.
- No quadrático, o termo quadrático é significativo e os desvios **não** são (Tabela 9): **o quadrático é o modelo adequado**. O cúbico não acrescenta nada (p = 0,49).
- Equação: **ŷ = 41,16 + 0,2192x − 0,000639x²** (R² = 0,99); **DMET** (dose de máxima eficiência técnica) **= 171,4 kg ha⁻¹** de N; volume máximo estimado **ŷmax ≈ 59,95 m³ ha⁻¹**.

**Sobre o R²:** o `ExpDes.pt` calcula o R² sobre as **médias** dos tratamentos (R² = 0,99 no quadrático; 0,85 no linear). Se a IA ajustar a curva sobre as 20 parcelas individuais, o R² será menor (≈ 0,89), com a mesma equação. Os dois estão certos; só informe no relatório qual foi usado.

## Exercício 6: contagem de pragas, quando os pressupostos falham

**Arquivo:** `dic_contagem_pragas.csv` (24 linhas)

**Como os dados chegam** (3 primeiras linhas do arquivo):

| `manejo` | `repeticao` | `insetos_praga` |
|-------------------------|----------------------:|------------------------------:|
| convencional | 1 | 9 |
| convencional | 2 | 12 |
| convencional | 3 | 33 |

Dados de **contagem** (número de insetos) costumam ter variância que cresce com a média, o que viola a homogeneidade exigida pela ANOVA.

```
Atue como estatístico experimental em ciências agrárias.
Contexto: experimento em DIC com 4 manejos (convencional, pousio,
saf_simples, saf_biodiverso) e 6 repetições. Resposta: número de
insetos-praga por armadilha (contagem).
Dados: arquivo anexo dic_contagem_pragas.csv, colunas manejo,
repeticao, insetos_praga.
Tarefa: execute código em Python para:
1. calcular média e variância por manejo;
2. fazer a ANOVA e testar Shapiro-Wilk (resíduos) e Bartlett;
3. se algum pressuposto falhar, refazer a análise com a transformação
   raiz quadrada de (x + 0,5), testando os pressupostos de novo;
4. fazer também o teste não paramétrico de Kruskal-Wallis;
5. aplicar Tukey 5% na análise que for válida.
Formato: tabelas, CV% de cada análise, e um parágrafo explicando qual
análise deve ir para o relatório e por quê. Não invente valores;
mostre o código.
```

**O que esperar:**

: Tabela 11 – Análise de variância do número de insetos-praga por armadilha (dados originais), em função do manejo

| FV | GL | SQ | QM | F |
|----------------|-------------:|---------------:|-------------:|-----------------:|
| Manejo | 3 | 1.093,3 | 364,44 | 9,62\*\* |
| Resíduo | 20 | 758,0 | 37,90 | |
| Total | 23 | 1.851,3 | | |

::: {custom-style="Fonte da tabela"}
Fonte: dados fictícios do curso (2026).

Nota: CV = 52,03 %. \*\* significativo a 1 % de probabilidade pelo teste F. Teste de Bartlett: p = 0,020 (variâncias heterogêneas; pressuposto violado).
:::

: Tabela 12 – Análise de variância do número de insetos-praga por armadilha, com os dados transformados em √(x + 0,5), em função do manejo

| FV | GL | SQ | QM | F |
|----------------|-------------:|-------------:|-------------:|--------------------:|
| Manejo | 3 | 27,52 | 9,17 | 13,66\*\* |
| Resíduo | 20 | 13,43 | 0,67 | |
| Total | 23 | 40,95 | | |

::: {custom-style="Fonte da tabela"}
Fonte: dados fictícios do curso (2026).

Nota: CV = 25,14 %. \*\* significativo a 1 % de probabilidade pelo teste F. Teste de Bartlett: p = 0,497 (variâncias homogêneas).
:::

: Tabela 13 – Número médio de insetos-praga por armadilha, em função do manejo

| Manejo | Insetos-praga por armadilha |
|---------------------------|--------------------------------------------------:|
| Convencional | 21,17 a |
| Pousio | 13,83 ab |
| SAF simples | 9,83 b |
| SAF biodiverso | 2,50 c |

::: {custom-style="Fonte da tabela"}
Fonte: dados fictícios do curso (2026).

Nota: Médias originais (sem transformação). A análise foi feita com os dados transformados em √(x + 0,5); médias seguidas pela mesma letra na coluna não diferem entre si pelo teste de Tukey a 5 % de probabilidade, aplicado aos dados transformados.
:::

- Shapiro-Wilk: p = 0,834 nos dados originais e p = 0,506 nos transformados (normal nos dois casos). O problema era a **homogeneidade**.
- Média (variância) por manejo: convencional 21,17 (97,4); pousio 13,83 (18,6); SAF simples 9,83 (31,4); SAF biodiverso 2,50 (4,3). Veja como a variância acompanha a média.
- **Kruskal-Wallis:** H = 15,20; GL = 3; **p = 0,0017** (mesma conclusão: os manejos diferem).

**Interpretação esperada:** os dados originais violam a homogeneidade de variâncias; a transformação resolveu o problema e a análise transformada (ou o Kruskal-Wallis) é a que deve ser relatada. O SAF biodiverso teve menos pragas que todos os outros manejos. Note que, nos dados originais, o Tukey dá `bc` para SAF simples; depois da transformação, ele passa a `b`. **A conclusão pode mudar quando você respeita os pressupostos.**

**Atenção:** uma boa IA **avisa sozinha** que o pressuposto falhou. Se ela fizer a ANOVA nos dados originais e seguir em frente sem comentar o Bartlett, isso é sinal de que você precisa conferir com mais cuidado.

## Exercício 7: planeje o seu próprio experimento

Para fechar, use a skill de planejamento (`01-planejamento-experimento`, já incluída no `gem-unico.md`) para desenhar um experimento **seu**, real ou imaginado.

No seu Gem (criado no Capítulo 5) ou colando a skill no chat, escreva:

```
Quero planejar um experimento. Minha ideia: [descreva em 2 ou 3 frases:
o que quer comparar, em que cultura/espécie, onde será feito e o que
pretende medir].
Restrições: [área disponível, número de mudas/plantas, tempo, se o
terreno é desuniforme (declive, sombra, solo variável)].
Faça as perguntas necessárias, uma de cada vez. No final, me entregue:
1. o delineamento recomendado e a justificativa;
2. o número de tratamentos, de repetições e o total de parcelas, com o
   número de graus de liberdade do resíduo;
3. o croqui casualizado (sorteio feito com código, mostrando a semente
   usada);
4. a planilha modelo em formato longo, vazia, para eu anotar os dados
   no campo (CSV para baixar);
5. a análise estatística que deverá ser feita depois da coleta.
```

**Para conferir o planejamento:**

- O resíduo tem **pelo menos 10 a 12 GL**? Menos do que isso deixa o teste F pouco sensível.
- Se o terreno é desuniforme, a IA sugeriu **blocos (DBC)**?
- Se há dois fatores, ela explicou a diferença entre **fatorial** e **parcela subdividida** e por que escolheu um deles?
- O sorteio foi feito **com código** (e não "de cabeça")?
- A planilha modelo tem **1 linha por parcela**?

Exemplos de ideia para quem não tem um experimento em mente:

- comparar 4 tipos de cobertura morta no crescimento de mudas de cacau num SAF;
- testar 5 doses de pó de rocha em mudas de baru no viveiro;
- avaliar 3 espaçamentos e 2 espécies de adubo verde em aleias.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Ética e boas práticas

## Nunca invente dados

A IA consegue gerar uma planilha "realista" em segundos. Usar dados gerados por IA (ou "completar" parcelas perdidas com valores inventados) como se fossem medidos é **fabricação de dados**, uma das faltas mais graves na pesquisa científica.

- Dados simulados (como os deste curso) servem **só para treinar**, e devem ser identificados como simulados.
- Parcela perdida é **perdida**: registre como `NA` e analise como experimento desbalanceado. Se for preciso estimar a parcela, use um método estatístico reconhecido e **declare** isso no texto.
- Nunca peça à IA para "ajustar" dados até dar significativo.

## Confira cada resultado

- Use o **checklist do Apêndice B** em toda análise.
- Para trabalhos que vão ser publicados ou defendidos, **refaça a análise em outro programa** (R, SISVAR, Colab) e veja se bate.
- Guarde o **código** que gerou cada resultado (copie do Gemini para um documento ou use o Colab).
- **Confira as referências bibliográficas** sugeridas pela IA, uma por uma.

## Declare o uso de IA

Revistas, programas de pós-graduação e a própria UFVJM têm adotado regras para o uso de IA. O princípio geral é: **a IA não é autora, mas o seu uso deve ser declarado**. Verifique as normas da revista ou do programa.

Exemplo de frase para a seção de **Material e Métodos**:

> "As análises estatísticas foram conduzidas com o auxílio do assistente de inteligência artificial Gemini (Google; acesso em outubro de 2026), que gerou e executou código em Python (bibliotecas pandas, statsmodels e scipy). Os dados foram submetidos aos testes de Shapiro-Wilk e Bartlett, à análise de variância e, quando significativa, ao teste de Tukey a 5 % de probabilidade. Todos os resultados foram conferidos pelos autores no software R, com o pacote ExpDes.pt."

Se a IA ajudou na **redação**, isso também deve ser declarado (geralmente nos agradecimentos ou numa nota), conforme a norma da revista.

## Privacidade e proteção de dados

- **Não envie dados pessoais** (nome, CPF, telefone de agricultores, localização exata de propriedades) para a IA. Substitua por códigos (`produtor_01`).
- **Dados ainda não publicados** ou com sigilo (parcerias com empresas, patentes): verifique o acordo antes de enviá-los. Na versão gratuita do Gemini com conta pessoal, as conversas podem ser revisadas e usadas para melhorar o serviço, a menos que você desative a atividade em *Configurações → Atividade*.
- Contas institucionais (Workspace for Education) costumam ter **proteções de dados mais fortes**; quando disponível, prefira a conta `@ufvjm.edu.br` para dados de pesquisa.
- Respeite a **LGPD** e o comitê de ética, quando houver pessoas envolvidas na pesquisa (entrevistas, questionários).

## Resumo das boas práticas

1. Organize os dados em formato longo, em CSV.
2. Escreva o prompt com Papel, Contexto, Dados, Tarefa e Formato de saída.
3. Exija que a IA **rode código** e **mostre o código**.
4. Confira com o checklist.
5. Declare o uso de IA.
6. Nunca invente nem "ajuste" dados.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Apêndice A: Glossário {-}

**ANOVA (análise de variância):** método que divide a variação total dos dados em partes (tratamentos, blocos, resíduo) para testar se as médias dos tratamentos diferem.

**Bartlett (teste de):** testa se as variâncias dos tratamentos são homogêneas (iguais). Se p < 0,05, as variâncias são **heterogêneas** e um pressuposto da ANOVA foi violado. Alternativas: Levene, O'Neill-Mathews.

**CV (coeficiente de variação):** precisão do experimento, em %: CV = √QMresíduo / média geral × 100. Em experimentos de campo, valores até cerca de 10 a 20 % costumam ser considerados bons, mas a referência depende da cultura e da variável.

**DBC (delineamento em blocos casualizados):** as parcelas são agrupadas em **blocos** homogêneos (mesmo declive, mesma faixa de solo, mesmo dia de avaliação) e cada bloco recebe todos os tratamentos, sorteados dentro dele. Usado quando a área é desuniforme.

**DIC (delineamento inteiramente casualizado):** os tratamentos são sorteados entre todas as parcelas, sem restrição. Usado quando as condições são uniformes, como em viveiro ou laboratório.

**Desdobramento:** quando a interação é significativa, estuda-se um fator **dentro de cada nível** do outro (por exemplo, comparar as espécies separadamente em cada adubação).

**F (estatística F):** razão entre o QM do tratamento e o QM do resíduo. Quanto maior, maior a evidência de diferença entre tratamentos.

**GL (graus de liberdade):** número de informações independentes usadas em cada fonte de variação. No DIC: tratamentos = t − 1; resíduo = t(r − 1); total = tr − 1. Conferir os GL é a forma mais rápida de ver se a IA usou o modelo certo.

**Interação:** quando o efeito de um fator **depende** do nível do outro fator. Exemplo: o mogno responde muito ao adubo mineral, a aroeira não responde.

**Kruskal-Wallis (teste de):** alternativa **não paramétrica** à ANOVA de um fator (DIC); compara os tratamentos usando a ordem (postos) dos dados, sem exigir normalidade nem homogeneidade.

**DMET (dose de máxima eficiência técnica):** dose que produz a maior resposta numa curva quadrática: DMET = −b₁ / (2b₂). Não considera custos (para isso existe a máxima eficiência econômica).

**p-valor:** probabilidade de observar um resultado tão extremo quanto o obtido **se não houvesse efeito** dos tratamentos. Se p < 0,05, dizemos que o efeito é significativo a 5 %.

**Parcela (unidade experimental):** a menor unidade que recebe um tratamento e é medida: um vaso, uma linha de plantio, um grupo de árvores. Em parcela subdividida, a parcela é dividida em **subparcelas** que recebem um segundo fator.

**QM (quadrado médio):** soma de quadrados dividida pelos graus de liberdade (QM = SQ / GL). É uma estimativa de variância.

**Regressão:** ajuste de uma equação (reta, curva quadrática) que descreve como a resposta muda com um fator **quantitativo** (dose, espaçamento, idade).

**Repetição:** cada vez que um tratamento aparece no experimento. Mais repetições aumentam a precisão e os GL do resíduo.

**Shapiro-Wilk (teste de):** testa se os **resíduos** seguem distribuição normal. Se p < 0,05, a normalidade foi violada.

**Transformação de dados:** aplicar uma função aos dados (raiz quadrada, logaritmo, arco-seno) para corrigir falta de normalidade ou de homogeneidade. Para contagens, usa-se muito √(x + 0,5).

**Tratamento:** cada condição que está sendo comparada no experimento (um substrato, uma cultivar, uma dose, uma combinação espécie × adubo).

**Tukey (teste de):** compara todas as médias duas a duas, controlando o erro. Médias seguidas da **mesma letra** não diferem entre si.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Apêndice B: Checklist "Conferindo a resposta da IA" {-}

Marque cada item antes de usar qualquer resultado:

- [ ] **1. A IA rodou código?** Há um bloco de código e a saída do programa, e não só texto?
- [ ] **2. Leu o arquivo certo?** O número de linhas bate com o experimento (tratamentos × repetições)?
- [ ] **3. Modelo correto?** O delineamento (DIC, DBC, fatorial, parcela subdividida) é o que você descreveu? O bloco entrou no modelo?
- [ ] **4. Fatores como categoria?** Tratamento e bloco foram tratados como fator (e não como número), exceto doses na regressão?
- [ ] **5. GL conferem?** Calcule você mesmo os GL de tratamento, bloco e resíduo (veja o Glossário) e compare.
- [ ] **6. Médias conferem?** Calcule a média de pelo menos um tratamento (no Excel ou na calculadora) e compare.
- [ ] **7. Pressupostos testados?** Normalidade dos resíduos e homogeneidade das variâncias foram testadas, e a IA comentou o resultado?
- [ ] **8. Teste adequado?** Tukey para tratamentos qualitativos; regressão para quantitativos; desdobramento se houver interação significativa; dois resíduos em parcela subdividida.
- [ ] **9. A conclusão bate com os números?** "Significativo" só com p < 0,05; letras iguais = médias que não diferem.
- [ ] **10. Nada inventado?** Nenhuma referência, valor ou parcela perdida foi "criado". Pedi o código e guardei para reproduzir.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Apêndice C: Gabarito dos exercícios {-}

Resultados de referência calculados no R 4 com o pacote `ExpDes.pt` (script `notebooks/analise_exemplos.R`; saída completa em `dados/gabarito_resultados.txt`). Significância a 5 %.

**As tabelas de ANOVA e de médias estão no Capítulo 6**, já no padrão ABNT, para não repeti-las aqui:

| Exercício | Tabelas no Capítulo 6 |
|---|---|
| 1. DIC mudas (altura) | Tabela 1 (ANOVA) e Tabela 2 (Tukey) |
| 2. DBC milho | Tabela 3 (ANOVA) e Tabela 4 (Tukey) |
| 3. Fatorial espécie × adubação | Tabela 5 (ANOVA) e Tabela 6 (desdobramento) |
| 4. Parcela subdividida, café | Tabela 7 (ANOVA) e Tabela 8 (cultivares em cada sombreamento) |
| 5. Doses de N | Tabela 9 (ANOVA com regressão), Tabela 10 (médias) e Figura 1 |
| 6. Pragas | Tabelas 11 e 12 (ANOVA original e transformada) e Tabela 13 (médias) |

Este apêndice traz os detalhes que não cabem nas tabelas: p-valores exatos, pressupostos e modelos de regressão.

## p-valores do teste F {-}

| Exercício | Fonte de variação | F | p-valor |
|---|---|---:|---:|
| 1. DIC mudas | Substrato | 34,57 | 2,09 × 10⁻⁷ |
| 2. DBC milho | Cultivar | 34,69 | 1,7 × 10⁻⁶ |
| | Bloco | 7,73 | 0,0039 |
| 3. Fatorial | Espécie | 111,10 | < 0,0001 |
| | Adubação | 53,06 | 4,4 × 10⁻¹⁰ |
| | Espécie × Adubação | 15,71 | 9,3 × 10⁻⁷ |
| 4. Parcela subdividida | Sombreamento | 6,48 | 0,0317 |
| | Bloco | 4,38 | 0,0590 |
| | Cultivar | 78,61 | < 2,2 × 10⁻¹⁶ |
| | Sombreamento × Cultivar | 5,97 | 0,0031 |
| 5. Doses de N | Doses | 32,55 | 3,1 × 10⁻⁷ |
| | Desvios da regressão (quadrático) | 0,51 | 0,608 |
| 6. Pragas, originais | Manejo | 9,62 | 0,00039 |
| 6. Pragas, √(x + 0,5) | Manejo | 13,66 | 4,5 × 10⁻⁵ |
| 6. Pragas, Kruskal-Wallis | Manejo | H = 15,20 | 0,0017 |

*Observação: na saída do `ExpDes.pt` para o fatorial, a coluna QM aparece com valores incorretos de exibição (4, 2, 5, 3); os QM corretos (SQ/GL) estão na Tabela 5 e conferem com o F mostrado.*

## Pressupostos {-}

| Exercício | Shapiro-Wilk (p) | Homogeneidade (p) | Conclusão |
|---|---:|---:|---|
| 1. DIC mudas | 0,807 | 0,0946 (Bartlett) | atendidos |
| 2. DBC milho | 0,313 | 0,503 (O'Neill-Mathews) | atendidos |
| 3. Fatorial | 0,500 | não avaliado | normalidade atendida |
| 5. Doses de N | 0,569 | 0,563 (Bartlett) | atendidos |
| 6. Pragas, originais | 0,834 | **0,0198 (Bartlett)** | **homogeneidade violada** |
| 6. Pragas, √(x + 0,5) | 0,506 | 0,497 (Bartlett) | atendidos |

## Detalhes dos testes de médias {-}

**Exercício 3, desdobramento:** adubação dentro de aroeira, F = 0,99; p = 0,385 (não significativo).

**Exercício 4, sombreamento dentro de cultivar:** Arara p = 0,062 (ns); Catuaí 144 p = 0,083 (ns); Topázio p = 0,002, quadrático ŷ = 25,4500 + 0,4639x − 0,0077x².

**Exercício 6, pragas:** médias na escala transformada √(x + 0,5): convencional 4,54 a; pousio 3,75 ab; SAF simples 3,12 b; SAF biodiverso 1,62 c (são essas as letras usadas na Tabela 13). Se o Tukey for aplicado aos dados originais (o que não é correto, porque a homogeneidade foi violada), SAF simples recebe `bc` em vez de `b`.

## Regressão (Exercício 5) {-}

| Modelo | Equação | R² (médias) | Termo de maior grau (p) | Desvio da regressão (p) |
|----------|------------------------------------|--------:|----------:|---------------:|
| Linear | ŷ = 44,3550 + 0,0914x | 0,8469 | < 0,0001 | 0,0045 (significativo) |
| Quadrático | ŷ = 41,1586 + 0,2192x − 0,00063929x² | 0,9921 | 0,0006 | 0,608 (não significativo) |
| Cúbico | ŷ = 41,4686 + 0,1748x − 0,00002x² − 0,000002x³ | 0,9960 | 0,487 | 0,482 |

**Modelo escolhido: quadrático.** DMET (dose de máxima eficiência técnica): **171,4 kg ha⁻¹ de N**, com volume máximo estimado de **59,95 m³ ha⁻¹**.

---

*Bom trabalho e bons experimentos!*
