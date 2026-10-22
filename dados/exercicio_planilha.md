# Exercício: organizar uma planilha de campo com o Gemini

**Arquivo:** `planilha_campo_baguncada.xlsx`
**Tempo sugerido:** 15 a 20 minutos
**Objetivo:** transformar uma planilha "do jeito que veio do campo" em uma planilha **pronta para análise** (formato longo), usando IA, e **conferir** se a IA fez certo.

---

## 1. Conheça o problema

Abra o arquivo. Ele traz a altura (cm) de mudas de ipê-amarelo em 5 substratos, com 4 repetições:

| Substrato usado | Rep 1 (cm) | Rep 2 (cm) | Rep 3 (cm) | Rep 4 (cm) |
|---|---|---|---|---|
| comercial␣ | 33,0 | 33,7 | 32,8 | 33,4 |
| Composto Orgânico | 40,7 | 37,1 | perdida | 36,0 |
| Terra | 25,9 | 23,1 | 29,7 | 27,2 |
| terra + areia | 27,2 | 22,7 | 23,7 | 26,3 |
| Terra c/ esterco | 35,3 | 37,9 | 35,8 | 36,4 |

Antes de usar a IA, tente achar **5 problemas** sozinho. Resposta:

1. **Formato largo:** as repetições estão em colunas. Programas de estatística (R, Python, SISVAR, a própria IA) querem **formato longo**: 1 linha = 1 parcela.
2. **Nomes de colunas ruins:** espaços, acentos, parênteses e unidade dentro do nome (`Rep 1 (cm)`).
3. **Nomes de tratamentos despadronizados:** maiúsculas e minúsculas misturadas, espaço sobrando no fim de `comercial `, símbolos (`+`, `c/`) e acento.
4. **Vírgula decimal gravada como texto:** `33,0` não é número para a maioria dos programas, e a planilha guarda esses valores como texto.
5. **Valor faltante escrito como palavra:** `perdida`. O certo é deixar a **célula vazia** (ou `NA`). **Nunca** coloque zero: zero é um dado e puxaria a média para baixo.

---

## 2. Escolha o caminho

### Caminho gratuito (recomendado no curso): app do Gemini

O **painel lateral do Gemini dentro do Google Planilhas** (e a função `=AI()`) **exige plano pago** (Google AI Pro/Ultra ou Google Workspace com Gemini). **Com uma conta Google gratuita, use o app do Gemini:**

1. Acesse **gemini.google.com** com sua conta Google.
2. Clique em **+** (Adicionar arquivos) → **Fazer upload de arquivos** e escolha `planilha_campo_baguncada.xlsx`. (Se preferir, suba antes o arquivo para o Google Drive e use **+ → Drive**.)
3. Cole os prompts da seção 3, um de cada vez.
4. Peça o resultado como **tabela** e como **CSV** e copie para o Google Planilhas (ou baixe o arquivo, se o Gemini oferecer o download).

### Caminho com plano pago ou Workspace com Gemini: dentro do Planilhas

1. Abra o arquivo no Google Planilhas (**Arquivo → Importar → Fazer upload**).
2. Clique no ícone do **Gemini** (✦) no canto superior direito para abrir o painel lateral.
3. Use os mesmos prompts. O painel pode criar uma **nova aba** com a tabela organizada.

> Dica: **nunca apague a aba original**. Peça sempre para a IA criar o resultado em uma aba ou arquivo novo, para poder comparar.

---

## 3. Prompts prontos (copie e cole)

**Prompt 1: diagnóstico (antes de mexer em nada)**
```
Você é um técnico de pesquisa que organiza dados experimentais. Analise a planilha anexada, que traz a altura de mudas de ipê (cm) em 5 substratos com 4 repetições, em delineamento inteiramente casualizado. NÃO altere nada ainda. Liste todos os problemas que impedem a análise estatística (formato, nomes de colunas, nomes de tratamentos, separador decimal, valores faltantes ou estranhos) e diga como corrigir cada um.
```

**Prompt 2: converter para formato longo e limpar**
```
Agora reorganize os dados em formato longo (1 linha = 1 parcela), com exatamente 3 colunas:
- substrato: nomes padronizados, em minúsculas, sem acentos, sem espaços (use _), assim: comercial, composto_organico, terra, terra_areia, terra_esterco
- repeticao: número inteiro de 1 a 4 (tirado do nome da coluna "Rep X")
- altura_cm: número com PONTO como separador decimal
O valor "perdida" deve virar célula vazia (NA). Não invente nem estime esse valor e não coloque zero. Não altere nenhum outro número. Mostre a tabela final com as 20 linhas e me dê também o conteúdo em formato CSV.
```

**Prompt 3: relatório de conferência**
```
Faça uma conferência da tabela que você gerou: (1) quantas linhas tem; (2) quantas repetições há por substrato; (3) quantos valores faltantes existem e onde; (4) a média de altura por substrato, ignorando o faltante. Compare com a planilha original e confirme que nenhum número foi alterado além da troca de vírgula por ponto.
```

**Prompt 4 (opcional): já analisar**
```
Com a tabela organizada, faça a ANOVA (DIC) da altura em função do substrato, teste os pressupostos (Shapiro-Wilk e Bartlett), calcule o CV% e aplique Tukey a 5%. Atenção: há uma parcela perdida, então o substrato composto_organico tem 3 repetições. Explique como isso afeta a análise e mostre o código que você usou.
```

---

## 4. O que conferir depois (checklist)

Marque cada item. **Se algum falhar, corrija a IA no próprio chat** (ex.: "Você trocou o valor X, refaça mantendo os números originais").

- [ ] A tabela tem **20 linhas** e **3 colunas** (`substrato`, `repeticao`, `altura_cm`).
- [ ] Existem exatamente **5 substratos**, escritos de forma idêntica em todas as linhas (sem `comercial ` com espaço, sem `Terra` com maiúscula).
- [ ] Cada substrato tem repetições **1, 2, 3 e 4**.
- [ ] Os números usam **ponto** decimal e são reconhecidos como número (no Planilhas, ficam alinhados à direita).
- [ ] Há **1 valor faltante** (composto_organico, repetição 3), como **célula vazia/NA**, e **não** como 0, nem como média, nem como "perdida".
- [ ] Nenhum número mudou. Confira por amostragem: terra rep 2 = **23.1**; terra_areia rep 1 = **27.2**; terra_esterco rep 4 = **36.4**.
- [ ] Médias por substrato (sem o faltante): comercial **33,225**; composto_organico **37,933**; terra **26,475**; terra_areia **24,975**; terra_esterco **36,350**.

**Se você rodou o Prompt 4**, os valores de referência (19 parcelas) são: ANOVA **F ≈ 33,40**, **p ≈ 5 × 10⁻⁷**, **CV ≈ 6,2%**, com 4 GL de tratamento e **14 GL de resíduo** (e não 15, porque uma parcela foi perdida). Se a IA mostrar 15 GL no resíduo, ela provavelmente **inventou** o valor faltante ou o trocou por zero.

> Para comparar: com os 20 dados completos (arquivo `dic_mudas.csv`, onde o valor "perdido" é 35,8), o resultado é F = 34,57 e CV = 6,1%.

---

## 5. Para discutir com a turma

- Por que **não** se deve preencher o valor perdido com zero ou com a média, sem avisar?
- O que muda numa análise **desbalanceada** (repetições diferentes entre tratamentos)?
- Como montar a planilha de campo **já no formato longo**, para não precisar desse trabalho? (Veja a planilha modelo da skill de planejamento.)
- A IA errou alguma coisa? Qual pedido no prompt evitou (ou evitaria) o erro?
