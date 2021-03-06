from tkinter import *
from tkinter import messagebox
import pandas as pd
from random import choice
from gtts import gTTS
from playsound import playsound
from pygame import mixer
from glob import glob
import os



# ------------------------ variables ------------------------
# unused colors: '#1c242b', '#32373c', '#3c4146'
BACKGROUND_COLOR = '#ffffff'
FLIP_TIME = 5000
AUDIO_PLAYBACK_SPEED = 250
FONT = 'Century Gothic'

# NOTE: Tkinter has compile problems with the path so it must be an absolute path
AUDIO_PATH = '/Users/anonymous/Desktop/python_projects/multi_language_flashcard_app/audio/'
DATA_PATH = '/Users/anonymous/Desktop/python_projects/multi_language_flashcard_app/data/'
IMAGE_PATH = '/Users/anonymous/Desktop/python_projects/multi_language_flashcard_app/images/'
LANGUAGES_TO_STUDY_PATH = '/Users/anonymous/Desktop/python_projects/multi_language_flashcard_app/languages_to_study/'


# Window
window = Tk()
window.title('Multi-lang Flashcards')
window.config(padx=0, pady=0, background=BACKGROUND_COLOR)
window.resizable(False, False)



# languages
lang_abbrev = {
    'Danish':'da',
    'French':'fr',
    'German':'de',
    'Japanese':'ja',
    'Kazakh':'kk',
    'Korean':'ko',
    'Mandarin':'zh-cn',
    'Romanian':'ro',
    'Russian':'ru',
    'Spanish':'es',
    'Tagalog':'tl',
    'Thai':'th',
    'Vietnamese':'vi'
}

languages = list(lang_abbrev.keys())



# ------------------------- option menu -------------------------
options = StringVar(window)
options.set(choice(languages))
menu = OptionMenu(window, options, *languages)
menu.config(width=53)
menu.grid(column=0, row=2, columnspan=3, pady=(0, 20))

current_word = {}
dictionary_words = {}



# ---------------------- audio ----------------------
def play_audio():
    # language = options.get()
    language = list(current_word.keys())[0]

    try:
        read_word = current_word[language].split()[0] # read the first chinese word, no pinyin
        # tts = gTTS(text=read_word, lang=lang_abbrev[language])
        # tts.save(f'{AUDIO_PATH}{language}.mp3')
        # playsound(f'{AUDIO_PATH}{language}.mp3')

        # or with pygame.mixer

        tts = gTTS(text=read_word, lang=lang_abbrev[language])
        tts.save(f'{AUDIO_PATH}{language}.mp3')
        mixer.init()
        mixer.music.load(f'{AUDIO_PATH}{language}.mp3')
        mixer.music.play(loops=0)
        os.remove(f'{AUDIO_PATH}{language}.mp3')
    except ValueError:
        pass



# ---------------------- memorized btn ---------------------- 
def memorized_btn(*args):
    global current_word

    language = options.get()

    csv_words = pd.read_csv(f'{DATA_PATH}{language}.csv')
    dictionary_words = csv_words.to_dict(orient='records')

    current_word = choice(dictionary_words)
    canvas.itemconfig(card_img, image=card_front_img)
    canvas.itemconfig(card_title, text=language, fill='#000000')
    canvas.itemconfig(card_word, text=current_word[language], fill='#000000')

    audio_icon_btn = Button(image=audio_icon_front, highlightthickness=0, command=play_audio)
    audio_icon = canvas.create_window(565, 420, window=audio_icon_btn)

    window.after(AUDIO_PLAYBACK_SPEED, func=play_audio) 

options.trace('w', memorized_btn)



# ---------------------- forgotten btn ----------------------
def forgotten_btn(*args):
    # language = options.get()

    try:
        language = list(current_word.keys())[0]
    except IndexError:
        language = options.get()
        

    data = pd.DataFrame([current_word])
    data.to_csv(f'{LANGUAGES_TO_STUDY_PATH}{language}_to_study.csv', mode='a', header=False, index=False)

    canvas.itemconfig(card_img, image=card_back_img)
    
    try:
        canvas.itemconfig(card_title, text='English', fill='#ffffff')
        canvas.itemconfig(card_word, text=current_word['English'], fill='#ffffff')
        
        audio_icon_btn = Button(image=audio_icon_back, highlightthickness=0, command=play_audio)
        audio_icon = canvas.create_window(565, 420, window=audio_icon_btn)
    except KeyError:
        canvas.itemconfig(card_title, text='Please select', fill='#ffffff')
        canvas.itemconfig(card_word, text='a language', fill='#ffffff')

    # window.after(FLIP_TIME, func=memorized_btn) # auto-flip to new random card

options.trace('w', forgotten_btn)



# ---------------------------- save_files ----------------------------
def save_files():
    for csv_file in glob(f'{LANGUAGES_TO_STUDY_PATH}*.csv'):

        file_name = csv_file.replace(f'{LANGUAGES_TO_STUDY_PATH}', '').replace('_to_study.csv', '')
        csv_data = pd.read_csv(csv_file, names=[file_name, 'English']) # provide header
        # print(csv_data.size)

        csv_data_clearn = csv_data.drop_duplicates()
        data = pd.DataFrame(csv_data_clearn)

        # print(data.empty)
        if data.empty: # if file is empty delete it else create the csv
            os.remove(f'{LANGUAGES_TO_STUDY_PATH}{file_name}_to_study.csv')
        else:
            data.to_csv(f'{LANGUAGES_TO_STUDY_PATH}{file_name}_to_study.csv', index=False) # test_folder_path/{file_name}_to_study.csv



# ---------------------------- save_and_quit ----------------------------
def save_and_quit():
    # if messagebox.askokcancel('quit', 'Save and quit your progress.'):
    save_files()
    window.destroy()
window.protocol('WM_DELETE_WINDOW', save_and_quit)



# ------------------------------ cards ------------------------------
canvas = Canvas(width=600, height=480)
flags = PhotoImage(file=f'{IMAGE_PATH}flags.png')
card_front_img = PhotoImage(file=f'{IMAGE_PATH}card_front.png')
card_back_img = PhotoImage(file=f'{IMAGE_PATH}card_back.png')

flag_banner = canvas.create_image(300, 0, image=flags)
card_img = canvas.create_image(300, 265, image=card_front_img)
card_title = canvas.create_text(300, 165, text='Select', font=(FONT, 35, 'italic'), justify='center')
card_word = canvas.create_text(300, 265, text='Language', font=(FONT, 45, 'normal'), justify='center')

audio_icon_front = PhotoImage(file=f'{IMAGE_PATH}audio_icon_front.png')
audio_icon_back = PhotoImage(file=f'{IMAGE_PATH}audio_icon_back.png')

canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=1, columnspan=3)



# ------------------------------ btns ------------------------------
btn_forgot_img = PhotoImage(file=f'{IMAGE_PATH}forgot_btn.png')
btn_forgot = Button(image=btn_forgot_img, highlightthickness=0, command=forgotten_btn)
btn_forgot.grid(column=0, row=3, pady=(0, 20))

save_quit_img = PhotoImage(file=f'{IMAGE_PATH}save_quit_btn.png')
save_quit = Button(image=save_quit_img, highlightthickness=0, command=save_and_quit)
save_quit.grid(column=1, row=3, pady=(0, 20))

btn_memorize_img = PhotoImage(file=f'{IMAGE_PATH}memorize_btn.png')
btn_memorize = Button(image=btn_memorize_img, highlightthickness=0, command=memorized_btn)
btn_memorize.grid(column=2, row=3, pady=(0, 20))



window.mainloop()