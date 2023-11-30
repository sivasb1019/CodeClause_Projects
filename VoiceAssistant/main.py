import os
import speech_recognition as sr
import pyttsx3 as pyt
import subprocess
import datetime
import randfacts
import wikipedia
import webbrowser
import pyjokes
import pywhatkit
import warnings


def listenCommand():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening for commands...")
        recognizer.pause_threshold = 1
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print("You:", command)
        return command.lower()
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return   None


def speakCommand(command):
    print("Sara:", command)
    engine.say(command)
    engine.runAndWait()


def greetings():
    now = datetime.datetime.now()
    hour = int(now.strftime("%H"))
    if hour >= 4 and hour < 12:
        return "Good Morning"
    elif hour  >= 12 and hour < 16:
        return "Good Afternoon"
    elif hour >= 16 and hour < 18:
        return "Good Evening"
    else:
        return "Good Night"


def note(notes):
    date = datetime.date.today()
    print(date)
    global file_no
    filename = f"{str(date)}-note{str(file_no)}.txt"
    file_no += 1
    with open(filename, "w") as f:
        f.write(notes)
    subprocess.Popen(["notepad.exe", filename])


def openApp(command):
    if "chrome" in command:
        speakCommand("Opening Google Chrome")
        os.startfile("C:/Program Files/Google/Chrome/Application/chrome.exe")
    elif "edge" in command:
        speakCommand("Opening Microsoft Edge")
        os.startfile("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe")
    elif "word" in command:
        speakCommand("Opening Microsoft Word")
        os.startfile("C:Program Files/Microsoft Office/root/Office16/WINWORD.EXE")
    elif "excel" in command:
        speakCommand("Opening Microsoft Excel")
        os.startfile("C:/Program Files/Microsoft Office/root/Office16/EXCEL.EXE")
    elif "powerpoint" in command:
        speakCommand("Opening Microsoft Power Point")
        os.startfile("C:/Program Files/Microsoft Office/root/Office16/POWERPNT.EXE")
    elif "eclipse" in command:
        speakCommand("Opening Eclipse")
        os.startfile("C:/Users/sivab/eclipse/java-2022-12/eclipse")
    elif "youtube" in command:
        speakCommand("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "github" in command:
        speakCommand("Opening Git hub")
        webbrowser.open("https://github.com/sivasb1019")
    elif "linkedin" in command:
        speakCommand("Opening Linked In")
        webbrowser.open("https://www.linkedin.com/in/sivabalanv10")
    else:
        speakCommand("Application not available")


def stopPlaying():
    while True:
        command = listenCommand()
        if command == None:
            continue
        elif "exit" in command or "quit" in command or "close" in command:
            speakCommand("Closing YouTube")
            os.system("taskkill /f /im msedge.exe")
            break


def main():
    while True:
        command = listenCommand()
        if command and "sara" in command:
            speakCommand(f"{greetings()} Sir, How can I help you?")
            while True:
                command = listenCommand()
                if command != None:
                    if "who are you" in command or "define yourself" in command:
                        speakCommand("Hello! I'm Sara, your helpful assistant here to assist you with anything you need.")

                    elif "who am i" in command or "who i am" in command:
                        speakCommand("Sorry, I can't identify individuals. It seems like you're a human! "
                                     "But I'm here to help you with anything you need!")

                    elif "your name" in command:
                        speakCommand("My name is Sara")

                    elif "why do you exist" in command or "why did you come to this word" in command:
                        speakCommand("It's a secret")

                    elif "made you" in command or "created you" in command:
                        speakCommand("I was created by Siva Bawlan")

                    elif "how are you" in command or "how r u"in command:
                        speakCommand("I'm doing well, thank you! How about you?")
                        command = listenCommand()
                        if "am fine" in command or "am good" in command or "doing good" in command:
                            speakCommand("Glad to hear that! Anything on your mind today?")
                        else:
                            speakCommand("I'm sorry to hear that. I'm here to help lift your spirits.")
                            speakCommand("I know some jokes! Would you like to hear one?")
                            if 'yes' in listenCommand():
                                speakCommand(pyjokes.get_joke())
                            else:
                                speakCommand("How can I bring some cheer into your day?")

                    elif any(phrase in command for phrase in NOTE_PHRASE):
                        notes = None
                        speakCommand("what would you like me to note down?")
                        while True:
                            notes = listenCommand()
                            if notes != None:
                                note(notes)
                                speakCommand("I've made a note of that successfully.")
                                break
                            else:
                                speakCommand("Please dictate a note for me to write down, so I can take a note for you.")
                                continue

                    elif "day" in command or "date" in command or "month" in command:
                        now = datetime.datetime.now()
                        speakCommand(f"Today is {now.strftime('%A')}, {now.strftime('%B')} "
                                f"{now.strftime('%d')}, {now.strftime('%Y')}.")

                    elif "time" in command:
                        now = datetime.datetime.now()
                        speakCommand(f"It's {int(now.strftime('%I'))} {now.strftime('%M')} "
                                f"{now.strftime('%p')}.")

                    elif "fact" in command or "facts" in command:
                        speakCommand("Here is a fact for you Sir.")
                        fact = randfacts.get_fact()
                        speakCommand("Did you know, " + fact)

                    elif any(phrase in command for phrase in WIKI_PHRASE):
                        wiki_list  = command.split()
                        query = wiki_list[-2] + " " + wiki_list[-1]
                        speakCommand(f"Searching for {query}")
                        try:
                            result = wikipedia.summary(query, sentences=2)
                            speakCommand(result)
                        except wikipedia.exceptions.PageError:
                            speakCommand("Sorry, I couldn't find any information about that.")

                    elif "open" in command:
                        openApp(command)

                    elif "search" in command and "youtube" in command or "google" in command:
                        query = command
                        for phrase in SEARCH_PHRASE:
                            if phrase in query:
                                query = query.replace(phrase, "")
                        if "in youtube" in command:
                            speakCommand(f"Searching for {query} in Youtube")
                            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
                        elif "in google" in command:
                            speakCommand(f"Searching for {query} in Google")
                            webbrowser.open(f"https://www.google.com/search?q={query}")

                    elif "joke" in command or "jokes" in command:
                        speakCommand(pyjokes.get_joke())
                        speakCommand("Thats funny right?")
                        speakCommand("Why aren't you laughing at my joke Sir? You're so mean.")

                    elif "play" in command:
                        if "song" in command or "songs" in command:
                            speakCommand("Which song would you like me to play?")
                        elif "video" in command or "videos" in command:
                            speakCommand("Which video would you like me to play?")
                        else:
                            command = command.replace("play", "")
                            pywhatkit.playonyt(command)
                            exitApp("YouTube")
                            continue
                        query = listenCommand()
                        if 'play' in query or 'any' in query:
                            pywhatkit.playonyt("Nippon Egao Hyakkei")
                        else:
                            pywhatkit.playonyt(query)
                        stopPlaying()


                    elif "bye" in command or "exit" in command or "quit" in command:
                        speakCommand("Goodbye Sir, Have a nice day.")
                        exit()

                    else:
                        speakCommand("Apologies, I'm afraid I don't have information on that. My knowledge is somewhat limited.")

                else:
                    speakCommand("Please say something. So that I can assist you")



if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    engine = pyt.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.setProperty("rate", 150)
    NOTE_PHRASE = ["make a note", "write a note","write this down",
                   "save this", "remember this"]
    WIKI_PHRASE = ["tell me about", "who is", "who are","brief", "wikipedia"]
    SEARCH_PHRASE = ["sara", "search","for", " in google", "in youtube"]
    file_no = 1
    main()
