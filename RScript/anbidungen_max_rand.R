user = "MR"
if(user == "CP"){
  setwd("//adb.intra.admin.ch/Userhome$/ARE-01/U80879660/data/Documents/NPVM/Model Lite/Anbindungen")
}
if(user == "MR"){
  setwd("E:/ARE/ProjekteTIE/PTV_model_lite")
}
anb = read.csv("AnbindugenMIV.csv")
anbVisum = read.csv("AnbindugenMIV_maxWeight_Visum.csv")

# ============================================================
# Anbindungen: split PW / SGV, sample & max-weight selection, plots
# ============================================================
library(ggplot2)
library(magrittr)

anb = plyr::rename(anb, c("ZONE.MAINZONE.NO" = "USPAT"))
# ---- 1. Split into PW and SGV -------------------------------
# PW rows: PW length & weight non-zero (SGV zero)
anbPW <- subset(anb, LAENGE_PW != 0 & GEWICHT_PW != 0 )

# SGV rows: SGV length & weight non-zero (PW zero)
anbSGV <- subset(anb, LAENGE_SGV != 0 & GEWICHT_SGV != 0)

# ---- 2. Selection functions ---------------------------------
# One random anbindung per ZONENO
pick_random <- function(df) {
  do.call(rbind, lapply(split(df, df$ZONENO), function(z) {
    z[sample(nrow(z), 1), ]
  }))
}

# The anbindung with the largest weight per ZONENO
pick_maxweight <- function(df, wcol) {
  do.call(rbind, lapply(split(df, df$ZONENO), function(z) {
    z[which.max(z[[wcol]]), ]
  }))
}

set.seed(123)  # reproducible random selection

anbPW_weight_total = anbPW %>% dplyr::group_by(ZONENO, USPAT) %>% dplyr::summarise(weight_total_VZ = sum(GEWICHT_PW))
anbPW_weight_total = anbPW_weight_total %>% dplyr::group_by(USPAT) %>% dplyr::mutate(weight_total_USPAT = sum(weight_total_VZ))
anbPW = merge(anbPW, anbPW_weight_total, by = c("ZONENO", "USPAT"))

anbSGV_weight_total = anbSGV %>% dplyr::group_by(ZONENO, USPAT) %>% dplyr::summarise(weight_total_VZ = sum(GEWICHT_SGV))
anbSGV_weight_total = anbSGV_weight_total %>% dplyr::group_by(USPAT) %>% dplyr::mutate(weight_total_USPAT = sum(weight_total_VZ))
anbSGV = merge(anbSGV, anbSGV_weight_total, by = c("ZONENO", "USPAT"))

anbPW_rand  <- pick_random(anbPW)
anbPW_max   <- pick_maxweight(anbPW,  "GEWICHT_PW")
sum(anbPW_max$GEWICHT_PW)/sum(anb$GEWICHT_PW)
# 0.2396184
sum(anbPW_rand$GEWICHT_PW)/sum(anb$GEWICHT_PW)
# 0.1523864

anbSGV_rand  <- pick_random(anbSGV)
anbSGV_max   <- pick_maxweight(anbSGV,  "GEWICHT_SGV")
sum(anbSGV_max$GEWICHT_SGV)/sum(anb$GEWICHT_PW)
# 0.2396184
sum(anbSGV_rand$GEWICHT_PW)/sum(anb$GEWICHT_PW)
# 0.1523864

summary(anb$LAENGE_PW)
# Min.  1st Qu.   Median     Mean  3rd Qu.     Max. 
# 0.00000  0.00000  0.02817  0.16553  0.08525 79.95200 
summary(anbPW_rand$LAENGE_PW)
# Min.      1st Qu.    Median      Mean   3rd Qu.      Max. 
# 0.00090  0.04619    0.08466     0.55742  0.17608     79.95200 
summary(anbPW_max$LAENGE_PW)
# Min.  1st Qu.   Median     Mean  3rd Qu.     Max. 
# 0.00027  0.04489  0.07930  0.50091  0.13598 79.95200

