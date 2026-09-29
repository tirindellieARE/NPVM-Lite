user = "CP"
if(user == "CP"){
  setwd("//adb.intra.admin.ch/Userhome$/ARE-01/U80879660/data/Documents/NPVM/Model Lite/Anbindungen")
}
anb = read.csv("AnbindugenMIV.csv")

# ============================================================
# Anbindungen: split PW / SGV, sample & max-weight selection, plots
# ============================================================
library(ggplot2)
library(magrittr)

anb = plyr::rename(anb, c("ZONE.TNN_AGGGEMEINDE" = "USPAT"))
# ---- 1. Split into PW and SGV -------------------------------
# PW rows: PW length & weight non-zero (SGV zero)
anbPW <- subset(anb, LAENGE_PW != 0 & GEWICHT_PW != 0 &
                  LAENGE_SGV == 0 & GEWICHT_SGV == 0)

# SGV rows: SGV length & weight non-zero (PW zero)
anbSGV <- subset(anb, LAENGE_SGV != 0 & GEWICHT_SGV != 0 &
                   LAENGE_PW == 0 & GEWICHT_PW == 0)

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

anbPW_rand  <- pick_random(anbPW)
anbPW_max   <- pick_maxweight(anbPW,  "GEWICHT_PW")
sum(anbPW_max$GEWICHT_PW)/sum(anb$GEWICHT_PW)
# 0.2396184
sum(anbPW_rand$GEWICHT_PW)/sum(anb$GEWICHT_PW)
# 0.1523864

summary(anb$LAENGE_PW)
# Min.  1st Qu.   Median     Mean  3rd Qu.     Max. 
# 0.00000  0.00000  0.02817  0.16553  0.08525 79.95200 
summary(anbPW_rand$LAENGE_PW)
# Min.   1st Qu.    Median      Mean   3rd Qu.      Max. 
# 0.000805  0.043048  0.075693  0.164743  0.136317 10.627863 
summary(anbPW_max$LAENGE_PW)
# Min.  1st Qu.   Median     Mean  3rd Qu.     Max. 
# 0.000269 0.041984 0.072367 0.103065 0.114672 6.366664

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

summary(anbPW_max$prop_VZ)
# Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
# 0.08833 0.19125 0.23849 0.25670 0.30167 0.50000 
summary(anbPW_rand$prop_VZ)
# Min.   1st Qu.    Median      Mean   3rd Qu.      Max. 
# 0.0008532 0.0874639 0.1442223 0.1688482 0.2193376 0.5000000 
summary(anbPW_max$prop_USPAT)
# Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
# 0.0935  0.2067  0.2393  0.2501  0.2833  0.5000 
summary(anbPW_rand$prop_USPAT)
# Min.   1st Qu.    Median      Mean   3rd Qu.      Max. 
# 0.0009921 0.1136687 0.1496247 0.1601732 0.1948772 0.5000000 
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

pool <- anbPW %>% distinct(ZONENO, NODENO, DIRECTION, LAENGE_PW, GEWICHT_PW) %>% 
  dplyr::group_by(ZONENO) %>% dplyr::mutate(tot_weight_per_zone = sum(GEWICHT_PW)) %>% 
  dplyr::ungroup() %>% dplyr::mutate(weight_per_zone =GEWICHT_PW/tot_weight_per_zone, 
                                     weighted_length =weight_per_zone * LAENGE_PW) %>%
  dplyr::group_by(ZONENO) %>% dplyr::summarise(LAENGE_PW = sum(weighted_length))

len_pool <- pool$LAENGE_PW
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
# pool   0.04435175 0.05977995 0.08387980 0.1215505 0.1909207 0.2659819 --> pool is now weighted length for each VZ
# random 0.02431643 0.04304781 0.07569341 0.1363168 0.2964880 0.5614036
# max    0.02364243 0.04198390 0.07236735 0.1146722 0.1766758 0.2461492

# within each VZ, does the heaviest anbindung tend to be the shortest?
rank_check <- pool %>%
  group_by(ZONENO) %>%
  filter(n() >= 2) %>%
  summarise(
    cor_wl = cor(GEWICHT_PW, LAENGE_PW, method = "spearman"),
    .groups = "drop"
  )
summary(rank_check$cor_wl)   # strongly negative => max systematically picks short anbindungen
# Min. 1st Qu.  Median    Mean 3rd Qu.    Max.    NA's 
# -1.0000 -0.8000 -0.4000 -0.1261  0.5000  1.0000     345 

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
cmpPW  <- build_compare(anbPW,  anbPW_rand,  anbPW_max,  "LAENGE_PW",  "GEWICHT_PW")
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