import re
import requests
import itertools

wzor_artykulu = r'<li[^>]*>.*<a[^>]*href=\"(/wiki/(?![^"]*:)[^"]+)\"[^>]*title=\"([^"]+)\"[^>]*>.*</li>'
wzor_linku_wewnetrznego = r'<a[^>]*href=\"(/wiki/(?![^"]*:)[^"]+)\"[^>]*title=\"([^"]+)\"[^>]*>'
wzor_obrazka = r'<img[^>]*src=\"(//upload\.wikimedia\.org/[^"]+)\"[^>]*/>'
wzor_linku_zewnetrznego = r'<a[^>]*class=\"external[^"]*\"[^>]*href=\"([^"]+)\"[^>]*>'
wzor_kategorii = r'<a[^>]*href=\"(/wiki/Kategoria:[^"]+)\"[^>]*title=\"([^"]+)\"[^>]*>'

nazwa_kategorii = input("nazwa kategorii: ").strip()
adres_kategorii = f'https://pl.wikipedia.org/wiki/Kategoria:{nazwa_kategorii.replace(" ", "_")}'
odpowiedz_kategorii = requests.get(adres_kategorii)
zawartosc_strony_kategorii = odpowiedz_kategorii.text

artykuly = [dopasowanie.groups() for dopasowanie in itertools.islice(re.finditer(wzor_artykulu, zawartosc_strony_kategorii), 3)]

for sciezka, tytul in artykuly:
    adres_artykulu = "https://pl.wikipedia.org" + sciezka
    zawartosc_artykulu = requests.get(adres_artykulu).text
    zawartosc_glowna = zawartosc_artykulu[zawartosc_artykulu.find('<div id="mw-content-text"'):zawartosc_artykulu.find('<div id="catlinks"')]
    sekcja_przypisow = zawartosc_artykulu[zawartosc_artykulu.find('id="Przypisy"'):]
    sekcja_przypisow = sekcja_przypisow[:sekcja_przypisow.find('<div class="mw-heading')]
    sekcja_kategorii = zawartosc_artykulu[zawartosc_artykulu.find('<div id="catlinks"'):]

    linki_wewnetrzne = [dopasowanie.groups()[1] for dopasowanie in itertools.islice(re.finditer(wzor_linku_wewnetrznego, zawartosc_glowna), 5)]
    print(" | ".join(linki_wewnetrzne))

    obrazy = [dopasowanie.groups()[0] for dopasowanie in itertools.islice(re.finditer(wzor_obrazka, zawartosc_glowna), 3)]
    print(" | ".join(obrazy))

    linki_zewnetrzne = [dopasowanie.groups()[0] for dopasowanie in itertools.islice(re.finditer(wzor_linku_zewnetrznego, sekcja_przypisow), 3)]
    print(" | ".join(linki_zewnetrzne))

    kategorie = [dopasowanie.groups()[1].replace('Kategoria:', '') for dopasowanie in itertools.islice(re.finditer(wzor_kategorii, sekcja_kategorii), 3)]
    print(" | ".join(kategorie))
