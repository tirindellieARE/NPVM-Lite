user = "MR"
if(user == "CP"){
  setwd("//adb.intra.admin.ch/Userhome$/ARE-01/U80879660/data/Documents/NPVM/Model Lite/Anbindungen")
}
if(user == "MR"){
  setwd("E:/ARE/ProjekteTIE/PTV_model_lite")
}

library(magrittr)

anb = read.csv("AnbindugenOEV.csv")
anbVisum = read.csv("AnbindugenOEV_maxWeight_Visum.csv")

anb = plyr::rename(anb, c("ZONE.MAINZONE.NO" = "USPAT"))
anbVisum = plyr::rename(anbVisum, c("ZONENO" = "USPAT"))

anb = anb %>% dplyr::group_by(ZONENO, DIRECTION) %>%
  dplyr::mutate(WEIGHT_VZ = sum(WEIGHT)) %>% dplyr::ungroup()


# The anbindung with the largest weight per ZONENO
pick_maxweight <- function(df, wcol) {
  do.call(rbind, lapply(
    split(df, list(df$ZONENO, df$DIRECTION), drop = TRUE),
    function(z) z[which.max(z[[wcol]]), ]
  ))
}

anb   <- pick_maxweight(anb,  "WEIGHT")

anb = anb %>% dplyr::group_by(USPAT, DIRECTION, NODENO) %>% dplyr::mutate(dup = dplyr::n()) %>% dplyr::ungroup()
nrow(anb)
dup = dplyr::filter(anb, dup > 1)
nrow(dup)
anb = dplyr::filter(anb, dup == 1)
nrow(anb)

dup = dup %>% dplyr::group_by(USPAT, NODENO, DIRECTION) %>% dplyr::mutate(WEIGHT_USPAT = sum(WEIGHT_VZ))
dup = dup %>% dplyr::group_by(USPAT, NODENO, DIRECTION) %>% 
  dplyr::mutate(LENGTH_new = sum(LENGTH*WEIGHT_VZ/WEIGHT_USPAT))
dup = dup %>% dplyr::mutate(LENGTH = LENGTH_new, WEIGHT_VZ = WEIGHT_USPAT)
dup = dup %>% dplyr::select(-c(LENGTH_new,WEIGHT_USPAT)) %>% dplyr::ungroup()

anb = rbind(anb, dup)
anb = anb %>% dplyr::select(c(USPAT, NODENO, DIRECTION, WEIGHT_VZ, LENGTH))  %>% 
  plyr::rename(c("WEIGHT_VZ" = "WEIGHT")) %>%
  dplyr::filter(!is.na(USPAT)) %>% 
  dplyr::distinct()

dplyr::n_distinct(anb$USPAT, anb$DIRECTION, anb$NODENO)
dplyr::n_distinct(anbVisum$USPAT, anbVisum$DIRECTION, anbVisum$NODENO)

c = dplyr::left_join(anb[c("USPAT", "NODENO", "DIRECTION", "WEIGHT", "LENGTH")], 
                     anbVisum[c("USPAT", "NODENO", "DIRECTION", "WEIGHT", "LENGTH")], 
                     by = c("USPAT", "NODENO", "DIRECTION"))
gewicht = dplyr::filter(c, WEIGHT.x != WEIGHT.y)
nrow(gewicht)
laenge = dplyr::filter(c, LENGTH.x != LENGTH.y)
nrow(laenge)

summary(c$LENGTH.x-c$LENGTH.y)
