# Curso IA para Estatística Experimental — Inova Agroflorestal
# Análises de referência (gabarito) com o pacote ExpDes.pt
# Rode a partir da pasta do projeto:  Rscript notebooks/analise_exemplos.R
# Instalação (uma vez): install.packages(c("ExpDes.pt", "agricolae"))
#   Se o CRAN não tiver o ExpDes.pt para sua versão do R:
#   remotes::install_url("https://cran.r-project.org/src/contrib/Archive/ExpDes.pt/ExpDes.pt_1.2.2.tar.gz")

library(ExpDes.pt)

ler <- function(nome) read.csv(file.path("dados", paste0(nome, ".csv")))

cat("\n========== 1) DIC — substratos x altura de mudas de ipê ==========\n")
d <- ler("dic_mudas")
dic(d$substrato, d$altura_cm, quali = TRUE, mcomp = "tukey", sigT = 0.05, sigF = 0.05)

cat("\n========== 2) DBC — cultivares de milho em aleias ==========\n")
d <- ler("dbc_milho")
dbc(d$cultivar, d$bloco, d$produtividade_kg_ha, quali = TRUE, mcomp = "tukey")

cat("\n========== 3) Fatorial 3x3 (DIC) — espécie x adubação ==========\n")
d <- ler("fatorial_adubacao")
fat2.dic(d$especie, d$adubacao, d$massa_seca_g, quali = c(TRUE, TRUE),
         mcomp = "tukey", fac.names = c("Especie", "Adubacao"))

cat("\n========== 4) Parcela subdividida (DBC) — sombreamento x cultivar de café ==========\n")
d <- ler("parcela_sub_cafe_sombra")
psub2.dbc(d$sombreamento_pct, d$cultivar, d$bloco, d$produtividade_sc_ha,
          quali = c(FALSE, TRUE), mcomp = "tukey",
          fac.names = c("Sombreamento", "Cultivar"))

cat("\n========== 5) Regressão — doses de N x volume de eucalipto ==========\n")
d <- ler("doses_nitrogenio")
dic(d$dose_n_kg_ha, d$volume_m3_ha, quali = FALSE)
m <- lm(volume_m3_ha ~ dose_n_kg_ha + I(dose_n_kg_ha^2), data = d)
b <- coef(m)
cat("Dose de máxima eficiência técnica (kg/ha):", round(-b[2] / (2 * b[3]), 1), "\n")

cat("\n========== 6) Contagem de pragas — pressupostos violados ==========\n")
d <- ler("dic_contagem_pragas")
dic(d$manejo, d$insetos_praga, quali = TRUE)
cat("\n--- Com transformação raiz(x + 0.5) ---\n")
dic(d$manejo, sqrt(d$insetos_praga + 0.5), quali = TRUE)
cat("\n--- Alternativa não paramétrica: Kruskal-Wallis ---\n")
print(kruskal.test(insetos_praga ~ manejo, data = d))
