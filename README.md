# Matury 
#### Analiza danych od roku 2010

## Spis treści
* [Wprowadzenie](#wprowadzenie)
* [Technologie](#technologie)
* [Uruchomienie](#uruchomienie)

## Wprowadzenie
Aplikacja służąca do analizy danych o uczestnikach matur od roku 2010 i powstala w ramach procesu rekrutacji.

## Technologie
Projekt stwożony jest z pomocą:
* Python version 3.7.3
Biblioteki:
* Urllib
* Json
* Pytest

Wymagania techniczne rekrutacji wymagały wykorzystania modułów ze standardowej biblioteki Pythona.
- Osobiścię do wykonania zadanie użyłbym biblioteki Requests zamias Urllib, gdyż ma wbudowaną funkcję odczytu danych 
w formie json, co by oszczędziło kilka linijek kodu i uprościło sprawę.
- Użyłbym również biblioteki Pandas do obróbki danych. Wczytał bym wszystkie dane do tabeli po czym, korzystając
z wbudowanych funkcji wyszukiwałbym określonych wierszy. Ponadto, wyniki poszczególnych operacji zwracałbym w formie 
tabeli dla lepszej przejrzystości

## Uruchomienie

W konsoli Pythona importujemy klasę Maruty z modułu matury.py:

Przykład:

>>>from matury import Matury

Następnie tworzyy instancję klasy:

>>>matury = Matury()

Aplikacja potrzebuje chwili aby zebrać dane.
Klasa posiada 5 głównych fukncji:

*srednia_liczba_osob - Funkcja do zadania nr. 1, która zwraca średnią liczbę osób które przystąpiły do 
                        matury w danym roku i województwie.
    Funkcja przyjmuje 3 parametry:
        - terytorium - (wymagany) Naley podać województwo bądź liste województw dla których chcemy 
                        wyliczyć śre∂nią uczestników. Należy zwrócić uwagę na użycie polskich znaków.   
        - rok - (wymagany) Rok do którego chcemy wyliczyć średnią od roku 2010
        - płeć - (domyślny) -> bez rozróżnienia,
                'k' - kobiety
                'm' - mężczyźni
Przykład:
>>>matury.srednia_liczba_osob('podkarpackie', 2011)
Wynik:
>>>11594
        
*zdawalnosc - Funkcja do zadania nr. 2, która zwraca procentową zdawalnośc dla danego województwa 
                na przestrzeni lat. 
    Funkcja przyjmuje 3 parametry:
        - terytorium - (wymagany) Naley podać województwo bądź liste województw dla których chcemy 
                        wyliczyć procentową zdawalność danego województwa. Należy zwrócić uwagę 
                        na użycie polskich znaków.   
        - rok - (doyślny) -> maksymalny dostępny. Rok do którego chcemy wyliczyć zdawalność od roku 2010
        - płeć - (domyślny) -> bez rozróżnienia,
                'k' - kobiety
                'm' - mężczyźni
Przykład:
>>>matury.zdawalnosc(['polska', 'podkarpackie'], 2011)
Wynik:
>>>{'podkarpackie': {2010: 0.81, 
                     2011: 0.75}, 
    'polska': {2010: 0.81, 
               2011: 0.75}}
                    
*najlepsze_woj - Funkcja do zadania nr. 3, która Zwraca województwo o najlepszej zdawalności w konkretnym roku
    Funkcja przyjmuje 3 parametry:
        - rok - (wymagany) Należy podać rok, w których chcemy sprawdzić, które z województw miało najlepszą zdawalność
        - terytorium - (domyślny) -> wszystkie. Można podać minimum dwa województwa, które chcemy ze soba porównać dla 
                        danego roku. Należy zwrócić uwagę na użycie polskich znaków.  
        - płeć - (domyślny) -> bez rozróżnienia,
                'k' - kobiety
                'm' - mężczyźni
Przykład:
>>>matury.najlepsze_woj(2011, ['lubuskie', 'mazowieckie'], 'k')
Wynik:
>>>'mazowieckie'
        
*spadek_formy - Funkcja do zadania nr. 4, która zwraca województwa, w których zdawalność w kolejnym roku spadła
    Funkcja przyjmuje 2 parametry:
        - terytorium - (domyślny) Można podać województwo lub listę województw, które chcemy sprawdzić, czy zdawalność
                        w kolejnym roku spadła. Należy zwrócić uwagę na użycie polskich znaków.  
        - płeć - (domyślny) -> bez rozróżnienia,
                'k' - kobiety
                'm' - mężczyźni
 Przykład:
 >>>matury.spadek_formy('polska', 'm')
 Wynik:
 >>>{'polska': [[2010, 2011], 
                [2013, 2014], 
                [2016, 2017]]}
         
*i_kto_tu_jest_the_besciak ;) - Funkcja do zadania nr. 5, która zwraca województwo o lepszym wyniku zdawalności dla 
                                każdego dostępnego roku.
    Funkcja przyjmuje 3 parametry:
        - woj_a - województwo A, do porównanie z województwem B
        - woj_b - województwo B, do porównanie z województwem A
        - płeć - (domyślny) -> bez rozróżnienia,
                'k' - kobiety
                'm' - mężczyźni
Przykład:
>>>matury.i_kto_tu_jest_the_besciak('Świętokrzyskie', 'warmińsko-mazurskie', plec=None)
Wynik:
>>>{2010: 'warmińsko-mazurskie',
    2011: 'świętokrzyskie',
    2012: 'warmińsko-mazurskie',
    2013: 'warmińsko-mazurskie',
    2014: 'świętokrzyskie',
    2015: 'świętokrzyskie',
    2016: 'świętokrzyskie',
    2017: 'świętokrzyskie',
    2018: 'świętokrzyskie'}
        

