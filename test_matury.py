import pytest
from matury import Matury


@pytest.fixture(scope='module')
def matury():
    m = Matury()
    return m


def test_srednia_liczba_osob(matury):
    assert matury.srednia_liczba_osob('podkarpackie', 2018, 'k') == 10825
    assert matury.srednia_liczba_osob('podkarpackie', 2018, 'm') == 8626
    assert matury.srednia_liczba_osob(['podkarpackie', 'polska'], 2011) == 11594


def test_zdawalnosc(matury):
    result = {'lubuskie': {2010: 0.82, 2011: 0.77}, 'polska': {2010: 0.81, 2011: 0.75}}
    assert matury.zdawalnosc(['polska', 'Lubuskie'], 2011) == result


def test_najlepsze_woj(matury):
    assert matury.najlepsze_woj(2010) == 'kujawsko-pomorskie'
    assert matury.najlepsze_woj(2011) == 'małopolskie'
    assert matury.najlepsze_woj(2011, ['lubuskie', 'mazowieckie']) == 'lubuskie'
    assert matury.najlepsze_woj(2011, ['lubuskie', 'mazowieckie'], 'k') == 'mazowieckie'


def test_spadek_formy(matury):
    assert matury.spadek_formy('polska') == {'polska': [[2010, 2011], [2013, 2014], [2016, 2017]]}
    assert matury.spadek_formy('polska', 'm') == {'polska': [[2010, 2011], [2013, 2014], [2016, 2017]]}

def test_i_kto_tu_jest_the_besciak(matury):
    result = {2010: 'kujawsko-pomorskie',
              2011: 'podkarpackie',
              2012: 'kujawsko-pomorskie',
              2013: 'podkarpackie',
              2014: 'podkarpackie',
              2015: 'podkarpackie',
              2016: 'podkarpackie',
              2017: 'kujawsko-pomorskie',
              2018: 'podkarpackie'}
    assert matury.i_kto_tu_jest_the_besciak('kujawsko-pomorskie', 'podkarpackie', 'k') == result


if __name__ == '__main__':
    pytest.main()
