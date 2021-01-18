from tkinter import *
import pandas as pd
from random import choice


# unused colors: '#1c242b', '#32373c', '#3c4146'
BACKGROUND_COLOR = '#ffffff'
FLIP_TIME = 5000


current_word = {}
df_to_dict = {}


try:
    df = pd.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    original_df = pd.read_csv('data/mandarin_concatenated.csv')
    df_to_dict = original_df.to_dict(orient='records')
else:
    df_to_dict = df.to_dict(orient='records')


# random mandarin word
def random_word():
    global current_word, flip_timer
    window.after_cancel(flip_timer)

    current_word = choice(df_to_dict)
    canvas.itemconfig(card_img, image=card_front_img)
    canvas.itemconfig(card_title, text='Mandarin', fill='#000000')
    canvas.itemconfig(card_word, text=current_word['Mandarin'], fill='#000000')
    flip_timer = window.after(FLIP_TIME, func=flip_card)


def flip_card():
    canvas.itemconfig(card_img, image=card_back_img)
    canvas.itemconfig(card_title, text='English', fill='#ffffff')
    canvas.itemconfig(card_word, text=current_word['English'], fill='#ffffff')


def is_known():
    df_to_dict.remove(current_word)
    data = pd.DataFrame(df_to_dict)
    data.to_csv('data/words_to_learn.csv', index=False)
    random_word()


# Window
window = Tk()
window.title('flashy flashcards')
window.config(padx=0, pady=0, background=BACKGROUND_COLOR)
window.resizable(False, False)
flip_timer = window.after(3000, func=flip_card)


# Card
canvas = Canvas(width=600, height=480)
flags = PhotoImage(file='images/flags.png')
card_front_img = PhotoImage(file='images/card_front.png')
card_back_img = PhotoImage(file='images/card_back.png')
flag_banner = canvas.create_image(300, 0, image=flags)
card_img = canvas.create_image(300, 265, image=card_front_img)
card_title = canvas.create_text(300, 165, text='title', font=('Century Gothic', 35, 'italic'), justify='center')
card_word = canvas.create_text(300, 265, text='word', font=('Century Gothic', 45, 'normal'), justify='center')
canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=1, columnspan=2)


# Buttons
btn_crossed_img = PhotoImage(file='images/wrong.png')
btn_wrong = Button(image=btn_crossed_img, highlightthickness=0, command=random_word)
btn_wrong.grid(column=0, row=2, pady=(0, 20))

btn_right_img = PhotoImage(file='images/right.png')
btn_right = Button(image=btn_right_img, highlightthickness=0, command=is_known)
btn_right.grid(column=1, row=2, pady=(0, 20))


# language
lang = Entry(foreground='#ffffff', background='#1c242b', width=55, justify='center')
lang.insert(END, 'Choose lang')
lang.grid(column=0, row=3, columnspan=2, pady=(0, 20))

random_word()
window.mainloop()