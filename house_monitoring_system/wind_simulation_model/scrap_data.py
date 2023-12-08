import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz

from .models import WindTurbine, WindTurbineParameter


main_url = 'https://ua.sinoptik.ua'


def get_hour():
    ukraine_tz = pytz.timezone('Europe/Kiev')
    current_time_ukraine = datetime.now(ukraine_tz)

    return current_time_ukraine.hour


def parse_data(city):
    url = f'{main_url}/погода-{city}'

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Елемент поточного часу
    current_forecast_table_element = soup.find('div', class_='rSide')
    all_data = current_forecast_table_element.find_all('tr')

    return all_data


# Елемент поточного часу
def find_time(all_data):
    current_hour = get_hour()

    td_elements_time = all_data[1].find_all('td')

    for td in td_elements_time:
        forecast_hour = int(td.get_text(strip=True).split(':')[0])
        if forecast_hour >= current_hour:
            current_period = forecast_hour
            current_class = td.get('class')

            return current_class


# Елемент поточної температури
def find_temperature(all_data, td_name):
    td_elements_temperature = all_data[3].find_all('td')

    for td in td_elements_temperature:
        if td.get('class') == td_name:
            return td.get_text()


# Елемент поточного тиску
def find_air_pressure(all_data, td_name):
    td_elements_wind_speed = all_data[5].find_all('td')

    for td in td_elements_wind_speed:
        if td.get('class') == td_name:
            return td.get_text()


# Елемент поточної швидкості вітру
def find_wind_speed(all_data, td_name):
    td_elements_wind_speed = all_data[7].find_all('td')

    for td in td_elements_wind_speed:
        if td.get('class') == td_name:
            div_element = td.find('div')
            data_tooltip = div_element.get('data-tooltip')

            return td.get_text(), data_tooltip


def get_local_data(city):
    all_data = parse_data(city)

    class_name = find_time(all_data)

    data_from_sinoptic = {
        'temperature': transform_temperature(find_temperature(all_data, class_name)),
        'airPressure': int(find_air_pressure(all_data, class_name)),
        'windSpeedNum': float(find_wind_speed(all_data, class_name)[0]),
        'windSpeedText': find_wind_speed(all_data, class_name)[1],
    }

    return data_from_sinoptic


def transform_temperature(temperature_str):
    return int(temperature_str[:-1])


def transform_wind_speed(wind_speed_str):
    current_wind_speed = wind_speed_str.split(' ')[0]
    return current_wind_speed.strip()


#####################################################
def parse_data_forecast(city, current_day):
    url = f'{main_url}/погода-{city}/{current_day}'

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Елемент поточного часу
    current_forecast_table_element = soup.find('div', class_='rSide')
    all_data = current_forecast_table_element.find_all('tr')

    temperature = []
    air_pressure = []
    wind_speed = []

    temperature_data = all_data[3].find_all('td')
    air_pressure_data = all_data[5].find_all('td')
    wind_speed_data = all_data[7].find_all('td')

    # temperature
    for elem in temperature_data:
        print(elem.get_text()[:-1].strip())
        temperature.append(elem.get_text()[:-1].strip())

    # air pressure
    for elem in air_pressure_data:
        air_pressure.append(int(elem.get_text()))

    # wind speed
    for elem in wind_speed_data:
        wind_speed.append(elem.get_text())

    data = {
        'temperature': temperature,
        'air_pressure': air_pressure,
        'wind_speed': wind_speed
    }

    return data


def parse_data_today_tomorrow(city, current_day):
    url = f'{main_url}/погода-{city}/{current_day}'

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Елемент поточного часу
    current_forecast_table_element = soup.find('div', class_='rSide')
    all_data = current_forecast_table_element.find_all('tr')

    temperature = []
    air_pressure = []
    wind_speed = []

    temperature_data = all_data[3].find_all('td')
    air_pressure_data = all_data[5].find_all('td')
    wind_speed_data = all_data[7].find_all('td')

    # temperature
    for i, elem in enumerate(temperature_data):
        if i % 2 != 0:
            continue
        temperature.append(elem.get_text()[:-1].strip())

    # air pressure
    for i, elem in enumerate(air_pressure_data):
        if i % 2 != 0:
            continue
        air_pressure.append(elem.get_text())

    # wind speed
    for i, elem in enumerate(wind_speed_data):
        if i % 2 != 0:
            continue
        wind_speed.append(elem.get_text())

    data = {
        'temperature': temperature,
        'air_pressure': air_pressure,
        'wind_speed': wind_speed
    }

    return data


def get_data_for_day(city, current_day, day_check):
    if day_check == True:
        result = parse_data_today_tomorrow(city, current_day)
    else:
        result = parse_data_forecast(city, current_day)
    return result


def calculate_capacity(data, turbine_name):
    total_capacity = 0

    M = 29      # г / моль - молярна маса повітря
    R = 8.314   # Дж / (моль⋅К) - газова стала

    rotor_area_instance = WindTurbineParameter.objects.filter(name=turbine_name).first()
    rotor_area = rotor_area_instance.rotor_area

    for i in range(len(data['temperature'])):
        temperature = int(data['temperature'][i]) + 273
        air_pressure = int(data['air_pressure'][i])
        wind_speed = float(data['wind_speed'][i])

        # Обчислимо щільність повітря
        ro = (M * (air_pressure * 133.33 / 1000)) / (R * temperature)

        try:
            capacity_instance = WindTurbine.objects.filter(name=turbine_name, wind_speed=float(int(wind_speed))).first()
            table_capacity = capacity_instance.power_output
        except:
            total_capacity += 0
            continue

        Cp = (table_capacity * 1000) / (rotor_area * (0.5 * ro * wind_speed ** 3))  # коефіцієнт
        Cp = int(Cp * 100) / 100

        total_capacity += (((0.5 * ro * rotor_area * (wind_speed ** 3) * Cp) / 1000) * 6)

    return total_capacity


def get_local_data_forecast(city, turbine_name, date_1, date_2):
    current_date = datetime.strptime(date_1, '%Y-%m-%d')
    date2 = datetime.strptime(date_2, '%Y-%m-%d')

    today = datetime.now().strftime('%Y-%m-%d')
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    all_data = []
    total_capacity = 0

    while current_date <= date2:
        day_check = False
        if current_date.strftime('%Y-%m-%d') == today or current_date.strftime('%Y-%m-%d') == tomorrow:
            day_check = True

        result = get_data_for_day(
            city,
            str(current_date.strftime('%Y-%m-%d')),
            day_check
        )

        total_capacity += calculate_capacity(result, turbine_name)
        result['capacity'] = calculate_capacity(result, turbine_name)
        result['date'] = str(current_date.strftime('%Y-%m-%d'))

        all_data.append(result)
        current_date += timedelta(days=1)

    return all_data, total_capacity
