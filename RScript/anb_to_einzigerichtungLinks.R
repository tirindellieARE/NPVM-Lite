user = "MR"
if(user == "CP"){
  setwd("//adb.intra.admin.ch/Userhome$/ARE-01/U80879660/data/Documents/NPVM/Model Lite/")
}
if(user == "MR"){
  setwd("E:/ARE/ProjekteTIE/PTV_model_lite")
}

anb_corr = read.csv("xls/AnbindugenOEV_maxWeight_Visum_corr.csv")
anbVisum = read.csv("xls/AnbindugenMIV_maxWeight_Visum.csv")
anb = read.csv("xls/AnbindugenMIV.csv")
anb = plyr::rename(anb, c("ZONE.MAINZONE.NO" = "USPAT"))

links = sf::st_read("shp/Strecken")
links = sf::st_drop_geometry(links)
links = dplyr::filter(links, is.na(TSYSSET) | is.na(R_TSYSSET))

anb_closed = dplyr::filter(anb, NODENO %in% unique(c(links$FROMNODENO, links$TONODENO)))
