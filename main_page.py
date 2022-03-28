from faulthandler import disable
from glob import glob
from importlib.resources import path
from select import select
from telnetlib import STATUS
import tkinter as tk
from cv2 import split
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
# # Change Window's size
# root.geometry("800x600")
# Fix window's size
root.resizable(width=False, height=False)
# ==============================================================================

# =======================================================================================================================



# Left Side
if True:
    left_frame = tk.Frame(root, height="600", width="400", padx=5, pady=5, bg="red")
    left_frame.configure(height=left_frame["height"],width=left_frame["width"])
    left_frame.grid_propagate(0)

    # Prerequisite for search
    if True:
        def check_valid():
            # Collect input
            u_search = searchBar.get()
            # Check the length of search <=30
            if len(u_search) >= 31 or u_search =='':
                # Not valid
                result_reportEntry.set("Invalid Search")
            else:
                search_data(u_search)

        # Search in Database
        def search_data(u_search):
            searchAudioQuery ="select aid, audio_name, uid, audio_path from audio_tbl where audio_name like" + "'%" + u_search + "%';"
            mycursor.execute(searchAudioQuery)
            myresult = mycursor.fetchall()
            search_result_handle(myresult)
            print(is_song)

        def search_result_handle(myresult):
            # Save in global
            global search_result
            search_result = myresult

            # Get result
            result_list = []
            audio_num = 0
            for x in myresult:
                a_aid = x[0] # Potato code because it will wait until it load all songs (maybe limit/ use pages)
                a_name = x[1]
                a_path = x[2]
                audio_num += 1

                result_list.append(a_name)
            result_reportEntry.set("{} Results Found".format(audio_num))

            # Display result in listbox
            result_listbox.delete(0,"end")
            for audioname in result_list:
                result_listbox.insert('end', audioname)
            result_listbox.grid(row=0,column=0, padx=10)

        # For select from listbox
        def pick_from_list():
            # Get selection from listbox
            cs = result_listbox.curselection()
            global item_picked
            item_picked = result_listbox.get(cs)

            if True:
                # name of item picked
                entryText_name.set("{}".format(item_picked))

                #Artist of the song (uploader)
                for i in search_result:
                    if i[1] == item_picked:
                        item_id = i[0]
                        item_artist_id = i[2]
                searchAudioQuery ="select username from user_tbl where uid = {}".format(item_artist_id)
                mycursor.execute(searchAudioQuery)
                myresult = mycursor.fetchall()
                for i in myresult:
                    for j in i:
                        artist_name = j
                entryText_artist.set("{}".format(artist_name))

                searchAudioQuery ="select category_name from category_tbl, song_in_category where (song_in_category.cid = category_tbl.cid) and song_in_category.aid = {}".format(item_id)
                mycursor.execute(searchAudioQuery)
                myresult = mycursor.fetchall()
                categories = ""
                for i in myresult:
                    for j in i:
                        if categories != "":
                            categories =categories +", " + str(j)
                        else:
                            categories = str(j)
                entryText_category.set("{}".format(categories))

                # path of the song
                searchAudioQuery ="select audio_path from audio_tbl where aid = {}".format(item_id)
                mycursor.execute(searchAudioQuery)
                myresult = mycursor.fetchall()
                for i in myresult:
                    for j in i:
                        global selected_path
                        selected_path = j






    # Top left
    if True:
        tl_frame = tk.LabelFrame(left_frame, text="Search", padx=5, pady=5, bg="blue")

        # Creating label for search bar
        searchLabel = tk.Label(tl_frame, text = "Search: ", font = ('Italic', 14), fg="dark blue")
        searchLabel.grid(row = 0, column = 0, columnspan=2)
        # Creating input bar
        searchBar = tk.Entry(tl_frame, width=50)
        searchBar.grid(row = 1, column = 0, columnspan=4)
        # Search Button
        searchButton = tk.Button(tl_frame, text = "Search", command = check_valid)
        searchButton.grid(row = 1, column = 4)

        # Checkboxes for artist, songs and playlist
        song_var = tk.IntVar()
        song_chk = tk.Checkbutton(tl_frame, text="Song", variable=song_var)
        song_chk.select()
        song_chk.grid(row=2, column = 0)

        playlist_var = tk.IntVar()
        playlist_chk = tk.Checkbutton(tl_frame, text="Playlist", variable=playlist_var)
        playlist_chk.select()
        playlist_chk.grid(row=2, column = 1)

        artist_var = tk.IntVar()
        artist_chk = tk.Checkbutton(tl_frame, text="Artist", variable=artist_var)
        artist_chk.select()
        artist_chk.grid(row=2, column = 2)

        user_var = tk.IntVar()
        user_chk = tk.Checkbutton(tl_frame, text="User", variable=user_var)
        user_chk.select()
        user_chk.grid(row=2, column = 3)

        #Get Checkbox value by
        def show():
            checkLabel = tk.Label(tl_frame,text=song_var.get())
            checkLabel.grid()
            global is_song
            global is_artist
            global c
            global a
            y = song_var.get()
            m = playlist_var.get()
            c = artist_var.get()
            a = user_var.get()
            print(y,m,c,a)
        # checkbooo = tk.Button(tl_frame, text="check", command=show)
        # checkbooo.grid()

        tl_frame.grid(row=0, column=0)


    # Bottom left
    if True:
        bl_frame = tk.LabelFrame(left_frame, text="Result", padx=5, pady=5, bg="blue")
        # Create listbox
        result_listbox = tk.Listbox(bl_frame, height=25, width=52)
        result_listbox.bind('<<ListboxSelect>>', lambda x: pick_from_list())
        result_listbox.grid(row=0,column=0, padx=10, columnspan=1)

        scrollbar = tk.Scrollbar(bl_frame)
        scrollbar.grid(row=0,column=2, sticky='ns' )

        global result_reportEntry
        result_reportEntry = tk.StringVar()
        resultEntry =tk.Entry(bl_frame, textvariable=result_reportEntry, state="disabled")
        resultEntry.insert(0, "Search a Song :)")
        resultEntry.grid(row=1, column=0)
        # Select and display to right
        # select_button = tk.Button(bl_frame, text="Select", command= pick_from_list)
        # select_button.grid(row=1, column=1)

        

        bl_frame.grid(row=1, column=0)

    left_frame.grid(row=0, column=0)


