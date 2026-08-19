#-------------------------------------------------------------------------------
# Purpose:     Export und Aggregation (= gewichtetes Mittel) der Mobilitätsraten 
#
# Author:      birgit dugge
#
# Created:     Nov 2024 in V 24-10
# 
# Hinweise siehe unten
#-------------------------------------------------------------------------------

# Python-Bibliotheken -------
import time
import numpy as np
import pandas as pd

# Initialisierung-------

t1= time.time() #Startzeit speichern
udtName="TNN_Mobilitaetsraten"

# Berechnung -----------
rechenvorschrift_dict={}  # {AufkRate_Name : StuGroe_Name]
bez_attNamen_dict={}      # deu und engl Namen des Bezirksattribute

# Bezirksattribute und Rechenvorschrift für alle Nachfragemodelle

NModCodes=[i.AttValue("Code") for i in Visum.Net.DemandModels.GetAll]
for demandModel in NModCodes:
    ds_Namen=[[att.AttValue('Code'), int(att.AttValue('ORIGDESTTYPE')) ] for att in  Visum.Net.DemandModels.ItemByKey(demandModel).DemandStrata.GetAll] # alle NSch
    pg_Namen = [i.AttValue("Code") for i in Visum.Net.DemandModels.ItemByKey(demandModel).PersonGroups.GetAll] # Liste aller Strukturgrößennamen
    for pg in pg_Namen:
        bez_attNamen_dict.update( {f'ANZAHLPERSONEN({pg})' : f'NUMPERSONS({pg})'} )
        #MOBILITYRATE(01_WA,PG_0005N0)
    for ds in ds_Namen:
            for pg in pg_Namen:
                bez_attNamen_dict.update( {f'Mobilitätsrate({ds[0]}, {pg})' : f'MOBILITYRATE({ds[0]}, {pg})'}   )
                rechenvorschrift_dict.update( {f'MOBILITYRATE({ds[0]}, {pg})' :f'NUMPERSONS({pg})' } )
# Ende Loop NModCodes
# OUT: bez_attNamen_dict: {'ANZAHLPersonen(PG_0005N0)': 'NUMPERSONS(PG_0005N0)', 'ANZAHLPersonen(PG_0610N0)': 'NUMPERSONS(PG_0610N0)',
# OUT: rechenvorschrift_dict: {'MOBILITYRATE(01_WA, PG_0005N0)': 'NUMPERSONS(PG_0005N0)',...

Visum.Filters.ZoneFilter().Init()
Visum.Filters.ZoneFilter().UseFilter=True
Visum.Filters.ZoneFilter().AddCondition("OP_None", False, "MAINZONE\TNN_TOCHTER_RO_PEK_NR", "LessVal", 3)

bez_Daten_list = Visum.Net.Zones.GetMultipleAttributes(['NO', 'MAINZONENO']+list(bez_attNamen_dict.values()) , True) # nur Aktive Bezirke
df_bez = pd.DataFrame(bez_Daten_list, columns = ['NO', 'MAINZONENO']+list(bez_attNamen_dict.values()))

# OberBez-Liste anlegen
df_OBez=df_bez.groupby('MAINZONENO').agg( AnzMutterBez = ('NO', 'size')).reset_index() #Ergebnis-df anlegen und mit einer Spalte füllen

# Mittelwerte berechnen
for key, value in rechenvorschrift_dict.items():
    
    df_bez['SP']=df_bez[value]*df_bez[key] # Summenprodukt Hilfswert := Stukturgröße (als Gewicht) * Wert

    df_gruppiert = df_bez.groupby('MAINZONENO').agg(
        AnzMutterBez = ('NO', 'size'), # Anzahl der Elemente pro Gruppe
        Sum_W  = (key,  'sum'),        # Summe der Werte pro Gruppe (Summe der Rate)
        Mean_W = (key,  'mean'),       # Mittel des Wertes pro Gruppe (Mittel der Rate)
        Sum_G  = (value,'sum'),        # Summe der Gewichtsgröße (Strukturgröße)
        Sum_SP = ('SP', 'sum'),        # Summe Summenprodukt
        ).reset_index()
    
    df_gruppiert[key] = df_gruppiert.apply(
        lambda row: row['Mean_W'] if (row['Sum_G'] == 0) else row['Sum_SP'] / row['Sum_G'],
        axis=1
    ) # Rechenanweisung in lamda-Funktion: falls G==0 arith. Mittel, sonst gewichtetes Mittel
    df_OBez[key]=df_gruppiert[key]

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

Visum.Log(20480,"Export Mobilitätsraten  fertig " +str(round(time.time()-t1))+" sec.")


# Hinweis: 
# Visum 24-10 hat ein Bug bei .Attributes.GetAll und beim Herausschreiben der Attr in eine bdt (Nutzung der internen Funktion CreateTableFromList)
# Attribute mit Subattributen werden ausgegeben ohne Subattributen, z.B. nur T0-TSys statt T0-TSys(FGV), T0-TSys(RAD), ...
# Das betrifft MobRaten und Aufkommensraten, diese Attribute haben sogar zwei Subattributen (Nachfrageschicht und Raumstrukturgröße).


# MobRaten, Aufkommensraten und Untersuchungsraumanteile müssen beim Aggregieren mit der Strukturgröße gewichtet werden.
# Bei Nutzung der in Visum eingebauten Funktion wird ein gewichtete Mittel mit Gewicht 0 gleich 0.
# Beispiel: Bezirke ohne Kindergartenplätze oder Bezirke ohne Einwohner. 
# Der Nullwert für die Aufkommensrate kann bei einer Strukturdatenprognose stören. 
# Deshalb wird dann das arithmetische Mittel der MobRaten verwendet, damit der Wert > 0  gesetzt wird.
# Deshalb:
# - Das gewichtete Mittel bzw das arithmetische Mittel wird im Skript berechnet, nicht in Visum.
# - die benötigten Bezirksattribute und zugehörige Namen werden selbst ermittelt in diesem Skript. 
# - Die benutzerdefinierte Tabelle mit allen bdA wird selbst angelegt, nicht durch die Visum-eigene Funktion.

# Exportiert wird eine Liste mit Aggregierten Bezirken, die Oberbezirksnummer in der Mutter wird zum Schlüssel in der bdT und 
# und zur Nummer in der Tochterversion 
# 