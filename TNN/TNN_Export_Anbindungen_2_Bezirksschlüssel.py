#-------------------------------------------------------------------------------
# Name:        TNN_Export_Anbindungen
# Purpose:     Export Anbindungsinformationen (Knoten, Bezirk, Oberbezirk, VSys, Gewichte, Anbindungstyp, benutzerdefinierte Atribute)
#              in benutzerdefinierte Tabelle,
#              keine Zusammenfassung nach Oberbezirken
#              Filter auf Anbindungen nur für neue Tochterbezirke
#              Zweck: Rekonstruktion der Anbindung in der Tochterversion
#
# Author:      birgit dugge
#
# Created:     22.10.2024
#
# Beschreibung siehe unten; Anweisungen unter 'Nutzereinstellungen beachten
#-------------------------------------------------------------------------------
import csv
import os
import time
import numpy as np
import pandas as pd


# Initialisierung-------
t1= time.time() #Startzeit speichern
udtName="TNN_Anbindungen_Bezirk"


# Nutzereinstellungen -------------
# die Liste der bda wird ermittelt, indem nach bdA gesucht wird
# der Standard für die Aggregationsfunktionb ist das Arithmetische Mittel
# Wenn etwas anders erwünscht ist, dann manuell ersetzen nach Abschluss der Berechnung



# Berechnung ---------- -----------
# 1. Array der Anbindungsattribute erstellen
# Codierung der Gruppierungsfunktion siehe unten
AttData_dict={#Key="AttName "                  : [0'GroupOrAggrFunction', 1'WeightedAvgAttribute'],
                     'ZONENO'                     : [ 9, ''],   #9   Anzahl
                     'ZONE\MAINZONENO'            : [ 1, ''],   #1   Gruppieren, wird Schlüssel
                     'DIRECTION'                  : [ 1, ''],   #1   Gruppieren, wird Schlüssel
                     'NODENO'                     : [ 1, ''],   #1   Gruppieren, wird Schlüssel
                     'TSYSSET'                    : [ 12, ''],  #12  Verschiedene #Test OBez105, K6549
                     'LENGTH'                     : [ 4, ''],   #4   Mittel
                     'TYPENO'                     : [ 2, '']    #2   Min
                   }

# weitere Atributgruppe: Liste der T0_TSYS(VSysCode)-Attribute generieren und anfügen
hlp_dict={#key= T0-AttName: [0'GroupOrAggrFunction', 1'WeightedAvgAttribute']
         f'T0_TSYS({i.AttValue("Code").upper()})'  :  [ 6, f'VOLPERS_TSYS({i.AttValue("Code").upper()},AP)' ] for i in Visum.Net.TSystems.GetAll if i.AttValue('TYPE') != 'PUT'
         }

for key, value in hlp_dict.items():
    if ('FGV' in key) or ('FUS' in key):
        value[0] = 4
        value[1] = '' # Für FGV abweichend den Durchschnitt einstellen, da keine Belastungswerte für gewichteten Mittelwert vorhanden

AttData_dict.update(hlp_dict)


# weitere Atributgruppe: Anbindungsgewichte hinzufügen
hlp_dict= {#key= T0-AttName: [0'GroupOrAggrFunction', 1'WeightedAvgAttribute']
           i.ID : [5, ''] for i in Visum.Net.Connectors.Attributes.GetAll if ('TNN_ANBINDUNG_GEWICHT' in i.ID)
          }           #5  Summe

AttData_dict.update(hlp_dict)

# weitere Atributgruppe: Liste der benutzerdefinierten Attribute abgleichen und ggf. anfügen
bda_List =[ i.ID for i in Visum.Net.Connectors.Attributes.GetAll if (i.IsUserDefined  and i.Editable and (i.ID.startswith('SIKO') == False) ) ] # alle editierbaren bdA in Visum außer SIKO

fehlende_bdA =[ i for i in bda_List if i not in AttData_dict.keys() ]

hlp_dict={}
if len(fehlende_bdA)  > 0:
    hlp_dict = {i.upper() : [ 4, '' ]  for i in fehlende_bdA }   # 4:Mittel als Standardwert für nicht näher spezifizierte benutzerdefinierte Attribute

AttData_dict.update(hlp_dict) # anhängen

# Filter setzen, für Gebietskulisse

##Visum.Filters.ZoneFilter().Init()
##Visum.Filters.ZoneFilter().RemoveConditions()
##Visum.Filters.ZoneFilter().UseFilter=True
##Visum.Filters.ZoneFilter().AddCondition("OP_None", False, "MAINZONE\TNN_TOCHTER_RO_PEK_NR", "LessVal", 3)
##
##Visum.Filters.ConnectorFilter().Init()
##Visum.Filters.ConnectorFilter().RemoveConditions()
##Visum.Filters.ConnectorFilter().UseFilter=True
##Visum.Filters.ConnectorFilter().AddCondition("OP_None", False, "ZONE\MAINZONE\TNN_TOCHTER_RO_PEK_NR", "LessVal", 3)

# Anbindungsdaten in dataframe übernehmen
anb_Daten_list = Visum.Net.Connectors.GetMultipleAttributes(list(AttData_dict.keys()) , True) # nur Aktive Bezirke
df_anb = pd.DataFrame(anb_Daten_list, columns = list(AttData_dict.keys()))


