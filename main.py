from dotenv import load_dotenv
import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

load_dotenv()

recogniser = sr.Recognizer()
engine = pyttsx3.init()
newsApiKey = os.getenv('NEWSAPIKEY')

openaiapikey = os.getenv('OPENAIAPIKEY')

def speakOld(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the audio file
    audio_file = "temp.mp3"  # Replace with your actual file
    pygame.mixer.music.load(audio_file)

    # Play the audio
    pygame.mixer.music.play()

    # Keep the script running while the music plays
    while pygame.mixer.music.get_busy():
        # pygame.mixer.music.stop()
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()

    os.remove(audio_file)


def aiProcess(command):
    client = OpenAI(
        api_key=openaiapikey
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        # store=True,
        messages=[
            {"role": "system", "content": "You are a virtual assistant named siri skilled in general tasks like alexa and google cloud. Give short responses please"},
            {"role": "user", "content": command}
        ]
    )
    return completion.choices[0].message.content

def processCommand(command):
    """Process the spoken command."""
    command = command.lower()
    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    elif "open youtube" in command:
        speak("Opening Youtube")
        webbrowser.open("https://youtube.com")
    elif "play" in command.lower():
        song = command.lower().split()[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in command.lower():
        # integrate new api
        response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsApiKey}")
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            
            # Print the headlines
            for i, article in enumerate(articles, start=1):
                speak(article['title'])
        
    else:
        # speak("Sorry, I didn't understand that.")
        # let open ai handle request
        output = aiProcess(command)
        speak(output)
         

if __name__ == "__main__":
    speak("Hey Siri....")
    
    while True:
        recogniser = sr.Recognizer()
        
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")  
                recogniser.adjust_for_ambient_noise(source, duration=1)  # Reduce background noise
                audio = recogniser.listen(source, timeout=5, phrase_time_limit=3)

                word = recogniser.recognize_google(audio).lower() 
                print("Heard:", word)

                if word.lower() == "hey siri":
                    speak("Yeah")
                    print("Siri Active")

                    with sr.Microphone() as source:
                        print("Listening for command...")
                        recogniser.adjust_for_ambient_noise(source, duration=1)
                        audio = recogniser.listen(source, timeout=5, phrase_time_limit=5)

                        command = recogniser.recognize_google(audio)
                        print("Command:", command)
                        processCommand(command)

        except sr.UnknownValueError:
            print("Could not understand the audio")
        except sr.RequestError as e:
            print(f"Request error from Google Speech Recognition: {e}")
        except Exception as e:
            print(f"Error: {e}")
