import speech_recognition as sr
from gradio_client import Client
import pyttsx3
from pydub import AudioSegment
from pydub.playback import play
import requests

client = Client("https://facebook-seamless-m4t-v2-large.hf.space/--replicas/6w5sk/")

def get_voice_input():
 recognizer = sr.Recognizer()
 with sr.Microphone() as source:
     print("Speak Anything :")
     audio = recognizer.listen(source)
     with open("audio_sample.wav", "wb") as file:
         file.write(audio.get_wav_data())
     try:
         result = client.predict(
             "audio_sample.wav", # filepath in 'Input speech' Audio component
            #  "Bengali", # Source language
             "English", # Target language
            #  api_name="/s2tt"
            api_name="/asr"
         )
        #  print(type(result))
         print(result)
         return result
     except Exception as e:
         print(f"Error with the speech recognition service; {e}")
         return ""

def play_audio(file_path):
  audio = AudioSegment.from_file(file_path)
  play(audio)

def chat_with_rasa(message):
   print("Sending message to Rasa...")

   response = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"message": message})

   print("Bot says:")
   for resp in response.json():
       try:
           bot_message = resp['text']
           print(bot_message)
           # use m4t to speak
           result = client.predict(
               bot_message, # filepath in 'Input speech' Audio component
               "English", # Source language
               "Hindi", # Target language
               api_name="/t2st"
           )
           print(result)
           print(type(result))
        #  result is   
           play_audio(result[0])

       except KeyError:
           print("Error: 'text' key not found in the bot's response.")

if __name__ == "__main__":
   while True:
       message = get_voice_input()
       if message:
           chat_with_rasa(message)
