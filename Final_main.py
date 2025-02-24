import speech_recognition as sr
import os
import webbrowser
import openai
import pyttsx3
import datetime
import subprocess
from config import apikey

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('voice', engine.getProperty('voices')[0].id)

chat_history = []  # Store chat history

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def chat(query):
    """Handles AI chat responses using OpenAI's new API."""
    global chat_history
    openai.api_key = apikey

    chat_history.append({"role": "user", "content": query})
    
    client = openai.OpenAI(api_key=apikey)
  # NEW CLIENT INSTANCE
    response = client.chat.completions.create(  # NEW API CALL
        model="gpt-4o mini",  # Use "gpt-4" if available
        messages=chat_history,
        temperature=0.7,
        max_tokens=256
    )
    
    reply = response.choices[0].message.content
    speak(reply)
    chat_history.append({"role": "assistant", "content": reply})
    return reply

def chat(query):
    """Handles AI chat responses using OpenAI's new API."""
    global chat_history
    openai.api_key = apikey

    chat_history.append({"role": "user", "content": query})
    
    client = openai.OpenAI(api_key=apikey)  # NEW CLIENT INSTANCE
    response = client.chat.completions.create(  # NEW API CALL
        model="gpt-3.5-turbo",  # Change this to a valid model
        messages=chat_history,
        temperature=0.7,
        max_tokens=256
    )
    
    reply = response.choices[0].message.content
    speak(reply)
    chat_history.append({"role": "assistant", "content": reply})
    return reply

    
    text = f"OpenAI response for Query: {query}\n*************************\n\n{reply}"
    
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    filename = f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt"
    with open(filename, "w") as f:
        f.write(text)

def takeCommand():
    """Takes voice command from the microphone."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception:
            return "Some Error Occurred. Sorry from Jarvis"

if __name__ == '__main__':
    print('Welcome to Jarvis AI')
    speak('Welcome')
    speak('I will be activating soon please wait for a while sir!')
    speak("Jarvis AI is Now Activated sir!")
    
    while True:
        query = takeCommand().lower()

        # Open websites
        sites = {
            "youtube": "https://www.youtube.com",
            "wikipedia": "https://www.wikipedia.org",
            "google": "https://www.google.com"
        }
        for site, url in sites.items():
            if f"open {site}" in query:
                speak(f"Opening {site} sir...")
                webbrowser.open(url)
                break

        # Open music
        if "open music" in query:
            musicPath = "C:\\Users\\Public\\Music\\Sample Music.mp3"  # Change to your music file path
            subprocess.Popen(["start", "", musicPath], shell=True)

        # Tell the time
        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            speak(f"Sir, the time is {hour} hours and {minute} minutes")

        # AI response
        elif "using artificial intelligence" in query:
            chat(query)

        # Exit the program
        elif "jarvis quit" in query:
            speak("Goodbye sir! have a nice day")
            exit()

        # Reset chat history
        elif "reset chat" in query:
            chat_history = []

        # AI chatbot response
        else:
            print("Chatting...")
            chat(query)
