import tkinter as tk
import pygame as pg
from py_SQL import db_connection

db, mycursor = db_connection()
root = tk.Tk()

# initialise pygame mixer
pg.mixer.init()


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



# Creating label for search bar
searchLabel = tk.Label(root, text = "Search Audio: ", font = ('Italic', 14), fg="dark blue")
# Creating input bar
searchBar = tk.Entry(root)
# Display Search bar & Input Bar
searchLabel.grid(row = 0, column = 0)
searchBar.grid(row = 0, column = 1)

def playSong(path):
    pg.mixer.music.load(path)
    pg.mixer.music.play(loops=0)

# Collect input data & Check if "" OR >30
def check_valid():
    # Collect input
    u_search = searchBar.get()
    # Check the length of search <=30
    if len(u_search) >= 31 or u_search =='':
        # Not valid
        searchValid = tk.Label(root, text = f"Invalid Search")
        searchValid.grid(row=2,column=1)
    else:
        # Valid
        searchValid = tk.Label(root, text = f"Displaying Search Result for: {u_search}")
        searchValid.grid(row=2,column=1)
        search_data(u_search)

def search_data(u_search):
    # Search in Database
    searchAudioQuery ="select audio_name, audio_path from audio_tbl where audio_name like" + "'%" + u_search + "%';" 
    mycursor.execute(searchAudioQuery)
    myresult = mycursor.fetchall()

    # Get result
    audio_num = 0
    for x in myresult:
        print(x) # -- FOR LOG --
        a_name = x[0] # Potato code because it will wait until it load all songs (maybe limit/ use pages)
        a_path = x[1]
        audio_num += 1

        # Display Results
        audioLabel = tk.Label(root, text = f"Audio Name = {a_name}")
        audioLabel.grid(row=3+audio_num, column=1) # row 0 = search bar, row 1= search button, row 2 = Displaying Search Result for:

        # Play Audio
        #
        # Issue - Play the last song on all button,
        # Solution probably use list, call list
        audioButton = tk.Button(root, text = "Play", command = lambda:[playSong(a_path)])
        audioButton.grid(row=3+audio_num, column=2)

    # Display number of results after loop
    numLabel = tk.Label(root, text = f"Number of Result {audio_num}")
    numLabel.grid(row=4+audio_num, column=1)






# Search Button
searchButton = tk.Button(root, text = "Search", command = check_valid)
# Display search button
searchButton.grid(row = 1, column = 0)




root.mainloop()