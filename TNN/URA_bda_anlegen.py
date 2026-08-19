# bdA für Untersuchungsraumanteile anlegen, das umfasst:
# für Bezirke, je ein UDA für URA für {HV, QV, ZV} x {PG|SG} anlegen
# für NSch je ein UDA für {HV, QV, ZV}
# Setzen der Bezirksattributnamen in das Nachfrageschichtattribut

# bdA-Werte werden angelegt, der bdA- Kommentar wird einheitlich gesetzt
# PTV Transport Consult, BD

# Nutzereinstellung -----------------------------------------------------
HQZTyp_List=["HV","QV","ZV"] # Heimataufkommen, Quellaufkommen, Zielaufkommen
 
# Initialisierung -------------------------------------------------------
z=0
 
# Berechnung ------------------------------------------------------------
# hier für alle Nachfrageschichten der Nachfragemodelle vom Nachfragemodelltyp "EVA-P", 

NSchList=[i.AttValue("Code") for i in Visum.Net.DemandStrata.GetAll if  i.AttValue("DEMANDMODEL\TYPE") == 'EVA-P']

# Bezirks-bda anlegen 
for t in HQZTyp_List:
    for n in NSchList:
        NameUDA="URA_"+n+"_"+t
        if Visum.Net.Zones.AttrExists(NameUDA)==False:
            Visum.Net.Zones.AddUserDefinedAttribute(NameUDA, NameUDA, NameUDA, 2) #2=Datentyp real
            Visum.Net.Zones.Attributes.ItemByKey(NameUDA).Comment="TNN | Bezirks-bda für Untersuchungsraumanteile je Nachfrageschicht | relevant Teilnetznachfrage"
            z=z+1  

# NSch-bda anlegen 
for t in HQZTyp_List:
    NameUDA="UDA_URA_"+t
    if Visum.Net.DemandStrata.AttrExists(NameUDA)==False:
        Visum.Net.DemandStrata.AddUserDefinedAttribute(NameUDA, NameUDA, NameUDA, 5) #5 = Datentyp Text
        Visum.Net.DemandStrata.Attributes.ItemByKey(NameUDA).Comment="TNN | Name des Bezirks-bda für Untersuchungsraumanteile  | relevant Teilnetznachfrage"
        z=z+1

# in NSch-Attribut den Bezirks-bda-Namen setzen
for t in HQZTyp_List:
    for n in NSchList:
        NameBezUDA="URA_"+n+"_"+t
        Visum.Net.DemandStrata.ItemByKey(n).SetAttValue("UDA_URA_"+t,"URA_"+n+"_"+t) 
        

# Finalisierung / Aufräumen -----------
 
Visum.Log(20480, str(z)+" Bezirks- und Nachfrageschicht-bdA für URA-Daten angelegt und Namen zugeoardnet.")