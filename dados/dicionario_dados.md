# Dicionário de dados: curso "IA para Estatística Experimental" (Inova Agroflorestal, UFVJM)

Todos os conjuntos são **fictícios**, simulados com semente fixa pelo script `gerar_dados.py` para fins didáticos. Eles imitam situações reais de pesquisa agroflorestal.

**Formato:** todos (exceto a planilha bagunçada) estão em **formato longo**, em que **1 linha = 1 parcela (unidade experimental)**. Cada arquivo existe em `.csv` (separador vírgula, decimal ponto) e em `.xlsx`, com o mesmo conteúdo.

**Resultados esperados:** os números abaixo vêm do gabarito em R (`gabarito_resultados.txt`, gerado por `notebooks/analise_exemplos.R` com o pacote `ExpDes.pt`). O notebook `notebooks/analise_exemplos.ipynb` reproduz os mesmos valores em Python. Use-os para **conferir o que a IA responder**.

---

## 1. `dic_mudas`: substratos para mudas de ipê-amarelo

| Item | Descrição |
|---|---|
| Delineamento | Inteiramente casualizado (DIC) |
| Tratamentos | 5 substratos: `terra`, `terra_esterco`, `comercial`, `composto_organico`, `terra_areia` |
| Repetições | 4 por substrato (20 parcelas) |
| Contexto | Produção de mudas de ipê-amarelo (*Handroanthus* sp.) em viveiro para plantio em sistemas agroflorestais (SAF). Viveiro = ambiente homogêneo, por isso DIC. |

| Coluna | Tipo | Unidade | Descrição |
|---|---|---|---|
| `substrato` | texto (fator) | – | Substrato usado no tubete/saco |
| `repeticao` | inteiro | – | Número da repetição (1 a 4) |
| `altura_cm` | decimal | cm | Altura da muda aos 120 dias (**variável resposta principal**) |
| `diametro_mm` | decimal | mm | Diâmetro do coleto aos 120 dias (resposta secundária, para exercícios extras) |

**Resultado esperado (altura_cm):**
- ANOVA: F = 34,57; p = 2,1 × 10⁻⁷ (efeito significativo de substrato). CV = 6,1%.
- Pressupostos OK: Shapiro-Wilk p = 0,807; Bartlett p = 0,095.
- Tukey 5%: composto_organico (37,40) **a**, terra_esterco (36,35) **a**, comercial (33,23) **a**, terra (26,48) **b**, terra_areia (24,98) **b**.

**Objetivo didático:** primeiro exemplo, o caso "de livro". Ensina a ler o quadro da ANOVA, o CV, os pressupostos e as letras do Tukey.

---

## 2. `dbc_milho`: cultivares de milho em aleias de gliricídia

| Item | Descrição |
|---|---|
| Delineamento | Blocos casualizados (DBC) |
| Tratamentos | 5 cultivares: `BRS_Caimbe`, `AL_Bandeirante`, `BRS_Gorutuba`, `Crioulo_local`, `Hibrido_comercial` |
| Blocos | 4 (faixas do terreno com declives diferentes); 20 parcelas |
| Contexto | Cultivo em aleias (*alley cropping*): milho nas entrelinhas de gliricídia (*Gliricidia sepium*), adubo verde. O terreno tem declive, o que justifica o uso de blocos. |

| Coluna | Tipo | Unidade | Descrição |
|---|---|---|---|
| `bloco` | inteiro (fator) | – | Bloco/faixa de declive (1 a 4) |
| `cultivar` | texto (fator) | – | Cultivar de milho |
| `produtividade_kg_ha` | inteiro | kg/ha | Produtividade de grãos (**resposta**) |

