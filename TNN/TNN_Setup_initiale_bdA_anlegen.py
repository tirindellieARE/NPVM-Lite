# Teilnetznachfrage: Anlegen von bda, die für die TeilraumNachfrage-Modell benötigt werden
# Fuegt neue bdA in Visum Version ein, bda muessen vorher in uda_dict definiert werden
# wenn bdA vorhanden, dann bleibt bdA erhalten

# Beim Übertrag auf Andere Modelle z.B. Validaäte oder landesmodell xyz, dann müssen ggf bda-Namen Angepasst werden, weil die nachfragemodellkürzel oder Modinamen anderes sind 
#
# Richtige Schreibung (Groß- und Klein!) der Visum-Objekte beachten. Beispiele:
# Zones, MainZones, TSystems, DemandModels, DemandSegments, DemandStrata, PersonGroups, StructuralProps, Links, Nodes, Connectors, POICategories, POIs,
# Lines, LineRoutes, LineRouteItems, Stops, StopAreas, StopPoints, SystemRoutes,  etc

# teilraumattribute für erzeugung werden automatisch miterzeugt SOFERN im Namen der String 'Teilraum' enthalten ist. Ansonsten muss manuell hinzugefügt werden
# Eric Pestel, geänd. BD Okt 24 in Visum 24
import time


# Nutzereinstellung -----------------------
t1= time.time() #Startzeit speichern

