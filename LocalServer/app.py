import numpy as np
from flask import Flask, request, render_template
import requests
import pickle
import datetime
app = Flask(__name__)
api_key = '04bb72b44289d6aa7473e3c0e76f43f3'

# Load the pickle model
temperatureModel = pickle.load(open('E:/WeatherData/temperatureModel.pkl', 'rb'))
feelsLikeModel = pickle.load(open('E:/WeatherData/feelsLikeModel.pkl', 'rb'))

@app.route('/')
def home():  # put application's code here
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    city = request.form['city']
    weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={api_key}")
    month = datetime.datetime.now().month
    hour = datetime.datetime.now().hour
    latitude = weather_data.json()['coord']['lat']
    longitude = weather_data.json()['coord']['lon']
    minTemperature = weather_data.json()['main']['temp_min']
    maxTemperature = weather_data.json()['main']['temp_max']
    pressure = weather_data.json()['main']['pressure']
    humidity = weather_data.json()['main']['humidity']
    visibility = weather_data.json()['visibility']
    windSpeed = weather_data.json()['wind']['speed']
    windDirection = weather_data.json()['wind']['deg']
    try:
        windGust = weather_data.json()['wind']['gust']
    except:
        windGust = 0
    try:
        precipitation = weather_data.json()['precip']['total']
    except:
        precipitation = 0
    cloudCover = weather_data.json()['clouds']['all']

    tempPredictorsFirst = [month, hour, latitude, longitude, minTemperature, maxTemperature, pressure, humidity,
                  visibility, windSpeed, windDirection, windGust, precipitation, cloudCover]
    tempPredictorsSecond = [float(x) for x in tempPredictorsFirst]
    predictors = [np.array(tempPredictorsSecond)]
    prediction = temperatureModel.predict(predictors)
    temperature = prediction[0]

    newPredictorsFirst = [month, hour, latitude, longitude, temperature, minTemperature, maxTemperature,
                          pressure, humidity, visibility, windSpeed, windDirection, windGust, precipitation, cloudCover]
    newPredictorsSecond = [float(x) for x in newPredictorsFirst]
    newPredictors = [np.array(newPredictorsSecond)]
    newPrediction = feelsLikeModel.predict(newPredictors)
    feelsLike = newPrediction[0]

    return render_template('index.html',
                           month=month,
                           hour=hour,
                           latitude=latitude,
                           longitude=longitude,
                           minTemperature=minTemperature,
                           maxTemperature=maxTemperature,
                           pressure=pressure,
                           humidity=humidity,
                           visibility=visibility,
                           windSpeed=windSpeed,
                           windDirection=windDirection,
                           windGust=windGust,
                           precipitation=precipitation,
                           cloudCover=cloudCover,
                           actualTemperature=weather_data.json()['main']['temp'],
                           predictedTemperature=temperature,
                           actualFeelsLike=weather_data.json()['main']['feels_like'],
                           predictedFeelsLike=feelsLike,)


if __name__ == '__main__':
    app.run(debug=True)
