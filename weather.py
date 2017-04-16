from endpoint import CurrentConditions
from endpoint import SunPhase
from endpoint import WeatherAlerts
from endpoint import TenDayForecast
from endpoint import HurricaneAdvisory
from clear import clear_screen
import re


def get_zipcode():
    first = True
    while first or (len(user_input) != 5 and not re.search(r'^[0-9]{5}?$', user_input)):
        first = False
        user_input = input("Enter a 5 digit zipcode: ")
    return user_input


def main():

    print("Let's check the weather")
    zipcode = get_zipcode()
    curr_weather = CurrentConditions(zipcode)
    sun_phase = SunPhase(zipcode)
    ten_day = TenDayForecast(zipcode)
    weather_alerts = WeatherAlerts(zipcode)
    h = HurricaneAdvisory()

    print(curr_weather.get_current_conditions())
    print(sun_phase.get_sun_phase())

    print("\nWhat else would you like to know about {}?".format(curr_weather.city_full_name))

    while True:
        user_input = input("\n1) 10 day forcast\n2) Weather Alerts\n3) Hurricane Advisory\n4) Quit\n")
        if user_input == '1':

            ten_day.get_ten_day_forcast()

        elif user_input == '2':

            weather_alerts.get_alerts()

        elif user_input == '3':

            h.get_hurricanes()
        elif user_input == '4':
            exit()



if __name__ == "__main__":
    clear_screen()
    main()
