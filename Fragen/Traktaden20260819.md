* Fur die Modusversionen fehlen noch die Tochterattributen (immer noch die Nachfrage att in Verfahrensablauf)
* Github repo for Verfahrensablauf
* Skript die TNN\_AggGemeinde zu importieren
* TNN\_SetUp\_Siko/Heimataufkommen py scripts?
* Can we simplify a bit the Verfahrensablauf? for instance the flag for aggregating is useless in this context
* 2026-08-12 09:50:39.362           Error MATRIX: Attribut mit ID EINHEIT nicht gefunden. Schritte 198
* MIV: Error Fehler bei der Ausführung von Verfahrensschritt  57: "Attribut ändern": Beim Berechnen der Formel ist ein Fehler aufgetreten: "OBERBEZIRK: Attribut mit ID SUM:ZONES\\LÄNGE\_MAINZONENBINNENVERKEHR nicht gefunden.". Formel: "if (\[TNN\_TOCHTER\_RO\_PEK\_NR]=3,0,\[SUM:ZONES\\LÄNGE\_MAINZONENBINNENVERKEHR])"
* MIV: Error Fehler bei der Ausführung von Verfahrensschritt  74: "Attribut ändern": Beim Berechnen der Formel ist ein Fehler aufgetreten: "OBERBEZIRK: Attribut mit ID SUM:ZONES\\TTC\_MAINZONENBINNENVERKEHR nicht gefunden.". Formel: "if (\[TNN\_TOCHTER\_RO\_PEK\_NR]=3,0,\[SUM:ZONES\\TTC\_MAINZONENBINNENVERKEHR])"
* RO\_PEK\_Nummer and RO\_PEK\_Code what is it?
* POI 841300000 (liguria) does not get assinged any zone --> corrected manually but why?
* added this to TNN\_Import\_Anbindungen\_Ges.py:

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

* Export\_Anbindugen for OEV fails --> does it really make sense? :So the AttrExists guard fixes the crash correctly and lets the export complete. But before relying on the output, confirm what the PT Tochter reconstruction actually needs from these connectors. If it just needs the connectors recreated with their TSYSSET and structural attributes (which the import script's AddConnector + TSYSSET handles), you're fine. If it needs PT walk-access times preserved, we'd need to add the appropriate PuT connector-time attribute to the export list, separate from T0\_TSYS

