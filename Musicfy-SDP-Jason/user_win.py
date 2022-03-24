# ===================================== User Main =====================================
import tkinter as tk
from py_SQL import db_connection

# database connection 
db, cursor = db_connection()

# username will be showned in the window when a specific user log in, on line 23 (already tested it)
# put username here to test the user function
username = 'test'

def raise_frame(frame):
    frame.tkraise()


root = tk.Tk()
root.geometry("500x500")
root.title("Musicfy")
# root.iconbitmap(r"musicfy.ico") # musicfy window icon


top = tk.Frame(root)
profile = tk.Frame(root)

for frame in (top, profile):
    # frame.grid(row=0, column=0, sticky="news")
    frame.place(x=0, y=0, width=500, height=500)


tk.Label(top, text="Welcome, " +username).grid(row=1, column=7) 

# selection either listener or artist (to upload songs)

# ========================================= First Frame (top) =====================================
user_profile_button = tk.Button(top, text="Profile", command=lambda: raise_frame(profile))
user_profile_button.grid(row=1, column=9)

user_quit_button = tk.Button(top, text="Quit", command=lambda: quit(top))
user_quit_button.grid(row=1, column=10)

# ========================================= Second Frame (profile) =====================================

profile_button = tk.Button(profile, text="Profile Button")
profile_button.grid()


raise_frame(top)
root.mainloop()