import requests


class HotWeather:

    def __init__(self, zipcode):
        self.zipcode = zipcode
        self.response = self.get_request()

    def get_request(self):
        return requests.get(self.url.format(self.zipcode))


class CurrentConditions(HotWeather):

    url = "http://api.wunderground.com/api/d04b489ffdf2e7e8/conditions/q/{}.json"


    def get_current_conditions(self):

        if 'error' not in self.response.json()['response']:

            weather_dict = self.response.json()["current_observation"]

            self.last_update = weather_dict["observation_time"]
            self.city_full_name = weather_dict["display_location"]["full"]
            self.weather = weather_dict['weather']
            self.temperature = weather_dict['temperature_string']
            self.feels_like = weather_dict['feelslike_string']
            self.relative_humidity = weather_dict['relative_humidity']

            return "\n** {} **\n\n\tWeather: {}\n\tTemperature: {}\n\tFeels like: {}\n\tHumidity: {}\n\t{}".format(self.city_full_name, self.weather, self.temperature, self.feels_like, self.relative_humidity, self.last_update)

        else:
            print("No location found for {}".format(self.zipcode))
            exit()


class SunPhase(HotWeather):

    url = "http://api.wunderground.com/api/d04b489ffdf2e7e8/astronomy/q/{}.json"

    def get_sun_phase(self):
        sun_dict = self.response.json()
        self.sun_rise = sun_dict['sun_phase']['sunrise']
        self.sun_set = sun_dict['sun_phase']['sunset']
        return "\n\tSunrise: {}:{} AM\n\tSunset: {}:{} PM".format(self.sun_rise['hour'], self.sun_rise['minute'], (int(self.sun_set['hour'])-12), self.sun_set['minute'])


class TenDayForecast(HotWeather):


    url = "http://api.wunderground.com/api/d04b489ffdf2e7e8/forecast10day/q/{}.json"

    def get_ten_day_forcast(self):
        ten_day_dict = self.response.json()

        for day in ten_day_dict['forecast']['simpleforecast']['forecastday']:
            date = "{}/{}".format(day['date']['month'], day['date']['day'])
            weather = day['conditions']
            daily_high = "{}F, {}C".format(day['high']['fahrenheit'], day['high']['celsius'])
            daily_low = "{}F, {}C".format(day['low']['fahrenheit'], day['low']['celsius'])

            print("\n\t{}\n\tWeather: {}\n\tDaily High: {}\n\tDaily Low: {}".format(date, weather, daily_high, daily_low))


class WeatherAlerts(HotWeather):


    url = "http://api.wunderground.com/api/d04b489ffdf2e7e8/alerts/q/{}.json"

    def get_alerts(self):
        alert_dict = self.response.json()
        alerts = alert_dict['alerts']

        if len(alerts) > 0:
            for alert in alerts:
                print("\n{}".format(alert['description']))
                print('\nAs of {}'.format(alert['date']))
                print(alert['message'])
                print("Ending {}".format(alert['expires']))

        else:
            print("No weather alerts")


class HurricaneAdvisory(HotWeather):

    def __init__(self):
        super().__init__('')

    def get_request(self):
        return requests.get("http://api.wunderground.com/api/d04b489ffdf2e7e8/currenthurricane/view.json")

    def get_hurricanes(self):
        cane_dict = self.response.json()
        dem_canes = cane_dict['currenthurricane']

        if len(dem_canes) > 0:
            for cane in dem_canes:
                stormInfo = cane['stormInfo']['stormName_Nice']
                category = cane['Current']['SaffirSimpsonCategory']
                wind_speed = cane['Current']['WindSpeed']['Mph']
                wind_gust = cane['Current']['WindGust']['Mph']

                print("\n\tStorm info: {}\n\tCategory: {}\n\tWind Speed: {} mph\n\tWind Gusts: {} mph".format(stormInfo, category, wind_speed, wind_gust))
