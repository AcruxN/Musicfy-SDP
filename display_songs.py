import tkinter as tk
import pygame as pg
from py_SQL import db_connection

db, mycursor = db_connection()
root = tk.Tk()

# ============================= Application Design =============================
# Change Window(Application) Title
root.title("Musicfy")
# Change icon
root.iconbitmap(r"musicfy.ico")
# Change Window's size
root.geometry("400x400")
# Fix window's size
root.resizable(width=False, height=False)

# ------------------- Button to change application Size ------------------------
# def resize():
#     w = 400
#     h = 400
#     root.geometry(f"{w}x{h}") 

# resizeButton = tk.Button(root, text="Resize to 400 x 400", command = resize)
# resizeButton.grid(row=2, column=2)
# ------------------------------------------------------------------------------


# ==============================================================================

# initialise pygame mixer
pg.mixer.init()

def playSong():
    pg.mixer.music.load(r"audio_files/The_Moon_Song.mp3")
    pg.mixer.music.play(loops=0)

def pauseSong():
    pg.mixer.music.pause()

def unpauseSong():
    pg.mixer.music.unpause()

def changeButton_pause():
    pass

def changeButton_unpause():
    pass

def stopSong():
    pg.mixer.music.stop()

playButton = tk.Button(root, text = "Play", command = playSong)
playButton.grid(row=1,column=0)

pauseButton = tk.Button(root, text = "Pause", command = lambda:[pauseSong(),changeButton_pause()])
pauseButton.grid(row=1,column=2)

unpauseButton = tk.Button(root, text = "Unpause", command = lambda:[unpauseSong(),changeButton_unpause()])
unpauseButton.grid(row=2,column=2)

stopButton = tk.Button(root, text = "Stop", command = stopSong)
stopButton.grid(row=1,column=3)

root.mainloop()