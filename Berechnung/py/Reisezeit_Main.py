#-------------------------------------------------------------------------------
# Name:        export_in_udT_Main
# Purpose:
#
# Author:      janna.ulrich
#
# Created:     19.05.2022
# Copyright:   (c) PTV Transport Consult GmbH janna.ulrich birgit.dugge 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import time
import importlib
import Reisezeit_Modul
importlib.reload(Reisezeit_Modul)

UDA_MatNo_Skim = "MatNo_Skim"
UDA_MatNo_Demand = "MatNo_Demand"
UDA_MatNo_Filter = "MatNo_Filter"
UDA_Mean = "VM_MEAN"
UDA_MatSum = "MatDemand_Sum"
UDA_Mat2Sum = "MatDemand_x_Skim_Sum"
UDA_Calc = "Calc"
UDA_CR="CR"

t1= time.time() #Startzeit speichern
Visum.Log(20480,"Start Auswertung Reisezeit ")
bin = [0, 5, 10, 15, 30, 45, 60, 90, 120, 9999]
bin_UDAs = ['VM_Anteil_000005', 'VM_Anteil_005010', 'VM_Anteil_010015', 'VM_Anteil_015030', 'VM_Anteil_030045', 'VM_Anteil_045060', 'VM_Anteil_060090', 'VM_Anteil_090120', 'VM_Anteil_120999']
bin_EM_UDAs = ['EM_Anteil_000005', 'EM_Anteil_005010', 'EM_Anteil_010015', 'EM_Anteil_015030', 'EM_Anteil_030045', 'EM_Anteil_045060', 'EM_Anteil_060090', 'EM_Anteil_090120', 'EM_Anteil_120999']

tableName = "Dashboard Reisezeit"
if Visum.Net.TableDefinitions.ItemByKey(tableName).TableEntries.Count>0:
    export = Reisezeit_Modul.export_udT(Visum, UDA_MatNo_Skim, UDA_MatNo_Demand, UDA_MatNo_Filter, UDA_Calc, UDA_Mean, UDA_MatSum, UDA_Mat2Sum, UDA_CR, bin, bin_UDAs, bin_EM_UDAs, tableName)
    export.write_Verteilung()
    #export.write_CR_Wert() empirische Daten noch eintragen
    Visum.Log(20480,"Ende Auswertung Reisezeit, Zeitbedarf" +str(round(time.time()-t1,1))+" sec.")
else:
    Visum.Log(16384,"Keine Matrizen auszuwerten (Tabelle ohne Datensätze)! " +str(round(time.time()-t1,1))+" sec.")