# Analiza zbirov Yu-Gi-Oh! igralnih kart
#### Projektna naloga na temo analize in predstavitve podatkov.

## Cilji projekta in viri podatkov
Cilj projekta je analizirati uspešnost različnih strategij in kart v igri Yu-Gi-Oh!. V ta namen sem zbral podatke o zbirih s spletne strani https://www.masterduelmeta.com.
Glavnina podatkov je pribljižno 350 zbirov, pri čemer vsak vsebuje med 40 in 75 posameznih igralnih kart. Ob času pisanja je to 28358 kart. Poleg osnovne analize podatkov
program omogoča še pregled prenesenih zbirov, njihovo izvažanje v obliki .ydk datoteke ter ogled podatkov posamezne karte.

### Delovanje programa
Program je razdeljen v datoteki **html_scraper.py** in **predstavitev.ipynb**. 

Prva datoteka prenese html vira s pomočjo knjižnice *requests*, s knjižnico *re* iz html-jev izlušči podatke in jih nato s knjižnicama *csv* in *os* urejeno 
shrani kot .csv in . text datoteke v podmapi **podatki**. Iz datoteke tier_list.html pridobi tabelo tier_list.csv. Iz top_deck.html pridobi število zbirov
za posamezno stretegijo (top_decks.csv), vse posamezne zbire (.text datoteke v mapi **zbiri**) ter prešteje pojavitve posameznih kart (total_cards.csv).

Druga datoteka analizira podatke v csv datotekah. Pri tem uporablja knjižnice *pandas*, *matplotlib.mpatches* in *numbpy* za oblikovanje tabel in grafov.
Datoteka omogoča tudi ogled pozameznih zbirov in kart v njih.

## Navodila za uporabo
Za delovaje programov je potrebno delujoče okolje jupyter notebooks z vsemi v zgornjem odseku omenjenimi knjižnicami. Za ogled analize podatkov je potrebno odpreti interaktivno
datoteko *predstavitev.ipynb*. Na začetku te datoteke je zakomentirana (torej izkloplenja) opcija ponovnega nalaganja podatkov s spleta.
Podatki naloženi v repozitoriju so z datuma 19. 8. 2024. 
