import logging
from typing import Optional

import requests
import xml.etree.ElementTree as ET


def get_exchange(currency: str) -> Optional[str]:
    """
    Получает курс обмена для заданной валюты
    Args:
        currency:
            Код валюты в виде строки
    Returns:
        Курс обмена в виде строки или None если данные недоступны
    """
    url = "https://www.cbr.ru/scripts/XML_daily.asp"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            root = ET.fromstring(response.text)
            rate = None
            for item in root.findall("Valute"):
                if item.find("CharCode").text == currency:
                    rate = item.find("Value").text
                    break
            return rate
        except ET.ParseError as e:
            logging.error(f"Ошибка парсинга XML: {str(e)}")
            return None
    else:
        logging.error("Не удалось получить данные")
        return None
