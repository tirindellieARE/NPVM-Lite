* **Schritt 6:** 

\# In dieser Obermutter kann dann der Verfahrensablauf für Mutterversion geladen werden (wenn er noch nicht vorhanden ist).

\# Zum Nachschauen/Vergleichen kann man die Obermutterversion in einer zweiten Version laden. --> Verfahrensablauf für Mutterversion ist immer noch 1\_TNN\_NPVM\_NMod\_Mutter\_003.xml? 



* **Schritt 20:** 

\# Anleitung:



\# Jetzt ist manuelle Arbeit notwendig.



\# In den POI-Kategorien 500 (Auslandsbezirke) 501 (Bundesländer) und 502 (Kreise) ist ein Flag in das Attribut "TNN\_PEK\_Select" zu setzen, 

\# --> Welcher Räume werden Planungsgebiet, Einflussbereich oder Kordon ?

\# Aus der Kennzeichnung der Kreise und  Bundesländer leitet sich ab, welche Bezirke später zum Modell gehören und welche aggregiert werden



\# Gebraucht wird das Attribut TNN\_PEK\_Select und TNN\_PEK\_Select\_Aggr und hilfreich ist das Attribut BL-Nr für die Bundeslandnummer



\# Setzung für das Beispiel Gelsenkrichen

\# POI 502 TNN Kreise: Setze TNN\_PEK\_Select       = 1 (Planungsgebiet) -> für den  Kreis Gelsenkrichen --> originalen Verkehrsbezirke werden weiter verwendet

\# POI 502 TNN Kreise: Setze TNN\_PEK\_Select       = 2 (Einflussraum)   -> für die direkt angrenzende Kreise Essen, Bottrop, Recklinghausen, Bochum, Herne -> originalen Verkehrsbezirke werden weiter verwendet

\# POI 502 TNN Kreise: Setze TNN\_PEK\_Select       = 3 (Kordon)         -> für restliche Kreise DES HEIMAT-BUNDESLANDES NRW: Düsseldorf, Duisburg, Krefeld, usw. --> zukünftige Verkehrsbezirke entsprechen den Kreisen

\# POI 501 TNN Bundesländer: Setze TNN\_PEK\_Select = 3 (Kordon)         -> angrenzende Bundesländer AUSSERHALB NRW: Schleswig, Hamburg, Niedersachen, Bremen,--> zukünftige Verkehrsbezirke entsprechen den Kreisen

\# POI 500 TNN Ausland: Setze TNN\_PEK\_Select      = 3 (Kordon)         -> ausländische Zellen / Staaten außer D                                            --> zukünftige Verkehrsbezirke entsprechen den Staaten / ausländischen Zellen



\#Setzung für TNN\_PEK\_Select\_Aggr

\# 0 - keine Aggregation, originalen Verkehrsbezirke werden übernommen

\# 1 - Aggregation z.B. auf Untergemeinde-, Gemeinde- oder Kreisebene 



\# ggf alte Setzungen aus anderen Exporten initialisieren, Initialisierungswert =0 --> TNN\_PEK\_Select\_Aggr = 1 und TNN\_PEK\_Select = 1, ist es korrekt? was soll ich hier genau machen? 



* **Schritt 105:** Skript TNN\_Export\_MobRate2.py muss noch debuggt werden, der Übertrag funktioniert noch nicht richtig. Ich melde mich, sobald das Skript funktioniert --> debugged Skript?
