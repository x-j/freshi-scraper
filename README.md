# freshi-scraper

scraper do swiezego info, wersja dwa

## jak tego uzyc

0. sklonuj se to repo

1. zainstaluj potrzebne pythonowe moduły:

    ```
    pip install -r requirements.txt
    ```

2. odwiedź folder [`curses`](/freshis/curses/README.md) i skonfiguruj swoje klątwy w plikach .csv które tam znajdziesz

3. wejdz na olx i ustaw parametry wyszukiwania. kliknij "Szukaj" i skopiuj link, na którym wylądujesz. Powinien wyglądać na przyklad tak:

    ```https://www.olx.pl/nieruchomosci/mieszkania/wynajem/poznan/?search%5Bfilter_float_price:to%5D=3000&search%5Bfilter_enum_rooms%5D%5B0%5D=two```

    ![setup](/doc/setup.png)

### odpal *fiolxs*

> potem zajrzyj do folderu `out` sprawdzić rezultaty w pliku `fresh-info.csv`

jednorazowe przefiltrowanie pierwszej strony wynikow z olxa:

```
    scrapy crawl fiolxs -a search_url="TWOJ LINK Z OLX"
```

zwróć uwagę na to że link musi (?) znajdować się między cudzysłowami. i zwróć też uwagę na spacje, niech będą tak jak w przykladzie powyzej. 
    sugeruję jeszcze dać flagę `-L INFO` żeby nie zaspamować sobie terminala za bardzo

> żeby zatrzymac odpalonego w terminalu crawlera wyślij SIGINT (Ctrl+C) dwa razy 

#### a zeby sie uruchamiało samo co jakis czas?

skorzystaj ze schedulera:

```
    python fiolxscheduler.py "TWOJ LINK Z OLX"
```

domyślnie odpali się raz na 60 minut. możesz to zmienić podając liczbe z argumentem `--every`, na przyklad, żeby fiolxs odpalal sie co 30 minut:

```
    python fiolxscheduler.py --every 30 "TWOJ LINK Z OLX"
```

do schedulera możesz przekazac te same argumenty co w przypadku jednorazowego fiolxa **ALE** muszą one być podane wewnątrz cudzysłowu, po linku. Na przykład, żeby ustawić logging na poziomie INFO:

```
python fiolxscheduler.py "TWOJ LINK Z OLX -L INFO"
```

####  a moge output do innego folderu?

tak, mozesz, ale tak czy siak bedziesz miec oprocz tego output do pliku `fresh-info.csv` w folderze `out`

na przyklad zeby dac output do pewnego pliku CSV na twoim dysku C:

```
python fiolxscheduler.py "TWOJ LINK Z OLX -o C:\Users\Marwo\informacje-z-olx.csv"
```


**uwaga**: kiedy ustawisz output do nowego pliku csv tak jak powyżej, twoj poprzedni plik `fresh-info.csv` zmieni swoją nazwe, o ile istniał. to ma sens. poprzednio znalezione linki nie będa oflitrowywane, tzn mogą pojawić się też w tym nowym pliku.

> mozesz też robic output do plikow json, jl i xml! 

> coming *soon*: output do htmla

---

LICENSE:: jeb sie
