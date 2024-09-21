WYKAZ WAŻNIEJSZYCH OZNACZEŃ I SKRÓTÓW

WSTĘP I CEL PRACY

WSTĘP TEORETYCZNY
    zastosowania światła w medycynie
        fototerapia
    <!-- 
    Metody symulacji światła
        Metody analityczne
        Metody statystyczne
        Kryteria wyboru
    -->
    metoda monte carlo
        próbkowanie monte carlo
        długość kroku fotonu
        <!-- (funkcja gęstości prawdopodobieństwa, dystrybuanta, funkcja próbkująca cechy) -->
        funkcje rozpraszania
            - kąt azymutalny
            - kąt zenitalny
        normalizacja wyników
        alternatywne funkcje losujące
    przykładowe implementacje symulacji światła
    algorytm maszerujących sześcianów
    właściwości optyczne skóry

METODOLOGIA

    własna implementacja symulacji
        - statystyki kodu
        diagram aplikacji
        spis wszystkich klas
        opis działania
            (od paragrafów)
            - zarządzanie generatorami liczb pseudolosowych
            <!-- interfejs generatorów
            interfejs funkcji losujących -->
            - przebieg symulacji
            - zapis do plików
            - normalizacja wyników
        wizualizacja wyników

            <!-- wykorzystanie biblioteki matplotlib
                proste wyświetlanie trójwymiarowej tablicy
                próbkowanie trójwymiarowej tablicy
                mapy ciepła
            wykorzystanie biblioteki vispy
                proste wyświetlanie trójwymiarowej tablicy
                wizualizacja objętości biblioteki vispy
                wizualizacja obiektów z wykorzystaniem biblioteki pandas
            zarządzanie wizualizacją wyników
                wyświetlanie statystyk
                przygotowanie schematów rysowania strzałek dla tablic
                przygotowanie stosu brył geometrycznych materiałów
                podgląd środowiska symulacji
                podgląd absorpcji na tle ośrodka propagacji
                wyświetlanie tablicy absorpcji
                wyświetlanie rejestru pozycji fotonów
                wyświetlanie tablicy absorpcji zsumowanej wzdłóż wybranej osi
                projekcje rejestru fotonów na płaszczyznę 2d -->

            - narzędzia pomocnicze
            - strzałki zmiany pozycji fotonów
            - triangularyzowane powierzchnie tkanek
            - obrazy png zapis
            - uniwersalne schematy kolorowania

            <!-- metody kolorowania
                progowanie "threshold"
                pętla kolorów "loop"
                    tworzenie palety kolorów
                jednolity kolor "solid"
                według id wiązki "photonwise"
                losowo "random"
                tęcza "rainbow"
                normalizacja min-max "min-max"
                wyśrodkowanie mediany "median"
                transformacja danych do rozkładu normalnego "trans-normal"
                skala logarytmiczna "logarithmic"
                mapa ciepła normalizacji min-max "heatmap min-max"
                mapa ciepła po wyśrodkowaniu mediany "heatmap median"
                mapa ciepła rozkładu normalnego "heatmap trans-normal"
                mapa ciepła skali logarytmicznej "heatmap logarithmic"
            narzędzia pomocnicze schematów kolorowania
                resetowanie kolorów
                stos schematów kolorowania
                szukanie przodków wiązki
                - kolorowanie według najstarszego przodka
                - dodawanie wiązek pokrewnych do wyświetlenia 
                szukanie potomków wiązki
                sumowanie wartości leżących na zbliżonych pozycjach
                rozproszenie wartości -->
            
        plik konfiguracyjny
            - porównanie ważniejszych ustawień
        domyślne nastawy

    próba kontrolna
    - przetłumaczone skrypty

    implementacja trójwymiarowych modeli skóry
        jednolity ośrodek propagacji
        implementacja bazująca na trójwymiarowej tablicy
        implementacja bazująca na opisie brył geometrycznych
        modele skóry
            - jednolity ośrodek
            - dwuwarstwowy model skóry
            - trzywarstwowy model skóry
            - model skóry z naczyniami krwionośnymi
        identyfikacja przekroczenia granicy ośrodków
            -zakładkowanie warstw
        zapis do pliku

    implementacja źródła światła
        - punktowe źródło światła
        - agregowanie punktowych źródeł światła
        - wiązka fotonów

    przeprowadzone eksperymenty
    - skrypty pomocnicze
    - jednolity ośrodek propagacji
        mati-sim my_params 10k-100mln
        mati-sim org_params 10k-10mln
        mati-sim my_params 10k g {0, 0.5, 0.9, 1}
        mc456 my_params 10k-100mln
        mc456 org_params 10k-100mln
        mc456 rozne g 100mln
        mc456 rozne_skóry_z_tabeli 100mln
        tiny my_params 10k-100mln
        tiny org_params 10k-100mln
        small my_params 10k-100mln
        small org_params 10k-100mln
    - model dwuwarstwowy 100-1mln
    - model trzywarstwowy 100-1mln
    - model z naczyniami krwionośnymi 100-100k
    - model z naczyniami krwionośnymi on vec 100

    metody porównawcze

analiza i dyskusja uzyskanych wyników
podsumowanie

wykaz literatury
