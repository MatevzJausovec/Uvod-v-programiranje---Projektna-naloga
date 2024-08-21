import re
import requests
import json

# 1. del: omejimo se na zbire, ki vsebujejo najboljših n kart



def file_to_dict(text_file):
    """Pretvori .text datoteke z zbiri v slovar"""
    dict = {"#main": [], "#extra": [], "!side": []}
    with open(f"podatki\\zbiri\\{text_file}", encoding='utf-8') as zbir:
        current = "a"
        for line in zbir:
            line = line.strip()
            if line in ["#main", "#extra", "!side"]:
                current = line
                continue
            if line:
                if not current:
                    return "Error: no current location"
                karta = re.search("(.+?) x(\d)", line)
                dict[current].append((karta[1], int(karta[2])))
    return dict

def cards_in_list(text_file, seznam):
    """Preveri, če so vse karte na seznamu v danem zbiru"""
    zbir = file_to_dict(text_file)
    for karta in seznam:
        is_in = False
        for part in zbir:
            for name in zbir[part]:
                if karta == name[0]:
                    is_in = True
        if not is_in:
            return False
    return True

def check_df_for_cards(zbiri_pd, seznam):
    """Preveri, v katerih zbirih v tabeli so vse karte s seznama"""
    sez = []
    for file in zbiri_pd["zbir"]:
        if cards_in_list(file, seznam):
            sez.append(file.strip(".text"))
    return sez
        
def top_cards(sorted_df,n=7):
    """Vrne seznam 7 najbolj preiljubljenih kart; rabi že urejen seznam"""
    sez = []
    for i in range(n):
        sez.append(sorted_df["karta"][i])
    return sez

def allowed_decks(vsi_zbiri, karte_df,n=7):
    return check_df_for_cards(vsi_zbiri, seznam = top_cards(karte_df, n))

# 2. del: printer

def printer(df,n=0):
    try:
        text_file = df["zbir"].iloc[n]
        avtor = df["avtor"].iloc[n]
        strat =  df["strategija"].iloc[n]
    except IndexError:
        return "Na voljo ni toliko zbirov. Poskusi manjši indeks" 
    with open(f"podatki\\zbiri\\{text_file}", encoding='utf-8') as zbir:
        print(f"Strategija: {strat} Avtor: {avtor}\n")
        for line in zbir:
            print(line.strip()) 

# 3. del: downloader

text_file = "66b57c94d97a3ef024d23081.text"

def download_url_to_string(url):
    try:
        page_content = requests.get(url)
        page_content.encoding = 'UTF-8'
        return page_content.text
    except Exception:
        print("Napaka!")

def card_id(karta):
    data = json.loads(download_url_to_string(f"https://db.ygoprodeck.com/api/v7/cardinfo.php?name={karta}"))
    return data["data"][0]["id"]


def downloader(deck_dict, file_name="Moj_zbir.ydk"):
    """naredi .ydk iz zbira kot slovarja"""
    with open(file_name, "w", encoding='utf-8') as zbir:
        for part in deck_dict:
            print(part, file=zbir)
            for karta in deck_dict[part]:
                karta2 = karta[0].replace("&", "%26") # Znak "&" API uporablja kot poseben znak
                id_karte = card_id(karta2)
                for _ in range(karta[1]):
                    print(id_karte, file=zbir)

def make_ydk(text_file, file_name):
    return downloader(file_to_dict(text_file),file_name="Moj_zbir.ydk")