from cProfile import label
from cgitb import text
from tkinter import *

# def main_page():
#     page = Tk()
#     page.geometry("300x250")
#     page.title("Musicfy 2.0")
#     label(text = "Musify 2.0", bg = "grey", font = ("Calibri", 13)).pack()
#     label(text = "").pack()
#     Button(text = "Login").pack()
#     label(text = "").pack()
#     Button(text = "Sign Up").pack()

#     page.mainloop()

# main_page()

# # ==========================Display Text========================================================
# # Creating a label Widget
# label_1 = Label(root, text = "Hello World")
# label_2 = Label(root, text = "This is second label")

# # # Display on screen [On the middle]
# # label_1.pack()

# # Display with Grid ** 'grid' are relative to each other, to create distance, create a blank label as standard
# label_1.grid(row = 0, column = 0)
# label_2.grid(row = 1, column = 0)

# # # Another way to display with grid
# # label_3 = Label(root, text = "This is third label")

# ==========================Buttons========================================================
# button_1 = Button(root, text = "Can Click")
# button_2 = Button(root, text = "Can't Click", state = DISABLED)
# button_3 = Button(root, text = "Big Button",  padx = 50, pady = 50)

# def clickedButton():
#     label_button = Label(root, text = "Success, You clicked")
#     label_button.pack()

# button_4 = Button(root, text="Working Button", command=clickedButton)

# button_1.pack()
# button_2.pack()
# button_3.pack()
# button_4.pack()

# # Didnt work welp
# for i in range(1, 4):
#     x = "button_"
#     y = str(i)
#     x+y.pack()

# Constant Loop & Create Window
# root.mainloop()
