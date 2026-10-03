user = "MR"
if(user == "CP"){
  setwd("//adb.intra.admin.ch/Userhome$/ARE-01/U80879660/data/Documents/NPVM/Model Lite/Anbindungen")
}
if(user == "MR"){
  setwd("E:/ARE/ProjekteTIE/PTV_model_lite")
}
anb = read.csv("AnbindugenMIV.csv")
anbVisum = read.csv("AnbindugenMIV_maxWeight_Visum.csv")
anb_full = read.csv("AnbindugenMIV_full.csv")

anb = plyr::rename(anb, c("ZONE.MAINZONE.NO" = "USPAT"))
anbVisum = plyr::rename(anbVisum, c("ZONENO" = "USPAT"))

anb = anb %>% dplyr::group_by(ZONENO, DIRECTION) %>%
  dplyr::mutate(GEWICHT_VZ = sum(GEWICHT_PW)) %>% dplyr::ungroup()

library(magrittr)

# ---- 1. Split into PW and SGV -------------------------------
# PW rows: PW length & weight non-zero (SGV zero)
anbPW <- subset(anb, GEWICHT_PW != 0)

# SGV rows: SGV length & weight non-zero (PW zero)
anbSGV <- subset(anb, GEWICHT_SGV != 0)

anbVisumPW <- subset(anbVisum, GEWICHT_PW != 0)


# SGV rows: SGV length & weight non-zero (PW zero)
anbVisumSGV <- subset(anbVisum, GEWICHT_SGV != 0)


# The anbindung with the largest weight per ZONENO
pick_maxweight <- function(df, wcol) {
  do.call(rbind, lapply(
    split(df, list(df$ZONENO, df$DIRECTION), drop = TRUE),
    function(z) z[which.max(z[[wcol]]), ]
  ))
}

anbPW   <- pick_maxweight(anbPW,  "GEWICHT_PW")
anbSGV   <- pick_maxweight(anbSGV,  "GEWICHT_SGV")

anbPW = anbPW %>% dplyr::group_by(USPAT, DIRECTION, NODENO) %>% dplyr::mutate(dup = dplyr::n()) %>% dplyr::ungroup()
nrow(anbPW)
dup = dplyr::filter(anbPW, dup > 1)
nrow(dup)
anbPW = dplyr::filter(anbPW, dup == 1)
nrow(anbPW)

dup = dup %>% dplyr::group_by(USPAT, NODENO, DIRECTION) %>% dplyr::mutate(GEWICHT_USPAT = sum(GEWICHT_VZ))
dup = dup %>% dplyr::group_by(USPAT, NODENO, DIRECTION) %>% 
  dplyr::mutate(LAENGE_new = sum(LAENGE_PW*GEWICHT_VZ/GEWICHT_USPAT))
dup = dup %>% dplyr::mutate(LAENGE_PW = LAENGE_new, GEWICHT_VZ = GEWICHT_USPAT)
dup = dup %>% dplyr::select(-c(LAENGE_new,GEWICHT_USPAT)) %>% dplyr::ungroup()
# 1721045  1123218 
# dplyr::filter(dup, USPAT == 1123218  )

anbPW = rbind(anbPW, dup)
anbPW = anbPW %>% dplyr::select(c(USPAT, NODENO, DIRECTION, GEWICHT_VZ, LAENGE_PW))  %>% 
  plyr::rename(c("GEWICHT_VZ" = "GEWICHT_PW")) %>%
  dplyr::filter(!is.na(USPAT)) %>% 
  dplyr::distinct()

dplyr::n_distinct(anbPW$USPAT, anbPW$DIRECTION, anbPW$NODENO)
dplyr::n_distinct(anbVisumPW$USPAT, anbVisumPW$DIRECTION, anbVisumPW$NODENO)

c = dplyr::left_join(anbVisumPW[c("USPAT", "NODENO", "DIRECTION", "GEWICHT_PW", "LAENGE_PW")], 
                     anbPW[c("USPAT", "NODENO", "DIRECTION", "GEWICHT_PW", "LAENGE_PW")], 
                     by = c("USPAT", "NODENO", "DIRECTION"))
gewicht = dplyr::filter(c, GEWICHT_PW.x != GEWICHT_PW.y)
nrow(gewicht)
laenge = dplyr::filter(c, LAENGE_PW.x != LAENGE_PW.y)
nrow(laenge)

summary(c$LAENGE_PW.x-c$LAENGE_PW.y)
