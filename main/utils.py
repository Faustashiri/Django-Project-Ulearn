from datetime import datetime
import requests
from bs4 import BeautifulSoup


# -------------------------
# Помощники для работы с текстом
# -------------------------

def extract_text_from_html(html_content):
    """
    Извлекает текст из HTML-контента, удаляя все теги.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()


# -------------------------
# Форматирование дат
# -------------------------

def format_date_of_publication(published_on):
    """
    Форматирует дату публикации в строку в формате "день месяц год в часы:минуты".
    """
    months_in_russian = [
        "января", "февраля", "марта", "апреля", "мая", "июня",
        "июля", "августа", "сентября", "октября", "ноября", "декабря"
    ]

    publication_date = datetime.strptime(published_on, "%Y-%m-%dT%H:%M:%S%z")

    return f"{publication_date.day} {months_in_russian[publication_date.month - 1]} {publication_date.year} года в {publication_date.strftime('%H:%M')}"


# -------------------------
# Работа с валютами
# -------------------------

def fetch_exchange_rate(currency_code):
    """
    Получает актуальный курс валюты по отношению к рублю.
    Возвращает None, если валюта не найдена.
    """
    if currency_code in ['RUR', 'RUB']:
        return 1

    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    if currency_code in data['Valute']:
        rate = data['Valute'][currency_code]['Value'] / data['Valute'][currency_code]['Nominal']
        return rate

    return None


def convert_amount_to_rub(amount, currency_code):
    """
    Конвертирует сумму в рубли, используя курс валюты.
    Возвращает None, если курс не найден.
    """
    rate = fetch_exchange_rate(currency_code)
    if rate:
        return round(amount * rate, 2)
    return None


# -------------------------
# Конвертация зарплаты
# -------------------------

def convert_salary_to_rub(salary_info):
    """
    Конвертирует зарплату из исходной валюты в рубли.
    Возвращает зарплату в рублях (или None, если конвертация не удалась).
    """
    salary_lower_limit = salary_info['from']
    salary_upper_limit = salary_info['to']
    currency_code = salary_info['currency']

    salary_from_rub = salary_to_rub = None

    # Конвертируем минимальное значение зарплаты
    if salary_lower_limit:
        salary_from_rub = convert_amount_to_rub(salary_lower_limit, currency_code)

    # Конвертируем максимальное значение зарплаты
    if salary_upper_limit:
        salary_to_rub = convert_amount_to_rub(salary_upper_limit, currency_code)

    return {
        'from': salary_from_rub,
        'to': salary_to_rub,
        'currency': 'RUB'
    }
