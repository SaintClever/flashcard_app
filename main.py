from tkinter import *
import pandas as pd
from random import choice


BACKGROUND_COLOR = "#B1DDC6"
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
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_img, image=card_back_img)
    canvas.itemconfig(card_title, text='English', fill='#ffffff')
    canvas.itemconfig(card_word, text=current_word['English'], fill='#ffffff')


def is_known():
    df_to_dict.remove(current_word)
    # print(len(df_to_dict))
    data = pd.DataFrame(df_to_dict)
    data.to_csv('data/words_to_learn.csv', index=False)
    random_word()


# Window
window = Tk()
window.title('Flashy: flashcards')
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)
window.resizable(False, False)
flip_timer = window.after(3000, func=flip_card)

# Card
canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file='images/card_front.png')
card_back_img = PhotoImage(file='images/card_back.png')
card_img = canvas.create_image(400, 263, image=card_front_img) # NOTE: name is 'card_background'
card_title = canvas.create_text(400, 150, text='title', font=('Arial', 40, 'italic'))
card_word = canvas.create_text(400, 263, text='word', font=('Arial', 60, 'bold'))
canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)


# Buttons
btn_crossed_img = PhotoImage(file='images/wrong.png')
btn_wrong = Button(image=btn_crossed_img, highlightthickness=0, command=random_word)
btn_wrong.grid(column=0, row=1)

btn_right_img = PhotoImage(file='images/right.png')
btn_right = Button(image=btn_right_img, highlightthickness=0, command=is_known)
btn_right.grid(column=1, row=1)



random_word()



window.mainloop()