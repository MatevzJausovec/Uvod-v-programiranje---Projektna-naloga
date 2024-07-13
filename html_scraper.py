import csv
import os
import requests
import re

html_tier_list = "https://www.masterduelmeta.com/tier-list"
file_tier_list = "tier_list.html"
html_top_decks = "https://www.masterduelmeta.com/top-decks"
file_top_decks = "top_decks.html"
mapa_podatkov = "podatki"

# url --> html file splošno

def download_url_to_string(url):
    try:
        page_content = requests.get(url)
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
    
# shrani seznam --> csv

def write_csv(fieldnames, rows, directory, filename):
    """
    Funkcija v csv datoteko podano s parametroma "directory"/"filename" zapiše
    vrednosti v parametru "rows" pripadajoče ključem podanim v "fieldnames"
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for strat in rows:
            writer.writerow(strat)
    return

# 1. del: tier list

# save_frontpage(html_tier_list, mapa_podatkov, file_tier_list)


def tier_list_reader(string):
    vzorec = r'<div class="label svelte-1w4psuu">(?P<ime strategije>.+?)</div>.+?<div class="power-label svelte-1winidr">Power: <b>(?P<moč>\d\d?\.\d)</b></div>'
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
        nov_sez.append({"ime strategije": par[0],"moč": float(par[1]),"stopnja": rang})
    return nov_sez

# prilični je zaporedje pojavetve v html datoteki že razvrščeno po moči

# tier_list = tier_list_reader(read_file_to_string(mapa_podatkov, file_tier_list))
# write_csv(["ime strategije","moč","stopnja"], tier_list, mapa_podatkov, "tier_list.csv  ")

# 2. del: top decks (2 tedna nazaj)

# save_frontpage(html_top_decks, mapa_podatkov, file_top_decks)

def top_decks_reader(string):
    new_string = string.split(r'mn mt-1 is-full-tablet safar')[1]
    vzorec = r'label svelte-1w4psuu padding">(?P<ime_strategije>.+?)</div>.+?bottom-sub-label svelte-1w4psuu">(?P<število_zbirov>\d+)</div></div>'
    sez = [pojavitev.groupdict() for pojavitev in re.finditer(vzorec, new_string, flags=re.DOTALL)]
    return sez
    
# top_decks = top_decks_reader(read_file_to_string(mapa_podatkov, file_top_decks))


# že razvrščeno po številu objavljenih seznamov za strategijo
