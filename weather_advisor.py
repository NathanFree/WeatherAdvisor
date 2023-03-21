import requests
from enum import Enum
from dotenv import load_dotenv
import os

class TemperatureType(Enum):
    FAHRENHEIT = 1
    CELSIUS = 2,
    KELVIN = 3,

temperature_type_dict = {
    TemperatureType.FAHRENHEIT: {"openweathermapName": "imperial", "abbreviation": "F"},
    TemperatureType.CELSIUS: {"openweathermapName": "metric", "abbreviation": "C"},
    TemperatureType.KELVIN: {"openweathermapName": "standard", "abbreviation": "K"},
}

class WeatherAdvisor:
    def __init__(self, jacket_temperature: int, coat_temperature: int, temperature_type: TemperatureType):
        load_dotenv()
        self.OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
        self.ZIP_CODE = os.getenv("ZIP_CODE")
        self.jacket_temperature = jacket_temperature
        self.coat_temperature = coat_temperature
        self.temperature_type = temperature_type
        self.weather_data = self.get_current_openweathermap_data(temperature_type)

    class PrecipitationType(Enum):
        NONE = 0
        LIGHT_SNOW = 1
        SNOW = 2
        HEAVY_SNOW = 3
        LIGHT_RAIN = 4
        RAIN = 5
        HEAVY_RAIN = 6

    precipitation_dict = {
        PrecipitationType.NONE: "none",
        PrecipitationType.LIGHT_SNOW: "lightly snowing",
        PrecipitationType.SNOW: "snowing",
        PrecipitationType.HEAVY_SNOW: "heavily snowing",
        PrecipitationType.LIGHT_RAIN: "lightly raining",
        PrecipitationType.RAIN: "raining",
        PrecipitationType.HEAVY_RAIN: "heavily raining"
    }

    def get_current_openweathermap_data(self, temperature_type: TemperatureType):
        # we could use self.temperature_type instead, but we want to get the current weather data in the init, and it's bad practice to use other init'd values to compute an init'd value
        return requests.get(f"https://api.openweathermap.org/data/2.5/weather?zip={self.ZIP_CODE}&appid={self.OPENWEATHERMAP_API_KEY}&units={temperature_type_dict[temperature_type]['openweathermapName']}").json()

    def get_temperature_advice(self):
        current_temperature = self.weather_data['main']['temp']

        # convert current temperature to Fahrenheit or Celsius based on self.temperature_type
        # if self.temperature_type == TemperatureType.Fahrenheit:
        #     current_temperature = (current_temperature - 273.15) * 9/5 + 32
        # elif self.temperature_type == TemperatureType.Celsius:
        #     current_temperature = current_temperature - 273.15

        # compare current temperature to jacket_temperature and coat_temperature
        output_text = f"Current temperature is {current_temperature:.1f} {temperature_type_dict[self.temperature_type]['abbreviation']}. "

        if current_temperature > self.jacket_temperature and current_temperature <= self.jacket_temperature + 5:
            output_text += "Consider wearing a jacket."
        elif current_temperature > self.coat_temperature + 5 and current_temperature <= self.jacket_temperature:
            output_text += "Grab a jacket."
        elif current_temperature > self.coat_temperature and current_temperature <= self.coat_temperature + 5:
            output_text += "Consider wearing a coat."
        elif current_temperature <= self.coat_temperature:
            output_text += "Grab a coat."

        return output_text

    def get_precipitation_advice(self):
        precipitation_id = self.weather_data['weather'][0]['id']
        
        current_precipitation_mode = self.determine_precipitation_type(precipitation_id)

        # generate output text based on current precipitation mode
        output_text = f"Current precipitation: {self.precipitation_dict[current_precipitation_mode]}. "
        if current_precipitation_mode in [self.PrecipitationType.SNOW, self.PrecipitationType.HEAVY_SNOW, self.PrecipitationType.RAIN, self.PrecipitationType.HEAVY_RAIN]:
            output_text += "Grab a rainjacket."
        elif current_precipitation_mode in [self.PrecipitationType.LIGHT_SNOW, self.PrecipitationType.LIGHT_RAIN]:
            output_text += "Consider wearing a rainjacket."

        return output_text
    
    # determine precipitation mode based on precipitation id
    # openweathermap weather condition codes (ex: 600): https://openweathermap.org/weather-conditions
    def determine_precipitation_type(self, precipitation_id):
        current_precipitation_mode = self.PrecipitationType.NONE
        if precipitation_id in [600, 612, 615, 620]:
            current_precipitation_mode = self.PrecipitationType.LIGHT_SNOW
        elif precipitation_id in [601, 611, 613, 616, 621]:
            current_precipitation_mode = self.PrecipitationType.SNOW
        elif precipitation_id > 600 and precipitation_id < 700:
            current_precipitation_mode = self.PrecipitationType.HEAVY_SNOW
        elif precipitation_id in [200, 230, 300, 310, 500]:
            current_precipitation_mode = self.PrecipitationType.LIGHT_RAIN
        elif precipitation_id in [201, 231, 301, 311, 321, 501, 521, 531]:
            current_precipitation_mode = self.PrecipitationType.RAIN
        elif precipitation_id > 500 and precipitation_id < 600:
            current_precipitation_mode = self.PrecipitationType.HEAVY_RAIN
        return current_precipitation_mode

    def get_weather_advice(self):
        return f"{self.get_temperature_advice()}\n{self.get_precipitation_advice()}"

my_weather_advisor = WeatherAdvisor(
    jacket_temperature=56,
    coat_temperature=48,
    temperature_type=TemperatureType.FAHRENHEIT
)
print(my_weather_advisor.get_weather_advice())