**Resultado esperado:**
- ANOVA: cultivar F = 34,69, p = 1,7 × 10⁻⁶; bloco F = 7,73, p = 0,0039. CV = 5,04%.
- Shapiro-Wilk p = 0,313. Homogeneidade OK (o `ExpDes.pt` usa O'Neill-Mathews, p = 0,50; Bartlett também não rejeita).
- Tukey 5%: Hibrido_comercial (6147) **a**, BRS_Gorutuba (6130) **a**, BRS_Caimbe (5213) **b**, AL_Bandeirante (4974) **b**, Crioulo_local (4291) **c**.

**Objetivo didático:** mostrar o papel do **bloco** (controle local). O bloco foi significativo, ou seja, valeu a pena usar blocos. Armadilha comum: rodar Tukey "simples" (ex.: `pairwise_tukeyhsd`) que ignora os blocos e usa o erro errado.

---

## 3. `fatorial_adubacao`: espécie florestal × adubação

| Item | Descrição |
|---|---|
| Delineamento | Fatorial 3 × 3 em DIC |
| Fatores | `especie` (angico, aroeira, mogno_africano) × `adubacao` (sem_adubo, organico, mineral) |
| Repetições | 4 por combinação (36 parcelas/vasos) |
| Contexto | Crescimento inicial de espécies arbóreas usadas em SAF e recomposição, sob diferentes adubações de plantio, em casa de vegetação. |

| Coluna | Tipo | Unidade | Descrição |
|---|---|---|---|
| `especie` | texto (fator A) | – | Espécie florestal |
| `adubacao` | texto (fator B) | – | Tipo de adubação |
| `repeticao` | inteiro | – | Repetição (1 a 4) |
| `massa_seca_g` | decimal | g | Massa seca total da planta aos 6 meses (**resposta**) |

**Resultado esperado:**
- ANOVA: espécie F = 111,10 (p < 10⁻¹³); adubação F = 53,06 (p = 4,4 × 10⁻¹⁰); **interação F = 15,71 (p = 9,3 × 10⁻⁷)**. CV = 8,55%. Shapiro p = 0,50.
- Desdobramento (QM resíduo = 3,464, 27 GL):
  - Espécie dentro de mineral: F = 94,32. mogno (33,60) **a**, angico (23,43) **b**, aroeira (15,58) **c**.
  - Espécie dentro de orgânico: F = 40,41. mogno (28,33) **a**, angico (26,03) **a**, aroeira (17,13) **b**.
  - Espécie dentro de sem adubo: F = 7,80. mogno (20,23) **a**, angico (16,03) **b**, aroeira (15,48) **b**.
  - Adubação dentro de angico: F = 31,09. orgânico **a**, mineral **a**, sem adubo **b**.
  - **Adubação dentro de aroeira: F = 0,99, p = 0,385 (não significativo)**.
  - Adubação dentro de mogno: F = 52,42. mineral **a**, orgânico **b**, sem adubo **c**.

**Objetivo didático:** **interação** e **desdobramento**. Com interação significativa, não existe "melhor adubo" geral: o mogno responde muito ao mineral e a aroeira não responde. Gráfico de interação com linhas que não são paralelas.

> Observação: no gabarito do `ExpDes.pt`, a coluna QM do quadro principal do fatorial sai impressa com valores errados (falha de formatação do pacote). Os F e p estão corretos.

---

## 4. `parcela_sub_cafe_sombra`: sombreamento × cultivar de café

| Item | Descrição |
|---|---|
| Delineamento | **Parcelas subdivididas** em DBC |
| Parcela (fator A) | `sombreamento_pct`: 0, 30 e 50% de sombra por árvores |
| Subparcela (fator B) | `cultivar`: Catuai_144, Arara, Topazio |
| Blocos | 4 (36 subparcelas) |
| Contexto | Café arborizado (SAF cafeeiro). O sombreamento só pode ser aplicado em áreas grandes (parcelas); as cultivares são plantadas dentro de cada parcela (subparcelas). |

| Coluna | Tipo | Unidade | Descrição |
|---|---|---|---|
| `bloco` | inteiro (fator) | – | Bloco (1 a 4) |
| `sombreamento_pct` | inteiro (fator quantitativo) | % de sombra | Nível de sombreamento da parcela |
| `cultivar` | texto (fator) | – | Cultivar de café da subparcela |
| `produtividade_sc_ha` | decimal | sacas de 60 kg/ha | Produtividade de café beneficiado (**resposta**) |

**Resultado esperado:**
- Sombreamento: F = 6,48, **p = 0,032** (testado contra o **erro a** = bloco × sombreamento, 6 GL, QM = 9,40).
- Bloco: F = 4,38, p = 0,059 (contra o erro a).
- Cultivar: F = 78,61, p < 0,001; interação: F = 5,97, **p = 0,0031** (contra o **erro b** = resíduo, 18 GL, QM = 1,45).
- CV 1 (parcela) = 9,47%; CV 2 (subparcela) = 3,72%.
- Cultivar dentro de sombreamento (erro b): 0% → Arara **a**, Catuai **a**, Topazio **b**; 30% → Arara **a**, Catuai **ab**, Topazio **b**; 50% → Arara **a**, Catuai **b**, Topazio **c**.
- Sombreamento dentro de cultivar (erro combinado, QM = 4,10, GL de Satterthwaite = 9,97): significativo só para Topazio (F = 12,13, p = 0,002).

**Objetivo didático:** mostrar que existem **dois erros**. Se analisado como fatorial simples (erro errado), o F do sombreamento salta para cerca de 41,9 (p ≈ 10⁻⁷): uma conclusão exagerada. É um ótimo teste para ver se a IA "sabe" o delineamento.

---

## 5. `doses_nitrogenio`: doses de N no eucalipto em ILPF

| Item | Descrição |
|---|---|
| Delineamento | DIC com tratamentos **quantitativos** (análise por regressão) |
| Tratamentos | 5 doses de N em cobertura: 0, 50, 100, 150 e 200 kg/ha |
| Repetições | 4 por dose (20 parcelas) |
| Contexto | Eucalipto no componente arbóreo de um sistema de integração lavoura-pecuária-floresta (ILPF). |

| Coluna | Tipo | Unidade | Descrição |
|---|---|---|---|
| `dose_n_kg_ha` | inteiro (quantitativo) | kg/ha de N | Dose de nitrogênio |
| `repeticao` | inteiro | – | Repetição (1 a 4) |
| `volume_m3_ha` | decimal | m³/ha | Volume de madeira (**resposta**) |

**Resultado esperado:**
- ANOVA (dose como fator): F = 32,55, p = 3,1 × 10⁻⁷. CV = 5,14%. Shapiro p = 0,569; Bartlett p = 0,563.
- Linear: ŷ = 44,355 + 0,0914·x; R² = 0,847, mas desvios significativos (p = 0,0045), então o modelo linear **não serve**.
- **Quadrático:** ŷ = 41,1586 + 0,2192·x − 0,000639·x²; efeito quadrático F = 18,90 (p = 0,0006); desvios F = 0,51 (p = 0,61, não significativo); **R² = 0,992**.
- **Dose de máxima eficiência técnica: MET = −b1/(2·b2) = 171,4 kg/ha de N** (volume estimado ≈ 59,9 m³/ha).

**Objetivo didático:** para fatores **quantitativos**, usar **regressão, não Tukey**. Mostra a decomposição em efeito linear, efeito quadrático e desvios, o R² e o cálculo da MET.

---

## 6. `dic_contagem_pragas`: insetos-praga em diferentes manejos

| Item | Descrição |
|---|---|
| Delineamento | DIC |
| Tratamentos | 4 manejos: `convencional`, `saf_simples`, `saf_biodiverso`, `pousio` |
| Repetições | 6 armadilhas por manejo (24 parcelas) |
| Contexto | Monitoramento de insetos-praga com armadilhas em áreas com diferentes níveis de diversificação. |

| Coluna | Tipo | Unidade | Descrição |
|---|---|---|---|
| `manejo` | texto (fator) | – | Sistema de manejo |
| `repeticao` | inteiro | – | Armadilha (1 a 6) |
| `insetos_praga` | inteiro (contagem) | nº de insetos/armadilha | Contagem de insetos-praga (**resposta**) |

**Resultado esperado:**
- **Dados originais:** F = 9,62, p = 0,0004, mas **CV = 52,0%** e **Bartlett p = 0,0198 (variâncias heterogêneas: pressuposto violado)**. Levene (mediana) p = 0,008. Shapiro p = 0,834. As variâncias crescem com a média (convencional: média 21,2, variância 97,4; SAF biodiverso: média 2,5, variância 4,3).
- **Transformação √(x + 0,5):** F = 13,66, p = 4,5 × 10⁻⁵; CV = 25,1%; Bartlett p = 0,497 (OK); Shapiro p = 0,506. Tukey: convencional **a**, pousio **ab**, saf_simples **b**, saf_biodiverso **c**.
- **Kruskal-Wallis:** H = 15,20, 3 GL, p = 0,0017.

**Objetivo didático:** **violação de pressupostos**. Dados de contagem quase nunca têm variâncias homogêneas. Ensina a desconfiar de um CV alto, a ler os testes de pressupostos e a escolher entre transformar, usar um teste não paramétrico ou (avançado) um GLM Poisson/binomial negativo. Verifica se a IA testa os pressupostos **antes** de concluir.

---

## 7. `planilha_campo_baguncada.xlsx`: exercício de organização de dados

| Item | Descrição |
|---|---|
| Origem | Mesmos dados de `dic_mudas` (altura), "estragados" de propósito |
| Formato | **Largo** (1 linha por substrato, 1 coluna por repetição), e não longo |

| Coluna | Problema |
|---|---|
| `Substrato usado` | Nome com espaço e acento; valores despadronizados: `comercial ` (espaço no fim), `Composto Orgânico`, `Terra`, `terra + areia`, `Terra c/ esterco` |
| `Rep 1 (cm)` … `Rep 4 (cm)` | Unidade no nome da coluna; números com **vírgula decimal** gravados como **texto**; a célula Composto Orgânico × Rep 3 contém a palavra **`perdida`** |

**Resultado esperado após a limpeza:** 20 linhas no formato longo (`substrato`, `repeticao`, `altura_cm`), sendo 1 valor faltante (NA). Com o NA removido (19 parcelas): ANOVA F = 33,40, p = 5,1 × 10⁻⁷, CV ≈ 6,16%; média do composto orgânico = 37,93 (3 repetições).

**Objetivo didático:** mostrar como organizar dados de campo (formato longo/tidy, nomes sem espaço/acento, decimal com ponto, faltante = célula vazia/NA e nunca texto ou zero) e usar a IA para isso. Veja `exercicio_planilha.md`.
