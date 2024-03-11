import os
import time
import pyaudio
import playsound
import pygame.event
from gtts import gTTS
import openai
import speech_recognition as sr
from pygame import mixer
import tempfile
from tempfile import TemporaryFile
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv('OPENAI')
deepgram_key = os.getenv('DEEPGRAM')
lang = "en-us"

openai.api_key = openai_api_key

END_EVENT = pygame.USEREVENT+1

pygame.init()

while True:
    def get_audio():
        r = sr.Recognizer()
        with sr.Microphone(device_index=1) as source:
            audio = r.listen(source)
            said = ""

            try:
                said = r.recognize_google(audio)
                print("User: " + said)

#               #if "Hello" in said:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an assistant who helps people with their studies."},
                        {"role": "user", "content": said},
                    ]
                )
                text = (response['choices'][0]['message']['content'])
                print("ChatGPT: " + text)
                speech = gTTS(text=text, lang=lang, slow=False, tld="com.au")
                mixer.init()
                sf = TemporaryFile()
                speech.write_to_fp(sf)
                sf.seek(0)
                mixer.music.load(sf)
                mixer.music.play()
                mixer.music.set_endevent(END_EVENT)
                while pygame.mixer.music.get_busy():
                    time.sleep(1)
                    #speech.save("welcome1.mp3")
                #playsound.playsound("welcome1.mp3")

            except Exception as error:
                print(error)

        return said
    get_audio()
