# Bike Sharing Dashboard
**Tugas Akhir Proyek Analisis Data**

## Setup environment
```
conda create --name projek1 python=3.11
conda activate projek1
pip install numpy pandas matplotlib seaborn jupyter streamlit 
```

## Run steamlit app
```
streamlit run dashboard.py
```

## Dataset Characteristics

Both `hour.csv` and `day.csv` have the following fields, except `hr` which is not available in `day.csv`:

- `instant`: record index
- `dteday`: date
- `season`: season (1:springer, 2:summer, 3:fall, 4:winter)
- `yr`: year (0: 2011, 1:2012)
- `mnth`: month (1 to 12)
- `hr`: hour (0 to 23)
- `holiday`: weather day is holiday or not (extracted from [DC Government Holiday Schedule](http://dchr.dc.gov/page/holiday-schedule))
- `weekday`: day of the week
- `workingday`: if day is neither weekend nor holiday is 1, otherwise is 0.
- `weathersit`: 
  - 1: Clear, Few clouds, Partly cloudy, Partly cloudy
  - 2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist
  - 3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds
  - 4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog
- `temp`: Normalized temperature in Celsius. The values are divided by 41 (max)
- `atemp`: Normalized feeling temperature in Celsius. The values are divided by 50 (max)
- `hum`: Normalized humidity. The values are divided by 100 (max)
- `windspeed`: Normalized wind speed. The values are divided by 67 (max)
- `casual`: count of casual users
- `registered`: count of registered users
- `cnt`: count of total rental bikes including both casual and registered

Information about `main_data.csv`:

- `date`: date format yyyy-mm-dd
- `season`: category (spring, summer, fall, winter)
- `year`: category (2011, 2012)
- `month`: category ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
- `hour`: int (0 to 23)
- `holiday`: category, day is holiday or not
- `weekday`: category, day of the week ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
- `workingday`: category, if day is neither weekend nor holiday is YES, otherwise is No.
- `weather`: category (Clear, Misty, Light_RainSnow, Heavy_RainSnow)
- `temp`: float, temperature in Celsius. The values are multiplied by 41 (max)
- `atemp`: float, feeling temperature in Celsius. The values are multiplied by 50 (max)
- `humidity`: float, humidity. The values are multiplied by 100 (max)
- `windspeed`: float, wind speed. The values are multiplied by 67 (max)
- `casual`: count of casual users
- `registered`: count of registered users
- `total_count`: count of total rental bikes including both casual and registered
```
# Dicoding
