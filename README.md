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

4. odpal *fiolxs*:

    ```
    scrapy crawl fiolxs -a search_url="TWOJ LINK Z OLX"
    ```
    zwróć uwagę na to że link musi (?) znajdować się między cudzysłowami. i zwróć też uwagę na spacje, niech będą tak jak w przykladzie powyzej. 
    sugeruję jeszcze dać flagę `-L INFO` żeby nie zaspamować sobie terminala za bardzo

5. zajrzyj do folderu `out` sprawdzić rezultaty

---

LICENSE:: jeb sie
