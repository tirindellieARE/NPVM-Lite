# -*- coding: utf-8 -*-
# ##############################################################################
#    Script zum Kopieren von Visum-Listen nach Excel
#    Aufruf von VISUM aus
#    HIER: Modul Excel - Handling des Excel-Master / Exceldatei
#
#    Erstellt durch PTV Transport Consult GmbH, Dr. Birgit Dugge
#
# ##############################################################################


import win32com.client      #Bibliothek für COM-Schnittstelle (VISUM und Excel)
import os

class Exceldatei(object):

    def __init__(self,Masterdatei,SaveAsDatei):
        self.__Masterdatei=Masterdatei
        self.__SaveAsDatei=SaveAsDatei
        self.__Excelobj=win32com.client.Dispatch("Excel.Application")
        self.__ExcelDateiOeffnen()


    def __del__(self):
        self.__ExcelDateiSchliessen()


    def __ExcelDateiOeffnen(self):
        try:
            self.__Excelobj.Workbooks.Open(self.__Masterdatei)

        except:
            print("Masterdatei nicht gefunden")
            return False
            exit

        self.__Excelobj.Visible = True

        return True


    def __ExcelDateiSchliessen(self):

        try:
            os.remove(self.__SaveAsDatei)
        except:
           pass

        self.__Excelobj.ActiveWorkbook.SaveAs(self.__SaveAsDatei)
        self.__Excelobj.Quit()

        return True


    def ExcelDatenEinfuegen(self,Blattname,Versatz):
        #  Paste from Clipboard

        try:
            sheet=self.__Excelobj.ActiveWorkbook.Sheets(Blattname)
            sheet.Paste(sheet.Range("B3").Offset(Versatz+1,1))                      #Offset=1,1--> ergibt Zelle B3
        except:
            print("Blatt " +Blattname + " fehlt oder Daten fehlerhaft")
        pass

        return True


    def ExcelHistoDatenZeileweiseEinfuegen(self,Blattname,Versatz):
        #  Paste aus der Zwischenablage, zeilwenweise
        # Für Histogramm
        try:
            sheet=self.__Excelobj.ActiveWorkbook.Sheets(Blattname)
            sheet.Paste(sheet.Range("C3").Offset(Versatz+1,1))                      #Offset=1,1--> ergibt Zelle B3
        except:
            print("Blatt " +Blattname + " fehlt oder Daten fehlerhaft")
            pass

    def ArrayToClipboard(self, Array, Zeile):
        #  Join Befehl -> Trennzeichen am Anfang
        #  Join Befehl -> Listeninhalt muss str sein
        #  Umwandlung so: str(e) for e in list1
        #  eineZeile = ein vektor = self.__ListeHistogrammDaten[a]
        #eineZeile="\t".join(str(self.__ListeHistogrammDaten[a][e]) for e in range(len(self.__ListeHistogrammDaten[a])))+chr(10)  #chr(10) ist Zeilenumbruch,"\t" Tabulator

        eineZeile=" ".join(str(Array[Zeile][e]) for e in range(len(Array[Zeile])))  #chr(10) ist Zeilenumbruch,"\t" Tabulator
        eineZeile=eineZeile.replace(".",",")                                    #Dezimaltrennzeichen ersetzen
        textToCopy=eineZeile

        # der Befehl funktioniert nicht mit Tabulator und Zeilenumbruch
        # Deshalb Leerzeichen, in Excel ist der Befehl Daten|Text in Spalten einmalig auszuführen
        command = "echo " + textToCopy + " | clip"
        os.system(command)

    # für Parameter-Schnelltest
    def ExcelDatenUmkopieren(self, Blattname, Blattname2, Versatz):
        #  Daten umkopieren vom Rohdaten-Blatt
        # Zeile einfügen (Altdaten "nach unten durchschieben")
        # Blattname - Visum-Rohdatenblatt
        # Blattname2 - Zusammenfassungsblatt
        # Versatz .. auf Zusammenfassungsblatt

        try:
            # Zeile einfügen
            sheet=self.__Excelobj.ActiveWorkbook.Sheets(Blattname2)

            sheet.Rows("4:4").Select
            #Sheets(c).Select
            Rows("4:4").Select
            MyWorksheet.Range['A1', 'A1'].EntireRow.Insert(xlShiftDown);
            #Selection.Insert Shift:=xlDown, CopyOrigin:=xlFormatFromLeftOrAbove
            vis_sheet=self.__Excelobj.ActiveWorkbook.Sheets(Blattname)
            vis_sheet.Range("B8:S8").Select

            Selection.Copy
            sheets.Range("K4").Select
            #Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks:=False, Transpose:=False
            #markiere
            sheet.Paste(sheet.Range("K4").Offset(Versatz+1,1))                      #Offset=1,1--> ergibt Zelle B3
        except:
            print("Blatt " +Blattname + " fehlt oder Daten fehlerhaft")
            pass

#"Hauptprogramm - Testumgebung für Klasse
if __name__ == '__main__':

    testdatei=r"n:\C823068_IVM_Magdeburg\4_Visum\xls-Auswertung\pstMaster2.xlsm"
    save_As_Datei=r"n:\C823068_IVM_Magdeburg\4_Visum\xls-Auswertung\test.xlsm"
    myxls=Exceldatei(testdatei,save_As_Datei)
    myxls.ExcelDatenUmkopieren("vis","Alle",0)

    pass            #Klammer ist wichtig bei Funktionsaufrufen
