from urllib.request import urlopen
import json


class Matury:

    def __init__(self):

        url = 'https://api.dane.gov.pl/resources/17363/data'
        resp = urlopen(url)
        data = json.loads(resp.read())
        last_page = int(data['links']['last'].split('=')[1])
        # last_page = 20

        data = []
        years = set()
        regiony = set()
        for page in range(1, last_page+1):
            resp = urlopen('https://api.dane.gov.pl/resources/17363/data?page=' + str(page))
            for num, attr in enumerate(json.loads(resp.read())['data']):
                data.append(attr['attributes'])
                regiony.add(attr['attributes']['col1'])
                years.add(int(attr['attributes']['col4']))

        self.regiony = {regiony.lower() for regiony in regiony}
        self.years = years
        self.data = data
        self.rok = None
        self.terytorium = None
        self.plec = None

    def sprawdz_poprawnosc(self, rok=None, terytorium=None, plec=None):

        try:
            if rok is None:
                rok = max(self.years)
            elif rok not in self.years:
                print("Podano niepoprawny rok: '{}'. \nSprawdzam dla domyślny: {}\n".format(rok, max(self.years)))
                rok = max(self.years)
        except TypeError:
            print("Podano niepoprawny format daty. Oczekiwany <class 'int'>, podano {}".format(type(rok)))

        try:
            if terytorium is None:
                terytorium = self.regiony
            else:
                if type(terytorium) == str:
                    terytorium = [terytorium.lower()]
                terytorium = [terytorium.lower() for terytorium in terytorium]
                bledne_wojewodztwa = set(terytorium) - set(self.regiony)
                terytorium = set(terytorium) - bledne_wojewodztwa
                if len(bledne_wojewodztwa) > 0:
                    print('Podano błędne województwa:')
                    print(', '.join(bledne_wojewodztwa))
                    if len(terytorium) == 0:
                        print('Wszystkie województwa podano błędnie \nWybieram domyślne -> Wszystkie\n')
                        terytorium = self.regiony
                    else:
                        print('Sprawdzam dla: ')
                        print(', '.join(terytorium))
                        print('')
        except TypeError:
            print("Podano niepoprawny format terytorium. Oczekiwany <class 'str'> lub <class 'list'>, podano {}"
                  .format(type(rok)))

        if plec is None:
            plec = ['kobiety', 'mężczyźni']
        elif plec == 'k':
            plec = ['kobiety']
        elif plec == 'm':
            plec = ['mężczyźni']
        else:
            print('Błędna nazwa atrybutu płci ("{}")\n"m" -> mężczyźni \n"k" -> kobiety'.format(plec))
            print('Sprawdzam dla wartości domyślnej -> bez rozróżnienia\n')
            plec = ['kobiety', 'mężczyźni']

        self.rok = rok
        self.terytorium = terytorium
        self.plec = plec

    # Zad 1
    def srednia_liczba_osob(self, terytorium, rok, plec=None):
        """
        Zwraca średnią liczbę osób które przystąpiły do matury w danym roku i województwie

        :param terytorium: str or list
        :param rok: int
        :param plec: str;   'k'->kobiety,
                            'm'->mężczyźni,
                            domyślnie->bez rozróżnienia
        :return: int
        """
        self.sprawdz_poprawnosc(terytorium=terytorium, rok=rok, plec=plec)
        if 'polska' in self.terytorium and len(self.terytorium) > 1:
            self.terytorium.remove('polska')
            print('Średnia dla województw + całej Polski byłaby niemiarodajna')
        suma_region = 0
        mianownik_region = 0
        for row in self.data:
            if row['col1'].lower() in self.terytorium \
                    and row['col4'] <= self.rok \
                    and row['col3'] in self.plec \
                    and row['col2'] == 'przystąpiło':
                suma_region += row['col5']
                mianownik_region += 1
        out = round(suma_region/mianownik_region)
        print(', '.join(self.terytorium))
        print(self.rok, '-', out)
        return out

    # Zad 2
    def zdawalnosc(self, terytorium, rok=None, plec=None):
        """
        Zwraca procentową zdawalnośc dla danego województwa na przestrzeni lat

        :param terytorium: str or list
        :param rok: int
        :param plec: str;   'k'->kobiety,
                            'm'->mężczyźni,
                            domyślnie->bez rozróżnienia
        :return: dict
        """
        self.sprawdz_poprawnosc(terytorium=terytorium, rok=rok, plec=plec)
        out = {}
        for region in self.terytorium:
            temp = {}
            for rok in range(min(self.years), self.rok+1):
                zdalo = 0
                przystapilo = 0
                for row in self.data:
                    if row['col4'] == rok \
                            and row['col1'].lower() == region \
                            and row['col3'] in self.plec:
                        if row['col2'] == 'zdało':
                            zdalo += row['col5']
                        elif row['col2'] == 'przystąpiło':
                            przystapilo += row['col5']
                wynik = zdalo / przystapilo
                temp[rok] = round(wynik, 2)
            out[region] = temp
        return out

    # Zad 3
    def najlepsze_woj(self, rok, terytorium=None, plec=None):
        """
        Zwraca województwo o najlepszej zdawalności w konkretnym roku

        :param rok: int
        :param terytorium: str or list
        :param plec: str;   'k'->kobiety,
                            'm'->mężczyźni,
                            domyślnie->bez rozróżnienia
        :return: str
        """
        self.sprawdz_poprawnosc(rok=rok, terytorium=terytorium, plec=plec)

        if len(self.terytorium) < 2:
            print('Wybrano tylko jedno województwo')

        temp_wynik = 0
        temp_reg = ''
        for region in self.terytorium:
            zdalo = 0
            przystapilo = 0
            for row in self.data:
                if row['col4'] == rok \
                        and row['col1'].lower() == region \
                        and row['col3'] in self.plec:
                    if row['col2'] == 'zdało':
                        zdalo += row['col5']
                    elif row['col2'] == 'przystąpiło':
                        przystapilo += row['col5']
            wynik = zdalo / przystapilo
            if wynik > temp_wynik:
                temp_reg = region
                temp_wynik = wynik

        print(rok, temp_reg, round(temp_wynik, 3), '%')
        return temp_reg

    # Zad 4
    def spadek_formy(self, terytorium=None, plec=None):
        """
        Zwraca województwa, w których zdawalność w kolejnym roku spadła

        :param terytorium: str or list;
        :param plec: str;   'k'->kobiety,
                            'm'->mężczyźni,
                             domyślnie->bez rozróżnienia
        :return: dict
        """
        self.sprawdz_poprawnosc(rok=max(self.years), terytorium=terytorium, plec=plec)
        out = {}
        for region in self.terytorium:
            temp_wynik = 0
            temp_rok = 0
            lata = []
            for _, rok in enumerate(range(min(self.years), self.rok+1)):
                zdalo = 0
                przystapilo = 0
                for row in self.data:
                    if row['col1'].lower() == region \
                            and row['col3'] in self.plec \
                            and row['col4'] == rok:
                        if row['col2'] == 'zdało':
                            zdalo += row['col5']
                        elif row['col2'] == 'przystąpiło':
                            przystapilo += row['col5']
                wynik = zdalo/przystapilo
                if wynik < temp_wynik:
                    if _ > 0:
                        print(region + ':', temp_rok, '->', rok, '|', round(temp_wynik, 3), '->', round(wynik, 3))
                        lata.append([temp_rok, rok])
                temp_wynik = wynik
                temp_rok = rok
            out[region] = lata
        return out

    # Zad 5
    def i_kto_tu_jest_the_besciak(self, woj_a, woj_b, plec=None):
        """
        Zwraca województwo o lepszym wyniku w każdym dostępnym roku

        :param woj_a: str; Nazwa województwa do porównania. Uwzględnij polskie znaki
        :param woj_b: str; Nazwa województwa do porównania. Uwzględnij polskie znaki
        :param plec: str;   'k'->kobiety,
                            'm'->mężczyźni,
                            domyślnie->bez rozróżnienia
        :return: dict
        """
        self.sprawdz_poprawnosc(rok=max(self.years), terytorium=[woj_a, woj_b], plec=plec)
        out = {}
        for rok in range(min(self.years), self.rok+1):
            temp_wynik = 0
            temp_rok = 0
            temp_region = 0
            for region in self.terytorium:
                zdalo = 0
                przystapilo = 0
                for row in self.data:
                    if row['col4'] == rok \
                            and row['col1'].lower() == region \
                            and row['col3'] in self.plec:
                        if row['col2'] == 'zdało':
                            zdalo += row['col5']
                        elif row['col2'] == 'przystąpiło':
                            przystapilo += row['col5']
                wynik = zdalo / przystapilo
                if wynik > temp_wynik:
                    temp_wynik = wynik
                    temp_region = region
                    temp_rok = rok
            out[rok] = temp_region
            # print(temp_rok, '-', temp_region, round(temp_wynik, 2), '%')
        return out
