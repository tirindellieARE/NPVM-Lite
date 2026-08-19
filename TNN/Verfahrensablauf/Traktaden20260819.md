* Fur die Modusversionen fehlen noch die Tochterattributen (immer noch die Nachfrage att in Verfahrensablauf)
* Github repo for Verfahrensablauf
* Skript die TNN\_AggGemeinde zu importieren
* TNN\_SetUp\_Siko/Heimataufkommen py scripts?
* Vereinfachung des Verfahrensablauf? TNN\_Agreg\_Select ist für alle POI = 1 so es ist nicht wirklich nutzlich
* ID EINHEIT, ZONES\\LÄNGE\_MAINZONENBINNENVERKEHR, TTC\_MAINZONENBINNENVERKEHR nicht gefunden
* RO\_PEK\_Nummer and RO\_PEK\_Code what is it exyclty?
* POI 841300000 (liguria) does not get assinged any zone --> corrected manually but why?
* added this to TNN\_Import\_Anbindungen\_Ges.py (some MAINZONENO = 0 create problems) : 

Gruppieren nach 'MAINZONENO', 'DIRECTION', und 'NODENO', Anwenden der Aggregationsregeln und Sortieren

grouped = df.groupby(\['MAINZONENO', 'DIRECTION', 'NODENO'])
result = grouped.apply(custom\_aggregation).reset\_index()

Datensätze ohne gültige Hauptzone (MAINZONENO == 0) entfernen

vorher = len(result)
result = result\[result\['MAINZONENO'].astype(float) != 0].reset\_index(drop=True)
Visum.Log(20480, "Datensätze mit MAINZONENO=0 entfernt: " + str(vorher - len(result)))

Sortieren nach \['MAINZONENO', 'NODENO' , 'DIRECTION'] in aufsteigender Reihenfolge

result = result.sort\_values(by=\['MAINZONENO', 'NODENO', 'DIRECTION']).reset\_index(drop=True)
\*

* Export\_Anbindugen for OEV fails --> CHATGPT explanation:So the AttrExists guard fixes the crash correctly and lets the export complete. But before relying on the output, confirm what the PT Tochter reconstruction actually needs from these connectors. If it just needs the connectors recreated with their TSYSSET and structural attributes (which the import script's AddConnector + TSYSSET handles), you're fine. If it needs PT walk-access times preserved, we'd need to add the appropriate PuT connector-time attribute to the export list, separate from T0\_TSYS
* Kordon haben keine Geometrie und sie ausfallen im Prozess (210 Zonen mit MAINZONENO=0 entfernt) 

