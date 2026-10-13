# -*- coding: cp1252 -*-
# ##############################################################################
#    Script zum Kopieren von Visum-Listen nach Excel
#    Aufruf von VISUM aus
#    HIER: Modul Excel - Handling des Excel-Master / Exceldatei
#
#    Erstellt durch PTV Transport Consult GmbH, Dr. Birgit Dugge
#
# ##############################################################################


from win32com.client import DispatchEx      #Bibliothek f�r COM-Schnittstelle (VISUM und Excel)
import os

class Exceldatei(object):

    def __init__(self,Masterdatei,SaveAsDatei,Visum):
        self.__Masterdatei=Masterdatei
        self.__SaveAsDatei=SaveAsDatei
        self.__Excelobj=DispatchEx('Excel.Application')
        self.__ExcelDateiOeffnen()
        self.__MeinVisum=Visum


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


    def ExcelDatenEinfuegen(self,Blattname,Zelleadr):
        #  Paste a table from Clipboard
        try:
            sheet=self.__Excelobj.ActiveWorkbook.Sheets(Blattname)
            sheet.Paste(sheet.Range(Zelleadr))
        except:
            print( "Blatt " +Blattname + " fehlt oder Daten fehlerhaft")
            self.__MeinVisum.Log(20480, u"Blatt "+ Blattname +" nicht gefunden.")
        pass
        return True
        
    #def ExcelDatenEinfuegen(self,Blattname,Versatz):
        #  Paste a table from Clipboard
    #    try:
    #        sheet=self.__Excelobj.ActiveWorkbook.Sheets(Blattname)
    #        sheet.Paste(sheet.Range("B3").Offset(Versatz+1,1))                      #Offset=1,1--> ergibt Zelle B3
    #    except:
    #        print( "Blatt " +Blattname + " fehlt oder Daten fehlerhaft")
    #        self.__MeinVisum.Log(20480, u"Blatt "+ Blattname +" nicht gefunden.")
    #    pass
    #    return True


    def kopiereScreenshotsInMasterdatei(self,tabname_screenshots, path_png):
        #  Paste a list of screenshots in Excel
        adress_del_marker = "AA1"
        
        #User Input Visum-Tabellen Spaltennamen
        tabrow_fil = r'Fil'
        tabrow_gpa = r'GPA'
        tabrow_export = r'Export'
        tabrow_tabname = r'EXCELBLATT'
        tabrow_celladress = r'Excelzelle'
        tabrow_pngname = r'SCREENSHOTNAME'
        tabrow_left = r'Left'
        tabrow_top = r'Top'

        #Tabelle mit Daten in Visum ansprechen
        tabdef = self.__MeinVisum.Net.TableDefinitions.ItemByKey(tabname_screenshots)


        #L�schdoku f�r Screenshots initialisieren: Beim L�schen der Bilder muss sichergestellt werden, dass zwei Screenshots auf das selbe Tabellenblatt eingef�gt werden d�rfen
        for sheet in self.__Excelobj.ActiveWorkbook.Sheets:
            self.__Excelobj.Worksheets(sheet.Name).Activate()      
            sheet.Range(adress_del_marker).Value = "False"
        self.__MeinVisum.Log(20480, u"Loeschdoku fertig.")
        
        #Daten in Tabelle durchgehen, Screenshots erzeugen und
        for Screenshot in tabdef.TableEntries:

            if Screenshot.AttValue(tabrow_export) == 1.0:
                self.__MeinVisum.Filters.InitAll()
                ws_name = Screenshot.AttValue(tabrow_tabname)
                self.__MeinVisum.Log(20480, ws_name)
                filename_png = Screenshot.AttValue(tabrow_pngname)
                cell_adress = Screenshot.AttValue(tabrow_celladress)
                #left=Screenshot.AttValue(tabrow_left)
                #top=Screenshot.AttValue(tabrow_top)
                
                ws = self.__Excelobj.Worksheets(ws_name)
                #ws = self.__Excelobj.ActiveSheet
                del_done = ws.Range(adress_del_marker).Value
                
                if del_done == "False":
                    ws._images = []  #Vorhandene Screenshots l�schen
                    ws.Range(adress_del_marker).Value = "True" #L�schmarker setzen

                if Screenshot.AttValue(tabrow_fil) != '':
                    self.__MeinVisum.Filters.Open(Screenshot.AttValue(tabrow_fil))

                self.__MeinVisum.Net.GraphicParameters.Open(Screenshot.AttValue(tabrow_gpa))
            
                self.__MeinVisum.Graphic.Screenshot(filename_png,1)
                self.__MeinVisum.Log(20480, u"Fuege "+ filename_png+ " auf Blatt "+ws_name +", "+ cell_adress +" ein.")
                
                ws.Range(cell_adress).Value=cell_adress
                
                #ws.Range(cell_adress).Select
                self.__Excelobj.ActiveSheet.Pictures.Insert(path_png + '\\' + filename_png)
                
                #self.__MeinVisum.Log(20480, "Name: "+ws.Name)
                
                #ws.Pictures().Insert(path_png + '\\' + filename_png)
                #fn=path_png + '\\' + filename_png
                #ws.shapes.AddPicture(fn,True,True,left,top,-1,-1)
        
if __name__ == '__main__':
    pass            
    
    #Range("B3").Select
    #ActiveSheet.Pictures.Insert( "C:\Users\BD\Pictures\Screenshots\2022-10-28 09_48_18-Mooncake auf Twitter_ �Der Bahnhof f�hrt weg.. https___t.co_LN1cmiaiTT� _ Twitte.png" ).Select
    
    #https://stackoverflow.com/questions/50409440/python-insert-object-into-excel-in-a-specific-row-and-column-with-win32com
    #Sub Bildvariabel()


#https://www.gamestar.de/xenforo/threads/bilder-aus-hyperlinks-in-excel-direkt-anzeigen-lassen.384627/
#Dim url

#Sheets("Tabelle1").Select
#url = "http://picurama.com/_fotos/005_Events/007_Norisring_2010/001_Formel_3.JPG"

#ActiveSheet.Pictures.Insert(url).Select
#With Selection
#.Top = Range("A1").Top
#.Left = Range("A1").Left
#End With

#End Sub