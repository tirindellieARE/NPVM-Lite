# -*- coding: cp1252 -*-
# ##############################################################################
#    Script zum Kopieren von Visum-Listen nach Excel
#    Aufruf von VISUM aus
#    HIER: Modul Listen - Kopieren von Visum-Listen
#
#    Erstellt durch PTV Transport Consult GmbH, MSc Kevin Klopsch, Dr. Birgit Dugge
#
# ##############################################################################

import os                   #Betriebssystemfunktionen, z.B. Zerlegung von Dateinamen u.ä.
import pandas as pd
import win32com.client

class Visumlisten(object):
    #MeinVisum=None

    def __init__(self,Visum,Excel,bdtAusgabe):
        self.__MeinVisum=Visum
        self.__MeinExcel=Excel
        self.__bdtDaten=bdtAusgabe
        
    def get_sort_key(self, entry):
        return entry.AttValue(self.__bdtDaten["tabrow_tochter"])

    def kopiereListenInMasterdatei(self):

        """ Prozedur zum Kopieren von klassischen Visum-Listen (Kalibrierungsauswertung von VISUM nach Excel
        Excel Datei hat gleichen Namen wie VISUM-Version
        Jede Liste kommt auf ein eigenes Excelblatt
        ! Für benutzerdefinierte Tabellen gibt es eine eigene Funktion !
        """

        FilterPfad = self.__MeinVisum.GetPath(21)
        ListenPfad = self.__MeinVisum.GetPath(20)
        
        tabdef = self.__MeinVisum.Net.TableDefinitions.ItemByKey(self.__bdtDaten["bdTName"])
        
        tochter = ""
        
        for te in sorted(tabdef.TableEntries, key=self.get_sort_key):
            if te.AttValue(self.__bdtDaten["tabrow_export"]) == 1.0:
                if te.AttValue(self.__bdtDaten["tabrow_tochter"]) == tochter:
                    UseVisum2Again = True
                else:
                    UseVisum2Again = False
                    tochter = te.AttValue(self.__bdtDaten["tabrow_tochter"])
                
                llax = ListenPfad+te.AttValue(self.__bdtDaten["tabrow_llax"])
                fil = FilterPfad+te.AttValue(self.__bdtDaten["tabrow_fil"])
                blattname = te.AttValue(self.__bdtDaten["tabrow_blattname"])
                zelladresse = te.AttValue(self.__bdtDaten["tabrow_zellname"])
                COMFunktion = te.AttValue(self.__bdtDaten["tabrow_COMF"])
                
                self.__MeinVisum.Log(20480, "Ausgabe Blatt "+ str(blattname) +" .")

                aktListe=None
                aktFilter=None
                
                if tochter != "-":
                    if not(UseVisum2Again):
                        Visum2 = win32com.client.Dispatch("Visum.Visum")                # Starten eines 2. VISUM
                        Visum2.LoadVersion(os.path.join(self.__MeinVisum.GetPath(2), tochter))    # im 2. Visum: Laden der Versionsdatei
                else:
                    pass
                    
                #getattr setzt befehl zusammen: --> self.__MeinVisum.Workbench.Lists.CreateXYZList
                if tochter == "-": 
                    aktListe = getattr(self.__MeinVisum.Workbench.Lists, COMFunktion)
                    aktFilter = self.__MeinVisum.Filters
                else:
                    aktListe = getattr(Visum2.Workbench.Lists, COMFunktion)
                    aktFilter = Visum2.Filters
    
                #alle vorherigen Filter initalisieren
                aktFilter.InitAll()
            
                #Filterdatei laden
                if os.path.isfile(fil):
                    aktFilter.Open(fil)
                    self.__MeinVisum.Log(20480, "- Filterdatei "+ str(fil) +" gefunden.")
                else:
                    self.__MeinVisum.Log(20480, "- Filterdatei "+ str(fil) +" nicht angegeben oder nicht gefunden.")
                    
                #self.__MeinVisum.Log(20480, "Test")
                #ListLayout laden
                if os.path.isfile(llax):
                    aktListe.OpenLayout(llax)
                    aktListe.SaveToClipboard(9,0)
                    #self.__MeinVisum.Log(20480, u"- Listen für "+ str(llax) +" in Zwischenablage.")
                    self.__MeinExcel.ExcelDatenEinfuegen(blattname,zelladresse)
                    self.__MeinVisum.Log(20480, u"- Liste "+ str(llax) +" kopiert.")
                else:
                    self.__MeinVisum.Log(20480, u"- Listenlayoutdatei "+ str(llax) +" nicht gefunden.")
                
            else:
                continue

        aktFilter.InitAll()
        self.__MeinVisum.Log(20480, u" Alle Listen fertig.")
        
        Visum2 = None


        return True
    # Ende def -----------------


# Listen der Visumlisten, die kopiert werden
        # Syntax:   [Aktiv[0,1], ExcelTabellenblatt, Filterdateiname, 				Listenlayoutname, 					Visum-Funktion ]
#        ListenMat= [
#                    [1, "vis_NSch",                 FilterPfad+r"",                 ListenPfad+r"Ausw_NSch.llax",                       "CreateDemandStratumList"],
#                    [1, "vis_Hp_SPNV",              FilterPfad+r"Ausw_Hp.fil",      ListenPfad+r"Ausw_Hp.llax",                         "CreateStopPointBaseList"],
#                    ]


        

if __name__ == '__main__':
    pass            #Klammer ist wichtig bei Funktionsaufrufen