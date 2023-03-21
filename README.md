# WeatherAdvisor
tells you the weather and advises you on what to wear.

right now, it's hard-set that the jacket temperature is 56 F and the coat temperature is 48 F. i'll be tweaking this for myself if i use this.

example run: python3 weather_advisor.py

example output: 
Current temperature is 42.3 F. Grab a coat.
Current precipitation: none.

### First-Time Setup
as is, your openweathermap api key and your zip_code go in .env
the idea is that both of these may be private for you. would be more flexible if i allowed you to pass in a zip_code when creating a WeatherAdvisor instance, but that isn't needed right now!

how to get an openweathermap api key:
1. navigate to https://home.openweathermap.org/
2. create an account
3. log in
4. left-click your username in the top right of the screen (unless openweathermap changes the UI. good luck, then!)
5. click My API Keys in the dropdown
6. under "Create Key", click "Generate Key"

your zip_code is expected to be a 5 digit US zip code

FUTURE POSSIBILITIES
- allow user to pass in jacket_temperature and coat_temperature as input parameters when running the python file
- allow zip code as an input paramter when running the python file
- allow lat+lon as an alternative to zip code
- customization for the "consider" text. right now, regardless of unit, if you're 5 "units" greater than a coat_temperature or jacket_temperature, it will say "Consider wearing a ___" instead of "Grab a ___". 5 "units" is arbitrary and is silly for anything but Fahrenheit.
