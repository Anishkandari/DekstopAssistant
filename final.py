import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import requests
import pywhatkit as kit
import random
import platform
import time


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

recognizer = sr.Recognizer()
def speak(audio):
    print(f"Assistant: {audio}")
    engine.say(audio)
    engine.runAndWait()
    time.sleep(0.5)  # Delay


def wish_user():
    """Wish user based on time of day"""
    hour = datetime.datetime.now().hour
    
    if 0 <= hour < 12:
        greeting = "Good Morning! I am here to assist you. How can I help you today?"
    elif 12 <= hour < 18:
        greeting = "Good Afternoon! I am here to assist you. How can I help you today?"
    else:
        greeting = "Good Evening! I am here to assist you. How can I help you today?"
    
    speak(greeting)


def take_command():
    """take commands"""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        recognizer.energy_threshold = 300
        
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-in')
            print(f"You said: {query}\n")
            return query.lower()
        
        except sr.WaitTimeoutError:
            print("No speech detected")
            return "none"
        except sr.UnknownValueError:
            print("Could not understand audio")
            return "none"
        except sr.RequestError:
            speak("Sorry, speech service is unavailable")
            return "none"
        except Exception as e:
            print(f"Error: {e}")
            return "none"


def get_time():
    """Tell current time"""
    time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {time}")


def get_date():
    """Tell current date"""
    date = datetime.datetime.now().strftime("%B %d, %Y")
    day = datetime.datetime.now().strftime("%A")
    speak(f"Today is {day}, {date}")


def search_wikipedia(query):
    """Search Wikipedia and read summary"""
    try:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
    except wikipedia.exceptions.DisambiguationError:
        speak("There are multiple results. Please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("Sorry, I couldn't find any results on Wikipedia.")
    except Exception as e:
        speak("Sorry, I encountered an error while searching Wikipedia.")


def open_website(site):
    """Open popular websites"""
    websites = {
        'google': 'https://www.google.com',
        'youtube': 'https://www.youtube.com',
        'wikipedia': 'https://www.wikipedia.org',
        'github': 'https://www.github.com',
        'stackoverflow': 'https://stackoverflow.com',
        'gmail': 'https://mail.google.com',
        'facebook': 'https://www.facebook.com',
        'twitter': 'https://www.twitter.com',
        'instagram': 'https://www.instagram.com',
        'linkedin': 'https://www.linkedin.com'
    }
    
    for key, url in websites.items():
        if key in site:
            speak(f"Opening {key}")
            webbrowser.open(url)
            return True
    return False


def play_music_youtube(song):
    """Play song on YouTube"""
    try:
        speak(f"Playing {song} on YouTube")
        kit.playonyt(song)
    except Exception as e:
        speak("Sorry, I couldn't play the song.")


def tell_joke():
    """Tell a random joke"""
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        if response.status_code == 200:
            joke_data = response.json()
            setup = joke_data['setup']
            punchline = joke_data['punchline']
            speak(setup)
            speak(punchline)
        else:
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the scarecrow win an award? Because he was outstanding in his field!",
                "Why don't eggs tell jokes? They'd crack each other up!",
                "What do you call a bear with no teeth? A gummy bear!"
            ]
            speak(random.choice(jokes))
    except:
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!"
        ]
        speak(random.choice(jokes))


def get_news():
    """news headlines"""
    try:
        speak("Fetching latest news headlines")
        response = requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey=DEMO_KEY")
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])[:5]
            
            if articles:
                speak("Here are the top headlines")
                for i, article in enumerate(articles, 1):
                    speak(f"Headline {i}: {article['title']}")
            else:
                speak("No news articles found")
        else:
            speak("Unable to fetch news at the moment. Please check your internet connection.")
    except Exception as e:
        speak("Sorry, I couldn't fetch the news right now.")


def get_weather(city="London"):
    """Get weather information"""
    try:
        speak(f"Fetching weather information for {city}")
        response = requests.get(f"https://wttr.in/{city}?format=j1")
        
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            temp = current['temp_C']
            desc = current['weatherDesc'][0]['value']
            humidity = current['humidity']
            
            speak(f"The temperature in {city} is {temp} degrees Celsius")
            speak(f"Weather condition: {desc}")
            speak(f"Humidity is {humidity} percent")
        else:
            speak("Unable to fetch weather information")
    except Exception as e:
        speak("Sorry, I couldn't get the weather information.")


def calculate(expression):
    """Perform calculations"""
    try:
        expression = expression.replace("calculate", "").replace("what is", "").strip()
        result = eval(expression)
        speak(f"The answer is {result}")
    except:
        speak("Sorry, I couldn't calculate that.")


def system_info():
    """Get basic system information"""
    speak("Getting system information")
    speak(f"System: {platform.system()}")
    speak(f"Version: {platform.release()}")
    speak(f"Machine: {platform.machine()}")


def show_help():
    """Display available commands"""
    speak("I can help you with many things like:")
    speak("Tell you the time and date")
    speak("Search Wikipedia")
    speak("Open websites like Google, YouTube, Wikipedia")
    speak("Play songs on YouTube")
    speak("Tell jokes")
    speak("Get news and weather")
    speak("Perform calculations")
    speak("And much more! Just ask me.")


def main():
    """Main function to run the assistant"""
    wish_user()
    
    while True:
        query = take_command()
        
        if query == "none":
            continue
        
        # Exit commands
        if 'exit' in query or 'quit' in query or 'bye' in query or 'goodbye' in query:
            speak("Goodbye! Have a great day!")
            break
        
        # Time and Date
        elif 'time' in query:
            get_time()
        
        elif 'date' in query:
            get_date()
        
        # Wikipedia
        elif 'wikipedia' in query:
            search_wikipedia(query)
        
        # Open websites
        elif 'open' in query:
            if not open_website(query):
                speak("Sorry, I don't know that website")
        
        # Play music
        elif 'play' in query and ('song' in query or 'music' in query or 'youtube' in query):
            song = query.replace('play', '').replace('song', '').replace('music', '').replace('on youtube', '').strip()
            if song:
                play_music_youtube(song)
            else:
                speak("What song would you like to play?")
        
        # Jokes
        elif 'joke' in query:
            tell_joke()
        
        # News
        elif 'news' in query:
            get_news()
        
        # Weather
        elif 'weather' in query:
            if 'in' in query:
                city = query.split('in')[-1].strip()
                get_weather(city)
            else:
                speak("Which city's weather would you like to know?")
                city_query = take_command()
                if city_query != "none":
                    get_weather(city_query)
        
        # Calculate
        elif 'calculate' in query or ('what is' in query and any(op in query for op in ['+', '-', '*', '/', 'plus', 'minus', 'multiply', 'divide'])):
            calculate(query)
        
        # System info
        elif 'system info' in query or 'system information' in query:
            system_info()
        
        # Google search
        elif 'search' in query or 'google' in query:
            search_term = query.replace('search', '').replace('google', '').replace('for', '').strip()
            if search_term:
                speak(f"Searching Google for {search_term}")
                webbrowser.open(f"https://www.google.com/search?q={search_term}")
        
        # Help
        elif 'help' in query or 'what can you do' in query:
            show_help()
        
        else:
            speak("I'm not sure how to help with that. You can say 'help' to know what I can do.")


if __name__ == "__main__":
    print("=" * 50)
    print("PERSONAL DESKTOP VOICE ASSISTANT")
    print("=" * 50)
    print("\nInitializing assistant...")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\nAssistant stopped by user")
        speak("Goodbye!")
    except Exception as e:
        print(f"\nError occurred: {e}")
        speak("An error occurred. Shutting down.")