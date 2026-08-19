#-------------------------------------------------------------------------------
# Name:        TNN_Import_Anbindungen
# Purpose:     Aggregieren der Abbindungsdaten zu Tochterbezirken
#              Generieren neuer Anbindungen und Import von Anbindungsdaten (Knoten, Bezirk, Oberbezirk, VSys, Gewichte, Anbindungstyp, benutzerdefinierte Atribute)
#              aus einer benutzerdefinierte Tabelle,
#              verträgt auch kombinierte IV/ÖV-Anbindungen
#
# Author:      birgit dugge
#
# Created:     29.10.2024 in Visum 24-10
#
# Beschreibung siehe unten; Anweisungen unter 'Nutzereinstellungen beachten
#-------------------------------------------------------------------------------

# Import Bibliotheken -------------------------------
import time
import os
import numpy as np
import pandas as pd
import VisumPy.helpers as VPH

# Nutzereinstellungen -------------------

udtName="TNN_Anbindungen_Bezirk"   # Name der benutzerdefinierten Tabelle mit Anbindungsdaten

# Initialisierung-------

t1= time.time() #Startzeit speichern
OEVFuss_TSysCode  =  [ i.AttValue('Code') for i in Visum.Net.TSystems.GetAll if i.AttValue('TYPE') == 'PUTWALK'][0] # Code für ÖVFuss-System ermitteln
#OEV_Code    =   [ i.AttValue('Code') for i in Visum.Net.Modes.GetAll if OEVFuss_TSysCode in i.AttValue('TSYSSET') ] # Code für ÖV-Modus finden


# Schritt 1: Attributsnamen ermitteln und Daten aus der Tabelle lesen ---------------------
# Attributsliste der bdT

atts=Visum.Net.TableDefinitions.ItemByKey(udtName).TableEntries.Attributes

udt_attNamen_dict = {atts.ItemByKey(i.ID).Code : i.ID for i in atts.GetAll if i.ID not in ['TABLEDEFINITIONNAME', 'NO', 'EXISTSINNET']}

udt_attNamen=list(udt_attNamen_dict.values())

udt_List = Visum.Net.TableDefinitions.ItemByKey(udtName).TableEntries.GetMultipleAttributes(list(udt_attNamen_dict.values()))

df_udt = pd.DataFrame(udt_List, columns = list(udt_attNamen_dict.keys()))


# Schritt 2: vorhandene Anbindungen filtern und löschen -------------------

Visum.Net.Connectors.RemoveAll(OnlyActive=True)


#Schritt 3 : Anbindungen aggregieren -----------------------

df = df_udt # keine Selektion Datensätze für IV- oder ÖV-Anbindnungen

# Entfernen der Spalte 'ZONENO' und 'NO'
df.drop(columns=['ZONENO', 'NO'], inplace=True, errors='ignore')

# Aggregationsregeln
def weighted_average(group, value_col, weight_col):
    if weight_col in group:
        weight_sum = group[weight_col].sum()
        if weight_sum != 0:
            return (group[value_col] * group[weight_col]).sum() / weight_sum
    return group[value_col].mean()

def custom_aggregation(group):
    result = {}

    # Summieren aller Spalten, die mit 'TNN_ANBINDUNG_GEWICHT' beginnen
    for col in df.columns:
        if col.startswith('TNN_ANBINDUNG_GEWICHT'):
            result[col] = group[col].sum()

    # Verwenden des minimalen Werts für 'TYPENO'
    if 'TYPENO' in df.columns:
        result['TYPENO'] = group['TYPENO'].min()

    # Berechnung des arithmetischen Mittels für 'LENGTH'
    if 'LENGTH' in df.columns:
        result['LENGTH'] = group['LENGTH'].mean()

    # Erstellen einer eindeutigen Menge von Zeichenfolgen für 'TSYSSET'
    if 'TSYSSET' in df.columns:
        result['TSYSSET'] = ','.join(sorted(set(",".join(group['TSYSSET'].dropna()).split(","))))

    # Berechnung gewichteter Mittelwerte mit verbesserter Spaltenerkennung
    for col in df.columns:
        col_upper = col.upper()
        if any(keyword in col_upper for keyword in ['T0', 'ZEIT', 'TAKT']) and 'PKW' in col_upper:
            weight_col = next((w for w in df.columns if 'GEWICHT' in w.upper() and 'PKW' in w.upper()), None)
            if weight_col:
                result[col] = weighted_average(group, col, weight_col)
        elif any(keyword in col_upper for keyword in ['T0', 'ZEIT', 'TAKT']) and any(lkw_keyword in col_upper for lkw_keyword in ['LKW', 'L']):
            weight_col = next((w for w in df.columns if 'GEWICHT' in w.upper() and any(lkw_keyword in w.upper() for lkw_keyword in ['LKW', 'L'])), None)
            if weight_col:
                result[col] = weighted_average(group, col, weight_col)
        elif any(keyword in col_upper for keyword in ['T0', 'ZEIT', 'TAKT']) and 'RAD' in col_upper:
            weight_col = next((w for w in df.columns if 'GEWICHT' in w.upper() and 'RAD' in w.upper()), None)
            if weight_col:
                result[col] = weighted_average(group, col, weight_col)
        elif any(keyword in col_upper for keyword in ['T0', 'ZEIT', 'TAKT']) and 'FGV' in col_upper:
            result[col] = group[col].mean()
        elif any(keyword in col_upper for keyword in ['T0', 'ZEIT', 'TAKT']) and any(oev_keyword in col_upper for oev_keyword in ['OEV', 'ÖV']):
            weight_col = next((w for w in df.columns if 'GEWICHT' in w.upper() and any(oev_keyword in w.upper() for oev_keyword in ['OEV', 'ÖV'])), None)
            if weight_col:
                result[col] = weighted_average(group, col, weight_col)

    # Zählen der aggregierten Elemente je Gruppe
    result['TNN_Anbindung_AnzAggAnbind'] = len(group)

    return pd.Series(result)


