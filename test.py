from gtts import gTTS
from playsound import playsound


tts = gTTS(text='hello', lang='en') # zh-cn
tts.save('data/hello.mp3')
playsound('data/hello.mp3')