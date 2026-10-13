#--------------------------------------------------------------------------------------------------------------------------------------------
# Die Siko-Attribute haben den Aufgabe, Umlegungsergebnisse zu sichern z.B. für einen graphischen Vergleich,
# selbst wenn die Umlegung initialisiert ist
#
# Daten werden kopiert aus den Visum-Standardattributen
#
# PTV Transport Consult, BD
#
#---------------------------------------------------------------------------------------------------------------------------------------------
 
# Spezial-ÖV: Anzahl Servicefahrten
# für alle Umlegungsmodi außer FGV
# Für NSeg und VSys außer FGV
 
# Bibliotheken      -----------------------------------------------------
 
import VisumPy.helpers as VPH
import time
  
 
# Nutzereinstellung -----------------------------------------------------
#für Sonderfälle indentifizieren
# Setzung für NPVM
Modus_FGV_Code ="FGV" # wie ist der Code für den Fußgängermodus?
Modus_OEV_Code ="X" # wie ist der Code für den ÖV-Modus?
VSys_FGV_Code ="FGV" # wie ist der Code für den Fußgänger-VSys?
#VSys_OEV_Code ="X" # wie ist der Code für den ÖV-VSys?
 
 
# Initialisierung -------------------------------------------------------
t1 = time.time()
 
# Berechnung ------------------------------------------------------------
 
#Angebotsversion erkennen
if Visum.Net.Lines.Count == 0:
    OEVAngebot = False
else:
    OEVAngebot = True
    

if OEVAngebot:
    
    # Einsteiger Haltestellen -----------
     
     
    #ToDo Mittelwerte EA rechnen
    Namen_H_Einst =["PASSBOARD(AP)"]
    Namen_H_Einst_NSeg=["PASSBOARD_DSEG(" + i.AttValue("Code") +",AP)" for i in Visum.Net.DemandSegments.GetAll if (Modus_OEV_Code in i.AttValue("Code")) and ("GES" not in i.AttValue("Code")) and (i.AttValue("Code").startswith('TTN') == False)]
    Namen_H_Einst_VSys=["PASSBOARD_TSYS(" + i.AttValue("Code") +",AP)" for i in Visum.Net.TSystems.GetAll if i.AttValue("Type")=="PUT"]
     
    Namen_H_Einst_alle = Namen_H_Einst + Namen_H_Einst_NSeg + Namen_H_Einst_VSys
    
    NamenSiko_H_Einst = ['SIKO_OEV_GES']   
    NamenSiko_H_Einst_NSeg=[i.ID for i in Visum.Net.Stops.Attributes.GetAll if i.ID.startswith("SIKO_NSEG_") and ("GES" not in i.ID)]   # Untergruppen nur NSeg
    NamenSiko_H_Einst_VSys=[i.ID for i in Visum.Net.Stops.Attributes.GetAll if i.ID.startswith("SIKO_VSYS_") and ("GES" not in i.ID)]   # Untergruppen nur VSYs
     
    NamenSiko_H_Einst_alle = NamenSiko_H_Einst + NamenSiko_H_Einst_NSeg + NamenSiko_H_Einst_VSys
     
    werte=VPH.GetMultipleAttributesRaw(Visum, Visum.Net.Stops, Namen_H_Einst_alle, activeOnly = False, into_np_array = None) # Daten lesen
     
    VPH.SetMultipleAttributesRaw(Visum, Visum.Net.Stops, NamenSiko_H_Einst_alle, werte, activeOnly = False)  #Daten schreiben
     
     
    # LinBef der ÖV-Linien   ----------------------
     
     
    NamenSiko_Lin_LinBef=[i.ID for i in Visum.Net.Lines.Attributes.GetAll if i.ID.startswith("SIKO") and ("GES" not in i.ID) ]
     
    Namen_Lin_NSeg = ["PTRIPSUNLINKED_DSEG(" + i.AttValue("Code") +",AP)" for i in Visum.Net.DemandSegments.GetAll if Modus_OEV_Code in i.AttValue("Code") and "GES" not in i.AttValue("Code") and (i.AttValue("Code").startswith('TTN') == False)]
     
    werte = VPH.GetMultipleAttributesRaw(Visum, Visum.Net.Lines, Namen_Lin_NSeg, activeOnly = False, into_np_array = None) # Daten lesen
     
    VPH.SetMultipleAttributesRaw(Visum, Visum.Net.Lines, NamenSiko_Lin_LinBef, werte, activeOnly = False)   #Daten schreiben
    
    # Anzahl Servicefahrten
    NamenSiko_S_Servicefahrten = [i.ID for i in Visum.Net.Links.Attributes.GetAll if (i.ID.startswith("SIKO")) and ("SERVICEFAHRTEN" in i.ID)]
    Namen_S_Servicefahrten     = ["NUMSERVICETRIPS(AP)"]
    
    werte = VPH.GetMultipleAttributesRaw(Visum, Visum.Net.Links, Namen_S_Servicefahrten, activeOnly = False, into_np_array = None)
     
    VPH.SetMultipleAttributesRaw(Visum, Visum.Net.Links, NamenSiko_S_Servicefahrten, werte, activeOnly = False)   #Daten schreiben
 
# Ende if OEVAngebot:

 
# Anbindungen   ----------------------
 
NamenSiko_Anb_Bel=[i.ID for i in Visum.Net.Connectors.Attributes.GetAll if i.ID.startswith("SIKO") and ("GES" not in i.ID)]
 
Namen_Anb_NSeg = ["VOLPERS_DSEG(" + i.AttValue("Code") +",AP)" for i in Visum.Net.DemandSegments.GetAll if (Modus_FGV_Code not in i.AttValue("Code")) and ("GES" not in i.AttValue("Code")) and (i.AttValue("Code").startswith('TTN') == False)]
#VOLPERS_DSEG(PKW_FB,AP)    #Beispiel
 
werte=VPH.GetMultipleAttributesRaw(Visum, Visum.Net.Connectors, Namen_Anb_NSeg, activeOnly = False, into_np_array = None) # Daten lesen
 
VPH.SetMultipleAttributesRaw(Visum, Visum.Net.Connectors, NamenSiko_Anb_Bel, werte, activeOnly = False) #Daten schreiben
 

# Strecken   ----------------------
NamenSiko_S_Bel_NSeg=[i.ID for i in Visum.Net.Links.Attributes.GetAll if (i.ID.startswith("SIKO")) and ("GES" not in i.ID) and ("SERVICEFAHRTEN" not in i.ID)]
 
#Beispiel: VOLPERS_DSEG(L120_QZD,AP)
Namen_S_Bel_NSeg = ["VOLPERS_DSEG(" + i.AttValue("Code") +",AP)" for i in Visum.Net.DemandSegments.GetAll if (Modus_FGV_Code not in i.AttValue("Code") ) and ("GES" not in i.AttValue("Code")) and (i.AttValue("Code").startswith('TTN') == False)]
 
werte=VPH.GetMultipleAttributesRaw(Visum, Visum.Net.Links, Namen_S_Bel_NSeg, activeOnly = False, into_np_array = None) # Daten lesen
 
VPH.SetMultipleAttributesRaw(Visum, Visum.Net.Links, NamenSiko_S_Bel_NSeg, werte, activeOnly = False)   #Daten schreiben
 

 
# Finalisierung / Aufräumen--------------------- 
Visum.Log(20480,"SiKo-Werte kopiert " +str(round(time.time()-t1,1))+" sec.")