# Anlegen der bdT
if len([i.AttValue("Name") for i in Visum.Net.TableDefinitions.GetAll if i.AttValue("Name") == udtName]) == 1: # Prüfung, ob eine Tab gleichen namens existiert
    Visum.Net.RemoveTableDefinition(Visum.Net.TableDefinitions.ItemByKey(udtName))

udt = Visum.Net.AddTableDefinition(udtName)

# in bdT die bdA hinzufügen: für anzulegende bda.ID : Leerzeichen, Komma und Klammern ersetzen und einige Datentypen ersetzen
hlp_dict = {i.replace('(', '/').replace(')', '/').replace(', ', '---'): [i,0] for i in df_anb.columns.tolist()}
cols_dict={}

for key, value in hlp_dict.items():
    #Datentyp ermittel und sichern
    if Visum.Net.Connectors.AttrExists(value[0].upper()): # Datentyp im original ermitteln
        value[1] = Visum.Net.Connectors.Attributes.ItemByKey(value[0].upper()).ValueType
    else:
        value[1] = 2   # Datentyp Real für sonstige Attribute

    value[1] = 5 if value[1] == 26 else value[1]   # Datentyp 26 für Anbindungsrichtung wird ersetzt durch Texttyp
    value[1] = 5 if value[1] == 17 else value[1]   # Datentyp 17 für ModusSet wird ersetzt durch Texttyp

    # ZONE\MAINZONE austauschen, weil als bdA-Name nicht zu verwenden
    if key == 'ZONE\MAINZONENO':
        cols_dict.update({'MAINZONENO':['MAINZONENO',value[1]]})
    else:
        cols_dict.update({key:value})

for key, value in cols_dict.items():
    #print(f'{key},{value}')
    udt.TableEntries.AddUserDefinedAttribute(key, value[0], value[0], value[1])

# in bdT: n Datensätze generieren
udt.AddMultiTableEntries([i+1 for i in range(len(df_anb))])                              # n TE = Datensätze  anlegen mit lfd Nr als Schlüssel
# in bdT : Anbindungsdaten hinzufügen
udt.TableEntries.SetMultipleAttributes(list(cols_dict.keys()), df_anb.values.tolist(), OnlyActive=False)


# Init Bezirksfilter
#Visum.Filters.ZoneFilter().Init()
#Visum.Filters.ZoneFilter().UseFilter = False

# Init Anbindungsfilter
#Visum.Filters.ConnectorFilter().Init()
#Visum.Filters.ConnectorFilter().UseFilter=False


# Aufräumen /Finalisierung-------------------------

Visum.Log(20480,"Export Anbindungen fertig, Zeitverbrauch: " +str(round(time.time()-t1))+" sec.")


# Hinweise / Erläuterung
# In der Tochterversion werden die Anbindungen per Skript erzeugt,
# In der Mutterversion Bez-Nr <> Knoten, in der Tochterversion OBezNr <> Knoten.

# Durch die Aggregation von Bezirken zu Oberbezirken entstehen Duplikate,
# also mehrere Anbindungen mit dem gleichen Schlüsselpaar (OBezNr - KnotNr)
# Diese Anbindungen werden in der Liste zusammengefasst (Gruppierung).
# Daraus ergibt sich, dass für alle Attribut(gruppen) festgelegt werden muss,
# wie die gruppierten Attribute zusammengefasst werden müssen (Aggregationsfunktion).

# Diese Setzung erfolgt manuell am Beginnn der Skripte im Attribut 'AttGruppen_dict',
# wahlweise für Einzel- oder Attributgruppen.
# Die Gewichte (=Aufkommen der Umlegung) werden summiert und die Zeiten werden mit den Aufkommen gewichtet gemittelt.
# für weitere Attributsgruppen insbesondere benutzerdefinierte Attribut(gruppen) ist das inidividuell zu ergänzen


# Beim gewichteten Zusammenfassen von Werten werden die Belastungen berücksichtigt.
# Die Werte z.B. für die T0-VSYS sind 0, falls die Belastungen initialisiert sind.

# Alle Tochterbezirke sollen angebunden werden, auch die Kordonbezirke.
# Deswegen wird - anders als beim Herausschreiben der Erzeugungsdaten - kein Bezirksfilter gesetzt.

# Alle benutzerdefinierten  Attribute werden berücksichtigt
# Die benutzerdefinierten Attribute prüfen, ob dort Leerfelder vorhanden sind und ggf. mit 0 füllen.
#
# Die Aggregationsfunktion wird beim Hinzufügen einer Spalte angegeben über das Flag "GroupOrAggrFunction" =x
# Hier gilt:
#   0 : Standardwert / Initialer Wert
#   1 : diese Spalte gruppieren
#   2 : Minimum
#   3 : Maximum
#   4 : Mittel
#   5 : Sum
#   6 : gew Mittel , Gewichtungsattribut über WeightedAvgAttribute ='' angeben
#   7 : Vergleich
#   9 : Count
#  10 : Concatenate Verketten
#  12 : Distinct, Verschiedene
# COM-Hilfe siehe "AggregationFunction" unter AddColumn

# Codierung Dezimalstellen DecPlaces
# = -1: Standartwert für den Zahlentyp (Ganzzahl =0, ...)
# Codierung Format für den Export in att oder Zwischenablage - siehe StringFormatTypeT
# = 0: Standartwert für den Datentyp