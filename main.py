from tkinter import *
import pandas as pd
from random import choice
from gtts import gTTS
from tempfile import TemporaryFile
from playsound import playsound
import pygame


# ------------------------ variables ------------------------
# unused colors: '#1c242b', '#32373c', '#3c4146'
BACKGROUND_COLOR = '#ffffff'
FLIP_TIME = 5000
AUDIO_PLAYBACK_SPEED = 250
FONT = 'Century Gothic'



# Window
window = Tk()
window.title('flashy flashcards')
window.config(padx=0, pady=0, background=BACKGROUND_COLOR)
window.resizable(False, False)



# languages
lang_abbrev = {
    # 'Danish':'da',
    'French':'fr',
    # 'German':'de',
    # 'Japanese':'ja',
    # 'Kazakh':'kk',
    'Mandarin':'zh-cn',
    # 'Russian':'ru',
    # 'Spanish':'es',
    # 'Tagalog':'tl',
    # 'Thai':'th'
}

languages = list(lang_abbrev.keys())



# ------------------------- option menu -------------------------
options = StringVar(window)
options.set(choice(languages))
menu = OptionMenu(window, options, *languages)
menu.config(width=53)
menu.grid(column=0, row=2, columnspan=2, pady=(0, 20))

current_word = {}
dictionary_words = {}



# ---------------------- audio ----------------------
def play_sound():
    language = options.get()
    read_word = current_word[language].split()[0] # read the first chinese word, no pinyin

    tts = gTTS(text=read_word, lang=lang_abbrev[language])
    tts.save(f'audio/{language}.mp3')
    playsound(f'audio/{language}.mp3')

    # or with pygame.mixer

    # tts = gTTS(text=read_word, lang=lang_abbrev[language])
    # tts.save(f'audio/{language}.mp3')
    # pygame.mixer.init()
    # pygame.mixer.music.load(f'audio/{language}.mp3')
    # pygame.mixer.music.play(loops=0)



# ---------------------- memorized btn ---------------------- 
def memorized_btn(*args):
    global current_word

    language = options.get()
    csv_words = pd.read_csv(f'data/{language}.csv')
    dictionary_words = csv_words.to_dict(orient='records')

    current_word = choice(dictionary_words)
    canvas.itemconfig(card_img, image=card_front_img)
    canvas.itemconfig(card_title, text=language, fill='#000000')
    canvas.itemconfig(card_word, text=current_word[language], fill='#000000')

    window.after(AUDIO_PLAYBACK_SPEED, func=play_sound) 

options.trace('w', memorized_btn)



# ---------------------- forgotten btn ----------------------
def forgotten_btn(*args):
    language = options.get()

    data = pd.DataFrame([current_word])
    data.to_csv(f'data/{language}_to_learn.csv', mode='a', header=False, index=False)
    canvas.itemconfig(card_img, image=card_back_img)
    
    try:
        canvas.itemconfig(card_title, text='English', fill='#ffffff')
        canvas.itemconfig(card_word, text=current_word['English'], fill='#ffffff')
    except KeyError:
        canvas.itemconfig(card_title, text='Please select', fill='#ffffff')
        canvas.itemconfig(card_word, text='a language', fill='#ffffff')
    
    window.after(FLIP_TIME, func=memorized_btn) # auto-flip to new random card

options.trace('w', forgotten_btn)



# ------------------------------ cards ------------------------------
canvas = Canvas(width=600, height=480)
flags = PhotoImage(file='images/flags.png')
card_front_img = PhotoImage(file='images/card_front.png')
card_back_img = PhotoImage(file='images/card_back.png')
flag_banner = canvas.create_image(300, 0, image=flags)
card_img = canvas.create_image(300, 265, image=card_front_img)
card_title = canvas.create_text(300, 165, text='Select', font=(FONT, 35, 'italic'), justify='center')
card_word = canvas.create_text(300, 265, text='Language', font=(FONT, 45, 'normal'), justify='center')
canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=1, columnspan=2)



# ------------------------------ btns ------------------------------
btn_crossed_img = PhotoImage(file='images/wrong.png')
btn_wrong = Button(image=btn_crossed_img, highlightthickness=0, command=forgotten_btn)
btn_wrong.grid(column=0, row=3, pady=(0, 20))


btn_right_img = PhotoImage(file='images/right.png')
btn_right = Button(image=btn_right_img, highlightthickness=0, command=memorized_btn)
btn_right.grid(column=1, row=3, pady=(0, 20))



window.mainloop()