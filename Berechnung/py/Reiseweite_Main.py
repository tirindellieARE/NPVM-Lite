#-------------------------------------------------------------------------------
# Name:        export_in_udT_Main
# Purpose:
#
# Author:      janna.ulrich
#
# Created:     19.05.2022
# Copyright:   (c) PTV Transport Consult janna.ulrich birgit.dugge 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import time
import importlib
import Reiseweite_Modul
importlib.reload(Reiseweite_Modul)

UDA_MatNo_Skim = "MatNo_Skim"
UDA_MatNo_Demand = "MatNo_Demand"
UDA_MatNo_Filter = "MatNo_Filter"
UDA_Mean = "VM_MEAN"
UDA_MatSum = "MatDemand_Sum"
UDA_Mat2Sum = "MatDemand_x_Skim_Sum"
UDA_Calc = "Calc"
UDA_CR="CR"

t1= time.time() #Startzeit speichern
Visum.Log(20480,"Start Auswertung Reiseweite ")
bin = [0, 1, 2, 3, 5, 10, 15, 20, 30, 50, 100, 999999]
#Groß- und Kleinschreibung beachten
bin_UDAs = ['VM_Anteil_000001', 'VM_Anteil_001002', 'VM_Anteil_002003', 'VM_Anteil_003005', 'VM_Anteil_005010', 'VM_Anteil_010015', 'VM_Anteil_015020', 'VM_Anteil_020030', 'VM_Anteil_030050', 'VM_Anteil_050100', 'VM_Anteil_100999']
bin_EM_UDAs = ['EM_Anteil_000001', 'EM_Anteil_001002', 'EM_Anteil_002003', 'EM_Anteil_003005', 'EM_Anteil_005010', 'EM_Anteil_010015', 'EM_Anteil_015020', 'EM_Anteil_020030', 'EM_Anteil_030050', 'EM_Anteil_050100', 'EM_Anteil_100999']

tableName = "Dashboard Reiseweite"

if Visum.Net.TableDefinitions.ItemByKey(tableName).TableEntries.Count>0:
    export = Reiseweite_Modul.export_udT(Visum, UDA_MatNo_Skim, UDA_MatNo_Demand, UDA_MatNo_Filter, UDA_Calc, UDA_Mean, UDA_MatSum, UDA_Mat2Sum, UDA_CR, bin, bin_UDAs, bin_EM_UDAs, tableName)
    export.write_Verteilung()
    #export.write_CR_Wert()
    export.write_CR_Wert_Upp_Low_Wert()
    Visum.Log(20480,"Ende Auswertung Reiseweite, Gesamter Zeitbedarf " +str(round(time.time()-t1,1))+" sec.")
else:
    Visum.Log(16384,"Keine Matrizen auszuwerten (Tabelle ohne Datensätze)! " +str(round(time.time()-t1,1))+" sec.")