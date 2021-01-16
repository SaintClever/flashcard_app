from tkinter import *

BACKGROUND_COLOR = "#B1DDC6"


# Window
window = Tk()
window.title('Flashy: flashcards')
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)
window.resizable(False, False)


# Card
canvas = Canvas(width=800, height=526, highlightthickness=0)
bg_img = PhotoImage(file='images/card_front.png')
canvas.create_image(400, 263, image=bg_img)
canvas.config(background=BACKGROUND_COLOR)
canvas.grid(column=0, row=0, columnspan=2)


# Copy



# Buttons
btn_wrong_img = PhotoImage(file='images/wrong.png')
btn_wrong = Button(image=btn_wrong_img, highlightthickness=0)
btn_wrong.grid(column=0, row=1)

btn_right_img = PhotoImage(file='images/right.png')
btn_right = Button(image=btn_right_img, highlightthickness=0)
btn_right.grid(column=1, row=1)



window.mainloop()