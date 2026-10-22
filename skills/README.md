# Skills de Estatística Experimental

Curso **IA para Estatística Experimental** – Inova Agroflorestal (UFVJM)

Estas "skills" são **arquivos de instruções** que ensinam uma IA a se comportar como um assistente de estatística experimental: perguntar o que precisa, conferir a planilha, testar pressupostos, fazer ANOVA, Tukey, desdobramento ou regressão, e explicar tudo em linguagem simples, **sem inventar resultados**.

Você não precisa programar. Basta copiar e colar o texto na IA que você usa.

## O que tem nesta pasta

| Arquivo | Para quê |
|---|---|
| `00-assistente-estatistico/SKILL.md` | Skill "mãe": regras gerais e qual skill usar em cada situação |
| `01-planejamento-experimento/SKILL.md` | Escolher DIC/DBC/fatorial/parcela subdividida, nº de repetições, croqui, planilha modelo |
| `02-dic-dbc-anova-tukey/SKILL.md` | Um fator: ANOVA, pressupostos, CV% e Tukey |
| `03-fatorial-parcela-subdividida/SKILL.md` | Dois fatores: interação, desdobramento, erro a e erro b |
| `04-regressao-doses/SKILL.md` | Doses e níveis numéricos: regressão e máxima eficiência técnica |
| `05-interpretacao-relatorio/SKILL.md` | Texto para relatório/TCC, tabelas e figuras no padrão ABNT, como citar a IA |
| `gem-unico.md` | Versão resumida "tudo em um", para criar **um único Gem** |

Cada `SKILL.md` começa com um cabeçalho entre linhas `---` (nome e descrição). Esse cabeçalho serve para o Claude; nas outras IAs ele pode ser colado junto sem problema.

**Tabelas e figuras no padrão ABNT:** depois de toda análise, a IA entrega as tabelas (ANOVA, médias com letras, regressão) e as figuras no padrão ABNT/IBGE: título acima ("Tabela 1 – ..."), só três traços horizontais, "Fonte:" e nota abaixo, vírgula decimal e legenda de significância (**, *, ns). Cada tabela vem duas vezes: em Markdown para ler no chat (que mostra todas as bordas) e numa versão para exportar ao Google Docs ("Exportar para Documentos") ou ao Canvas, onde basta tirar as bordas e deixar só os três traços. Ela também informa a numeração e oferece um parágrafo pronto que cita as tabelas. O exemplo completo está na skill 05.

**Como abrir os arquivos:** são texto puro. Abra com o Bloco de Notas (Windows), TextEdit (Mac) ou direto no Google Drive. Selecione tudo (Ctrl+A), copie (Ctrl+C) e cole (Ctrl+V) onde for indicado.

---

## Opção 1 – Gemini (grátis, recomendado no curso)

Um **Gem** é um "Gemini personalizado" que guarda as instruções para você não precisar colar toda vez.

1. Entre em **gemini.google.com** com sua conta Google.
2. No menu lateral (ícone ☰ no celular), clique em **Gems** (ou "Explorar Gems").
3. Clique em **Novo Gem** (ou "Criar Gem").
4. Em **Nome**, escreva: `Assistente de Estatística Experimental`.
5. Em **Instruções**, cole **todo** o conteúdo do arquivo `gem-unico.md`.
6. Em **Conhecimento**, clique em **adicionar arquivos** (ícone +) e envie as skills que quiser como material de consulta (ex.: os 6 arquivos `SKILL.md`; renomeie para `00-assistente.md`, `02-dic-dbc.md` etc. para não ficarem com o mesmo nome). Opcional: envie também o dicionário de dados ou uma planilha modelo.
7. Clique em **Salvar**. O Gem aparece na lista do menu lateral.
8. Para usar: abra o Gem, anexe sua planilha (ícone + → arquivo CSV ou XLSX) e escreva, por exemplo:
   > "Este é um experimento em DIC com 5 substratos e 4 repetições. A variável é altura_cm. Faça a análise completa e mostre o código usado."

Dicas:
- Se o Gemini não mostrar o código, peça: "Mostre o código Python que você executou."
- Se ele der números sem ter rodado código, peça: "Rode o código de verdade e me mostre a saída."
- Os nomes e lugares dos botões podem mudar um pouco com as atualizações do Gemini.

