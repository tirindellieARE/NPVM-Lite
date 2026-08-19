bzk = sf::read_sf("//192.168.150.4/d$/VISUM/NPVM 2023/Visum Unterstzüng/PTV_model_light/shp/Bezirke")
bzk_to_uspat = sf::read_sf("//192.168.150.4/d$/VISUM/NPVM 2023/Visum Unterstzüng/PTV_model_light/shp/Bezirke_to_USPAT")

bzk_to_uspat = dplyr::left_join(bzk_to_uspat, sf::st_drop_geometry(bzk_agg[bzk_agg$uspat !=0, c("NO_agg", "uspat")]), by = )
bzk_to_uspat = dplyr::mutate(bzk_to_uspat, NO_agg = ifelse(is.na(NO_agg), NO, NO_agg))
bzk_to_uspat = bzk_to_uspat %>% plyr::rename(c("uspat" = "MakroBez_ID", "NO_agg" = "BezAggr_ID"))
sf::write_sf(bzk_to_uspat, "//192.168.150.4/d$/VISUM/NPVM 2023/Visum Unterstzüng/PTV_model_light/shp/Bezirke_to_USPAT/Bezirke_to_USPAT.shp")

bzk_agg = sf::read_sf("//192.168.150.4/d$/VISUM/NPVM 2023/Visum Unterstzüng/PTV_model_light/shp/Bezirke_aggreg")
bzk_agg = bzk_agg %>% plyr::rename(c("MAKROBEZ~1" = "uspat", "NO" = "NO_agg"))
bzk_agg = dplyr::mutate(bzk_agg, uspat = ifelse(uspat==0, NO, uspat))
bzk_agg = bzk_agg %>% dplyr::select(-NO) %>% plyr::rename(c("uspat" = "NO"))

anzBez0 = fread("//192.168.150.4/d$/VISUM/NPVM 2023/Visum Unterstzüng/PTV_model_light/AnzBez0.csv") 

sf::write_sf(bzk_agg, "//192.168.150.4/d$/VISUM/NPVM 2023/Visum Unterstzüng/PTV_model_light/shp/Bezirke_aggreg/Bezirke_aggreg_zone.shp")

bzk = bzk %>% plyr::rename(c("MAKROBEZ~1" = "staat", "MAKROBEZ~2" = "uspat"))

bzk_poi = readxl::read_excel("//192.168.150.4/d$/VISUM/NPVM 2023/Visum Unterstzüng/PTV_model_light/bezirke_from_visum.xlsx") 
bzk_poi = dplyr::left_join(bzk_agg, bzk_poi, by = c("NO" = "Nr"))

c = merge(sf::st_drop_geometry(bzk[c("NO", "uspat")]),sf::st_drop_geometry(bzk_agg[c("NO", "uspat", "staat")]), by = "NO")
c= c %>% dplyr::group_by(uspat.x) %>% dplyr::mutate(n = dplyr::n())

bzk_uspat = dplyr::mutate(bzk[c("NO", "uspat")], uspat = ifelse(uspat==0, NO, uspat))
sf::write_sf(bzk_uspat, "//192.168.150.4/d$/VISUM/NPVM 2023/Visum Unterstzüng/PTV_model_light/shp/Bezirke_to_USPAT/Bezirke_to_USPAT.shp")

bzk_uspat = sf::st_drop_geometry(bzk_uspat)


bzk_uspat = merge(bzk_uspat, bzk_agg[c("uspat_merge", "geometry")], by = "uspat_merge")
