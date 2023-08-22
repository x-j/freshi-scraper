tutaj skonfigurujesz swoje klątwy

**freshis** domyślnie będzie czytać przeklęte miejsca z pliku `curses/miejsca.csv` i przeklęte regexy z pliku `curses/regexy.csv`

Możesz zmienić te ścieżki overridując ustawienia CURSED_MIEJSCA_PATH oraz CURSED_REGEXII_PATH

> wielkość liter i polskie znaki nie mają znaczenia. Tzn jeśli podasz "Żółta Gęś" to w ofertach będe szukać "zolta ges"
>

Jeśli w tytule oferty jest przeklęte miejsce to będzie dropnięta. Jeśli jakiś przeklęty regex zmatchuje z opisem, albo jest w nim przeklęte miejsce, to oferta będzie dropnięta.

 ---

- w pliku `miejsca.csv` wylistuj na przyklad dzielnice, ulice, okolice. Są dwie kolumny: podaj prosze wersje w mianowniku w pierwszej, a w drugiej miejscownik u razem z przysłówkiem. 

    Tzn np `puławska,na puławskiej`

- w pliku `regexy.csv` wylistuj kurwa swoje regexy. Jest tam juz kilka poprzednich propozycji do odfiltrowywania aneksow kuchennych, przechodnich pokojow itd
