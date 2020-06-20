from plyer import notification
import requests
import datetime
import time

from bs4 import BeautifulSoup

import pyttsx3
import speech_recognition as kb

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

engine.setProperty('voice', voices[0].id)

def notifyMe(title,message):
    notification.notify(
        title = title,
        message = message,
        app_icon = r"C:\Users\hp\Downloads\corona.ico",
        timeout = 15

    )

def getData(url):
    r = requests.get(url)
    return r.text



def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = kb.Recognizer()

    with kb.Microphone() as source:

        #speak("listening...")          #bol listening
        print("listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        speak("Recognizing...")        #bol recognizing
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:

        speak("Say that again please...")         #bol again
        print("Say that again please...")
        return "None"
    return query

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("good morning sir")
    elif hour>=12 and hour<=18:
        speak("good afternoon sir")
    else:
        speak("good evening")

    speak("im lara , a python based , machine learnig program made by future vision team . Say coronavirus to see , coronavirus statewise cases in india.  say symptoms to listen symptoms . say precautions to know them .")
    speak('say stop , to close this program')
    speak('now speak , i am listening')



if __name__=="__main__":
    wishMe()

    b=True
    while b:
        query = takeCommand().lower()
        if 'coronavirus' in query:
            speak('You will see a pop up message , of statewise , coronavirus cases in india on your computer ')

            myHtmlData = getData('https://www.mohfw.gov.in/')
            soup = BeautifulSoup(myHtmlData, 'html.parser')

            # print(soup.prettify())

            myDataStr = ""
            for tr in soup.find_all('tbody')[0].find_all('tr'):
                myDataStr += tr.get_text()
            myDataStr = myDataStr[1:]
            itemList = myDataStr.split("\n\n")

            states = ['Chandigarh', 'Rajasthan', 'Punjab']
            for item in itemList[0:35]:
                dataList = item.split('\n')
                if dataList[1] in states:
                    print(dataList)
                    nTitle = "Cases of covid-19"
                    nText = f"State : {dataList[1]}\n Total confirm cases : {dataList[5]}\n Active cases : {dataList[2]}\n Cured : {dataList[3]} & Deaths : {dataList[4]}"
                    notifyMe(nTitle, nText)
                    time.sleep(6)
            speak('You can see as much states as you want . i can show cases of all states . just put name of you want to see in code   . now speak')


        elif 'symptoms' in query:
            speak('the symptoms of coronavirus are ')
            speak('fever \n dry cough \n tiredness \n difficulty in breathing \n chest pain \n loss of speech')
            speak('except symptoms , anything you want to know , speak now')

        elif 'precaution' in query:
            speak('one should take following precautions to avoid coronavirus')
            speak('clean your hands with a alcohol based handwash \n follow social distancing especially from one who has cough or cold \n '
                  'cover your mouth and nose with mask and avoid touching the mask often \n if you have difficulty in breathing take medical assistance \n avoid travelling in these days if possible'
                  )
            speak('we can beat corona by following the lockdown and guidelines issued by our indian government . So please do not go out ')
            speak('except precuations , anything you want to know , speak now')


        elif 'stop' in query:
            speak('i am turning off')
            break