weight_totals <- function(df, weight_col = "GEWICHT_PW") {
  wc <- sym(weight_col)
  df %>%
    dplyr::group_by(ZONENO, USPAT) %>%
    dplyr::mutate(weight_VZ = sum(!!wc), .groups = "drop") %>%
    dplyr::group_by(USPAT) %>%
    dplyr::mutate(
      weight_USPAT = sum(weight_VZ)
    ) %>%
    dplyr::ungroup() %>% 
    dplyr::mutate(prop_VZ = weight_VZ/weight_total_VZ, prop_USPAT = weight_USPAT/weight_total_USPAT)
}

anbPW_rand <- weight_totals(anbPW_rand, "GEWICHT_PW")
anbPW_max <- weight_totals(anbPW_max, "GEWICHT_PW")

anbSGV_rand <- weight_totals(anbSGV_rand, "GEWICHT_SGV")
anbSGV_max <- weight_totals(anbSGV_max, "GEWICHT_SGV")

summary(anbPW_max$prop_VZ)
# Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
# 0.08833 0.19585 0.24916 0.27750 0.33279 0.50000 
summary(anbPW_rand$prop_VZ)
# Min.   1st Qu.    Median      Mean   3rd Qu.      Max. 
# 0.0008532 0.0935492 0.1563651 0.1973631 0.2516570 0.5000000
summary(anbPW_max$prop_USPAT)
# Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
# 0.0935  0.2102  0.2456  0.2715  0.3012  0.5000
summary(anbPW_rand$prop_USPAT)
# Min.   1st Qu.    Median      Mean   3rd Qu.      Max. 
# 0.0009921 0.1181476 0.1570735 0.1897505 0.2165555 0.5000000 
# 


library(dplyr)

# totals, overall and per USPAT
weight_max    <- sum(anbPW_max$GEWICHT_PW)
weight_rand   <- sum(anbPW_rand$GEWICHT_PW)
weight_tot = sum(anbPW$GEWICHT_PW)
cat("random keeps", round(100 * weight_rand / weight_max, 1),
    "% of the max-achievable weight\n")
# random keeps 63.6 % of the max-achievable weight
cat("random keeps", round(100 * weight_rand / weight_tot, 1),
    "% of the total weight\n vs ", round(100 * weight_max / weight_tot, 1), "% of max")
# random keeps 15.3 % of the total weight vs  24.1 % of max

# per-USPAT, so you see if the loss is uniform or concentrated in some zones
weight_by_uspat <- anbPW_max %>%
  transmute(USPAT, ZONENO, w_max = GEWICHT_PW) %>%
  left_join(
    anbPW_rand %>% transmute(ZONENO, w_rand = GEWICHT_PW),
    by = "ZONENO"
  ) %>%
  group_by(USPAT) %>%
  summarise(w_max = sum(w_max), w_rand = sum(w_rand), .groups = "drop") %>%
  mutate(retained = w_rand / w_max)

summary(weight_by_uspat$retained)
hist(weight_by_uspat$retained, breaks = 40,
     main = "Weight retained by random, per USPAT (1 = matches max)",
     xlab = "sum(random weight) / sum(max weight)")

poolPW <- anbPW %>% distinct(ZONENO, NODENO, DIRECTION, LAENGE_PW, GEWICHT_PW) %>% 
  dplyr::group_by(ZONENO) %>% dplyr::mutate(tot_weight_per_zone = sum(GEWICHT_PW)) %>% 
  dplyr::ungroup() %>% dplyr::mutate(weight_per_zone =GEWICHT_PW/tot_weight_per_zone, 
                                     weighted_length =weight_per_zone * LAENGE_PW) %>%
  dplyr::group_by(ZONENO) %>% dplyr::summarise(LAENGE_PW = sum(weighted_length), GEWICHT_PW = max(GEWICHT_PW))

len_pool <- poolPW$LAENGE_PW
len_max  <- anbPW_max$LAENGE_PW
len_rand <- anbPW_rand$LAENGE_PW

