#-------------------------------------------------------------------------------
# Name:        
# Purpose:     Import der Daten zu Personengruppen in die Visum-Verkehrsbezirke
#
# Author:      birgit Dugge
#
# Created:     28.10.2025 in Visum 24-20
# 
# Hinweise siehe unten
#-------------------------------------------------------------------------------


# Python-Bibliotheken -------
import time

# Initialisierung-------
t1= time.time() #Startzeit speichern
udtName="TNN_Personengruppen"

# Berechnung -----------
 
# Attributsliste der bdT ermitteln und Daten aus der Tabelle lesen ---------------------
atts=Visum.Net.TableDefinitions.ItemByKey(udtName).TableEntries.Attributes
# Bezirksnummer und andere überflüssige Splaten werden nicht importiert
udt_attNamen_dict = {i.ID : atts.ItemByKey(i.ID).Code for i in atts.GetAll if i.ID not in ['MAINZONENO', 'TABLEDEFINITIONNAME', 'NO', 'EXISTSINNET', 'ANZMUTTERBEZ']}  

# Daten der bdT lesen und als Bezirksdaten einfügen
udt_Daten_list = Visum.Net.TableDefinitions.ItemByKey(udtName).TableEntries.GetMultipleAttributes(list(udt_attNamen_dict.keys()))

# Match mit Bezirksnummern --> Filtaer auf bezirke mit PEK_Nr =1 und 2, Pek_Nr 3 ist Umland un bekommt keine Strukturdaten
# Bezirksfilter ist wichtig, weil manchmal die Kordonbezirke niedirgere Nummern haben und deshlb zuerst geführt werden 
Visum.Filters.ZoneFilter().Init()
Visum.Filters.ZoneFilter().UseFilter=True
Visum.Filters.ZoneFilter().AddCondition("OP_None", False, "MAINZONE\TNN_TOCHTER_RO_PEK_NR", "LessVal", 3)

Visum.Net.Zones.SetMultipleAttributes(list(udt_attNamen_dict.values()), udt_Daten_list, OnlyActive = True)

Visum.Filters.ZoneFilter().Init()

# Aufräumen /Finalisierung-------------------------
Visum.Log(20480,"Import PG fertig, " +str(round(time.time()-t1))+" sec.")


# Hinweis: 
# Visum 24-10 hat ein Bug bei .Attributes.GetAll.
# Attribute mit Subattributen werden ausgegeben ohne Subattributen, z.B. nur T0-TSys statt T0-TSys(FGV), T0-TSys(RAD), ...
# Das betrifft auch MobRaten und Aufkommensraten, diese Attribute haben sogar zwei Subattributen (Nachfrageschicht und Rau 
