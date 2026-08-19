#-------------------------------------------------------------------------------
# Purpose:     Export zone data as input for demand model
#
# Author:      birgit dugge
#
# Created:     Nov 2024 in V 24-10
#
# HInweise siehe unten
#-------------------------------------------------------------------------------

# Python-Bibliotheken -------
import csv
import os
import pandas as pd
import time         # für Zeitvergleich

# Initialisierung-------

t1= time.time() #Startzeit speichern
udtName = "TNN_Strukturgroessen"

# besondere Attribute, die nicht ins Schema der 'normalen' SG passen, weil anders aggregiert, andere Zahl Deziamlstellen o.ä.
AttGruppen_dict = {} # im NRW-Modell gibt es keine "besonderen" StruGroe

# falls es besondere SG gibt, dann hier Liste einpflegen
# Codierung der Aggregationsfunktion wie für Listen.AddColumn() für Visum-Listen
#AttGruppen_dict = {#"Gruppenname "       : [0[Liste der Attributnamen],           1'GroupOrAggrFunction', 2'WeightedAvgAttribute'],
                   # 'SG_MOTOGRAD'        : [[ 'VALSTRUCTURALPROP(SG_MOTOGRAD)'],  6, 'VALSTRUCTURALPROP(SG_EW)']   #6 Gew Mittel für Motorisierungsgrad (Sonderfall für SG)
#                   }

# Berechnung -----------
# dict mit Attributnamen und Spalteninformationen erzeugen

vorhandene_bdA=[]
for key, value in AttGruppen_dict.items():
    vorhandene_bdA = vorhandene_bdA + value[0]

hlp_sg_Namen=[f'VALSTRUCTURALPROP({i.AttValue("Code").upper()})' for i in Visum.Net.StructuralProps.GetAll]

# doppelte AttNamen-Nennung entfernen
sg_Namen = [i for i in hlp_sg_Namen if i not in vorhandene_bdA]

standardAtt_dict = {#"Gruppenname "   : [0[Liste der Attributnamen],  1'Format' , 2'DecPlaces' , 3'DisplayUnits' , 4'GroupOrAggrFunction', 5'WeightedAvgAttribute'],
                     'Standard_SG'          : [ sg_Namen,                   5, '']   #5 = Summe-Anweisung für 'normale' Strukturgröße, 
                   }

AttGruppen_dict.update(standardAtt_dict)
#attNamen_list = [ i[0] for i in AttGruppen_dict.values() ] # hier entsteht eine geschachtelte Liste
attNamen_list = [att for i in AttGruppen_dict.values() for att in i[0]] # durch doppelte Schleife entsteht gleich eine flache Liste

#Filter setzen auf die Bezirke des Erzeugungsraumes
Visum.Filters.ZoneFilter().Init()
Visum.Filters.ZoneFilter().UseFilter=True
Visum.Filters.ZoneFilter().AddCondition("OP_None", False, "MAINZONE\TNN_TOCHTER_RO_PEK_NR", "LessVal", 3)

bez_Daten_list = Visum.Net.Zones.GetMultipleAttributes( ['NO', 'MAINZONENO'] + attNamen_list , True) # nur Aktive Bezirke
df_bez = pd.DataFrame(bez_Daten_list, columns = ['NO', 'MAINZONENO'] + attNamen_list)

df_OBez=df_bez.groupby('MAINZONENO').agg( AnzMutterBez = ('NO', 'size')).reset_index() #Ergebnis df-Anlegen und mit einer Spalte füllen

# Summe für Standarattribute berechnen, "besondere Attribute" fehlt hier noch
for att in hlp_sg_Namen:
    
    #df_bez['SP']=df_bez[value]*df_bez[key] # Summenprodukt Hilfswert := Stukturgröße (als Gewicht) * Wert
    
    df_gruppiert = df_bez.groupby('MAINZONENO').agg(
        AnzMutterBez = ('NO', 'size'), # Anzahl der Elemente pro Gruppe
        Sum_W  = (att,  'sum'),          # Summe der Werte pro Gruppe (Summe der Rate)

        ).reset_index()
    
    df_gruppiert[att] = df_gruppiert.apply(
        lambda row: row['Sum_W'] ,  axis=1 
    ) # Rechenanweisung in lamda-Funktion: Einfach Summe 
    df_OBez[att]=df_gruppiert[att]
    

# Export: bdt Anlegen, bda hinzufügen, Daten übertragen...
if len([i.AttValue("Name") for i in Visum.Net.TableDefinitions.GetAll if i.AttValue("Name") == udtName]) == 1: # Prüfung, ob eine Tab gleichen namens existiert
    Visum.Net.RemoveTableDefinition(Visum.Net.TableDefinitions.ItemByKey(udtName))
t=Visum.Net.AddTableDefinition(udtName)

cols_dict={i.replace('(', '/').replace(')', '/').replace(', ', '---'): i for i in df_OBez.columns.tolist()}  # für bda.ID : Leerzeichen, Komma und Klammern ersetzen
for key, value in cols_dict.items():
    if Visum.Net.Zones.AttrExists(value.upper()): # Datentyp im original ermitteln
        vt_orig=Visum.Net.Zones.Attributes.ItemByKey(value.upper()).ValueType
    else:
        vt_orig = 2   # Datentyp Real für sonstige Attribute
   
    t.TableEntries.AddUserDefinedAttribute(key, value, value, vt_orig)

t.AddMultiTableEntries(df_OBez['MAINZONENO'].tolist())                                                 # n TE = Datensätze  anlegen mit OBezNr als Schlüssel
t.TableEntries.SetMultipleAttributes(list(cols_dict.keys()), df_OBez.values.tolist(), OnlyActive=False) # Werte Setzen

# Init Bezirksfilter
Visum.Filters.ZoneFilter().Init()
Visum.Filters.ZoneFilter().UseFilter = False

# Aufräumen /Finalisierung-------------------------
Visum.Log(20480,"Export Strukturgrößen fertig, " +str(round(time.time()-t1))+" sec.")    

# Hinweis: 
# bei manchen Modellen sind unter Strukturdaten auch Daten eingehängt, die nicht summiert sonndern gemittelt werden müssen, z.B.
# Motorisierungsgrad, Dauerkartenanteil, mittleres Einkommen o.ä.
# Desswegen ist die Liste der zu aggregierenden Listen zweigeteilt - in einem ersten teil werden die "besonderen Strukturgrößen mit den besonderen Aggregationsfunktionen 
# abgelegt (manuell eingepflegt), in einem zweiten schritt werden die Standardattribute hinzugefügt.

# Die Aggregationsfunktion wird beim Hinzufügen einer "besonderen" Spalte angegeben über das Flag "GroupOrAggrFunction" =x 
# Hier gilt für x:
#   1 : diese Spalte gruppieren
#   4 : Mittel
#   5 : Sum
#   6 : gew Mittel , Gewichtungsattribut über WeightedAvgAttribute = xyz angeben
#   9 : Count
# COM-Hilfe siehe "AggregationFunction Enumeration" und AddColumn