# Init -----------------------
uda_dict = {
			# NAME : [0 NETWORK OBJECT, 1 LongName, 2 DecPlaces, 3 VALUE TYPE, 4 Comment        (, 5 DEFAULT, 6 FORMULA)] # Länge 5, 6 oder 7
														# ValueType_Int : 1
														# ValueType_Real : 2
														# ValueType_String : 5
														# ValueType_Bool : 9
														# ValueType_LongLength : 12
														# ValueType_ShortLength : 13
            # Achtung: NAME darf nicht mehrfach vergeben werden

			"Kreis_Nr"                         : ["Zones", "Kreis_Nr",                0, 1, 'PTV | TNN Raumzuordnung zu Kreisen,  Nummer | rechenrelevant' ],                                          # Beispiel Bezirksattr.
			"BL_Nr0"                           : ["Zones", "BL_Nr",                   0, 1, 'PTV | TNN Raumzuordnung zu Bundesland,  Nummer | rechenrelevant' ],                                       # Beispiel Bezirksattr.
			"NUTS0_Nr"                         : ["Zones", "NUTS0_Nr",                0, 5, 'PTV | TNN Raumzuordnung zu ausländischem Bezirk,  Nummer | rechenrelevant' ],                             # Beispiel Bezirksattr.
            "RO_PEK_Nr"                        : ["Zones", "RO_PEK_Nr",               0, 1, 'PTV | TNN PEK-Nr| rechenrelevant'],                                                              # Beispiel Bezirksattr.
            "RO_PEK_Code"                      : ["Zones", "RO_PEK_Code",             0, 5, 'PTV | TNN PEK-Code | rechenrelevant'],                                                              # Beispiel Bezirksattr.
			"TNN_Tochterbezirk_Nr"             : ["Zones", "TNN_Tochterbezirk_Nr",    0, 1, 'PTV | TNN Tochterbezirk Nummer | rechenrelevant' ],                                                       # Beispiel Bezirksattr.
            "TNN_Heimataufkommen_PV"           : ["Zones", "TNN_Heimataufkommen_PV",  2, 2, 'PTV | TNN Heimataufkommen Nachfragemodell PV | rechenrelevant' ],                                         # Heimataufkommen, je eines pro Nachfragemodell
            "TNN_Heimataufkommen_BM"           : ["Zones", "TNN_Heimataufkommen_BM",  2, 2, 'PTV | TNN Heimataufkommen Nachfragemodell BM | rechenrelevant' ],                                         # Heimataufkommen, je eines pro Nachfragemodell
            "TNN_Heimataufkommen_FH"           : ["Zones", "TNN_Heimataufkommen_FH",  2, 2, 'PTV | TNN Heimataufkommen Nachfragemodell FH | rechenrelevant' ],                                         # Heimataufkommen, je eines pro Nachfragemodell
            "TNN_Heimataufkommen_SVE"          : ["Zones", "TNN_Heimataufkommen_SVE", 2, 2, 'PTV | TNN Heimataufkommen Nachfragemodell SVE | rechenrelevant' ],                                         # Heimataufkommen, je eines pro Nachfragemodell
            "KALI_KORR_PENDLER"                : ["Zones", "Kali_Korr_Pendler",       2, 2, 'PTV | TNN Korrekturfaktor Pendlermatrix  | rechenrelevant'],                                              # wird für ext bW-Matrix verwendet, im Original pro OBez, Daten müssen auf Bezirksebene übertragen werden
            "KALI_KORR_PENDLER_WA"             : ["Zones", "Kali_Korr_Pendler_WA",    2, 2, 'PTV | TNN Korrekturfaktor Pendlermatrix  | rechenrelevant'],                                              # wird für ext bW-Matrix verwendet, im Original pro OBez, Daten müssen auf Bezirksebene übertragen werden
            "KALI_KORR_PENDLER_AW"             : ["Zones", "Kali_Korr_Pendler_AW",    2, 2, 'PTV | TNN Korrekturfaktor Pendlermatrix  | rechenrelevant'],                                              # wird für ext bW-Matrix verwendet, im Original pro OBez, Daten müssen auf Bezirksebene übertragen werden

			"TNN_Tochter_RO_PEK_Nr"           : ["MainZones", "TNN_Tochter_RO_PEK_Nr",           0, 1, 'PTV | TNN Tochter PEK-ID | rechenrelevant'],                                                            # Beispiel Oberbezirksattr.
			"TNN_Tochter_RO_PEK_Code"         : ["MainZones", "TNN_Tochter_RO_PEK_Code",         0, 5, 'PTV | TNN Tochter PEK-Code | rechenrelevant', '', 'TableLookup(TABLEENTRIES_PEK_DEFINITION UDTPEK, UDTPEK[NO]=[TNN_TOCHTER_RO_PEK_NR], UDTPEK[CODE])'], 
			"TNN_Tochter_RO_Gem_Nr"           : ["MainZones", "TNN_Tochter_RO_Gem_Nr",           0, 1, 'PTV | TNN Tochterbezirk Gemeindenummer | rechenrelevant'],                                                   
			"TNN_Tochter_RO_Kreis_Nr"         : ["MainZones", "TNN_Tochter_RO_Kreis_Nr",         0, 1, 'PTV | TNN Tochterbezirk Kreisnummer | rechenrelevant'],           
            "TNN_Tochter_RO_BL_Nr"            : ["MainZones", "TNN_Tochter_RO_BL_Nr",            0, 1, 'PTV | TNN Tochterbezirk Bundeslandnummer | rechenrelevant'],                                                                  
            "TNN_Tochter_RO_NUTS0_Nr"         : ["MainZones", "TNN_Tochter_RO_NUTS0_Nr",         0, 5, 'PTV | TNN Tochterbezirk Ausland-Nummer | rechenrelevant'],                                                                  
            "TNN_Tochter_RO_Raumtyp_Nr"       : ["MainZones", "TNN_Tochter_RO_Raumtyp_Nr",       0, 1, 'PTV | TNN Tochterbezirk Raumtypnr | rechenrelevant'],                                                      
            "MakroBez_Landkreis"              : ["MainZones", "MakroBez_Landkreis",              0, 1, 'PTV | TNN Tochterbezirk Landkreis | rechenrelevant'],                                           # wird in Erz mit Teilraumausgleich verwendet
            "MakroBez_Teilraum_Hochschule"    : ["MainZones", "MakroBez_Teilraum_Hochschule",    0, 1, 'PTV | TNN Teilraumzuordnung aus Mutterbezirk | rechenrelevant'],                                # wird in Erz mit Teilraumausgleich verwendet
            "MakroBez_Teilraum_KITA"          : ["MainZones", "MakroBez_Teilraum_KITA",          0, 1, 'PTV | TNN Teilraumzuordnung aus Mutterbezirk | rechenrelevant'],                                # wird in Erz mit Teilraumausgleich verwendet
            "MakroBez_Teilraum_Nahaktivitaet" : ["MainZones", "MakroBez_Teilraum_Nahaktivitaet", 0, 1, 'PTV | TNN Teilraumzuordnung aus Mutterbezirk | rechenrelevant'],                                # wird in Erz mit Teilraumausgleich verwendet
            "MakroBez_Teilraum_Nation"        : ["MainZones", "MakroBez_Teilraum_Nation",        0, 1, 'PTV | TNN Teilraumzuordnung aus Mutterbezirk | rechenrelevant'],                                # wird in Erz mit Teilraumausgleich verwendet            
            "MakroBez_Teilraum_Schulbezirk"   : ["MainZones", "MakroBez_Teilraum_Schulbezirk",   0, 1, 'PTV | TNN Teilraumzuordnung aus Mutterbezirk | rechenrelevant'],                                # wird in Erz mit Teilraumausgleich verwendet            
            "TNN_C_PARKKOSTEN"                : ["MainZones", "TNN_C_Parkkosten",                2, 2, 'PTV | TNN Parkosten gewichtet aus Mutterbezirk | rechenrelevant'],                              # wird bei KGM-berechnung verwendet              
            "TNN_C_PARKSUCHZEIT"              : ["MainZones", "TNN_C_Parksuchzeit",              2, 2, 'PTV | TNN Parksuchzeit gewichtet   | rechenrelevant'],                                          # wird bei KGM-berechnung verwendet              
            "TNN_UDA_PARKDRUCK"               : ["MainZones", "TNN_UDA_Parkdruck",               2, 2, 'PTV | TNN PArkdurck gewichtet   | rechenrelevant'],                                             # wird bei KGM-berechnung verwendet                         
            

            "TNN_PEK_Select0"                 : ["POIOFCAT_500", "TNN_PEK_Select",      0, 1, 'PTV | Einstellung, was dieser Teilraum im Tochtermodell sein soll: 1 - PG, 2- E, 3-Kordonbezirk | rechenrelevant'],  # Auswahl-Flag für Teilraum
            "TNN_PEK_Select1"                 : ["POIOFCAT_501", "TNN_PEK_Select",      0, 1, 'PTV | Setzung Rolle im Tochtermodell 1 - P, 2- E, 3-Kordonbezirk | rechenrelevant'],                                 # Auswahl-Flag für Teilraum
            "TNN_PEK_Select2"                 : ["POIOFCAT_502", "TNN_PEK_Select",      0, 1, 'PTV | Setzung Rolle im Tochtermodell 1 - P, 2- E, 3-Kordonbezirk | rechenrelevant'],                                 # Auswahl-Flag für Teilraum
            "TNN_PEK_Select3"                 : ["POIOFCAT_503", "TNN_PEK_Select",      0, 1, 'PTV | Setzung Rolle im Tochtermodell 1 - P, 2- E, 3-Kordonbezirk | rechenrelevant'],                                 # Auswahl-Flag für Teilraum
            "TNN_PEK_Select4"                 : ["POIOFCAT_504", "TNN_PEK_Select",      0, 1, 'PTV | Setzung Rolle im Tochtermodell 1 - P, 2- E, 3-Kordonbezirk | rechenrelevant'],                                 # Auswahl-Flag für Teilraum            
            "TNN_PEK_Select_Aggr0"            : ["POIOFCAT_502", "TNN_PEK_Select_Aggr", 0, 1, 'PTV | Setzung Aggr-Form im Tochtermod 0 - Originalbez übern , 1 Originalbez aggr | rechenrelevant'],            # Auswahl-Flag für Teilraum
            "TNN_PEK_Select_Aggr1"            : ["POIOFCAT_503", "TNN_PEK_Select_Aggr", 0, 1, 'PTV | Setzung Aggr-Form im Tochtermod 0 - Originalbez übern , 1 Originalbez aggr  | rechenrelevant'],           # Auswahl-Flag für Teilraum
            "TNN_PEK_Select_Aggr2"            : ["POIOFCAT_504", "TNN_PEK_Select_Aggr", 0, 1, 'PTV | Setzung Aggr-Form im Tochtermod 0 - Originalbez übern , 1 Originalbez aggr  | rechenrelevant'],           # Auswahl-Flag für Teilraum
            "AGS_0"                           : ["POIOFCAT_502", "AGS_0",               0, 5, 'PTV | TNN Kreis-ID  | rechenrelevant' ],                                                                             # Kreisattribute, für Import von shp-Dateien notwendig
            "AGS_1"                           : ["POIOFCAT_503", "AGS",                 0, 1, 'PTV | TNN Gemeinde-ID | rechenrelevant' ],                                                                           # Gemeindeattribute, für Import von shp-Dateien notwendig            
			"ARS_0"                           : ["POIOFCAT_502", "ARS_0",               0, 5, 'PTV | TNN | rechenrelevant' ],                                                                                       # Kreisattribute, für Import von shp-Dateien notwendig
			"BEM"                             : ["POIOFCAT_502", "BEM",                 0, 5, 'PTV | TNN | rechenrelevant' ],                                                                                       # Kreisattribute, für Import von shp-Dateien notwendig
			"BL_Nr1"                          : ["POIOFCAT_502", "BL_Nr",               0, 1, 'PTV | TNN Bundesland-ID|  rechenrelevant' ],                                                                         # Kreisattribute, für Import von shp-Dateien notwendig
			"GEN"                             : ["POIOFCAT_502", "GEN",                 0, 5, 'PTV | TNN | rechenrelevant' ],                                                                                       # Kreisattribute, für Import von shp-Dateien notwendig
			"NUTS"                            : ["POIOFCAT_502", "NUTS",                0, 5, 'PTV | TNN | rechenrelevant' ],                                                                                       # Kreisattribute, für Import von shp-Dateien notwendig
			"Bez"                             : ["POIOFCAT_503", "Bez",                 0, 5, 'PTV | TNN | rechenrelevant' ],                                                                                       # Gemeindeattribut, für Import von shp-Dateien notwendig            
			"BL_Nr1"                          : ["POIOFCAT_503", "BL_Nr",               0, 1, 'PTV | TNN Bundeslandnummer-Nr | rechenrelevant' ],                                                                                       # Gemeindeattribut, für Import von shp-Dateien notwendig            
			"RB_Nr"                           : ["POIOFCAT_503", "RB_Nr",               0, 1, 'PTV | TNN Regierungsbezirk-Nr| rechenrelevant' ],                                                                                       # Gemeindeattribut, für Import von shp-Dateien notwendig            
            "Kreis_KZ1"                       : ["POIOFCAT_503", "Kreis_KZ",            0, 5, 'PTV | TNN Kreiskennzahl | rechenrelevant' ],                                                                         # Gemeindeattribut, für Import von shp-Dateien notwendig            
            "Kreis_Nr1"                       : ["POIOFCAT_503", "Kreis_Nr",            0, 1, 'PTV | TNN Kreisnr| rechenrelevant' ],                                                                                       # Gemeindeattribut, für Import von shp-Dateien notwendig            
            "Gem_KZ1"                         : ["POIOFCAT_503", "Gem_KZ",              0, 5, 'PTV | TNN Gemeindekennzahl | rechenrelevant' ],                                                                      # Gemeindeattribut, für Import von shp-Dateien notwendig            
            "Kreis_KZ2"                       : ["POIOFCAT_504", "Kreis_KZ",            0, 5, 'PTV | TNN Kreiskennzahl | rechenrelevant' ],                                                                         # Gemeindeattribut, für Import von shp-Dateien notwendig            
            "Kreis_Nr2"                       : ["POIOFCAT_504", "Kreis_Nr",            0, 1, 'PTV | TNN Kreisnr | rechenrelevant' ],                                                                                       # Gemeindeattribut, für Import von shp-Dateien notwendig            
            "Gem_KZ2"                         : ["POIOFCAT_504", "Gem_KZ",              0, 5, 'PTV | TNN Gemeindekennzahl | rechenrelevant' ],                                                                      # Gemeindeattribut, für Import von shp-Dateien notwendig            
            "BL_Nr2"                          : ["POIOFCAT_504", "BL_Nr",               0, 1, 'PTV | TNN Bundeslandnummer | rechenrelevant' ],                                                                                       # Gemeindeattribut, für Import von shp-Dateien notwendig            

			"TNN_Anbindung_Gewicht_RAD"       : ["Connectors", "TNN_Anbindung_Gewicht_RAD",  2, 2, 'PTV | TNN Gewicht Rad-Anbindung | rechenrelevant'],                                                         # Beispiel Anbindung
			"TNN_Anbindung_Gewicht_PKW"       : ["Connectors", "TNN_Anbindung_Gewicht_PKW",  2, 2, 'PTV | TNN Gewicht PKW-Anbindung | rechenrelevant'],                                                  
			"TNN_Anbindung_Gewicht_LKW"       : ["Connectors", "TNN_Anbindung_Gewicht_LKW",  2, 2, 'PTV | TNN Gewicht LKW-Anbindung | rechenrelevant'],                                                  
			"TNN_Anbindung_Gewicht_OEV"       : ["Connectors", "TNN_Anbindung_Gewicht_OEV",  2, 2, 'PTV | TNN Gewicht OEV-Anbindung | rechenrelevant'],                                                  
            "TNN_Anbindung_AnzAggAnbind"      : ["Connectors", "TNN_Anbindung_AnzAggAnbind", 2, 2, 'PTV | TNN Anzahl aggr Anbindungen zur Kontrolle | Info'],                                           
                                                                                                                                                                                                        
			"TNN_Calc"                        : ["DemandStrata", "TNN_Calc",                    0, 1, 'PTV | TNN Berechnung ja=1,  nein=0 | rechenrelevant', '1'],                                            # Beispiel Nachfrageschicht, hier Flag zu berechnung URA
			"TNN_QZG3SubTyp"                  : ["DemandStrata", "TNN_QZG3SubTyp",              0, 1, 'PTV | TNN SubTyp für QZG-Typ 3, Setzung = 1,1 | rechenrelevant'],                                      #  Unterscheidung QZG-Typ für Berechn URA
            "TNN_Sum_NSch_Erzeugungsraum"     : ["DemandStrata", "TNN_Sum_NSch_Erzeugungsraum", 2, 2, 'TNN | Sicherung Aufkommen nur Erzeugungsraum Tochter| relevant'],                                      # Hilfswert MS-berechnung
            "TNN_Sum_NSch"                    : ["DemandStrata", "TNN_Sum_NSch",                2, 2, 'TNN | Sicherung Aufkommen Mutterraum| relevant'],                                                      # Hilfswert MS-Berechnung
            "TNN_MatNr_NSch"                  : ["DemandStrata", "TNN_MatNr_NSch",              0, 1, 'TNN | Nr der relevanten Nachfragematrix für NSch | relevant'],                                         # Hilfswert MS-Berechnung
            "TNN_MatNr_AktP"                  : ["DemandStrata", "TNN_MatNr_AktP",              0, 1, 'TNN | Nr der relevanten Nachfragematrix für AktPaar | relevant'],                                      # Hilfswert MS-Berechnung
            "TNN_Heimataufkommen"             : ["DemandStrata", "TNN_Heimataufkommen",         2, 2, 'PTV | Heimataufkommen'],                                                                               # 
            
            
            "TNN_Tochter_MatCode"         : ["Matrices",     "TNN_Tochter_MatCode",     0, 5, 'PTV | TNN Matrixcode für Tochterversion  | rechenrelevant']                                                    # Matrixnamen der zu importierenden Matrizen
			} # Ende Dict-Definition

