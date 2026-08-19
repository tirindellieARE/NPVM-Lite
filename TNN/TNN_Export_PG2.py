#-------------------------------------------------------------------------------
# Purpose:     Export zone data as input for demand model
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
udtName="TNN_Personengruppen"

# Berechnung -----------
#rechenvorschrift_dict={}  # {AufkRate_Name : StuGroe_Name]
bez_attNamen_dict={}      # deu und engl Namen des Bezirksattribute

# Bezirksattribute und Rechenvorschrift für alle Nachfragemodelle

NModCodes=[i.AttValue("Code") for i in Visum.Net.DemandModels.GetAll]
for demandModel in NModCodes:
    ds_Namen=[[att.AttValue('Code'), int(att.AttValue('ORIGDESTTYPE')) ] for att in  Visum.Net.DemandModels.ItemByKey(demandModel).DemandStrata.GetAll] # alle NSch
    pg_Namen = [i.AttValue("Code") for i in Visum.Net.DemandModels.ItemByKey(demandModel).PersonGroups.GetAll] # Liste aller Personengruppennamen
    for pg in pg_Namen:
        bez_attNamen_dict.update( {f'ANZAHLPERSONEN({pg})' : f'NUMPERSONS({pg})'} )
        #rechenvorschrift_dict.update( {f'NUMPERSONS({pg})' : f'NUMPERSONS({pg})' } )
# Ende Loop NModCodes
# OUT: bez_attNamen_dict: {'ANZAHLPERSONEN(PG_0005N0)': 'NUMPERSONS(PG_0005N0)', 'ANZAHLPERSONEN(PG_0610N0)': 'NUMPERSONS(PG_0610N0)', 


Visum.Filters.ZoneFilter().Init()
Visum.Filters.ZoneFilter().UseFilter=True
Visum.Filters.ZoneFilter().AddCondition("OP_None", False, "MAINZONE\TNN_TOCHTER_RO_PEK_NR", "LessVal", 3)

bez_Daten_list = Visum.Net.Zones.GetMultipleAttributes(['NO', 'MAINZONENO']+list(bez_attNamen_dict.values()) , True) # nur Aktive Bezirke
df_bez = pd.DataFrame(bez_Daten_list, columns = ['NO', 'MAINZONENO']+list(bez_attNamen_dict.values()))

# OberBez-Liste anlegen
df_OBez=df_bez.groupby('MAINZONENO').agg( AnzMutterBez = ('NO', 'size')).reset_index() #Ergebnis df-Anlegen und mit einer Spalte füllen
# 
for key, value in bez_attNamen_dict.items():
    
    #df_bez['SP']=df_bez[value]*df_bez[key] # Summenprodukt := Stukturgröße (als Gewicht) * Wert

    df_gruppiert = df_bez.groupby('MAINZONENO').agg(
        AnzMutterBez = ('NO', 'size'), # Anzahl der Elemente pro Gruppe
        Sum_W  = (value,  'sum'),        # Summe der Werte pro Gruppe (Summe der Rate)
        #Mean_W = (key,  'mean'),       # Mittel des Wertes pro Gruppe (Mittel der Rate)
        #Sum_G  = (value,'sum'),        # Summe der Gewichtsgröße (Strukturgröße)
        #Sum_SP = ('SP', 'sum'),        # Summe Summenprodukt
        ).reset_index()
    
    df_gruppiert[value] = df_gruppiert.apply(
        lambda row: row['Sum_W'] ,  axis=1 
    ) # Rechenanweisung in lamda-Funktion: Einfach Summe 
    df_OBez[value]=df_gruppiert[value]

# Export: bdt Anlegen, bda hinzufügen, Daten übertragen...
if len([i.AttValue("Name") for i in Visum.Net.TableDefinitions.GetAll if i.AttValue("Name") == udtName]) == 1: # Prüfung, ob eine Tab gleichen namens existiert
    Visum.Net.RemoveTableDefinition(Visum.Net.TableDefinitions.ItemByKey(udtName))
t=Visum.Net.AddTableDefinition(udtName)

cols_dict={i.replace('(', '/').replace(')', '/').replace(', ', '---'): i for i in df_OBez.columns.tolist()}  # für bda.ID : Leerzeichen, Komma und Klammern ersetzen

for key, value in cols_dict.items():
    if Visum.Net.Zones.AttrExists(value.upper()): # Datentyp im original ermitteln
        vt_orig = Visum.Net.Zones.Attributes.ItemByKey(value.upper()).ValueType
    else:
        vt_orig = 2   # Datentyp Real für sonstige Attribute
   
    t.TableEntries.AddUserDefinedAttribute(key, value, value, vt_orig)

t.AddMultiTableEntries(df_OBez['MAINZONENO'].tolist())                                                 # n TE = Datensätze  anlegen mit OBezNr als Schlüssel
t.TableEntries.SetMultipleAttributes(list(cols_dict.keys()), df_OBez.values.tolist(), OnlyActive=False) # Werte Setzen

# Init Bezirksfilter
Visum.Filters.ZoneFilter().Init()
Visum.Filters.ZoneFilter().UseFilter = False


# Aufräumen /Finalisierung-------------------------
Visum.Log(20480,"Export Personengruppen fertig, " +str(round(time.time()-t1))+" sec.")


# Hinweis: 
# Hinweis: 
# Visum 24-10 hat ein Bug bei .Attributes.GetAll und beim Herausschreiben der Attr in eine bdt (Nutzung der internen Funktion CreateTableFromList)
# Attribute mit Subattributen werden ausgegeben ohne Subattributen, z.B. nur T0-TSys statt T0-TSys(FGV), T0-TSys(RAD), ...
# Das betrifft Personengruppen, aber auch MobRaten und Aufkommensraten. Letztgenannte Attribute haben sogar zwei Subattributen (Nachfrageschicht und Raumstrukturgröße).

# bei der Aggregation von personengruppen gilt:
# - alle PG werden summiert beim Aggregieren

# Exportiert wird eine Liste mit Aggregierten Bezirken, die Oberbezirksnummer in der Mutter wird zum Schlüssel in der bdT und 
# und zur Nummer in der Tochterversion 