# KS statistic = max gap between ECDFs (use the statistic, ignore the p-value)
ks_max  <- ks.test(len_max,  len_pool)$statistic
ks_rand <- ks.test(len_rand, len_pool)$statistic
c(max = ks_max, random = ks_rand)

# quantile table: where does max distort?
probs <- c(.1, .25, .5, .75, .9, .95)
rbind(
  pool   = quantile(len_pool, probs),
  random = quantile(len_rand, probs),
  max    = quantile(len_max,  probs)
)
#         10%        25%        50%       75%       90%       95%
# pool   0.04558386 0.06231601 0.08946365 0.1443886 0.3483249 1.150500 --> pool is now weighted length for each VZ
# random 0.02589849 0.04618587 0.08466075 0.1760776 0.6299087 1.597653
# max    0.02498326 0.04488952 0.07930026 0.1359823 0.3426000 1.167018

# within each VZ, does the heaviest anbindung tend to be the shortest?
rank_check <- anbPW %>%
  group_by(ZONENO) %>%
  filter(n() >= 2) %>%
  summarise(
    cor_wl = cor(GEWICHT_PW, LAENGE_PW, method = "spearman"),
    .groups = "drop"
  )
summary(rank_check$cor_wl)   # strongly negative => max systematically picks short anbindungen
# Min. 1st Qu.  Median    Mean 3rd Qu.    Max.    NA's 
# -1.0000 -0.8000 -0.4000 -0.1259  0.5000  1.0000    1155  

build_compare <- function(full, rand, max, lcol, wcol) {
  mk <- function(df, v) data.frame(
    version = v,
    length  = df[[lcol]],
    weight  = df[[wcol]]
  )
  out <- rbind(
    mk(full, "Full (all anb)"),
    mk(rand, "Random pick"),
    mk(max,  "Max weight")
  )
  out$version <- factor(out$version,
                        levels = c("Full (all anb)", "Random pick", "Max weight"))
  out
}
cmpPW  <- build_compare(poolPW,  anbPW_rand,  anbPW_max,  "LAENGE_PW",  "GEWICHT_PW")
cmpSGV <- build_compare(anbSGV, anbSGV_rand, anbSGV_max, "LAENGE_SGV", "GEWICHT_SGV")

# ---- 4. Comparison plots ------------------------------------
compare_plots <- function(cmp, label) {
  
  # Filter for plotting only: keep weights above 200 and below 6000
  cmp <- subset(cmp, length > 0 & length < 1)
  
  # Length distribution: overlaid densities (fair when N differs)
  p_dens <- ggplot(cmp, aes(x = length, colour = version, fill = version)) +
    geom_density(alpha = 0.25) +
    labs(title = paste0("Length distribution - ", label),
         x = "Length", y = "Density", colour = "", fill = "") +
    theme_minimal()
  
  # Histograms with the three versions as side-by-side bars per bin
  p_hist <- ggplot(cmp, aes(x = length, fill = version)) +
    geom_histogram(bins = 40, colour = "white",
                   position = position_dodge2(preserve = "single")) +
    labs(title = paste0("Length distribution (histograms) - ", label),
         x = "Length", y = "Count", fill = "") +
    theme_minimal()
  
  # Scatter length vs weight, coloured by version
  p_scat <- ggplot(cmp, aes(x = length, y = weight, colour = version)) +
    geom_point(alpha = 0.4) +
    labs(title = paste0("Length vs Weight - ", label),
         x = "Length", y = "Weight", colour = "") +
    theme_minimal()
  
  list(density = p_dens, hist = p_hist, scatter = p_scat)
}


pw_cmp  <- compare_plots(cmpPW,  "PW trunc length 1")
sgv_cmp <- compare_plots(cmpSGV, "SGV")

# ---- 5. Show / save -----------------------------------------
print(pw_cmp$density)  
print(pw_cmp$hist)  
print(pw_cmp$scatter)

print(sgv_cmp$dens)

# Or save all eight to files:
ggsave("Plots/pw_density.png",  pw_cmp$density)
ggsave("pw_rand_scat.png",  pw_cmp$scatter)