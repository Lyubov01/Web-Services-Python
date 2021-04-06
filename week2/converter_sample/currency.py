from bs4 import BeautifulSoup
from decimal import Decimal

"""В этом задании придется написать свой конвертер валют (см. приложенный файл). Курсы валют нужно брать из API 
Центробанка """


def convert(amount, cur_from, cur_to, date, requests):
    """В функцию будет передана сумма amount в валюте с кодом
    cur_from, и её требуется перевести в валюту cur_to через рубль (код: RUR). Для запроса к API нужно использовать
    переданный requests, точнее, его метод get(). """
    response = requests.get(
        f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}")  # Использовать переданный requests
    soup = BeautifulSoup(response.content, 'xml')
    if cur_from == "RUR":
        val_from = Decimal(1.0)
    else:
        from_ = soup.find("CharCode", text=cur_from).find_next_sibling('Value').string
        nom_from = soup.find("CharCode", text=cur_from).find_next_sibling('Nominal').string
        val_from = Decimal(from_.replace(',', '.')) / Decimal(nom_from)
    to_ = soup.find("CharCode", text=cur_to).find_next_sibling('Value').string
    nom_to = soup.find("CharCode", text=cur_to).find_next_sibling('Nominal').string
    val_to = Decimal(to_.replace(',', '.')) / Decimal(nom_to)
    result = amount*Decimal(val_from)/Decimal(val_to)
    return result.quantize(Decimal('0.0001'))
    # не забыть про округление до 4х знаков после запятой
