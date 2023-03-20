from flask import Flask,request,jsonify
import requests
from geopy.geocoders import Nominatim
app= Flask(__name__)
@app.route('/',methods=['POST','GET'])
def index():
    data=request.get_json()
    source_city=data['queryResult']['parameters']['geo-city']
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(source_city)
    lat=location.latitude
    lon=location.longitude
    url="https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=013b716d17cad1e8064a6a092a8cf06d".format(lat,lon)
    response=requests.get(url)
    response=response.json()
    current_temp=round(float(response['main']['temp']-273.15),2)
    min_temp=round(float(response['main']['temp_min']-273.15),2)
    max_temp=round(float(response['main']['temp_max']-273.15),2)
    weather=response['weather'][0]['main']
    description=response['weather'][0]['description']
    final="The weather in {} is mainly {},more specifically {}. Current temprature is approximately {}C with minimum temperature {}C and maximum temperature {}C.".format(source_city,weather,description,current_temp,min_temp,max_temp)
    ft={"fulfillmentText":final}
    return jsonify(ft)
if __name__=="__main__":
    app.run()
