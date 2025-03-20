from bs4 import BeautifulSoup
import requests

def get_weather(city):
    """
    Get the current weather for a specific city in Uzbekistan.

    Args:
        city (str): The name of the city. Supported cities and their acceptable inputs are:
            - Tashkent: "tashkent", "toshkent"
            - Andijan: "andijan", "andijon"
            - Bukhara: "bukhara", "buxoro"
            - Gulistan: "gulistan", "guliston"
            - Jizzakh: "jizzakh", "jizzax"
            - Zarafshan: "zarafshan", "zarafshon"
            - Karshi: "karshi", "qarshi"
            - Navoi: "navoi", "navoiy"
            - Namangan: "namangan"
            - Nukus: "nukus"
            - Samarkand: "samarkand", "samarqand"
            - Termez: "termez", "termiz"
            - Urgench: "urgench", "urganch"
            - Ferghana: "ferghana", "farg'ona"
            - Khiva: "khiva", "xiva"
            """
    city = city.lower().strip()
    
    if city == "tashkent" or city == "toshkent":
        base_url = f'https://obhavo.uz/tashkent'
    elif city == "andijan" or city == "andijon":
        base_url = f'https://obhavo.uz/andijan'
    elif city == "bukhara" or city == "buxoro":
        base_url = f'https://obhavo.uz/bukhara'
    elif city == "gulistan" or city == "guliston":
        base_url = f'https://obhavo.uz/gulistan'
    elif city == "jizzakh" or city == "jizzax":
        base_url = f'https://obhavo.uz/jizzakh'
    elif city == "zarafshan" or city == "zarafshon":
        base_url = f'https://obhavo.uz/zarafshan'
    elif city == "karshi" or city == "qarshi":
        base_url = f'https://obhavo.uz/karshi'
    elif city == "navoi" or city == "navoiy":
        base_url = f'https://obhavo.uz/navoi'
    elif city == "namangan":
        base_url = f'https://obhavo.uz/namangan'
    elif city == "nukus":
        base_url = f'https://obhavo.uz/nukus'
    elif city == "samarkand" or city == "samarqand":
        base_url = f'https://obhavo.uz/samarkand'
    elif city == "termez" or city == "termiz":
        base_url = f'https://obhavo.uz/termez'
    elif city == "urgench" or city == "urganch":
        base_url = f'https://obhavo.uz/urgench'
    elif city == "ferghana" or city == "farg'ona":
        base_url = f'https://obhavo.uz/ferghana'
    elif city == "khiva" or city == "xiva":
        base_url = f'https://obhavo.uz/khiva'
    else:
        print("Bunday shahar ro'yxatda yo'q! 🤔 Iltimos, O'zbekiston shaharlaridan birini kiriting.")
        return None

    response = requests.get(base_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        current_day = soup.find('div', class_='current-day').text.strip()
        current_temp = soup.find('div', class_='current-forecast').find_all('span')[1].text.strip()
        weather_desc = soup.find('div', class_='current-forecast-desc').text.strip()
        return [current_day, current_temp, weather_desc]
    else:
        print(f"Xatolik yuz berdi! Status kodi: {response.status_code}")
        return None