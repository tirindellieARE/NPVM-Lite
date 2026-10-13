#--------------------------------------------------------------------------------------------------------------------------------------------
# Die Siko-Attribute haben den Aufgabe, Umlegungsergebnisse zu sichern z.B. für einen graphischen Vergleich,
# selbst wenn die Umlegung initialisiert ist
# Die Anzahl und Name der bdA ergibt sich aus den NSeg und VSys-Namen der Version und unterscheiden sich von Modell zu Modell , 
# werden teilweise ausgelesen
# 
# bdA-Werte werden angelegt, der bdA- Kommentar wird einheitlich gesetzt
#
# PTV Transport Consult, BD
#
#---------------------------------------------------------------------------------------------------------------------------------------------
 
 
# Nutzereinstellung -----------------------------------------------------
 
Modus_FGV_Code ="F" # wie ist der Code für den Fußgängermodus?
Modus_OEV_Code ="X" # wie ist der Code für den ÖV-Modus?

VSys_FGV_Code ="F" # wie ist der Code für das FGV-VSys?

 
 
# Initialisierung -------------------------------------------------------
Modi=[]
NSeg=[]
ModiList_nur_OEV=[Modus_OEV_Code]
z=0
 
# Berechnung ------------------------------------------------------------

#Angebotsversion erkennen    
if Visum.Net.Lines.Count == 0:
    OEVAngebot = False
else:
    OEVAngebot = True

if Visum.Net.Links.Count == 0:    
    IVAngebot = False
else:
    IVAngebot = True
    
 
ModiList=[i.AttValue("Code") for i in Visum.Net.Modes.GetAll if i.AttValue("Code") != Modus_FGV_Code]
NSegList=[i.AttValue("Code") for i in Visum.Net.DemandSegments.GetAll if (Modus_FGV_Code not in i.AttValue("Code")) 
                                                                          and ('GES' not in i.AttValue("Code"))
                                                                          and (i.AttValue("Code").startswith('TTN') == False)]
VSysList=[i.AttValue("Code") for i in Visum.Net.TSystems.GetAll if i.AttValue("Code") != VSys_FGV_Code]
NSegList_nur_OEV=[i.AttValue("Code") for i in Visum.Net.DemandSegments.GetAll if (Modus_OEV_Code in i.AttValue("Code")) 
                                                                           and (i.AttValue("Code").startswith('TTN') == False)]
VSysList_nur_OEV=[i.AttValue("Code") for i in Visum.Net.TSystems.GetAll if i.AttValue("Type") == "PUT" ]
 
 
# Strecken und Anbindungen -------------------
# alte löschen
loeschen=[i.ID for i in Visum.Net.Links.Attributes.GetAll if i.ID.startswith("SIKO_") ]
for i in loeschen:
    Visum.Net.Links.DeleteUserDefinedAttribute(i)

#anlegen
for n in NSegList:
    n = n.replace(" ", "_").replace("+", "_Plus")
    NameUDA="SiKo_"+n
    if Visum.Net.Links.AttrExists(NameUDA)==False:
        Visum.Net.Links.AddUserDefinedAttribute(NameUDA, NameUDA, NameUDA, 2) #2=Datentyp real
        z=z+1
    if Visum.Net.Connectors.AttrExists(NameUDA)==False:
        z=z+1
        Visum.Net.Connectors.AddUserDefinedAttribute(NameUDA, NameUDA, NameUDA, 2) #2=Datentyp real
 
# Spezialfälle ÖV:
if OEVAngebot:
    # 1. Servicefahrten auf Strecken -----------------
    NameUDA="SiKo_AnzahlServicefahrten"
    if Visum.Net.Links.AttrExists(NameUDA)==False:
        Visum.Net.Links.AddUserDefinedAttribute(NameUDA, NameUDA, NameUDA, 1) #2=Datentyp int
     
    # 2. Linien und Haltestellen -----------------
    loeschen=[i.ID for i in Visum.Net.Lines.Attributes.GetAll if i.ID.startswith("SIKO_") ]
    for i in loeschen:
        Visum.Net.Lines.DeleteUserDefinedAttribute(i)
    loeschen=[i.ID for i in Visum.Net.Stops.Attributes.GetAll if i.ID.startswith("SIKO_") ]
    for i in loeschen:
        Visum.Net.Stops.DeleteUserDefinedAttribute(i)
        
    #Attribute je NSeg
    for n in NSegList_nur_OEV:
        n = n.replace(" ", "_").replace("+", "_Plus")
        NameUDA="SiKo_NSeg_"+n
        if Visum.Net.Lines.AttrExists(NameUDA) == False:
            z=z+1
            Visum.Net.Lines.AddUserDefinedAttribute(NameUDA, NameUDA, NameUDA, 2) #2=Datentyp real
        if Visum.Net.Stops.AttrExists(NameUDA) == False:
            z=z+1
            Visum.Net.Stops.AddUserDefinedAttribute(NameUDA, NameUDA, NameUDA, 2) #2=Datentyp real
    
     
    #Attribute je VSys
    for n in VSysList_nur_OEV:
        n = n.replace(" ", "_").replace("+", "_Plus")
        NameUDA="SiKo_VSys_"+n
        if Visum.Net.Stops.AttrExists(NameUDA) == False:
            z=z+1
            Visum.Net.Stops.AddUserDefinedAttribute(NameUDA, NameUDA, NameUDA, 2) #2=Datentyp real
    
    NameUDA = "SiKo_OEV_GES"
    if Visum.Net.Lines.AttrExists(NameUDA) == False:
            z=z+1
            Visum.Net.Lines.AddUserDefinedAttribute(NameUDA, NameUDA, NameUDA, 2) #2=Datentyp real
            
    if Visum.Net.Stops.AttrExists(NameUDA) == False:
            z=z+1
            Visum.Net.Stops.AddUserDefinedAttribute(NameUDA, NameUDA, NameUDA, 2) #2=Datentyp real 

#  Ende öV Spezialfälle
     
# bdA-Kommentar für alle Attribute beschreiben -------------- 
ComText="PTV | Attribut zur Sicherung der Umlegungsergebnisse | auswertungsrelevant, nicht löschen"
 
AlleSiKos=[i.ID for i in Visum.Net.Lines.Attributes.GetAll if i.ID.startswith("SIKO")]
for a in AlleSiKos:
    Visum.Net.Lines.Attributes.ItemByKey(a).Comment=ComText
 
AlleSiKos=[i.ID for i in Visum.Net.Links.Attributes.GetAll if i.ID.startswith("SIKO")]
for a in AlleSiKos:
    Visum.Net.Links.Attributes.ItemByKey(a).Comment=ComText
 
AlleSiKos=[i.ID for i in Visum.Net.Connectors.Attributes.GetAll if i.ID.startswith("SIKO")]
for a in AlleSiKos:
    Visum.Net.Connectors.Attributes.ItemByKey(a).Comment=ComText
 
AlleSiKos=[i.ID for i in Visum.Net.Stops.Attributes.GetAll if i.ID.startswith("SIKO")]
for a in AlleSiKos:
    Visum.Net.Stops.Attributes.ItemByKey(a).Comment=ComText
 
 
# Finalisierung / Aufräumen -----------
 
Visum.Log(20480, str(z)+" bda für SiKo angelegt.")