import csv
import os
import requests
import re


html_tier_list = "https://www.masterduelmeta.com/tier-list"
file_tier_list = "tier_list.html"
html_top_decks = "https://www.masterduelmeta.com/top-decks"
file_top_decks = "top_decks.html"
mapa_podatkov = "podatki"
mapa_zbirk = "podatki\\zbiri"

# url --> html file splošno

def download_url_to_string(url):
    try:
        page_content = requests.get(url)
        page_content.encoding = 'UTF-8'
        return page_content.text
    except Exception:
        print("Napaka!")

def save_string_to_file(text, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None

def save_frontpage(page, directory, filename):
    html_besedilo = download_url_to_string(page)
    save_string_to_file(html_besedilo, directory, filename)

# file --> string za re

def read_file_to_string(directory, filename):
    with open(os.path.join(directory,filename), encoding="utf-8") as f:
        return f.read()
    
# shrani seznam dicts --> csv

def write_csv(fieldnames, rows, directory, filename):
    """
    Funkcija v csv datoteko podano s parametroma "directory"/"filename" zapiše
    vrednosti v parametru "rows" pripadajoče ključem podanim v "fieldnames"
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8',  newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for strat in rows:
            writer.writerow(strat)
    return

# 1. del: tier list

# save_frontpage(html_tier_list, mapa_podatkov, file_tier_list)


def tier_list_reader(string):
    vzorec = r'<div class="label svelte-1w4psuu">(?P<ime_strategije>.+?)</div>.+?<div class="power-label svelte-1winidr">Power: <b>(?P<moč>\d\d?\.\d)</b></div>'
    sez = re.findall(vzorec, string, flags=re.DOTALL)
    nov_sez = []
    for par in sez:
        rang = "ni uvrščen"
        if float(par[1]) >= 12:
            rang = "1."
        elif float(par[1]) >= 7:
            rang = "2."
        elif float(par[1]) >= 3:
            rang = "3."
        nov_sez.append({"ime strategije": par[0].strip(),"moč": par[1].strip(),"stopnja": rang.strip()})
    return nov_sez

# prilično je zaporedje pojavetve v html datoteki že razvrščeno po moči

# tier_list = tier_list_reader(read_file_to_string(mapa_podatkov, file_tier_list))
# write_csv(["ime strategije","moč","stopnja"], tier_list, mapa_podatkov, "tier_list.csv  ")

# 2. del: top decks (2 tedna nazaj)

# save_frontpage(html_top_decks, mapa_podatkov, file_top_decks)

def top_decks_reader(string):
    '''spodnji preprosti vzorec ima nekaj nezaželjenih zadetkov na začetku, 
    zato niz skrašamo v new_string'''
    new_string = string.split(r'mn mt-1 is-full-tablet safar')[1]
    vzorec = r'label svelte-1w4psuu padding">(?P<ime_strategije>.+?)</div>.+?bottom-sub-label svelte-1w4psuu">(?P<število_zbirov>\d+)</div></div>'
    sez = re.findall(vzorec, new_string, flags=re.DOTALL)
    nov_sez = []
    for par in sez:
        nov_sez.append({"ime strategije": par[0],"število zbirov": par[1]})
    return nov_sez

    
# top_decks = top_decks_reader(read_file_to_string(mapa_podatkov, file_top_decks))
# write_csv(["ime strategije","število zbirov"], top_decks, mapa_podatkov, "top_decks.csv  ")

# že razvrščeno po številu objavljenih seznamov za strategijo

# 3. del: ekstahiranje zbirov kart
'''vsi zbiri (~350) so (na videz neurejeno) zbrani na koncu top_decks.html. Ideja je vse zbire shraniti v datoteke 
in nato imena teh datotek +kakšne ekstra podatke v csv'''

def get_decks_string(vse):
    '''0 - deck id, 1 - avtor, 2 - zbirka(main, extrs, side), 3 - strategija 4 - ranked type
    vse = read_file_to_string(mapa_podatkov, file_top_decks)'''
    krajse = re.findall(r'ted\[\$gte\]=\(days-14.+?</script>', vse)
    vzorec = r'\\"_id\\":\\"(\w+?)\\",\\"author.+?username\\":\\"(.+?)\\".+?("main\\".+?"extra\\".+?"side\\".+?\]),\\"url.+?deckType\\":\{\\"name\\":\\"(.+?)\\".+?rankedType\\":\{\\"name\\":\\(.+?)\\'
    sez = re.findall(vzorec, krajse[0])

    return sez

def tuple_popravjalec(nterica,i=0):
    '''odstrani odvečne backslashe'''
    sez = list(nterica)
    popravil = nterica[i].replace("\\", "")
    sez[i] = popravil
    return tuple(sez)

def string_to_deck(string):
    '''pretvori sez[x][2] iz get_decks_string v uporabnejšo obliko'''
    vzorec_split = r'\\"extra\\":|\\"side\\":'
    deck_parts = re.split(vzorec_split, string)
    deck = {"main": [], "extra": [], "side": []}
    vzorec = r'\\"name\\":\\"(.+?)\\"\},\\"amount\\":(\d)'
    cards_main = re.findall(vzorec,  deck_parts[0])
    cards_extra = re.findall(vzorec,  deck_parts[1])
    cards_side = re.findall(vzorec,  deck_parts[2])

    for i in range(len(cards_main)):
        cards_main[i] = tuple_popravjalec(cards_main[i])
    for i in range(len(cards_extra)):
        cards_extra[i] = tuple_popravjalec(cards_extra[i])
    for i in range(len(cards_side)):
        cards_side[i] = tuple_popravjalec(cards_side[i])


    deck["main"] = cards_main
    deck["extra"] = cards_extra
    deck["side"] = cards_side
    return deck

def decks_to_files_and_cvs(sez,directory=mapa_zbirk):
    '''sez = get_decks_string(vse)
    1. naredi datoteke za posamezne zbire v podmapi zbiri
    2. naredi datoteko csv vseh zbirov
    3. naredi datoteko csv skupih pojavitev posameznih kart '''

    os.makedirs(directory, exist_ok=True)
    nov_sez = []
    vse_karte = {}
    for deck in sez:
        deck_dict = {}
        deck_id = deck[0]
        karte = string_to_deck(deck[2])
        file_name = deck_id + ".text"

        deck_dict["strategija"] = deck[3]
        deck_dict["avtor"] = deck[1]
        deck_dict["zbir"] = file_name
        deck_dict["id zbira"] = deck[0]
        nov_sez.append(deck_dict)

        path = os.path.join(directory, file_name)
        with open(path, 'w', encoding='utf-8') as text_file:
            print("#main", file=text_file)
            for karta in karte["main"]:
                print(f"{karta[0]} x{karta[1]}", file=text_file)
            print("", file=text_file)
            print("#extra", file=text_file)
            for karta in karte["extra"]:
                print(f"{karta[0]} x{karta[1]}", file=text_file)
            print("", file=text_file)
            print("!side", file=text_file)
            for karta in karte["side"]:
                print(f"{karta[0]} x{karta[1]}", file=text_file)

        for deck_part, cards in karte.items():
            for card in cards:
                if not card[0] in vse_karte:
                    vse_karte[card[0]] = [0,0,deck_part]
                if vse_karte[card[0]][2] == "side":
                    vse_karte[card[0]][2] = deck_part
                vse_karte[card[0]][0] += int(card[1])
                vse_karte[card[0]][1] += 1

    path = os.path.join(mapa_podatkov, "decks.csv")
    with open(path, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, ["strategija","avtor","zbir", "id zbira"])
        writer.writeheader()
        for strat in nov_sez:
            writer.writerow(strat)

    stolpci = ["karta", "število pojavitev", "število zbirov", "lokacija"]
    sez_vseh_kart = []
    for karta, info in vse_karte.items():
        dict = {stolpci[0]: karta, stolpci[1]: info[0], stolpci[2]: info[1],  stolpci[3]: info[2]}
        sez_vseh_kart.append(dict)

    path2 = os.path.join(mapa_podatkov, "total_cards.csv")
    with open(path2, 'w', encoding='utf-8', newline='') as csv_file2:
        writer2 = csv.DictWriter(csv_file2, stolpci,)
        writer2.writeheader()
        for strat in sez_vseh_kart:
            writer2.writerow(strat)
            
    return

# Main

def main(redownload=True, reparse=True):
    """Iz meni neznanih razlogov, se včasih z url naslova ne naloži html iste oblike.
    Če poskusi še enkrat deluje. Izgleda, da do tega pride ko prvič poskušaš naložiti html.
    V tem primeru top_decks_reader() poskuša iterirati prazen seznam, zato IndexError"""
    try:
        if redownload:
            save_frontpage(html_tier_list, mapa_podatkov, file_tier_list)
            save_frontpage(html_top_decks, mapa_podatkov, file_top_decks)
        if reparse:
            tier_list = tier_list_reader(read_file_to_string(mapa_podatkov, file_tier_list))
            write_csv(["ime strategije","moč","stopnja"], tier_list, mapa_podatkov, "tier_list.csv  ")

            top_decks = top_decks_reader(read_file_to_string(mapa_podatkov, file_top_decks))
            write_csv(["ime strategije","število zbirov"], top_decks, mapa_podatkov, "top_decks.csv  ")

            sez = get_decks_string(read_file_to_string(mapa_podatkov, file_top_decks))
            decks_to_files_and_cvs(sez)
    except IndexError:
        print("Wrong html, retrying")
        main()
    return
    
    
if __name__ == '__main__':
    main()


