import pyttsx3
import speech_recognition as sr 
import datetime
import wikipedia 
import webbrowser
import smtplib
import requests
import urllib3
import json
from googlesearch import search

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        print("Good Morning!")
        speak("Good Morning")

    elif hour>=12 and hour<18:
        print("Good Afternoon!")
        speak("Good Afternoon")

    else:
        print("Good Evening!") 
        speak("Good Evening") 

    print("Hello Ma'am. How may I help you?") 
    speak("Hello Ma'am. How may I help you")      

def takeCommand():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print("Say that again please...")  
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('aaliyawaziir@gmail.com', '@@!;y@123')
    server.sendmail('awazir_bemba20@gmail.com', to, content)
    server.close()


def get_temperature(json_data):
    temp_in_celcius = json_data['main']['temp']
    return temp_in_celcius

def get_weather_type(json_data):
    weather_type = json_data['weather'][0]['description']
    return weather_type

def get_wind_speed(json_data):
    wind_speed = json_data['wind']['speed']
    return wind_speed

def get_weather_data(json_data, city):
    description_of_weather = json_data['weather'][0]['description']
    weather_type = get_weather_type(json_data)
    temperature = get_temperature(json_data)
    wind_speed = get_wind_speed(json_data)
    weather_details = ''
    return weather_details + ("The weather in {} is currently {} with a temperature of {} degrees and wind speeds reaching {} km/ph".format(city, weather_type, temperature, wind_speed))


if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()



        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")
            speak("youtube opened")

        elif 'open google' in query:
            webbrowser.open("https://www.google.com")
            speak("google opened")
  
        elif 'open netflix' in query:
            webbrowser.open("https://www.netflix.com")
            speak("netflix opened")

        elif 'open prime' in query:
            webbrowser.open("https://www.primevideo.com")
            speak("prime opened")

        elif 'open git' in query:
            webbrowser.open("https://www.github.com")
            speak("github opened")

        elif 'open hotstar' in query:
            webbrowser.open("https://www.hotstar.com")
            speak("hotstar opened")

        elif 'open tinkercad' in query:
            webbrowser.open("https://www.tinkercad.com")
            speak("tinkercad opened")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Ma'am, the time is {strTime}")

        elif 'email to me' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "awazir_bemba20@thapar.edu"    
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry. I am not able to send this email")    

        elif 'the weather' in query:
                api_address = 'https://api.openweathermap.org/data/2.5/weather?q=Sydney,au&appid=a10fd8a212e47edf8d946f26fb4cdef8&q='
                speak("Which city are you in")
                city = takeCommand()
                units_format = "&units=metric"
                final_url = api_address + city + units_format
                json_data = requests.get(final_url).json()
                weather_details = get_weather_data(json_data, city)
                speak(weather_details)
                print(weather_details)

        elif 'my location' in query:
            http = urllib3.PoolManager()
            r = http.request('GET', 'http://ipinfo.io/json')
            data = json.loads(r.data.decode('utf-8'))
            city=data['city']
            loc=data['loc']
            print(city,loc)
            speak("Your IP location is "+city+" With cordinates "+loc)

        elif 'quit' in query:
            speak("Goodbye, have a nice day")
            exit()

        elif 'stop' in query:
            speak("Goodbye, have a nice day")
            exit()