## Opção 2 – ChatGPT

**Com GPT personalizado** (se o seu plano permitir criar GPTs):
1. Em **chatgpt.com**, menu lateral → **GPTs** → **Criar**.
2. Aba **Configurar**: dê um nome e cole `gem-unico.md` em **Instruções**.
3. Em **Conhecimento**, envie os arquivos `SKILL.md`.
4. Marque **Code Interpreter / Análise de dados** (para ele rodar o código).
5. Clique em **Criar** e depois use normalmente.

**Com Projeto** (disponível em mais planos):
1. Menu lateral → **Projetos** → **Novo projeto**.
2. Em **Instruções do projeto**, cole `gem-unico.md`.
3. Em **Arquivos do projeto**, envie as skills.
4. Abra uma conversa dentro do projeto e anexe sua planilha.

## Opção 3 – Claude

**Como Skill nativa** (se o seu plano tiver Skills):
1. Compacte **cada pasta** separadamente em um arquivo .zip (clique com o botão direito na pasta → "Compactar" / "Enviar para → Pasta compactada"). O .zip deve conter a pasta com o `SKILL.md` dentro.
2. Em **claude.ai** → **Configurações** → **Capacidades** → ative a execução de código e, em **Skills**, clique em **Enviar skill** e escolha o .zip.
3. Repita para cada skill. O Claude escolhe sozinho qual usar pela descrição.

**Como Projeto:**
1. Menu lateral → **Projetos** → **Criar projeto**.
2. Em **Instruções do projeto**, cole `gem-unico.md` (ou o `00-assistente-estatistico/SKILL.md`).
3. Em **Conhecimento do projeto**, envie os outros `SKILL.md`.
4. Converse dentro do projeto e anexe sua planilha.

## Opção 4 – Colar direto na conversa (qualquer IA)

Funciona em qualquer IA, sem criar nada:
1. Abra uma conversa nova.
2. Cole o conteúdo da skill que você precisa (ex.: `02-dic-dbc-anova-tukey/SKILL.md`) e escreva no final: "Siga essas instruções durante toda a conversa."
3. Na mesma mensagem ou na seguinte, anexe a planilha e faça o pedido.

Desvantagem: precisa colar de novo a cada conversa nova.

---

## Como testar se funcionou

Use os dados do curso (pasta `dados/`) e compare com o gabarito (`dados/gabarito_resultados.txt`):

| Arquivo | O que a IA deve encontrar |
|---|---|
| `dic_mudas.csv` | F = 34,57; CV = 6,1%; composto_organico, terra_esterco e comercial "a"; terra e terra_areia "b" |
| `dbc_milho.csv` | F = 34,69; CV = 5,04%; bloco significativo; 3 grupos de letras (a, b, c) |
| `fatorial_adubacao.csv` | Interação significativa → desdobramento; CV = 8,55% |
| `parcela_sub_cafe_sombra.csv` | Erro a (GL 6) e erro b (GL 18); CV1 = 9,47%, CV2 = 3,72% |
| `doses_nitrogenio.csv` | Regressão quadrática, R² = 0,99; máxima eficiência técnica ≈ 171 kg/ha |
| `dic_contagem_pragas.csv` | Variâncias heterogêneas (Bartlett p = 0,02) → sugerir √(x + 0,5) ou Kruskal-Wallis |

## Checklist para conferir a IA

- [ ] Ela conferiu a planilha (tratamentos, repetições) antes de analisar?
- [ ] Mostrou o código e disse que executou?
- [ ] Testou normalidade e homogeneidade e disse o que fazer se falharam?
- [ ] O GL do resíduo e o CV% fazem sentido?
- [ ] Usou Tukey só em fator qualitativo e regressão em doses?
- [ ] No fatorial, olhou a interação antes dos efeitos principais?
- [ ] Os números batem quando você roda de novo (ou no R/SISVAR)?
- [ ] As tabelas e figuras vieram no padrão ABNT (título acima, Fonte abaixo, 3 traços, vírgula decimal)?

**Lembre-se:** a IA ajuda, mas a responsabilidade pelos resultados é sua. Confira sempre e declare o uso de IA no seu trabalho (veja a skill 05).