# Alle Attribute für Teilraumausgleich
# Suche nach Namensbestandteil 'Teilraum' und nur wenn kein Formelattribut
uda_teilraumausgleich_dict = {i.ID : ["MainZones", i.Code, 0, 1, 'PTV | TNN Tochter Zuordnung zu Teilraum für Teilraumausgleich | rechenrelevant'] for i in Visum.Net.Zones.Attributes.GetAll if ("TEILRAUM" in i.ID) and (i.Editable == True) }

uda_dict.update( uda_teilraumausgleich_dict )


for key, value in uda_dict.items():

    if value[0] == 'Net':
        aktObjekt = getattr(Visum, value[0])  		#getattr() setzt Befehl aus Strings zusammen: --> getattr('Visum.Workbench.Lists', NameCOMBefehlStreckenListeAnlegen_als_string) ergibt Visum.Workbench.Lists.CreateLinkList
    elif value[0].startswith('POIOFCAT'):
        cat=value[0].split("_")[1]
        aktObjekt = Visum.Net.POICategories.ItemByKey(cat).POIs  		#getattr() setzt Befehl aus Strings zusammen: --> getattr('Visum.Workbench.Lists', NameCOMBefehlStreckenListeAnlegen_als_string) ergibt Visum.Workbench.Lists.CreateLinkList
    else:
        aktObjekt = getattr(Visum.Net, value[0])

    if aktObjekt.AttrExists(value[1]) == False:  # Abfrage, Ob Attribut schon existiert, dann wird übersprungen
        if len(value) == 5:
            aktObjekt.AddUserDefinedAttribute(ID=value[1],
                                                  ShortName=value[1],
                                                  LongName=value[1],
                                                  VT=value[3],
                                                  DecPlaces=value[2])

        elif len(value) == 6:
            aktObjekt.AddUserDefinedAttribute(ID=value[1],
                                                  ShortName=value[1],
                                                  LongName=value[1],
                                                  VT=value[3],
                                                  DecPlaces=value[2],
                                                  DefVal=value[5])
        else: #len(value)==7
            aktObjekt.AddUserDefinedAttribute(ID=value[1],
                                                  ShortName=value[1],
                                                  LongName=value[1],
                                                  VT=value[3],
                                                  DecPlaces=int(value[2]),
                                                  DefVal=value[5],
                                                  Formula=value[6])

        aktObjekt.Attributes.ItemByKey(value[1]).Comment=value[4] # Kommentar füllen
    # Ende if AttrExist() ......
#Ende for..

# Finalisierung / Aufräumen -----------
Visum.Log(20480, f"Initiale bda angelegt. {str(round(time.time()-t1))} sec.")

# VALUE TYPE
# 1 int, 2 -dez, 5 test