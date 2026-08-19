# -*- coding: utf-8 -*-
# ##############################################################################
#    Script zum Kopieren von Visum-Listen nach Excel
#    Aufruf von VISUM aus
#    Hauptmodul
#    Erstellt durch PTV Transport Consult GmbH, Dr. Birgit Dugge, Kevin Klopsch
#
# ##############################################################################

def starteVisumBeimDebuggen():
    """ Hilfsfunktion für das Debuggen
        Startet VISUM von Python aus, lädt Versionsdatei
        Vorgabe von Namen und Verzeichnissen,
        die im Normalfall aus dem (laufenden) Visum ausglesen werden
    """
    global Visum

    # Beim Debuggen einschalten: Vorgabe von Namen und Verzeichnissen
    verz_VisumVersion=r"\\SDRS-WN-F01\Data2\DD_TC11\C823079_NPVM_Schweiz_2016\08_VISUM\ver"
    name_VisumVersion=r"NPVM_PKW_01.ver"

    # Starten von VISUM aus Python heraus
    Visum = win32com.client.Dispatch("Visum.Visum.160") #VISUM-Objekt
    #Laden der Versionsdatei von Python aus
    Visum.LoadVersion(verz_VisumVersion+"\\"+name_VisumVersion)
    #Visum-Pfad laden für Filter etc'
    Visum.LoadPathFile(r"\\SDRS-WN-F01\Data2\DD_TC11\C823079_NPVM_Schweiz_2016\08_VISUM\pfd\H_NPVM2016.pfd")


#Ende >>  Funktion------------------------------------------------------------------

# ##############################################################################
#     Main-Prozedur des Scriptes                                               #
# ##############################################################################

#Import verschiedener Bibliotheken
import os                                                           #allgemeine Bibliothek Betriebssystemfunktionen, z.B. Zerlegung von Dateinamen u.ä.
import sys
import win32com.client                                              #allgemeine Bibliothek für COM-Schnittstelle (VISUM und Excel)
import datetime                                                     #Zeitformate etc.
import time
import importlib

#starteVisumBeimDebuggen()

#Module importieren
import NPVM_MIV_Auswertung_xls_Intern_EXCEL                         #Modul/Klasse für Excel-Handling
import NPVM_MIV_Auswertung_xls_Intern_LISTEN                        #Modul/Klasse für Handling der Visum-Listen


importlib.reload(NPVM_MIV_Auswertung_xls_Intern_EXCEL)
importlib.reload(NPVM_MIV_Auswertung_xls_Intern_LISTEN )                      #Modul/Klasse für Handling der Visum-Listen



# Hauptprogramm-----------------------------------------------------------------

# aktuellen Stand abspeichern
pfd = Visum.GetPath(21)
Filterobj = Visum.Filters
Filterobj.Save(pfd + r"TEMP_SAVE.fil")

#Visum-Pfad "sonstige Eingabe-Dateien"
Vorlagenpfad = Visum.GetPath(88)                               		           # enthält abschließendes Backslash; Visum-Pfad "Sonstige Eingabe-Dateien"
Auswertungspfad = Visum.GetPath(89)                               	           # enthält abschließendes Backslash; Visum-Pfad "Sonstige Ausgabe-Dateien"
#Name der Masterdatei
Auswertungsmaster = "NPVM_MIV_MasterIntern.xlsx"

Dateinamen = ["Versionsname", "Masterxls", "Auswertexls"]
Dateinamen[0] = Visum.UserPreferences.DocumentName                	           # Pfad und Name der Versionsdatei
Dateinamen[1] = os.path.join(Vorlagenpfad, Auswertungsmaster)                  # Pfad und Name der Excelmasterdatei

#Visumversionsnamen abspalten...
n = os.path.basename(Dateinamen[0]).split(".")[0]

date_string = datetime.datetime.now().strftime("%Y%m%d%H%M")
#... und zum Dateinamen der Excel-Auswertedatei zusammenfassen
Dateinamen[2] = Auswertungspfad + date_string + "_" + n + ".xlsx"

Visum.Graphic.StopDrawing = 1

xls = NPVM_MIV_Auswertung_xls_Intern_EXCEL.Exceldatei (Dateinamen[1], Dateinamen[2])
lst = NPVM_MIV_Auswertung_xls_Intern_LISTEN.Visumlisten (Visum, xls)

lst.kopiereListenInMasterdatei()

Visum.Graphic.StopDrawing = 0

xls=None
lst=None

# Filter wiederherstellen
Filterobj.Open(pfd+r"TEMP_SAVE.fil")
