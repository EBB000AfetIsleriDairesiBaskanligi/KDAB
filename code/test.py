import os
import requests
from time import sleep
from gtts import gTTS
import folium
import webbrowser
import datetime
import locale
import warnings
from urllib3.exceptions import InsecureRequestWarning
import variables

url = variables.url



def closeWarningsAboutCommendPrompt():
    warnings.filterwarnings("ignore", category=InsecureRequestWarning)

def controlTime():
    an = datetime.datetime.now()
    return datetime.datetime.strftime(an, '%d %B %Y')

def mapProcesses(coordinates, attention):
    map_center = coordinates
    my_map = folium.Map(location=map_center, zoom_start=13)
    marker_1 = folium.Marker(location=coordinates, popup=attention)
    my_map.add_child(marker_1)
    my_map.save(variables.exportMapFileName)
    webbrowser.open_new_tab(variables.exportMapFileName)

def scrappingData():
    return requests.get(url, verify=False)

def printEarthquakeInfo(data):
    return f"""Deprem Yeri: {data["area"]}, 
    Koordinatlar: {data["coords"][1]}, {data["coords"][0]}, 
    Derinlik: {data["depth"]}km, 
    Mw:, {data["mag"]}
    --------------------------"""

def controlEarthquakeData(response):
    data = response.json()
    area = data['features'][0]['properties']['place']
    coordinates = data['features'][0]['geometry']['coordinates']
    depth = data['features'][0]['properties']['depth']/1000
    mag = data['features'][0]['properties']['mag']
    return {"area": area, "coords": coordinates, "depth": depth, "mag": mag}


def app():
    print(variables.startMessage)
    locale.setlocale(locale.LC_ALL, '')
    closeWarningsAboutCommendPrompt()

    sira = 0
    earthquakeInfo = None
    while True:
        print(f"Tarih: {controlTime()}, Kontrol No: {sira + 1}")
        sleep(3)
        print(variables.takenDataMessage)
        sleep(5)
        try:
            response = scrappingData()
            if response.status_code == 200:
                earthquakeData = controlEarthquakeData(response)
                info = printEarthquakeInfo(earthquakeData)
                if earthquakeInfo != info:
                    print(info)
                    earthquakeInfo = info
                    if float(earthquakeData["mag"]) > 7.5:
                        mapProcesses([earthquakeData['coords'][1], earthquakeData['coords'][0]], info) 
                        tts = gTTS(variables.alertMessage, lang=variables.language, slow=True)
                        tts.save(variables.alertFileName)
                        y=0
                        while y<3:
                            os.system(f"start {variables.alertFileName}")
                            sleep(3)
                            y+=1
                else: print(variables.notFoundNewData)
            else:
                print(variables.errorMessage)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
        
        sleep(6)
        sira += 1


app()