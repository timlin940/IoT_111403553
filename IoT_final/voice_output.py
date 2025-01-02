from gtts import gTTS
import os

def play_tts(text):
    tts = gTTS(text=text, lang='zh-TW')
    tts.save("alert.mp3")
    os.system("mpg321 alert.mp3")
    os.remove("alert.mp3")
