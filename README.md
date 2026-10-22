# IA para Estatística Experimental — Curso Inova Agroflorestal (UFVJM)

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/guihenrique13/curso-ia-estatistica-inova-agroflorestal/blob/main/notebooks/analise_exemplos.ipynb)

Materiais do curso **IA para Estatística Experimental**: apostila, "skills" (instruções prontas para a IA), planilhas de exemplo e um notebook com as análises feitas passo a passo. Não é preciso saber programar para aproveitar o curso.

## Comece aqui

1. **Baixe a apostila**: [apostila/apostila.pdf](apostila/apostila.pdf). Clique no arquivo e depois no botão de download (seta para baixo), no canto direito.
2. **Crie o seu Gem** (o seu "Gemini personalizado"): copie todo o texto de [skills/gem-unico.md](skills/gem-unico.md) e cole nas instruções de um novo Gem. O passo a passo, com outras opções de IA, está em [skills/README.md](skills/README.md).
3. **Experimente com os dados de exemplo**: baixe uma planilha da pasta [dados/](dados/) (por exemplo, [dados/dic_mudas.csv](dados/dic_mudas.csv)), envie para o seu Gem e peça a análise. Depois, compare com as respostas certas em [dados/gabarito_resultados.txt](dados/gabarito_resultados.txt).
4. **Quer ver as contas feitas no computador?** Clique no botão **Abrir no Colab** acima. O notebook abre no navegador e já busca os dados deste repositório sozinho.

## O que tem em cada pasta

| Pasta | O que tem |
|---|---|
| [apostila/](apostila/) | A apostila do curso em PDF (para ler e imprimir), em Word (`.docx`, para editar) e o texto-fonte (`apostila.md`). A subpasta `build/` tem os scripts que geram o Word e o PDF. |
| [skills/](skills/) | Arquivos de instruções que transformam a IA num assistente de estatística experimental: planejamento, DIC/DBC com ANOVA e Tukey, fatorial e parcela subdividida, regressão de doses e redação do relatório no padrão ABNT. O `gem-unico.md` junta tudo num só arquivo. |
| [dados/](dados/) | Planilhas de exemplo (`.csv` e `.xlsx`), o dicionário de dados, um exercício com uma planilha de campo "bagunçada", o gabarito dos resultados e o script que gera os dados. |
| [notebooks/](notebooks/) | Notebook em Python para o Google Colab (`analise_exemplos.ipynb`), um script equivalente em R e o script que monta o notebook. |
| [slides/](slides/) | Slides da aula (46 slides): [PDF](slides/curso-ia-estatistica.pdf) para projetar e [PPTX](slides/curso-ia-estatistica.pptx) editável (abre no PowerPoint, Google Slides ou Canva). O arquivo `roteiro_slides.md` é o roteiro original usado para gerar o deck. |

## Sobre os dados

**Todos os dados são fictícios (simulados)**. Foram criados por computador só para o curso e não vêm de nenhum experimento real. Não use esses números como resultado de pesquisa.

- O que significa cada coluna: [dados/dicionario_dados.md](dados/dicionario_dados.md)
- Resultados esperados de cada análise (gabarito): [dados/gabarito_resultados.txt](dados/gabarito_resultados.txt)

## Para quem quer refazer os arquivos

- **Gerar os dados de novo:** `python3 dados/gerar_dados.py` (precisa de Python com `numpy` e `pandas`; para os `.xlsx`, também `openpyxl`).
- **Gerar a apostila de novo (Word e PDF):** `bash apostila/build/build.sh`. Precisa de [pandoc](https://pandoc.org), Python 3 e LibreOffice. Veja os comentários no início do script.
- **Montar o notebook de novo:** `python3 notebooks/build_nb.py` (precisa de `nbformat`, `nbclient`, `ipykernel` e das bibliotecas usadas no notebook).

## Aviso sobre o Gemini

Os recursos do Gemini (Gems, envio de arquivos, Canvas, exportar para o Google Docs, limites da versão grátis) mudam com frequência e podem variar conforme a conta, o país e o aparelho. Se algum botão estiver com outro nome ou em outro lugar, procure a opção equivalente. E sempre confira os resultados que a IA entregar.

---

Licença: a definir pelo autor.
