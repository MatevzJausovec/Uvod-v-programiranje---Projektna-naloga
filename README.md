# Analiza zbirov Yu-Gi-Oh! igralnih kart
#### Projektna naloga na temo analize in predstavitve podatkov.

## Cilji projekta in viri podatkov
Cilj projekta je analizirati uspešnost različnih strategij in kart v igri Yu-Gi-Oh!. V ta namen sem zbral podatke o zbirih igralnih kart s spletne strani [Master Duel Meta](https://www.masterduelmeta.com).
Glavnina podatkov je približno 350 zbirov, pri čemer vsak vsebuje med 40 in 75 posameznih igralnih kart. Ob času pisanja je to 28358 kart. Poleg osnovne analize podatkov
program omogoča še pregled prenesenih zbirov ter njihovo izvažanje v obliki .ydk datoteke. Za zadnji del je uporabljen tudi API spletnega mesta [YGOPRODeck](https://ygoprodeck.com/).

### Delovanje programa
Program je razdeljen v datoteke **html_scraper.py**, **predstavitev.ipynb** in **deck_creator.py**. 

Prva datoteka prenese html vira s pomočjo knjižnice *requests*, s knjižnico *re* iz html-jev izlušči podatke in jih nato s knjižnicama *csv* in *os* urejeno 
shrani kot .csv in . text datoteke v mapi **podatki**. Iz datoteke tier_list.html pridobi tabelo tier_list.csv. Iz top_deck.html pridobi število zbirov
za posamezno stretegijo (top_decks.csv), vse posamezne zbire (.text datoteke v podmapi **zbiri**) ter prešteje pojavitve posameznih kart (total_cards.csv).

Druga datoteka analizira podatke v csv datotekah. Pri tem uporablja knjižnice *pandas*, *matplotlib* in *numbpy* za oblikovanje tabel in grafov.
Datoteka omogoča tudi ogled pozameznih zbirov in prenos izbranega zbira v format .ydk. Za zadnji del so uporabljene funkcije iz tretje pomožne datoteke.
V tej je uporebljena tudi knjižnica *json*.

Zbiri kart, ki jih program obdela so tisti, ki so jih uporabniki naložili v zadnjih dveh tednih, zato je analiza vsebinsko delno vezana na
specifične podatke, ki so naloženi v repozitoriju. Podatki naloženi v repozitoriju so z datuma 21. 8. 2024. 

## Navodila za uporabo
Za delovaje programov je potrebno delujoče okolje jupyter notebooks z vsemi v zgornjem odseku omenjenimi knjižnicami. Za ogled analize podatkov je potrebno 
odpreti interaktivno datoteko *predstavitev.ipynb*. Na začetku te datoteke je zakomentirana (izkloplenja) opcija ponovnega nalaganja podatkov s spleta.

