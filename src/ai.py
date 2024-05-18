from openai import OpenAI
from playsound import playsound
from dotenv import load_dotenv
import os
import random
from speech_recognition import AudioData
from src.utils import clear_temp_dir
import subprocess

load_dotenv()

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
messageHistory = [
    {
        'role': 'system',
        'content': 'You are a helpful assistant who can run code on the user\'s computer. \
                    Whenever the user says something that relates to running a web search \
                    or anything else that you cant do without acces to the user\'s computer \
                    initially, you must say [RUN THIS CODE] and then without making a single space or a new line write your code you must run.\
                    you will afterwards recieve the output of your program code run and after \
                    decide whether to run it again or not (only python). if you need any libriries \
                    to run the code, it must also be run through the code you made. The most important rule is you CAN NOT say anything which is not in python code \
                    after saying [RUN THIS CODE]. You absolutely must say all of the natural language before you write any code necessary \
                    You can make internet searches by using python too. Now listen on how you will see the output. After you sent the program \
                    and user run it locally, user will send you all of the output the program has given including errors. So remember that \
                    anything you must see you must use a print() function for. Try to avoid making programs with long loops as you are not gonna be able to see the output then \
                    User\'s computer is mac os moneterey. Dont ever write code without [RUN THIS CODE]\
                    YOU CAN OPEN EXTERNAL PROGRAMS AND WEBSITE AND SEE INFORMATION ON THE INTERNET USING THIS METHOD\
                    MAKE SURE YOU ALWAYS TELL USER USEFUL OUTPUT FROM THE PROGRAM YOU RAN\
                    ALWAYS CHECK THE ERRORS CAREFULLY AND CONSIDER USEFUL LIBRARIES MAY BE MISSING (pip install them through code if they are)\
                    YOU DO NOT HAVE AND WILL NOT GET ANY API KEYS'
    }
]

def _say(text: str) -> None:

    response = client.audio.speech.create(
        model="tts-1-hd",
        voice="nova",
        input=text,
    )  
    
    fileName = 'temp/' + str(random.randint(10000, 99999)) + '.mp3'
    response.write_to_file(fileName)

    playsound(fileName, True)


def answer(audio: AudioData = None, text: str = None) -> None:

    if audio:
        with open("talk.wav", "wb") as file:
            file.write(audio.get_wav_data())
        audioFile= open("talk.wav", "rb")
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audioFile
        )
        userSaid = transcription.text
    else:
        userSaid = text

    messageHistory.append({'role': 'user', 'content': userSaid})
    print('User said:', userSaid)
    
    clear_temp_dir()

    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messageHistory
    )

    messageHistory.append({'role': 'assistant', 'content': completion.choices[0].message.content})
    print('Assistant said:', completion.choices[0].message.content)
    
    try:
        data = completion.choices[0].message.content.split('[RUN THIS CODE]')
        print(f'!!!CODE GIVEN!!!\n{data[1]}')
    except IndexError:
        print('saying correctly')
        print(data)
        _say(completion.choices[0].message.content)
    else:
        print('Index error', data)
        if data[0] != '':
            _say(data[0])
        fileName = 'ai_code/' + str(random.randint(10000, 99999)) + '.py'
        with open(fileName, 'w') as f:
            f.write(data[1])
        with open(f"{fileName}.out.txt", "w+") as output:
            subprocess.call(["python", f"./{fileName}"], stdout=output, stderr=output)
        print('SENDING OUTPUT', f"{fileName}.out.txt")
        with open(f"{fileName}.out.txt", "r") as f:
            outputData = f.read()
            print('SENDING REPEAT:', f'Output from the program you run: {outputData}')
        answer(text='Output from the program you run: ' + outputData)