# Gruppieren nach 'MAINZONENO', 'DIRECTION', und 'NODENO', Anwenden der Aggregationsregeln und Sortieren
grouped = df.groupby(['MAINZONENO', 'DIRECTION', 'NODENO'])
result = grouped.apply(custom_aggregation).reset_index()

# Datensätze ohne gültige Hauptzone (MAINZONENO == 0) entfernen
vorher = len(result)
result = result[result['MAINZONENO'].astype(float) != 0].reset_index(drop=True)
Visum.Log(20480, "Datensätze mit MAINZONENO=0 entfernt: " + str(vorher - len(result)))

# Sortieren nach ['MAINZONENO', 'NODENO' , 'DIRECTION'] in aufsteigender Reihenfolge
result = result.sort_values(by=['MAINZONENO', 'NODENO', 'DIRECTION']).reset_index(drop=True)

# Sicherstellen, dass alle erforderlichen Spalten für gewichtete Mittelwerte im Ergebnis enthalten sind
expected_columns = [col for col in df.columns if any(keyword in col.upper() for keyword in ['T0', 'ZEIT', 'TAKT']) and any(modus_keyword in col.upper() for modus_keyword in ['OEV', 'ÖV', 'X', 'LKW', 'L', 'PKW', 'RAD', 'FGV'])]
for col in expected_columns:
    if col not in result:
        result[col] = None

# Ersetzen von NaN-Werten: numerisch mit 0, Strings mit leerem String
result = result.fillna(value={col: 0 for col in result.select_dtypes(include=['number']).columns})
result = result.fillna(value={col: '' for col in result.select_dtypes(include=['object']).columns})

#Schritt 4 : Erzeugen neuer ÖV (oder kombinierten Anbindungen) ----------------------
for i, row in result.iloc[::2].iterrows():  #Iteration nur jeden zweiten Datensatz
    #print( f"Index: {i} , Z {result['MAINZONENO'][i]}, N {result['NODENO'][i]}, R {result['DIRECTION'][i]}, { Visum.Net.Connectors.ExistsByKey(result['NODENO'][i], result['MAINZONENO'][i]) == False}, Anz:{Visum.Net.Connectors.Count}" )

    #if i == 50:  Zum Debuggen der Schleife
    #    break
    if Visum.Net.Connectors.ExistsByKey(result['NODENO'][i], result['MAINZONENO'][i]) == False:  # Falls Anbindung noch nicht existiert
        neue_Anb=Visum.Net.AddConnector(result['MAINZONENO'][i], result['NODENO'][i]) # AddConnector() legt gleichzeitig Hin- und Rückrichtung an, verweist aber nur auf das Objekt für die Hinrichtung
        akt_Rückrichtung=Visum.Net.Connectors.DestItemByKey(result['NODENO'][i], result['MAINZONENO'][i]) # Objekt für Rückrichtung
        neue_Anb.SetAttValue('TSYSSet', result['TSYSSET'][i])
        akt_Rückrichtung.SetAttValue('TSYSSet', result['TSYSSET'][i+1])

# Schritt 5: Upload von Anbindungsdaten -----------------------
# Anbindungen in der Sortierung entsprechend der Schlüsselattributen laden

# Laden der Anbindungsdaten aus Visum und Umwandeln in ein DataFrame
x = Visum.Net.Connectors.GetMultipleAttributes(['ZONENO', 'NODENO', 'DIRECTION'])
df_Anb = pd.DataFrame(x, columns=['MAINZONENO', 'NODENO', 'DIRECTION'])

# Zusammenführen der DataFrames anhand der Schlüsselspalten von df_Anb; Schlüsselspalten konvergieren in int
result = pd.merge(df_Anb.astype({'MAINZONENO': int, 'NODENO': int, 'DIRECTION': int}),
                   result.astype({'MAINZONENO': int, 'NODENO': int, 'DIRECTION': int}),
                   on=['MAINZONENO', 'NODENO', 'DIRECTION'], how='left')

df_daten_import = result.drop(columns=['MAINZONENO',  'NODENO',  'DIRECTION'], axis=1)
df_daten_import_cols  = [col for col in df_daten_import.columns]

# von DataFrame nach Visum
Visum.Net.Connectors.SetMultipleAttributes(df_daten_import_cols, df_daten_import.values.tolist(), OnlyActive = True)

# Aufräumen /Finalisierung-------------------------
Visum.Log(20480, str(i)+" Anbindungen angelegt, Zeitbedarf " +str(round(time.time()-t1))+" sec.")


# Hinweise: ----------------------------------
#