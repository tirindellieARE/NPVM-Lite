# -*- coding: cp1252 -*-
# ##############################################################################
#    Script zum Kopieren von Visum-Listen nach Excel
#    Aufruf von VISUM aus
#    Hauptmodul
#    Erstellt durch PTV Transport Consult GmbH, Dr. Birgit Dugge
#
# ##############################################################################

def starteVisumBeimDebuggen():
    """ Hilfsfunktion für das Debuggen
        Startet VISUM von Python aus, lädt Versionsdatei
        Vorgabe von Namen und Verzeichnissen,
        die im Normalfall aus dem (laufenden) Visum ausglesen werden
    """
    try:
        global Visum
        Visum
        return False
    
    except NameError:
        import win32com.client as com
        Visum =com.Dispatch("Visum.Visum")
        verz_VisumVersion=r"c:\Users\eric.pestel\OneDrive - PTV Group\Projekte\NPVM\Testdaten\NPVM_Nachfrage_2017_EP_init.ver"
        # Starten von VISUM aus Python heraus
        Visum = win32com.client.Dispatch("Visum.Visum.240") #VISUM-Objekt
        #Laden der Versionsdatei von Python aus
        Visum.LoadVersion(verz_VisumVersion)
        #Visum-Pfad laden für Filter etc'
        Visum.LoadPathFile(r"C:\Users\eric.pestel\AppData\Roaming\PTV Vision\PTV Visum 2024\NPVM-Testdaten.pfd")
        return True


# ##############################################################################
#     Main-Prozedur des Scriptes                                               #
# ##############################################################################

#Import verschiedener Bibliotheken
import os
import sys
import time
import datetime
import importlib
import win32com.client

import Dashboard_ModulExcel                                                    # Modul/Klasse für Excel-Handling
import Dashboard_ModulListen                                                   # Modul/Klasse für Handling der Visum-Listen

importlib.reload(Dashboard_ModulExcel)
importlib.reload(Dashboard_ModulListen)

debug_mode = starteVisumBeimDebuggen()

#Nutzereinstellungen -----------
Auswertungsmaster = "NPVM2023_Nachfrage_MasterIntern.xlsx"                                      # Name der Masterdatei,
bdtDaten = {
            "bdTName" : "Dashboard Liste der Listen",                            # Daten der Ausgabetabelle
            "tabrow_fil" : r'fil',
            "tabrow_llax" : r'llax',
            "tabrow_export" : r'Export',
            "tabrow_blattname" : r'xlsBlatt',
            "tabrow_zellname" : r'xlsZelle',
            "tabrow_COMF" : r'COMFunktion',
            "tabrow_tochter" : r'Tochter'
            }
# tabname_screenshots = 'Auswertung Screenshots'
# xlsm-Dokumente funktioneren nicht, also  Endung  xlsx benutzen
# damit das Speichern unter neuem Namen klappt, muss das Zielverzeichnis als vertrauenswürdiger Speicherort zugelassen sein
# siehe Excel-Trust-Center

# Hauptprogramm  **************************************
Startzeit=time.time()


# Schritt 1: Dateinamen erstellen -----------
Vorlagenpfad = Visum.GetPath(88)                               		           # enthält abschließendes Backslash; Visum-Pfad "Sonstige Eingabe-Dateien"
Auswertungspfad = Visum.GetPath(89)                               	           # enthält abschließendes Backslash; Visum-Pfad "Sonstige Ausgabe-Dateien"
Screenshotpfad = Visum.GetPath(41)

Dateinamen = ["Versionsname","Masterxls", "Auswertexls"]				       # Visum-Liste für Dateinamen

Dateinamen[0] = Visum.UserPreferences.DocumentName                	           # Pfad und Name der Versionsdatei
Dateinamen[1] = os.path.join(Vorlagenpfad, Auswertungsmaster)                  # Pfad und Name der Excelmasterdatei
versionsname = os.path.basename(Visum.UserPreferences.DocumentName).split(".")[0]
zeitstempel = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")

if not os.path.isfile(Dateinamen[1]):                                          # Prüfung , ob Master gefunden
    Visum.Log(20480, "Masterdatei nicht gefunden.")
    #quit("Masterdatei nicht gefunden.")
else:
    # Pfad und Name der Auswertedatei
    Dateinamen[2] = os.path.join(Auswertungspfad, f"{zeitstempel}_Dashboard_{versionsname}.xlsx")
    Visum.Log(20480, f"Auswertungsergebnis in Datei: {Dateinamen[2]}")

    # Schritt 2: Initialisierung der Objekte ------
    Visum.Graphic.StopDrawing = True
    xls = Dashboard_ModulExcel.Exceldatei(Dateinamen[1], Dateinamen[2], Visum)
    lst = Dashboard_ModulListen.Visumlisten(Visum, xls, bdtDaten)

    # Schritt 3: Kopiervorgang   ------------------
    lst.kopiereListenInMasterdatei()
    #xls.kopiereScreenshotsInMasterdatei(tabname_screenshots, Screenshotpfad)

# Finalisierung              -------------------
xls = None
lst = None
Visum.Graphic.StopDrawing = False
Visum.Log(20480, f"Auswertung fertig. Zeit: {str(round(time.time() - Startzeit, 2))} sec.")

if debug_mode:
    Visum = None


