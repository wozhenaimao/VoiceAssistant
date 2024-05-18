from dotenv import load_dotenv
import speech_recognition as sr

from src.ai import *
from src.utils import clear_temp_dir


load_dotenv()
clear_temp_dir()

running = True

while running:

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Adjusting for background noise. One second")
        r.adjust_for_ambient_noise(source)
        print("Say something!")
        audio = r.listen(source)
        answer(audio)

