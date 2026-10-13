# Auswertung der Heimataufkommen pro Bezirk, Nachfrageschicht und Nachfragemodell
#  Anlegen der notwendigen bda passiert im Initialen Block
# Heimataufkommen wird benötigt für Aggregation z.B. von Affinitätsfaktoren
# EP und BD

import pandas as pd
import time
import sys

# Nutzereinstellungen VORHER
# uda für NSch ist "Heimataufkommen"	# Nachfrageschichten-uda für Summenwert; muss angelegt sein
# uda für Bezirke müssen angelegt sein in der Form: Heimataufkommen_Modell1Code, Heimataufkommen_Modell2Code,...
bool_Visem=False


# Initialisierung -------------------------------------------------------

t1=time.time() #Startzeit

if Visum.Net.DemandModels.Count > 0: # Nachfragemodell vorhanden
        
    Visum.Filters.ZoneFilter().UseFilter = False    
       
    Visum.Log(20480, "Start Berechnung Heimataufkommen...")
    
    vn=Visum.Net
    AlleNSch = vn.DemandStrata
    
    
    list_NSchCodes = [i.AttValue("Code") for i in vn.DemandStrata.GetAll]
    list_DemModCodes= [i.AttValue("Code") for i in vn.DemandModels.GetAll]
    list_Leer=[0]*len(list_DemModCodes)
    dict_DemMod_DemNSch=dict(zip(list_DemModCodes,list_Leer))
    
    
    for einDemMod in dict_DemMod_DemNSch:
        dict_DemMod_DemNSch[einDemMod]=[i.AttValue("Code") for i in vn.DemandModels.ItemByKey(einDemMod).DemandStrata.GetAll]
    
    list_ZoneNbs = [i.AttValue("NO") for i in vn.Zones.GetAll]
    
    # Anlegen von NSch-bda -----------------------------
    aktObjekt = Visum.Net.DemandStrata
    udaName = f"TNN_Heimataufkommen"
    if aktObjekt.AttrExists(udaName) == False:  # Abfrage, Ob Attribut schon existiert, dann wird übersprungen
       aktObjekt.AddUserDefinedAttribute(udaName, udaName, udaName, 2, 2)
       aktObjekt.Attributes.ItemByKey(udaName).Comment = f"PTV | TNN Heimataufkommen der Nachfrageschicht (Muttermodell) {einDemMod} | rechenrelevant " # Kommentar füllen
    
    # Anlegen von Bezirks-bda -----------------------------
    aktObjekt = Visum.Net.Zones
    for einDemMod in list_DemModCodes:
       udaName = f"TNN_Heimataufkommen_{einDemMod}"
       if aktObjekt.AttrExists(udaName) == False:  # Abfrage, Ob Attribut schon existiert, dann wird übersprungen
           aktObjekt.AddUserDefinedAttribute(udaName, udaName, udaName, 2, 2)
           aktObjekt.Attributes.ItemByKey(udaName).Comment = f"PTV | TNN Heimataufkommen des Nachfragemodells (Muttermodell) {einDemMod} | rechenrelevant " # Kommentar füllen
    
            
    list_udaBez_HV_x_NachModell = ["TNN_Heimataufkommen_" + str(i.AttValue("Code")) for i in vn.DemandModels.GetAll] #Heimataufkommen_PV, Heimataufkommen_ANAB, ....
    HeimatAufk_Attributnamen = ["Hometrips(" + str(i.AttValue("Code")) + ")" for i in vn.DemandStrata.GetAll]
    list_AktKettenLaenge_proNSch=[len(i.AttValue("Code"))-1 for i in vn.DemandStrata.GetAll]
    
    if bool_Visem:
    	# Im Visem-Modell steht im Attribute Heimataufkommen nur die Zahl der Wegeketten
    	kettenlaenge=Visum.Net.DemandStrata.GetMultipleAttributes(["Code","ACTIVITYCHAINCODE"])
    	kettenlaenge=[len(i[1])-1 for i in kettenlaenge]
    else:
    	kettenlaenge=[1]*len(list_NSchCodes)	# Für EVA-Modell : 1-Vektor
    
    df = pd.DataFrame(Visum.Net.Zones.GetMultipleAttributes(HeimatAufk_Attributnamen, OnlyActive=False), columns=HeimatAufk_Attributnamen)
    df = kettenlaenge*df 
    
                                                 
                                                      
    #Spaltensumme über alle Bezirke  -----------------------
    #= Aufkommen der Nachfrageschicht
    
    df_spaltensumme = df.sum(axis=0) 
    
    # Spaltensumme als NSch-Attribut schreiben
    x = list(zip(list_NSchCodes, df_spaltensumme.to_list()))
    #Visum.Log(20480, x)
    vn.DemandStrata.SetMultipleAttributes(["Code", "TNN_Heimataufkommen"], x, False)
    
    
    # Zeilensumme pro Nachfragemodell in Bezirksattribut schreiben --------------------
    # = Aufkommen des Bezirkes
    
    # Pro Nachfragemodell: List mit NSchNamen, die nicht zum akt. Nachfragemodell gehören
    for einDemMod in list_DemModCodes:
    	#Visum.Log(20480, einDemMod )
    	#Spaltennamen erzeugen, die gelöscht werden sollen; dazu überzählige NSch ermitteln
    	del_list=["Hometrips(" + str(i)+")" for i in list_NSchCodes if i not in dict_DemMod_DemNSch[einDemMod]]
    	#Visum.Log(20480, del_list )
    	#reduziertes_df=df.copy(deep=True)
    	reduziertes_df=df.drop(del_list, axis=1)	#überflüssige Spalten löschen
    
    	df_zeilensumme = reduziertes_df.sum(axis=1) # Summe über NSch akt. NachMod
    	y = list(zip(list_ZoneNbs, df_zeilensumme.to_list()))
    	Spaltennamen=["ADDVAL1","TNN_Heimataufkommen_"+str(einDemMod)]
    	#Visum.Log(20480, Spaltennamen)
    
    	vn.Zones.SetMultipleAttributes(Spaltennamen, y, False)
    
    Visum.Filters.ZoneFilter().UseFilter =True
    
else:
    Visum.Log(20480, "Berechnung Heimataufkommen nicht notwenig, weil kein Nachfragemodell vorhanden...") # nur Netzversion

# Aufräumen /Finalisierung-------------------------
Visum.Log(20480,"Ende Berechnung TNN_Heimataufkommen, Zeitverbrauch " +str(round(time.time()-t1,1))+" sec.")
