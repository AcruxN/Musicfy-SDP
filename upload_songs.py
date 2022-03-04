import os
import tkinter as tk
import pygame as pg
from tkinter import StringVar, filedialog, messagebox
from pathlib import Path
from py_SQL import db_connection
import shutil

db, mycursor = db_connection()
root = tk.Tk()

# initialise pygame mixer
pg.mixer.init()

# ============================= Application Design =============================
# Change Window(Application) Title
root.title("Musicfy")
# Change icon
# root.iconbitmap(r"musicfy.ico")
# Change Window's size
root.geometry("400x400")
# Fix window's size
root.resizable(width=False, height=False)

# ==============================================================================

# ============================ Functions =======================================
#IMPORTANT: py_SQL.py file make changes for cursor :- mycursor = db.cursor(buffered=True)

user_id = str(1) #Get user id from database when login with query
file_path=''
#Get menu choice
def get_category():
    global categoryList
    global audio_category
    audio_category = []
    #Get selected category
    categoryList = category_list.curselection()

#Select audio file
def Select_file():
    global file_path
    #Get file path
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", ".mp3 .wav .flac")])
    file_name = StringVar()
    #Display name of file selected
    file_name = Path(file_path).name
    file_selected = tk.Label(root, text = file_name, font=('Italic', 10), fg="black", )
    file_selected.grid(sticky='W',row=2,column=2)

#Upload file
def Audio_upload():
    #Audio name
    global audio_name
    global file_path
    global audio_category
    audio_creator = "_"  + str(user_id)
    audio_name = inputName.get() + audio_creator
    filepath = file_path
    # Catch error
    if audio_name == audio_creator:
        messagebox.showwarning('Error!', 'Please enter audio name!')
        
    elif filepath == '':
        messagebox.showwarning('Error!', 'Please upload audio file!')
    elif len(categoryList) == 0:        
        messagebox.showwarning('Error!', 'Please choose a category!')
    else:
        #Copy audio to the file (If able to host databse, change to upload to database)
        audio_uploaded = shutil.copy(file_path, 'C:/Users/USER/OneDrive/Documents/GitHub/Musicfy-SDP/audio_files folder/') #change to audio file path
        #rename file to match audio name and aid
        global audio_location

        audio_location = 'C:/Users/USER/OneDrive/Documents/GitHub/Musicfy-SDP/audio_files folder/' + audio_name  + '_'+user_id+'.mp3'
        os.rename(audio_uploaded, audio_location) #Rename audio in audio folder as name entered
        # All category selected

        for c in categoryList:
            c+=1
            audio_category.append(c)

#Update audio category
def updateAudio_category():
    #Get aid
    audio_id = "SELECT aid FROM audio_tbl WHERE audio_name = %s AND uid = %s"
    audio_tuple = (audio_name, user_id)
    global audioCategory_list
    global audio_category
    audioCategory_list = []
    mycursor.execute(audio_id, audio_tuple)
    
    aid_tuple = mycursor.fetchone()
    #Get a list of cid with aid
    if aid_tuple != None:
        if len(aid_tuple) > 0 :
            for x in audio_category:
                aid = aid_tuple[0]
                audioCategory_list.append((x, aid))

    audio_cat = "INSERT INTO song_in_category (cid, aid) VALUES (%s, %s)"
    mycursor.executemany(audio_cat, audioCategory_list)
    db.commit()

def Update_database():
    try:
        #Insert list into database
        audio_sql = "INSERT INTO audio_tbl (audio_name, uid, audio_path) VALUES ('{}','{}','{}')".format(audio_name, user_id, audio_location)
        mycursor.execute(audio_sql)
        db.commit()
        messagebox.showinfo('', 'Audio uploaded successfully!')
    except Exception as e:
        db.rollback()

#============================================================================================================================================

def Upload_audio():
    #Create and display upload audio label
    uploadAudio = tk.Label(root, text = "Upload Audio", font=('Italic', 14), fg="dark blue")
    uploadAudio.grid(row = 0, column = 0)
    #Create and display audio name input bar
    audioName = tk.Label(root, text = "Audio Name:", font=('Italic', 10), fg="black", )
    audioName.grid(sticky='W',row=1,column=0)
    global inputName
    inputName = tk.Entry(root)
    inputName.grid(row=1,column=1)
    #Select audio file label and button
    audioFile = tk.Label(root, text = "Select audio file:", font=('Italic', 10), fg="black", )
    audioFile.grid(sticky='W',row=2,column=0)

    Open_button = tk.Button(root, text='Open', command= Select_file)
    Open_button.grid(sticky='W', row=2,column=1)
    # Category label
    Category = tk.Label(root, text = "Category:", font=('Italic', 10), fg="black", )
    Category.grid(sticky='NW',row=3,column=0)
    #Create listbox
    global category_list
    category_list = tk.Listbox(root, selectmode=tk.MULTIPLE, height=6)
    categories = ['Lofi', 'Hit-hop', 'Jazz', 'Meme', 'Game OST', 'Acoustic']
    for i in categories:
        category_list.insert(tk.END, i)
        
    category_list.grid(row=3, column=1)
    #Upload button
    Upload_button = tk.Button(root, text='Upload', command=lambda:[get_category(), Audio_upload(), Update_database(), updateAudio_category()]) 
    Upload_button.grid(sticky='E', row=4,column=1)


Upload_audio()
root.mainloop()
    
