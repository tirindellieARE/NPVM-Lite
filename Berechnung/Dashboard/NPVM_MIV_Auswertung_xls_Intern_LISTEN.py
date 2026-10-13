# -*- coding: utf-8 -*-
# ##############################################################################
#    Script zum Kopieren von Visum-Listen nach Excel
#    Aufruf von VISUM aus
#    HIER: Modul Listen - Kopieren von Visum-Listen
#
#    Erstellt durch PTV Transport Consult GmbH, MSc Kevin Klopsch, Dr. Birgit Dugge
#
# ##############################################################################

import os                   #Betriebssystemfunktionen, z.B. Zerlegung von Dateinamen u.ä.

class Visumlisten(object):
    #MeinVisum=None

    def __init__(self,Visum,Excel):
        self.__MeinVisum=Visum
        self.__MeinExcel=Excel

    def kopiereListenInMasterdatei(self):

        """ Prozedur zum Kopieren von Listen (Kalibrierungsauswertung von VISUM nach Excel
            Excel Datei hat gleichen Namen wie VISUM-Version
            Jede Liste kommt auf ein eigenes Excelblatt
        """

        FilterPfad = self.__MeinVisum.GetPath(21)
        ListenPfad = self.__MeinVisum.GetPath(20)

        #Listenmatrix - {Aktiv[0,1], ExcelTabellenblatt, Filterdateiname, Listenlayoutname}
        ListenMat= []

        #vis_OBezBez_VL_NSch_BV
        ArrayBound = len(ListenMat)
        AnzNichtGefundeneListenLayouts=0
        
        for i in range(0, ArrayBound):

            #Liste rausschreiben?
            if ListenMat[i][0] > 0:

                #Liste Verkehrsysteme
                aktListe=None
                aktFilter=None

                #getattr --> self.__MeinVisum.Workbench.Lists.CreateXYZList
                aktListe = getattr(self.__MeinVisum.Workbench.Lists, ListenMat[i][4])

                aktFilter=self.__MeinVisum.Filters

                #alle vorherigen Filter initalisieren
                aktFilter.InitAll()

                #Filterdatei laden
                 #Filterdatei laden
                if os.path.isfile(ListenMat[i][2]):
                    aktFilter.Open(ListenMat[i][2])
                    self.__MeinVisum.Log(20480, u"Filter "+ str(ListenMat[i][2]) +" gefunden.")
                else:
                    self.__MeinVisum.Log(20480, u"Filter "+ str(ListenMat[i][2]) +" nicht gefunden.")
                    pass

                #ListLayout laden
                if os.path.isfile(ListenMat[i][3]):
                    aktListe.OpenLayout(ListenMat[i][3])
                    aktListe.SaveToClipboard(9,0)
                    self.__MeinExcel.ExcelDatenEinfuegen(ListenMat[i][1],0)
                    self.__MeinVisum.Log(20480, u"Listen "+ str(ListenMat[i][3]) +" fertig.")
                else:
                    self.__MeinVisum.Log(20480, u"Listenlayout "+ str(ListenMat[i][3]) +u" nicht gefunden.")
                    self.__MeinVisum.Log(20480, u"Listen "+ str(ListenMat[i][3]) +u" nicht befüllt.")
                    AnzNichtGefundeneListenLayouts=AnzNichtGefundeneListenLayouts+1
                    pass

        #aktFilter.InitAll()
        self.__MeinVisum.Log(20480, u"Ende Auswertung, "+str(AnzNichtGefundeneListenLayouts)+u" Listenlayouts nicht gefunden.")
        
        return True


if __name__ == '__main__':
    pass            #Klammer ist wichtig bei Funktionsaufrufen
