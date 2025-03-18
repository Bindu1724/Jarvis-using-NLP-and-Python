import datetime
import os
import sys
import time
import webbrowser
import pyautogui
import pyttsx3
import speech_recognition as sr
import json
import pickle
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore
import random
import numpy as np
import psutil


with open("intents.json") as file:
    data = json.load(file)

model = load_model("chat_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer=pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder=pickle.load(encoder_file)

def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume+0.05)
    return engine

def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()

#speak("Hello, I am Jarvis")

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening....", end="", flush=True)
        r.pause_threshold=1.0
        r.phrase_threshold=0.3
        r.sample_rate=48000
        r.dynamic_energy_threshold=True
        r.operation_timeout=5
        r.non_speaking_duration=0.5
        r.dynamic_energy_adjustment=2
        r.energy_threshold=4000
        r.phrase_time=10
        #print(sr.Microphone.list_microphone_names())
        audio = r.listen(source)
    try:
        print("\r", end="", flush=True)
        print("Recognizing.....", end="", flush=True)
        query = r.recognize_google(audio, language='en-in')
        print("\r", end="", flush=True)
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say it again please")
        return "None"
    return query

def cal_day():
    day = datetime.datetime.today().weekday() + 1
    day_dict={
        1:"Monday",
        2:"Tuesday",
        3:"Wednesday",
        4:"Thursday",
        5:"Friday",
        6:"Saturday",
        7:"Sunday"
    }  
    if day in day_dict.keys():
        day_of_week = day_dict[day]
        print(day_of_week)
    return day_of_week

        
def wishMe():
    hour = int(datetime.datetime.now().hour)
    t=time.strftime("%I:%M:%p")
    day = cal_day()

    if(hour>0) and (hour<12) and ('AM' in t):
        speak(f"Good Morning Bindu, it's {day} and the time is {t}")
    elif(hour>12) and (hour<16) and ('PM' in t):
        speak(f"Good afternoon Bindu, it's {day} and the time is {t}")
    else:
        speak(f"Good evening Bindu, it's {day} and the time is {t}")

def social_media(command):
    if 'facebook' in command:
        speak('opening your facebook')
        webbrowser.open("https://www.facebook.com/")
    elif 'whatsapp' in command:
        speak('opening your whatsapp')
        webbrowser.open("https://web.whatsapp.com/")
    elif 'instagram' in command:
        speak('opening your instagram')
        webbrowser.open("https://www.instagram.com/")


def schedule():
    day = cal_day().lower()
    speak("Bindu today's schedule is")
    week={
        "monday": "from 9:00 AM to 10:00 AM you have Python class, from 10:30 AM to 11:30 AM you have JavaScript class. You have a break for 30 minutes and you can go for a walk and do some exercises.",
        "tuesday": "from 9:00 AM to 10:00 AM you have Web Development class, from 10:30 AM to 11:30 AM you have Java class. You have a break for 30 minutes and you can go for a walk and do some exercises.",
        "wednesday": "from 9:00 AM to 10:00 AM you have DSA class, from 10:30 AM to 11:30 AM you have HTML and CSS class. You have a break for 30 minutes and you can go for a walk and do some exercises.",
        "thursday": "from 9:00 AM to 10:00 AM you have SQL class. You have a break for 30 minutes and you can go for a walk and do some exercises.",
        "friday": " from 9:00 AM to 10:00 AM you have Practical class. You have a break for 30 minutes and you can go for a walk and do some exercises.",
        "saturday": "Today you have more relaxed day.You can go for a walk and do some exercise for 40 minutes and take bath and go for the shopping at 5 PM.",
        "sunday": "Today is a Sunday and it is funday to you. You can chill in the garden at the evening 5 PM."
    }
    if day in week.keys():
        speak(week[day])

def openApp(command):
    if "calculator" in command:
        speak("opening calculator")
        os.startfile('c:\\Windows\\System32\\calc.exe')
    elif "notepad" in command:
        speak("opening notepad")
        os.startfile('c:\\Windows\\System32\\notepad.exe')
    elif "paint" in command:
        speak("opening paint")
        os.startfile('C:\\Users\\madis\\AppData\\Local\\Microsoft\\WindowsApps\\mspaint.exe')

def closeApp(command):
    if "calculator" in command:
        speak("closing calculator")
        os.system('taskkill /f /im calc.exe')
    elif "notepad" in command:
        speak("closing notepad")
        os.system('taskkill /f /im notepad.exe')
    elif "paint" in command:
        speak("closing paint")
        os.system('taskkill /f /im mspaint.exe')

def browsing(query):
    if 'google' in query:
        speak("Bindu, what should i search on google..")
        s = command().lower()
        webbrowser.open(f"{s}")
    # elif 'edge' in query:
    #     speak("opening your microsoft edge")
    #     os.startfile()

def condition():
    usage = str(psutil.cpu_percent())
    speak(f"CPU is at {usage} percentage")
    battery = psutil.sensors_battery()
    percentage = battery.percent
    speak(f"Bindu our system have {percentage} percentage battery")

    if percentage>=80:
        speak("we could have enough charging to do work")
    elif percentage>=40 and percentage<=75:
        speak("Bindu we should connect our system to charging point to charge our battery")
    else:
        speak("Bindu we have very low power, please connect to charging otherwise laptop should be off...")

if __name__ == "__main__":
    #wishMe()
    while True:
        #query = command().lower()
        #print(query)
        query = input("Enter your command-> ")
        if ('facebook' in query) or ('whatsapp' in query) or ('instagram' in query):
            social_media(query)
        #elif("university time table" in query) or ("schedule in query"):
            #schedule()
        elif("volume up" in query) or ("increase the volume" in query):
            pyautogui.press("volumeup")
            speak("volume increased")
        elif("volume down" in query) or ("decrease the volume" in query):
            pyautogui.press("volumedown")
            speak("volume decreased")
        elif("volume mute" in query) or ("mute the volume" in query):
            pyautogui.press("volumemute")
            speak("volume muted")   
        elif("open calculator" in query) or ("open notepad" in query) or ("open paint" in query):
            openApp(query)
        elif("close calculator" in query) or ("close notepad" in query) or ("close paint" in query):
            closeApp(query)
        elif ("what" in query) or ("who" in query) or ("how" in query) or ("hi" in query) or ("thanks" in query) or ("hello" in query):
                padded_sequences = pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=20, truncating='post')
                result = model.predict(padded_sequences)
                tag = label_encoder.inverse_transform([np.argmax(result)])

                for i in data['intents']:
                    if i['tag'] == tag:
                        speak(np.random.choice(i['responses']))
        elif ("open google" in query) or ("open edge" in query):
            browsing(query)
        elif ("system condition" in query) or ("condition of the system" in query):
            speak("checking the system condition")
            condition()
        elif "exit" in query:
            sys.exit()
        



