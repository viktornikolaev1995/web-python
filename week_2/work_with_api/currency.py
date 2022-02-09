from bs4 import BeautifulSoup
from decimal import Decimal



def convert(amount, cur_from, cur_to, date, requests):
    payloads = {'date_req': date}
    response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp', params=payloads)  # Использовать переданный requests
    xml = response.text
    bs_content = BeautifulSoup(xml, "lxml")
    currencies = {}
    for i in bs_content.body.find_all('valute'):
        nominal = float(i.nominal.text.replace(',', '.'))
        value = float(i.value.string.replace(',', '.'))
        currencies[i.charcode.text] = {'nominal': nominal, 'value': value}
    # print(currencies)

    if cur_from == 'RUR':
        nominal = Decimal(currencies[cur_to]['nominal'])
        value = Decimal(currencies[cur_to]['value'])
        result = Decimal(amount/(value/nominal))
        return result.quantize(Decimal("1.0000"))
    elif cur_to == 'RUR':
        nominal = Decimal(currencies[cur_from]['nominal'])
        value = Decimal(currencies[cur_from]['value'])
        result = Decimal(amount/(value/nominal))
        return result.quantize(Decimal("1.0000"))
    else:
        nominal_cur_from = Decimal(currencies[cur_from]['nominal'])
        value_cur_from = Decimal(currencies[cur_from]['value'])
        relative_unit_cur_from = value_cur_from / nominal_cur_from
        nominal_cur_to = Decimal(currencies[cur_to]['nominal'])
        value_cur_to = Decimal(currencies[cur_to]['value'])
        relative_unit_cur_to = value_cur_to / nominal_cur_to
        result = amount * relative_unit_cur_from / relative_unit_cur_to
        return result.quantize(Decimal("1.0000"))

