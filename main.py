import datetime
import pyttsx3
import speech_recognition as sr
import webbrowser
import requests
from dotenv import load_dotenv
import os
import openai

# Load environment variables from .env file
load_dotenv()

# Access the API keys from the environment variables
API_KEY = os.getenv("api_key")
def say(text):
    """Convert text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    """Recognizes voice input using the microphone."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')  # Convert speech to text
            print(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand. Please speak again.")
            return None
        except sr.RequestError:
            print("Could not request results. Check your internet connection.")
            return None

def ask_openrouter(query):
    """Get responses from OpenRouter API using DeepSeek model."""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}", 
    }
    data = {
        "model": "deepseek/deepseek-r1:free",  # Use the DeepSeek model
        "messages": [{"role": "user", "content": query}],
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()
        answer = response_data["choices"][0]["message"]["content"]
        return answer
    except requests.exceptions.RequestException as e:
        return "Sorry, I couldn't fetch a response from OpenRouter."


if __name__ == '__main__':
    say("Hello, I am Jarvis AI. How can I assist you?")

    # Dictionary of sites
    sites = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "wikipedia": "https://www.wikipedia.org",
        "github": "https://www.github.com",
        "stackoverflow": "https://stackoverflow.com"
    }

    while True:
        query = takeCommand()

        if query:
            # Check if the query is to stop the assistant
            if "stop" in query or "exit" in query:
                say("Goodbye! Have a great day.")
                break  # Exit the loop
            
            # Open websites based on the query
            for site in sites:
                if f"open {site}" in query:
                    say(f"Opening {site} for you...")
                    webbrowser.open(sites[site])
                    break  # Avoid unnecessary looping
            
            # Play music
            if "play music" in query:
                music_link = "https://www.youtube.com/watch?v=yIzCBU0_LyY"
                say("Playing music...")
                webbrowser.open(music_link)

            # Get current time
            if "the time" in query:
                strtime = datetime.datetime.now().strftime("%H:%M:%S")
                say(f"Sir, the time is {strtime}")

            # Ask OpenRouter (DeepSeek)
            if "open ai" in query or "deepseek" in query:
                say("Let me find the answer for you using OpenRouter...")
                openrouter_response = ask_openrouter(query)
                print(f"OpenRouter (DeepSeek): {openrouter_response}")
                say(openrouter_response)

            
