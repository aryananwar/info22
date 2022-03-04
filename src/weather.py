import requests
import json



key = '97b94bcdedc61ead5a00220cdd8ac6d3'

class Weather:
    def __init__(self):
        pass

    # @param time to check for weather, in unix
    # @param latitude of location to check
    # @param longitutde of location to check
    # @return array with information about weather for inputted unix time

    def get_weather_from_date(unixTime, lat, lon):

        x = requests.get('http://history.openweathermap.org/data/2.5/history/city'+
                            '?lat=' + str(lat) + '&lon=' + str(lon) +  '&type=hour&start=' + str(unixTime) + '&end=' + str(unixTime) +
                            '&units=metric&appid=' + key)
        a = json.loads(x.text)

        arr = []
        arr.append(a['list'][0]['main']['temp'])
        arr.append(a['list'][0]['main']['feels_like'])
        arr.append(a['list'][0]['main']['humidity'])
        arr.append(a['list'][0]['main']['temp_max'])
        arr.append(a['list'][0]['main']['temp_min'])
        arr.append(a['list'][0]['wind']['speed'])
        arr.append(a['list'][0]['clouds']['all'])
        arr.append(a['list'][0]['weather'][0]['description'])
        
        return arr

        

# latitude and longitude for college park maryland
lat =  '38.980666'
lon =  '-76.9369189'

# this is how u use it @rohit
#Weather.get_weather_from_date('1646373600', lat, lon)