# ===================== Right Side======================================================

# Right Side
if True:
    right_frame = tk.Frame(root, height="600", width="400", padx=5, pady=5, bg="black")
    right_frame.configure(height=right_frame["height"],width=right_frame["width"])
    right_frame.grid_propagate(0)

    # Prerequisite for Play music
    if True:

        #Music player
        def playSong():
            pg.mixer.music.load(r"{}".format(selected_path))
            pg.mixer.music.play(loops=0)
            entryPlayingAudio.set("{}".format(item_picked))
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

    # #Top Right
    if True:
        tr_frame = tk.Frame(right_frame, height=300, width=400, bg="purple")
        tr_frame.configure(height=tr_frame["height"],width=tr_frame["width"])
        tr_frame.grid_propagate(0)

        # top right details
        if True:
            tr_in_frame = tk.LabelFrame(tr_frame, text="Details", padx=5, pady=5)
            
            
            # Labels
            selected_SongName = tk.Label(tr_in_frame, text="Song Name: ")
            selected_SongName.grid()

            selected_Artist = tk.Label(tr_in_frame, text="Artist")
            selected_Artist.grid()

            selected_Category = tk.Label(tr_in_frame, text="Category")
            selected_Category.grid()

            # Displays of song detail with entries
            global entryText_name
            global entryText_artist
            global entryText_category
            entryText_name = tk.StringVar()
            entryText_artist = tk.StringVar()
            entryText_category = tk.StringVar()
            entry_name = tk.Entry(tr_in_frame, textvariable=entryText_name, state="disabled", fg="pink", justify=tk.CENTER)
            entry_name.grid(row=0, column=2)
            entry_artist = tk.Entry(tr_in_frame, textvariable=entryText_artist, state="disabled", fg="pink", justify=tk.CENTER)
            entry_artist.grid(row=1, column=2)
            entry_category = tk.Entry(tr_in_frame, textvariable=entryText_category, state="disabled", fg="pink", justify=tk.CENTER)
            entry_category.grid(row=2,column=2)

            tr_in_frame.grid(row=0, column=0)


        tr_frame.grid()


    # Bottom Right
    if True:
        global br_frame
        br_frame = tk.LabelFrame(right_frame, text="Music Player", padx=5, pady=5, bg="green")

        # Show Play buutton
        if True:
            playing_Label = tk.Label(br_frame, text="Now Playing: ", bg="green")
            playing_Label.grid(row=0, column=0)
            global entryPlayingAudio
            entryPlayingAudio = tk.StringVar()
            playing_entry = tk.Entry(br_frame, textvariable=entryPlayingAudio, state="disabled", justify=tk.CENTER)
            playing_entry.grid(row=0, column=1, columnspan=3)

            # copied code
            playButton = tk.Button(br_frame, text = "Play", command = playSong)
            playButton.grid(row=1,column=0)

            pauseButton = tk.Button(br_frame, text = "Pause", command = lambda:[pauseSong(),changeButton_pause()])
            pauseButton.grid(row=1,column=2)

            unpauseButton = tk.Button(br_frame, text = "Unpause", command = lambda:[unpauseSong(),changeButton_unpause()])
            unpauseButton.grid(row=2,column=2)

            stopButton = tk.Button(br_frame, text = "Stop", command = stopSong)
            stopButton.grid(row=1,column=3)




        br_frame.grid()

    #extra label

    right_frame.grid(row=0, column=1)




root.mainloop()