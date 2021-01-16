from tkinter import *
import pandas as pd
from random import randint

BACKGROUND_COLOR = "#B1DDC6"


df = pd.read_csv('data/mandarin_concatenated.csv')
df_to_dict = df.to_dict(orient='records')
# print(df_to_dict[0]['Mandarin'])


# random mandarin word
def random_mandarin_word():
    mandarin_word = df_to_dict[randint(0, 5000)]['Mandarin']
    canvas.delete('word')
    canvas.create_text(400, 263, text=mandarin_word, font=('Arial', 60, 'bold'), tag='word')


# Window
window = Tk()
window.title('Flashy: flashcards')
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)
window.resizable(False, False)


# Card
canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file='images/card_front.png')
canvas.create_image(400, 263, image=card_front_img)
canvas.create_text(400, 150, text='Mandarin', font=('Arial', 40, 'italic'))
canvas.create_text(400, 263, text='word', font=('Arial', 60, 'bold'), tag='word')
canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)


# Buttons
btn_crossed_img = PhotoImage(file='images/wrong.png')
btn_wrong = Button(image=btn_crossed_img, highlightthickness=0, command=random_mandarin_word)
btn_wrong.grid(column=0, row=1)

btn_right_img = PhotoImage(file='images/right.png')
btn_right = Button(image=btn_right_img, highlightthickness=0, command=random_mandarin_word)
btn_right.grid(column=1, row=1)



window.mainloop()