import speech_recognition as sr
import pyttsx3
import requests

def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak Anything :")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print("You said :", text)
            return text
        except sr.UnknownValueError:
            print("Sorry could not recognize your voice")
            return ""
        except sr.RequestError as e:
            print(f"Error with the speech recognition service; {e}")
            return ""

def chat_with_rasa(message):
    print("Sending message to Rasa...")

    response = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"message": message})

    print("Bot says:")
    for resp in response.json():
        try:
            bot_message = resp['text']
            print(bot_message)
            engine = pyttsx3.init()
            engine.say(bot_message)
            engine.runAndWait()
        except KeyError:
            print("Error: 'text' key not found in the bot's response.")

if __name__ == "__main__":
    while True:
        message = get_voice_input()
        if message:
            chat_with_rasa(message)
