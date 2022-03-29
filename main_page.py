# ============================= Imported Modules =============================
import tkinter as tk
from tkinter import DISABLED, StringVar, filedialog
from tkinter import messagebox, Listbox, Toplevel
import os
from pathlib import Path
import shutil
from PIL import ImageTk, Image
import re
import pygame as pg
from py_SQL import db_connection
from driveconnector import ImageDownload, ImageUpload

db, mycursor = db_connection()
root = tk.Tk()

guest_user = ""
# initialise pygame mixer
pg.mixer.init()
# pg.init()

# ============================= Application Design ============================= #
# Change Window(Application) Title
root.title("Musicfy")
# Change icon
# root.iconbitmap(r"musicfy.ico")
# # Change Window's size
# root.geometry("800x600")
# Fix window's size
# root.resizable(width=False, height=False)
# ============================================================================== #



# jason's code
if True:
    # ===================================== Main ============================================= #
    def login_win():
        def raise_frame(frame):
            frame.tkraise()


        login = tk.Toplevel()
        login.geometry("950x500")
        login.title("Musicfy") 
        login.configure(bg='#132933')
        login.resizable(width=False, height=False)
        # root.iconbitmap(r"musicfy.ico") # musicfy window icon


        # frame for the image 
        login_left_frame = tk.Frame(login, width=500, height=500, bg='#132933') 
        login_left_frame.grid()

        my_img = ImageTk.PhotoImage(Image.open("image\music logo design.png"))
        img_label = tk.Label(login_left_frame, image= my_img, borderwidth=0, highlightthickness=0)
        img_label.grid()

        main = tk.Frame(login, bg='#132933')
        signup = tk.Frame(login, bg='#132933')

        for frame in (main, signup):
            frame.place(x=500, y=0, width=500, height=500)





        # ===================================== User Main ======================================= #
        global user
        def user(username):
            login.withdraw()
            top = Toplevel()
            top.geometry("500x500")
            top.title("User Page")
            global guest_user
            guest_user = username

            # to declare first frame
            profile = tk.Frame(top)
            profile.configure(bg='#132933')
            #to declare edit profile(second frame)
            edit = tk.Frame(top)
            edit.configure(bg='#132933')


            def raise_frame(frame):
                frame.tkraise()

            for frame in (profile, edit):
                frame.place(x=0, y=0, width=500, height=500)


            # ===================================== First Frame [User Profile] ===================================== #


            # main title
            userprofile = tk.Label(profile, text="User Profile")
            userprofile.place(x=150, y=0)
            userprofile.config(fg='white', bg='#132933', font=('Helvatical bold',26, 'bold'))
            # to take select the row containing that username
            selecteduser = 'select * FROM user_tbl WHERE username = "%s"' % username
            mycursor.execute(selecteduser)
            results = mycursor.fetchall()

            # display profile
            for row in results:
                # display profile
                    path = "image/"+row[7]
                    print(path)
                    if os.path.exists(path):
                        ini_img = Image.open(path)
                        img = ImageTk.PhotoImage(ini_img.resize((150,150), Image.ANTIALIAS))
                        label = tk.Label(profile, image = img)
                        label.place(x=20, y=90)
                        print(path)
                    else:#display default profile if databse is none
                        ini_img = Image.open("image/defaultprofile.jpg")
                        img = ImageTk.PhotoImage(ini_img.resize((150,150), Image.ANTIALIAS))
                        label = tk.Label(profile, image = img)
                        label.place(x=20, y=90)




            # ============================================= Upload Songs Function ============================================= #
            # chloe's code
            def uploadSongs():
                top.withdraw()
                up_song = Toplevel()
                up_song.geometry("300x300")
                up_song.configure(bg='#132933')
                up_song.title("Upload Songs")
                up_song.resizable(width=False, height=False)


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
                    file_selected = tk.Label(up_song, text = file_name, font=('Italic', 10), fg="black", )
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

                # ============================================================================================================================================

                def Upload_audio():
                    #Create and display upload audio label
                    uploadAudio = tk.Label(up_song, text = "Upload Audio", font=('Italic', 15, "bold"), fg="white", bg='#132933')
                    uploadAudio.grid(row = 0, column = 0 , columnspan=2)
                    #Create and display audio name input bar
                    audioName = tk.Label(up_song, text = "Audio Name:", font=('Italic', 10, "bold"), fg="white", bg='#132933')
                    audioName.grid(sticky='W',row=1,column=0)
                    global inputName
                    inputName = tk.Entry(up_song)
                    inputName.grid(row=1,column=1)
                    #Select audio file label and button
                    audioFile = tk.Label(up_song, text = "Select audio file:", font=('Italic', 10, "bold"), fg="white", bg='#132933')
                    audioFile.grid(sticky='W',row=2,column=0)

                    Open_button = tk.Button(up_song, text='Open', command= Select_file)
                    Open_button.grid(sticky='W', row=2,column=1)
                    # Category label
                    Category = tk.Label(up_song, text = "Category:", font=('Italic', 10, "bold"), fg="white", bg='#132933')
                    Category.grid(sticky='NW',row=3,column=0)
                    #Create listbox
                    global category_list
                    category_list = tk.Listbox(up_song, selectmode=tk.MULTIPLE, height=6)
                    categories = ['Lofi', 'Hit-hop', 'Jazz', 'Meme', 'Game OST', 'Acoustic']
                    for i in categories:
                        category_list.insert(tk.END, i)
                        
                    category_list.grid(row=3, column=1)
                    #Upload button
                    Upload_button = tk.Button(up_song, text='Upload', command=lambda:[get_category(), Audio_upload(), Update_database(), updateAudio_category()]) 
                    Upload_button.grid(sticky='E', row=4,column=1)

                    upload_quit_button = tk.Button(up_song, text="Back", command= lambda: backButton())
                    upload_quit_button.grid(sticky='E', row=0, column=1)

                def backButton():
                    up_song.destroy()
                    top.update()
                    top.deiconify()


                Upload_audio()

            # ============================================= View Own Song Function ============================================= #
            # namtung code
            def viewownSong():
                
                temp_name = guest_user

                # function for select stuff in listbox
                def check_own_like():
                    # get what is clicked on the listbox
                    try:
                        cs = own_Listbox.curselection()
                        temp_own_pick = own_Listbox.get(cs)
                    except (UnboundLocalError, tk.TclError) as Error:
                        pass


                    # use data to sql 
                    searchAudioQuery ="select sum(l.like_status) from like_tbl l, audio_tbl a, user_tbl u where (a.aid = l.aid) and (a.uid = u.uid) and audio_name = '{}' and u.username = '{}'".format(temp_own_pick, temp_name)
                    mycursor.execute(searchAudioQuery)
                    myresult = mycursor.fetchall()
                    print(myresult)
                    for i in myresult:
                        for j in i:
                            likenum = j
                    # set the entry value
                    likeOwnnum.set("{}".format(likenum)) 

                searchAudioQuery = "select a.audio_name from audio_tbl a, user_tbl u where (a.uid = u.uid) and username ='{}'".format(temp_name)
                mycursor.execute(searchAudioQuery)
                myresult = mycursor.fetchall()
                print(myresult)

                # ================================================================================ #
                top.withdraw()
                ownsong = Toplevel()
                ownsong.title("My Published Song")
                ownsong.geometry("300x300")
                # ownsong.resizable(height=False, width=False)
                ownsong.configure(bg='#132933')

                # DISPLAY
                if True:
                    ownsongLabel = tk.Label(ownsong, text="List of Own Songs", fg="white", bg="#132933", font=("Calibri", 15, "bold"))
                    ownsongLabel.place(x=60, y=3)

                    own_Listbox = tk.Listbox(ownsong, height=10, width=30)
                    own_Listbox.bind('<<ListboxSelect>>', lambda x: check_own_like())
                    own_Listbox.place(x=50, y=45)

                    own_label = tk.Label(ownsong, text = "Number of likes: ", fg="white", bg="#132933", font=("Calibri", 12, "bold"))
                    own_label.place(x=60, y=220)

                    likeOwnnum = tk.StringVar()
                    likeentry = tk.Entry(ownsong, width=5, state=DISABLED, textvariable=likeOwnnum, justify=tk.CENTER)
                    likeentry.place(x=180, y=222)

                    ownsongButton = tk.Button(ownsong, text="Back", command=lambda: backButton())
                    ownsongButton.place(x=180, y=250)

                    def backButton():
                        ownsong.destroy()
                        top.update()
                        top.deiconify()

                # Put things into listbox
                own_Listbox.delete(0,"end")
                for j in myresult:
                    for i in j:
                        own_Listbox.insert('end', i)
                own_Listbox.grid(x=25, y=15)

            # ============================================= Manage Own Playlist Function ============================================= #
            # namtung code
            def manageownPlaylsit():
                
                tobeadded = entryText_name.get()
                # new window
                top.withdraw()
                cpl = Toplevel()
                cpl.geometry("500x400")
                cpl.title("My Playlist")
                # cpl.resizable(height=False, width=False)

                # get username
                temp_name = guest_user
                #get uid with username 
                searchQuery = "select uid from user_tbl where username = '{}'".format(temp_name)
                mycursor.execute(searchQuery)
                myresult = mycursor.fetchall()
                for i in myresult:
                    for j in i:
                        uid = j

                upframecp = tk.Frame(cpl, height="250", width="500", padx=5, pady=5, bg="#132933")
                upframecp.configure(height=upframecp["height"],width=upframecp["width"])
                upframecp.grid_propagate(0)
                # View own playlist and its song
                if True:

                    def dissam():
                        try:
                            cs = samlistbox.curselection()
                            plsam = samlistbox.get(cs)
                        except (UnboundLocalError, tk.TclError) as Error:
                            pass

                        global pickkplname
                        pickkplname = plsam

                        searchQuery = "select a.audio_name from audio_tbl a, playlist_tbl p, song_in_playlist s where (p.pid = s.pid) and (a.aid = s.aid) and playlist_name = '{}'".format(plsam)
                        mycursor.execute(searchQuery)
                        myresult = mycursor.fetchall()
                        listsg = []
                        for i in myresult:
                            for j in i:
                                listsg.append(j)
                        
                        sam2listbox.delete(0,"end")
                        for i in listsg:
                            sam2listbox.insert("end", i)
                        sam2listbox.grid(row=1, column=1)

                        # remove song selected from previous playlist
                        varsg.set('')

                    lblabel = tk.Label(upframecp, text = "Your playlist", fg='white', bg='#132933', font=("Calibri", 12, 'bold'))
                    lblabel.grid(row=0, column = 0)

                    samlistbox = tk.Listbox(upframecp, height=25, width=40)
                    samlistbox.bind('<<ListboxSelect>>', lambda x: dissam())
                    samlistbox.grid(row=1, column=0) 

                    # fill in playlist name in listbox
                    if True:
                        query = "select playlist_name from playlist_tbl where uid = '{}'".format(uid)
                        mycursor.execute(query)
                        myresult = mycursor.fetchall()
                        listpl = []
                        for i in myresult:
                            for j in i:
                                listpl.append(j)
                        
                        samlistbox.delete(0,"end")
                        for playname in listpl:
                            samlistbox.insert('end', playname)
                        samlistbox.grid(row=1,column=0)
                


                    def dissam2():
                        try:
                            cs = sam2listbox.curselection()
                            plsam2 = sam2listbox.get(cs)
                        except (UnboundLocalError, tk.TclError) as Error:
                            pass
                        varsg.set('{}'.format(plsam2))
                    
                    lb2label = tk.Label(upframecp, text ="Songs in playlist", fg='white', bg='#132933', font=("Calibri", 12, 'bold'))
                    lb2label.grid(row=0, column=1)

                    sam2listbox = tk.Listbox(upframecp, height=25, width=40)
                    sam2listbox.bind('<<ListboxSelect>>', lambda x: dissam2())
                    sam2listbox.grid(row=1,column=1)

                upframecp.grid()

                # Bottom part (functions)
                downframecp = tk.Frame(cpl, height="250", width="500", padx=5, pady=5, bg="#132933")
                downframecp.configure(height=downframecp["height"],width=downframecp["width"])
                downframecp.grid_propagate(0)


                if True:
                    # For create playlist
                    inframe_down3 = tk.LabelFrame(downframecp, bg="#132933", border=0)
                    inframe_down3.place(x=15, y=15)

                    # verify playlist no exist, if suc then insert
                    def createpl():
                        
                        temp_uname = guest_user
                        if guest_user == "":
                            login_win()
                        else:
                            def nice_sub():
                                query ="select uid from user_tbl where username = '{}'".format(temp_uname)
                                mycursor.execute(query)
                                myresult = mycursor.fetchall() 
                                for i in myresult:
                                    for j in i:
                                        uid = i

                                sql = "update user_tbl set subscription = 1 where uid = '{}'".format(uid)
                                mycursor.execute(sql)
                                db.commit()

                            
                            query = "select subscription from user_tbl where username = '{}'".format(temp_uname)
                            mycursor.execute(query)
                            myresult = mycursor.fetchall()
                            for i in myresult:
                                for j in i:
                                    is_sub = j
                            
                            if is_sub == 0:
                                cpl.withdraw()
                                subwin = Toplevel()
                                subwin.geometry("250x200")
                                subwin.title("Subscribe!")
                                subwin.configure(bg='#132933')
                                subwin.resizable(width=False, height=False)

                                subtitlabel = tk.Label(subwin, text="Oops! You are not subscribed... \n  Please Subscribe to Support Us", fg='white', bg='#132933', font=("Calibri", 12, 'bold'))
                                subtitlabel.place(x=10, y=6)

                                label_sample = tk.Label(subwin, text="Payment Details :", fg='white', bg='#132933', font=("Calibri", 10, 'bold'))
                                label_sample.place(x=3, y=70)
                                entry_sample1 = tk.Entry(subwin)
                                entry_sample1.place(x=110, y=70)


                                label_sample2 = tk.Label(subwin, text="Password :", fg='white', bg='#132933', font=("Calibri", 10, 'bold'))
                                label_sample2.place(x=3, y=100)
                                entry_sample2 = tk.Entry(subwin)
                                entry_sample2.place(x=110, y=100)

                                button_sample = tk.Button(subwin, text="Confirm", command=nice_sub)
                                button_sample.place(x=180, y=125)

                                subBackButton = tk.Button(subwin, text="Back", command= lambda: subButton())
                                subBackButton.place(x=135, y=125)

                                def subButton():
                                    subwin.destroy()
                                    cpl.update()
                                    cpl.deiconify()

                            else:
                                execute_cr = False
                                listex = []
                                varplname = entered_name.get()

                                if len(varplname) <= 3:
                                    messagebox.showinfo("Error", "Playlist name cannot be too short!")
                                elif len(varplname) >= 50:
                                    messagebox.showinfo("Error", "Playlist name cannot be too long!")
                                else:
                                    # search existing playlist
                                    searchQuery = "select p.playlist_name from playlist_tbl p"
                                    mycursor.execute(searchQuery)
                                    myresult = mycursor.fetchall()
                                    print(myresult)
                                    for i in myresult:
                                        for j in i:
                                            listex.append(j)
                                    if varplname not in listex:
                                        execute_cr = True
                                    else:
                                        messagebox.showinfo("Error", "Playlist exist!")

                                if execute_cr:
                                    insertnewplaylist = "insert into `playlist_tbl` (uid, playlist_name) values ('{}','{}');".format(uid, varplname)
                                    mycursor.execute(insertnewplaylist)
                                    db.commit()
                                    messagebox.showinfo("Error", "Playlist Created!")

                                    #refresh
                                    query = "select playlist_name from playlist_tbl where uid = '{}'".format(uid)
                                    mycursor.execute(query)
                                    myresult = mycursor.fetchall()
                                    listpl = []
                                    for i in myresult:
                                        for j in i:
                                            listpl.append(j)
                                    
                                    samlistbox.delete(0,"end")
                                    for playname in listpl:
                                        samlistbox.insert('end', playname)
                                    samlistbox.grid(row=1,column=0)

                    # for create new playlsit
                    elabel = tk.Label(inframe_down3, text= 'New Playlist Name: ', fg='white', bg='#132933', font=("Calibri", 12, 'bold'))
                    elabel.grid(row=0, column=1)

                    entered_name = tk.StringVar()
                    entrynew = tk.Entry(inframe_down3, textvariable=entered_name)
                    entrynew.grid(row=1, column=1)

                    create_button = tk.Button(inframe_down3, text="Create", command=createpl)
                    create_button.grid(row=2, column=1, padx=5, pady=5)
                    






                    # For remove song from playlst
                    inframe_down = tk.LabelFrame(downframecp, bg="#132933", border=0)
                    inframe_down.place(x=180, y=15)

                    def remol():

                        plsam = pickkplname
                        query = "select pid from playlist_tbl where playlist_name = '{}';".format(plsam)
                        mycursor.execute(query)
                        myresult = mycursor.fetchall()
                        for i in myresult:
                            for j in i:
                                pid = j
                        

                        remolsgname = entrysg.get()
                        query = "select aid from audio_tbl where audio_name = '{}';".format(remolsgname)
                        mycursor.execute(query)
                        myresult = mycursor.fetchall()
                        for i in myresult:
                            for j in i:
                                aid = j
                        
                        remolsong = "delete from song_in_playlist where pid = '{}' and aid = '{}';".format(pid, aid)
                        mycursor.execute(remolsong)
                        db.commit()
                    
                    # for delete song from playlist
                    labelsg = tk.Label(inframe_down, text = "Song selected :", fg='white', bg='#132933', font=("Calibri", 12, 'bold'))
                    labelsg.grid(row=0, column= 0)

                    global varsg
                    varsg = tk.StringVar()
                    entrysg = tk.Entry(inframe_down, textvariable=varsg, state=DISABLED)
                    entrysg.grid(row=1, column= 0)

                    buttonsg = tk.Button(inframe_down, text="Remove from playlist", command=remol)
                    buttonsg.grid(row=2, column=0, padx=5, pady=5)







                    # add song to playlsit
                    inframe_down2 = tk.LabelFrame(downframecp, bg="#132933", border=0)
                    # inframe_down2.grid(row=0,column=1)
                    inframe_down2.place(x=335, y=15)
                    def addmol():
                        plsam = pickkplname
                        query = "select pid from playlist_tbl where playlist_name = '{}';".format(plsam)
                        mycursor.execute(query)
                        myresult = mycursor.fetchall()
                        for i in myresult:
                            for j in i:
                                pid = j
                        
                        picked_sg = entryText_name.get()
                        query = "select aid from audio_tbl where audio_name = '{}';".format(picked_sg)
                        mycursor.execute(query)
                        myresult = mycursor.fetchall()
                        for i in myresult:
                            for j in i:
                                aid = j
                        print(picked_sg)
                        addmolsong = "insert into song_in_playlist (pid,aid) values({},{});".format(pid, aid)
                        mycursor.execute(addmolsong)
                        db.commit()



                    # add song to playlist
                    labelsg2 = tk.Label(inframe_down2, text = "Song selected :", fg='white', bg='#132933', font=("Calibri", 12, 'bold'))
                    labelsg2.grid(row=0, column= 0)

                    picked_sg = tk.StringVar()
                    
                    picked_sg.set('{}'.format(tobeadded))

                    entrysg2 = tk.Entry(inframe_down2, textvariable=picked_sg, state=DISABLED)
                    entrysg2.grid(row=1, column= 0)

                    buttonsg2 = tk.Button(inframe_down2, text="Add to playlist", command=addmol)
                    buttonsg2.grid(row=2, column=0, padx=5, pady=5)

                    myplaylist_back = tk.Button(downframecp, width=15, text="Back", command= lambda: backButton())
                    myplaylist_back.place(x=190, y=115)

                def backButton():
                    cpl.destroy()
                    top.update()
                    top.deiconify()

                downframecp.grid()
                #Create new playlist

            # Relabel/replace profile with latest detail after edit
            def copycat():
                # to take select the row containing that username
                selecteduser = 'select * FROM user_tbl WHERE username = "%s"' % username
                mycursor.execute(selecteduser)
                results = mycursor.fetchall()


                # display other info 
                usertype = results[0][1]
                username = results[0][2]
                subscription = results[0][4]
                uploaded = results[0][5]
                downloaded = results[0][6]

                if usertype == "artist":
                    # display button
                    uploadsong_button = tk.Button(profile, text="Upload Song", command=lambda: uploadSongs())#function here)
                    uploadsong_button.place(x=50, y=400)

                    viewownsong_button = tk.Button(profile, text="View Own Song", command=lambda:viewownSong())#function here)
                    viewownsong_button.place(x=150, y=400)

                    manageplaylist_button = tk.Button(profile, text="Manage Playlist", command=lambda:manageownPlaylsit())#function here)
                    manageplaylist_button.place(x=265, y=400)


                def changetoartist():
                    # change the user type database from listener to artist
                    changeusertype = f'update user_tbl set usertype = "artist" where username = "{username}"'
                    mycursor.execute(changeusertype)
                    db.commit()
                    messagebox.showinfo(title=None, message="You have successfully become an artist")
                    profile.update()
                    # raise_frame(profile)


                if usertype == "listener":
                    manageplaylist_button = tk.Button(profile, text="Manage Playlist", command=lambda:manageownPlaylsit())#function here)
                    manageplaylist_button.place(x=70, y=400)

                    changetoartist_button =tk.Button(profile, text="Become an Artist", command=lambda:changetoartist())#function here)
                    changetoartist_button.place(x=220, y=400)
                
                user_quit_button = tk.Button(profile, text="Quit", width=12, justify='center', command=lambda: quit(top))
                user_quit_button.place(x=380, y=400)

                displayusername = tk.Label(profile, text=f"User Name : {username} ")
                displayusername.place(x=200, y=80)
                displayusername.config(fg='white', bg='#132933', font=('Helvatical bold',14, 'bold'))

                displayusertype = tk.Label(profile, text=f"User Type : {usertype}")
                displayusertype.place(x=200, y=140)
                displayusertype.config(fg='white', bg='#132933', font=('Helvatical bold',14, 'bold'))

                if subscription == 0:
                    subscription = "Not Subscribed"
                else:
                    subscription = "Subscribed"

                displaysubscription = tk.Label(profile, text=f"Subscription : {subscription}")
                displaysubscription.place(x=200, y=200)
                displaysubscription.config(fg='white', bg='#132933', font=('Helvatical bold',14, 'bold'))

                displayuploaded = tk.Label(profile, fg='white', bg='#132933', text=f"Uploaded Songs : {uploaded}")
                displayuploaded.place(x=200, y=260)
                displayuploaded.config(fg='white', bg='#132933', font=('Helvatical bold',14, 'bold'))

                displaydownloaded = tk.Label(profile, text=f"Downloaded Songs : {downloaded}")
                displaydownloaded.place(x=200, y=320)
                displaydownloaded.config(fg='white', bg='#132933', font=('Helvatical bold',14, 'bold'))

                edit_profile_button = tk.Button(profile, text="Edit Profile", command=lambda: raise_frame(edit))
                edit_profile_button.place(x=60, y=250)




            # display other info 
            usertype = results[0][1]
            username = results[0][2]
            subscription = results[0][4]
            uploaded = results[0][5]
            downloaded = results[0][6]

            if usertype == "artist":
                # display button
                uploadsong_button = tk.Button(profile, text="Upload Song", command=lambda: uploadSongs())#function here)
                uploadsong_button.place(x=50, y=400)

                viewownsong_button = tk.Button(profile, text="View Own Song", command=lambda:viewownSong())#function here)
                viewownsong_button.place(x=150, y=400)

                manageplaylist_button = tk.Button(profile, text="Manage Playlist", command=lambda:manageownPlaylsit())#function here)
                manageplaylist_button.place(x=265, y=400)


            def changetoartist():
                # change the user type database from listener to artist
                changeusertype = f'update user_tbl set usertype = "artist" where username = "{username}"'
                mycursor.execute(changeusertype)
                db.commit()
                messagebox.showinfo(title=None, message="You have successfully become an artist")
                profile.update()
                # raise_frame(profile)


            if usertype == "listener":
                manageplaylist_button = tk.Button(profile, text="Manage Playlist", command=lambda:manageownPlaylsit())#function here)
                manageplaylist_button.place(x=70, y=400)

                changetoartist_button =tk.Button(profile, text="Become an Artist", command=lambda:changetoartist())#function here)
                changetoartist_button.place(x=220, y=400)
            
            user_quit_button = tk.Button(profile, text="Quit", width=12, justify='center', command=lambda: quit(top))
            user_quit_button.place(x=380, y=400)

            displayusername = tk.Label(profile, text=f"User Name : {username} ")
            displayusername.place(x=200, y=80)
            displayusername.config(fg='white', bg='#132933', font=('Helvatical bold',14, 'bold'))

            displayusertype = tk.Label(profile, text=f"User Type : {usertype}")
            displayusertype.place(x=200, y=140)
            displayusertype.config(fg='white', bg='#132933', font=('Helvatical bold',14, 'bold'))

            if subscription == 0:
                subscription = "Not Subscribed"
            else:
                subscription = "Subscribed"

            displaysubscription = tk.Label(profile, text=f"Subscription : {subscription}")
            displaysubscription.place(x=200, y=200)
            displaysubscription.config(fg='white', bg='#132933', font=('Helvatical bold',14, 'bold'))

            displayuploaded = tk.Label(profile, fg='white', bg='#132933', text=f"Uploaded Songs : {uploaded}")
            displayuploaded.place(x=200, y=260)
            displayuploaded.config(fg='white', bg='#132933', font=('Helvatical bold',14, 'bold'))

            displaydownloaded = tk.Label(profile, text=f"Downloaded Songs : {downloaded}")
            displaydownloaded.place(x=200, y=320)
            displaydownloaded.config(fg='white', bg='#132933', font=('Helvatical bold',14, 'bold'))

            edit_profile_button = tk.Button(profile, text="Edit Profile", command=lambda: raise_frame(edit))
            edit_profile_button.place(x=60, y=250)





            # ===================================== Second Frame [User Profile] ===================================== #
            modify = tk.Label(edit, text="Modify Profile")
            modify.place(x=120, y=30)
            modify.config(fg='white', bg='#132933', font=('Helvatical bold',30, 'bold'))





            # ===================================== Modify Username [User Profile] ===================================== #
            # username label
            changeusername = tk.Label(edit, fg='white', bg='#132933', text="Username: *", font=("Calibri", 15, "bold"))
            changeusername.place(x=130, y=100)
            # username entry
            username_entry = tk.Entry(edit, textvariable=changeusername)
            username_entry.place(x=250, y=107)




            # ===================================== Modify Password [User Profile] ===================================== #
            # password label
            changepassword = tk.Label(edit,fg='white', bg='#132933', text="Password: *", font=("Calibri", 15, "bold"))
            changepassword.place(x=130, y=150)
            # password entry
            password_entry = tk.Entry(edit, textvariable=changepassword, show="*")
            password_entry.place(x=250, y=157)




            # ===================================== Modify Profile [User Profile] ===================================== #
            # get user id
            selecteduser = 'select * FROM user_tbl WHERE username = "%s"' % username
            mycursor.execute(selecteduser)
            results = mycursor.fetchall()
            for getid in results:
                user_id=getid[0]
                break

            # upload image button
            changeprofile = tk.Label(edit, fg='white', bg='#132933', text="Change Profile Image:", font=("Calibri", 15, "bold"))
            changeprofile.place(x=110, y=200)
            def UploadAction(event=None):
                filename = filedialog.askopenfilename()
                print('Selected:', filename)
                file_id = ImageUpload(filename,user_id)
                uploadname = str(user_id)+'.jpg'
                print(file_id)
                ImageDownload(file_id, uploadname)

            # upload the info to sql
                upload_file = f'update user_tbl set profile_image = "{uploadname}", image_id="{file_id}" where username="{username}"'
                mycursor.execute(upload_file)
                db.commit()

            button = tk.Button(edit, text='Select Image', command=UploadAction)
            button.place(x=315, y=205)

            # ======================================= Username & Password Validation (Modify) ======================================= #
            # function to check if username taken/password long enough
            def check_info():
                usern = username_entry.get()
                passw = password_entry.get()
                checkuser = "SELECT username FROM user_tbl"
                mycursor.execute(checkuser)
                userexists = mycursor.fetchall()

                check_symbol= re.compile('[@_!#$%^&*()<>?/\|}{~:]')
                # messagebox.showinfo("Message","Username taken please use another username")
                if len(usern) == 0:
                    messagebox.showinfo("Error", "Username Can\'t be empty")
                elif len(passw) == 0:
                    messagebox.showinfo("Error", "Password Can\'t be empty")
                else:
                    try:
                        # checks if user exists in database
                        # if yes, it will show a error message
                        if userexists:
                            messagebox.showinfo("Error", "Username Already Exists!")
                            if len(passw) > 10:
                                messagebox.showinfo("Error", "Password cant be too long")
                                password_entry.delete(0, tk.END)

                            # chesk if password contain any special characters
                            elif check_symbol.search(passw):
                                messagebox.showinfo("Error", "Password cant contain any special characters")
                                password_entry.delete(0, tk.END)

                            # checks if password contain any whitespace    
                            elif " " in passw:
                                messagebox.showinfo("Error", "Password cant have any spacing in it")
                                password_entry.delete(0, tk.END)
                            
                            else:
                                pass_sql = "UPDATE user_tbl SET password =  '" + passw + "' WHERE username = '" + username + "'"
                                mycursor.execute(pass_sql)
                                db.commit()
                                messagebox.showinfo("Information", "Password Changed")

                                # clears the input box empty after a successful registration process
                                username_entry.delete(0, tk.END)
                                password_entry.delete(0, tk.END)


                        # length of username cant be shorter than 4 characters
                        elif len(usern) <= 4:
                            messagebox.showinfo("Error", "Username cant be too short")
                            username_entry.delete(0, tk.END)
                            password_entry.delete(0, tk.END)

                        # length of username cant exceed 15 characters
                        elif len(usern) > 15:
                            messagebox.showinfo("Error", "Username cant be too long")
                            username_entry.delete(0, tk.END)

                        # checks if username contain any special characters
                        elif check_symbol.search(usern):
                            messagebox.showinfo("Error", "Username cant contain any special characters")
                            username_entry.delete(0, tk.END)

                        # checks if the length of password is more then 10 characters
                        elif len(passw) > 10:
                            messagebox.showinfo("Error", "Password cant be too long")
                            password_entry.delete(0, tk.END)

                        # chesk if password contain any special characters
                        elif check_symbol.search(passw):
                            messagebox.showinfo("Error", "Password cant contain any special characters")
                            password_entry.delete(0, tk.END)

                        # checks if username contain any whitespace
                        elif " " in usern:
                            messagebox.showinfo("Error", "Username cant have any spacing in it")
                            username_entry.delete(0, tk.END)

                        # checks if password contain any whitespace    
                        elif " " in passw:
                            messagebox.showinfo("Error", "Password cant have any spacing in it")
                            password_entry.delete(0, tk.END)
                            
                        else:
                            reg_sql = "UPDATE user_tbl SET username = '" + usern + "', password =  '" + passw + "' WHERE username = '" + username + "'"
                            mycursor.execute(reg_sql)
                            db.commit()
                            messagebox.showinfo("Information", "Username and Password Changed")

                            # clears the input box empty after a successful registration process
                            username_entry.delete(0, tk.END)
                            password_entry.delete(0, tk.END)
                            # edit.destroy()
                            # raise_frame(profile)

                            copycat()
                    except:
                        messagebox.showerror("Error", "There is an error on the code")



            # ===================================== Button [User Profile] ===================================== #
            savebutton = tk.Button(edit, text="Save Changes", command=lambda:check_info())
            savebutton.place(x=250, y=250)

            # # button for edit frame to go back to the main frame
            mainbutton= tk.Button(edit, text="Main", command=lambda: raise_frame(profile))
            mainbutton.place(x=200, y=250)
                    
            # to display the first frame
            raise_frame(profile) 

        



        # ===================================== Admin Main ===================================== #
        def admin(username):
            login.withdraw()
            top = Toplevel()
            top.geometry("450x460")
            top.configure(bg='#132933')
            top.resizable(height=False, width=False)
            top.title("Admin Page")
            global guest_user
            guest_user = username

            # ============================================= Update Listbox [Admin] ============================================= #
            def update(data):

                # delete all records in listbox
                list.delete(0, tk.END)

                # updates listbox
                for row in data:
                    list.insert(list.size()+1, row)


            def check(e):

                user_input = userEntry.get()

                myquery = "SELECT uid, usertype, username FROM user_tbl WHERE NOT usertype = 'admin'"
                mycursor.execute(myquery)
                ui_result = mycursor.fetchall()

                # if input field is empty, list of all user is displayed
                if user_input == '':
                    showuser()
                else:
                    # display users that contains any letter inputted from the search input
                    user_data = []
                    for item in ui_result:
                        uidata = str(item[0])+ '  |  ' +item[1]+ '  |  ' +item[2]
                        if user_input in uidata:
                            user_data.append(uidata)

                    update(user_data)




            # ============================================= Delete [Admin] ============================================= #
            # delete a user in user table  
            def deleteuser():

                username_delete = userEntry.get()

                checkquery = "SELECT * FROM user_tbl WHERE username = '" + username_delete + "'"
                mycursor.execute(checkquery)
                du_result = mycursor.fetchone()

                # if user exist in database, query will execute and remove user
                if du_result:
                    try:
                        deletequery = "DELETE FROM user_tbl WHERE username = '" + username_delete + "'"
                        mycursor.execute(deletequery)

                        db.commit()
                        messagebox.showinfo("", "User has been removed")
                        userEntry.delete(0, tk.END)
                        
                    # if user input field is empty, display message 
                    except:
                        messagebox.showinfo("", "Input field is empty")

                else:
                    messagebox.showinfo("", "User does not exist in database")




            # ============================================= Banning [Admin] ============================================= #
            # ban a user in user table
            def banuser():

                usernameid_ban = userEntry.get()

                checkquery1 = "SELECT uid FROM user_tbl WHERE uid = '" + usernameid_ban + "'"
                mycursor.execute(checkquery1)
                bu_result = mycursor.fetchone()

                # checks if input is a number or letters and if it exist in database 
                if bu_result:
                    # if its a number, user will be banned 
                    try:
                        banquery = "UPDATE user_tbl SET usertype = 'banned' WHERE uid = '" + usernameid_ban + "'"
                        mycursor.execute(banquery)

                        db.commit()
                        messagebox.showinfo("", "User has been banned")
                        userEntry.delete(0, tk.END)
                        showuser()

                    # if its letters, error message will be prompt
                    except ValueError:
                        messagebox.showinfo("", "To banned the user, enter the user ID")
                
                # user does not exist in the database
                else:
                    messagebox.showinfo("", "User does not exist in database")




            # ============================================= Display User [Admin] ============================================= #
            # display all records in user table database
            def showuser():

                showquery = "SELECT uid, usertype, username FROM user_tbl WHERE NOT usertype = 'admin'"
                mycursor.execute(showquery)
                sdresult = mycursor.fetchall()

                list.delete(0, tk.END)

                for row in sdresult:
                    showdata = str(row[0])+ '  |  ' +row[1]+ '  |  ' +row[2]
                    list.insert(list.size()+1, showdata)




            # ============================================= Main [Admin]============================================= #
            wel_admin = tk.Label(top, width=25, fg='white', bg='#132933', text="Welcome back, " + username +"", font=("Calibri", 15, "bold"))
            wel_admin.grid(row=1, column=2, columnspan=5)

            admin_label = tk.Label(top, fg='white', bg='#132933', anchor='center', font=("Calibri", 15, "bold"), text="[To ban user, enter their user id]")
            admin_label.grid(row=2, column=5, columnspan=3, padx=10, pady=5)

            searchUser = tk.Label(top, fg='white', bg='#132933', font=("Calibri", 15, "bold"), text="Username | ID: ")
            searchUser.grid(row=3, column=5, padx=8, pady=8)

            userEntry = tk.Entry(top)
            userEntry.bind("<KeyRelease>", check)
            userEntry.grid(row=3, column=6)

            all_data = tk.Button(top, text="Show All Data", command = lambda: showuser())
            all_data.grid(row=4, column=5, columnspan=3)

            search_button = tk.Button(top, text="Ban", command = lambda: banuser())
            search_button.grid(row=4, column=6, columnspan=2)

            delete_button = tk.Button(top, text="Delete", command = lambda: deleteuser())
            delete_button.grid(row=4, column=7)

            quit_button = tk.Button(top, width=12, text="Quit", command= lambda: quit(top))
            quit_button.grid(row=1, column=8, padx=5, pady=5)

            list = Listbox(top, height=17)
            list.grid(row=6, column=3, columnspan=5, padx=20, pady=20, sticky='nsew')

            showuser()




        def quit(top):
            
            global guest_user
            guest_user = ""
            # destroy user / admin window 
            top.destroy()
            root.update()

            # unminimize window
            root.deiconify()
        




        # ===================================== Login ========================================= #
        def login_verify():
            global username
            username = username_verify.get()
            password = password_verify.get()

            sql = "SELECT * FROM user_tbl WHERE username = %s and password = %s"
            mycursor.execute(sql, [username, password])
            results = mycursor.fetchall()
            
            try:
                # checks whether usertype "listener" is in list
                if 'listener' in results[0]:
                    messagebox.showinfo("Musicfy", "You are logged in..")
                    loguser_entry.delete(0, tk.END)
                    logpass_entry.delete(0, tk.END)
                    login.withdraw()
                    user(username)

                # checks whether usertype "artist" is in list 
                elif 'artist' in results[0]:
                    messagebox.showinfo("Musicfy", "You are logged in..")
                    loguser_entry.delete(0, tk.END)
                    logpass_entry.delete(0, tk.END)
                    login.withdraw()
                    user(username)

                # checks whether usertype "admin" is in list
                elif 'admin' in results[0]:
                    messagebox.showinfo("Musicfy", "Admin logged in..")
                    loguser_entry.delete(0, tk.END)
                    logpass_entry.delete(0, tk.END)
                    login.withdraw()
                    admin(username)


                # checks whether user status is banned
                elif 'banned' in results[0]:
                    messagebox.showinfo("Musicfy", "Your account is banned!")
                    loguser_entry.delete(0, tk.END)
                    logpass_entry.delete(0, tk.END)


            except IndexError:
                messagebox.showinfo("Error", "Incorrect Username or Password!")
                loguser_entry.delete(0, tk.END)
                logpass_entry.delete(0, tk.END)


        username_verify = tk.StringVar()
        password_verify = tk.StringVar()

        # login form code
        login_label = tk.Label(main, text="Welcome to Musicfy", anchor='center', width=20, fg="white", bg='#132933', font=("Calibri", 30, "bold"))
        login_label.grid(row=0, column=0, columnspan=2, padx=20, pady=70)


        # username input code
        loguser_label = tk.Label(main, text="Username: ", fg="white",bg='#132933', font=("Calibri", 25, "bold"))
        loguser_label.grid(row=1, column=0)
        # username entry
        loguser_entry = tk.Entry(main, textvariable=username_verify)
        loguser_entry.grid(row=1, column=1)

        # password input code
        logpass_label = tk.Label(main, text="Password: ", fg="white", bg='#132933', font=("Calibri", 25, "bold"))
        logpass_label.grid(row=2, column=0)
        # password entry
        logpass_entry = tk.Entry(main, textvariable=password_verify, show="*")
        logpass_entry.grid(row=2, column=1)


        # login button in main frame
        loginbutton = tk.Button(main, width=8, fg='#132933', font=("Calibri", 15, "bold"), text="Login", command= login_verify)
        loginbutton.grid(row=3, column=1)


        # sign up button in main frame
        mainbutton = tk.Button(main, text="Sign Up", width=8, fg='#132933', font=("Calibri", 15, "bold"), command=lambda: raise_frame(signup))
        mainbutton.grid(row=3, column=0, columnspan=2, pady=5)




        # ===================================== Sign Up ===================================== #
        def reg_verify():
            usern = reg_username.get()
            passw = reg_password.get()
            checkuser = "SELECT username FROM user_tbl WHERE username = %s"
            mycursor.execute(checkuser, (usern, ))
            userexists = mycursor.fetchall()

            check_symbol= re.compile('[@_!#$%^&*()<>?/\|}{~:]')

            if len(usern) == 0:
                messagebox.showinfo("Error", "Username Can\'t be empty")
            elif len(passw) == 0:
                messagebox.showinfo("Error", "Password Can\'t be empty")
            else:
                try:
                    # cheks if user exists in database
                    # if yes, it will show a error message
                    if userexists:
                        messagebox.showinfo("Error", "Username Already Exists!")
                        reguser_entry.delete(0, tk.END)
                        regpass_entry.delete(0, tk.END)

                    # length of username cant be shorter than 4 characters
                    elif len(usern) <= 4:
                        messagebox.showinfo("Error", "Username cant be too short")
                        reguser_entry.delete(0, tk.END)
                        regpass_entry.delete(0, tk.END)

                    # length of username cant exceed 15 characters
                    elif len(usern) > 15:
                        messagebox.showinfo("Error", "Username cant exceed 15 characters")
                        reguser_entry.delete(0, tk.END)

                    # checks if username contain any special characters
                    elif check_symbol.search(usern):
                        messagebox.showinfo("Error", "Username cant contain any special characters")
                        reguser_entry.delete(0, tk.END)

                    # checks if the length of password is more than 10 characters
                    elif len(passw) > 10:
                        messagebox.showinfo("Error", "Password cant exceed 10 characters")
                        regpass_entry.delete(0, tk.END)

                    # checks if the length of password is less than 4 characters
                    elif len(passw) <= 4:
                        messagebox.showinfo("Error", "Password cant be shorter than 4 characters")
                        regpass_entry.delete(0, tk.END)

                    # chesk if password contain any special characters
                    elif check_symbol.search(passw):
                        messagebox.showinfo("Error", "Password cant contain any special characters")
                        regpass_entry.delete(0, tk.END)

                    # checks if username contain any whitespace
                    elif " " in usern:
                        messagebox.showinfo("Error", "Username cant have any spacing in it")
                        reguser_entry.delete(0, tk.END)

                    # checks if password contain any whitespace    
                    elif " " in passw:
                        messagebox.showinfo("Error", "Password cant have any spacing in it")
                        regpass_entry.delete(0, tk.END)
                        
                    else:
                        reg_sql = "INSERT INTO user_tbl (usertype, username, password) VALUES (%s, %s, %s)"
                        reg_val = ("listener", usern, passw)
                        mycursor.execute(reg_sql, reg_val)
                        db.commit()
                        messagebox.showinfo("Information", "Registration Successfull")

                        reg_username.set("")
                        reg_password.set("")

                        # clears the input box empty after a successful registration process
                        reguser_entry.delete(0, tk.END)
                        regpass_entry.delete(0, tk.END) 
                except:
                    messagebox.showerror("Error", "There is an error on the code")


        reg_username = tk.StringVar()
        reg_password = tk.StringVar()

        # sign up section in signup frame
        # signup button, navigate to signup frame
        signuplabel = tk.Label(signup, text="Sign Up", anchor="center", width=20, fg="white", bg="#132933", font=("Calibri", 30, "bold"))
        signuplabel.grid(row=0, column=0, columnspan=2, padx=20, pady=70)

        # username label
        reguser_label = tk.Label(signup, text="Username: *", fg="white",bg='#132933', font=("Calibri", 25, "bold"))
        reguser_label.grid(row=1, column=0)
        # username entry
        reguser_entry = tk.Entry(signup, textvariable=reg_username)
        reguser_entry.grid(row=1, column=1)

        # password label
        regpass_label = tk.Label(signup, text="Password: *", fg="white", bg='#132933', font=("Calibri", 25, "bold"))
        regpass_label.grid(row=2, column=0)
        # password entry
        regpass_entry = tk.Entry(signup, textvariable=reg_password, show="*")
        regpass_entry.grid(row=2, column=1)

        # button for signup
        signupbutton = tk.Button(signup, width=8, fg='#132933', font=("Calibri", 15, "bold"), text="Confirm", command=reg_verify)
        signupbutton.grid(row=3, column=1)

        # button for signup frame to go back to the main frame
        signupbuttonb = tk.Button(signup, width=8, fg='#132933', font=("Calibri", 15, "bold"), text="Main", command=lambda: raise_frame(main))
        signupbuttonb.grid(row=3, column=0, columnspan=2, pady=5)

        # run gui application window
        raise_frame(main)
        login.mainloop()

# ====================== Left Side============================================== #
# namtung code
# Left Side
if True:
    left_frame = tk.Frame(root, height="600", width="400", padx=5, pady=5, bg="#132933")
    left_frame.configure(height=left_frame["height"],width=left_frame["width"])
    left_frame.grid_propagate(0)

    # Prerequisite
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

            # Search scope
            global is_song
            global is_playlist
            global is_artist
            is_song = song_var.get()
            is_playlist = playlist_var.get()
            is_artist = artist_var.get()

            #actual search
            def run_search_artist(result_num, result_list):
                searchAudioQuery = "select username from user_tbl where usertype = 'artist' and username like '%{}%'".format(u_search)
                mycursor.execute(searchAudioQuery)
                myresult = mycursor.fetchall()

                # Save in global
                global search_result_3
                search_result_3 = myresult

                # Get result
                if not is_playlist:
                    result_list = [result_list]
                temp_re_list = []
                for x in myresult:
                    artistName = x[0] # Potato code because it will wait until it load all songs (maybe limit/ use pages)
                    # playlist_user = x[1]
                    result_num += 1

                    temp_re_list.append(artistName)
                result_reportEntry.set("{} Results Found".format(result_num))
                result_list.append(temp_re_list)

                # Display result in listbox / search artist
                result_listbox.delete(0,"end")
                if is_song and is_playlist:
                    for audioname in result_list[0]:
                        result_listbox.insert('end',  "Audio | " + audioname)
                    for playlistname in result_list[1]:
                        result_listbox.insert('end', "Playlist | "+ playlistname)
                    for artistname in result_list[2]:
                        result_listbox.insert('end', "Artist | "+ artistname)
                    result_listbox.grid(row=0,column=0, padx=10)
                elif is_song == False and is_playlist == True:
                    for playlistname in result_list[1]:
                        result_listbox.insert('end', "Playlist | "+ playlistname)
                    for artistname in result_list[2]:
                        result_listbox.insert('end', "Artist | "+ artistname)
                    result_listbox.grid(row=0,column=0, padx=10)
                elif is_playlist == False and is_song == True:
                    for audioname in result_list[0]:
                        result_listbox.insert('end',  "Audio | " + audioname)
                    for artistname in result_list[1]:
                        result_listbox.insert('end', "Artist | "+ artistname)
                    result_listbox.grid(row=0,column=0, padx=10)
                else:
                    for artistname in result_list[1]:
                        result_listbox.insert('end', "Artist | "+ artistname)
                    result_listbox.grid(row=0,column=0, padx=10)


            def run_search_playlist(result_num, result_list):
                searchAudioQuery = "select playlist_name, username from playlist_tbl p, user_tbl u where (p.uid = u.uid) and playlist_name like '%{}%'".format(u_search)
                mycursor.execute(searchAudioQuery)
                myresult = mycursor.fetchall()

                # Save in global
                global search_result_2
                search_result_2 = myresult

                # Get result
                nd_result_list = [result_list]
                temp_re_list = []
                for x in myresult:
                    playlistName = x[0] # Potato code because it will wait until it load all songs (maybe limit/ use pages)
                    # playlist_user = x[1]
                    result_num += 1

                    temp_re_list.append(playlistName)
                result_reportEntry.set("{} Results Found".format(result_num))
                nd_result_list.append(temp_re_list)

                # Display result in listbox / search artist
                if is_artist:
                    run_search_artist(result_num, nd_result_list)
                else:
                    result_listbox.delete(0,"end")
                    for audioname in nd_result_list[0]:
                        result_listbox.insert('end',  "Audio | " + audioname)
                    for playlistname in nd_result_list[1]:
                        result_listbox.insert('end', "Playlist | "+ playlistname)
                    result_listbox.grid(row=0,column=0, padx=10)

            def run_search_song():
                searchAudioQuery ="select aid, audio_name, uid, audio_path from audio_tbl where audio_name like" + "'%" + u_search + "%';"
                mycursor.execute(searchAudioQuery)
                myresult = mycursor.fetchall()


                #search_result_handle(myresult)
                # Save in global
                global search_result
                search_result = myresult
                
                # Get result
                result_list = []
                result_num = 0
                
                for x in myresult:
                    # a_aid = x[0]
                    a_name = x[1]
                    # a_path = x[2]
                    result_num += 1

                    result_list.append(a_name)
                result_reportEntry.set("{} Results Found".format(result_num))

                # Check other search/Display result in listbox
                if is_playlist:
                    run_search_playlist(result_num, result_list)
                elif is_artist:
                    run_search_artist(result_num, result_list)
                else:
                    result_listbox.delete(0,"end")
                    for audioname in result_list:
                        result_listbox.insert('end', "Audio | " + audioname)
                    result_listbox.grid(row=0,column=0, padx=10)

            if is_song:
                run_search_song()
            elif is_playlist:
                run_search_playlist(0,[])
            elif is_artist:
                run_search_artist(0,[])




        # For select from listbox
        def pick_from_list():
            # Get selection from listbox
            try:
                cs = result_listbox.curselection()
                item_picked = result_listbox.get(cs)
            except (UnboundLocalError, tk.TclError) as Error:
                pass
            
            try:
                # If song selected from search
                if "Audio | " in item_picked:
                    item_picked = item_picked.replace("Audio | ","")
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
                    

                    searchAudioQuery ="select sum(like_status) from like_tbl where aid = {}".format(item_id)
                    mycursor.execute(searchAudioQuery)
                    myresult = mycursor.fetchall()
                    for i in myresult:
                        for j in i:
                            likenum = j
                    entryLikenum.set("{}".format(likenum))

                if "Playlist | " in item_picked:
                    item_picked = item_picked.replace("Playlist | ","")
                    entryPlaylist_name.set("{}".format(item_picked))

                    for i in search_result_2:
                        if item_picked == i[0]:
                            entryPlaylist_user.set(i[1])
                    
                    searchAudioQuery ="select a.aid, a.audio_name, a.audio_path, a.uid from song_in_playlist s, playlist_tbl p, audio_tbl a where (s.pid = p.pid) and (s.aid = a.aid) and playlist_name = '{}'".format(item_picked)
                    mycursor.execute(searchAudioQuery)
                    myresult = mycursor.fetchall()

                    list_songs = []
                    for songs in myresult:
                        songid = songs[0]
                        songname = songs[1]
                        songpath = songs[2]
                        songartist = songs[3]

                        list_songs.append(songname)
                
                    playlist_Listbox.delete(0,"end")
                    for audioname in list_songs:
                        playlist_Listbox.insert('end', audioname)
                    playlist_Listbox.grid(row=2,column=0)

                if "Artist | " in item_picked:
                    item_picked = item_picked.replace("Artist | ","")
                    entryArtist_name.set("{}".format(item_picked))

                    # search_result_3 = username of the artist

                    searchAudioQuery ="select sum(l.like_status) from like_tbl l, audio_tbl a, user_tbl u where a.aid = l.aid and a.uid = u.uid and u.username = '{}'".format(item_picked)
                    mycursor.execute(searchAudioQuery)
                    myresult = mycursor.fetchall()
                    for i in myresult:
                        for j in i:
                            total_like_received = j
                    entryArtist_like.set("{}".format("Likes Received: "+ str(total_like_received)))

                    # select sum(like_status) from like_tbl where uid = 1
                    searchAudioQuery ="select a.audio_name from audio_tbl a, user_tbl u where (a.uid = u.uid) and u.username = '{}'".format(item_picked)
                    mycursor.execute(searchAudioQuery)
                    myresult = mycursor.fetchall()

                    songlist = []
                    for j in myresult:
                        for i in j:
                            arsongname = i
                            songlist.append(arsongname)
                
                    artist_Listbox.delete(0,"end")
                    for audioname in songlist:
                        artist_Listbox.insert('end', audioname)
                    artist_Listbox.grid(row=2,column=0)
            except:
                pass




    # top top left
    if True:
        top_frame = tk.Frame(left_frame, height=35, width="400", padx=5, pady=5, bg="#132933")
        top_frame.configure(height=top_frame["height"],width=top_frame["width"])
        top_frame.grid_propagate(0)

        profileButton = tk.Button(top_frame, text="Profile", padx=100, height=1, command = lambda: check_username(guest_user))
        profileButton.grid(row=0, column=0, padx= 30)
        quitButton = tk.Button(top_frame, text="Quit", height=1, padx=20, command= lambda: quit())
        quitButton.grid(row=0, column=1) 

        def check_username(guest_user):
            if guest_user == "":
                login_win()
                
            else:
                user(guest_user)

        def quit():

            root.destroy()

        top_frame.grid(row=0, column=0)


    # Top left
    if True:
        tl_frame = tk.LabelFrame(left_frame, height=100, width=380, bg="#132933", highlightthickness=0, border=0)

        # Creating label for search bar
        searchLabel = tk.Label(tl_frame, text = "Search: ", font = ('Calibri', 15, 'bold'), fg="white", bg="#132933")
        # searchLabel.grid(row = 0, column = 0, columnspan=3)
        searchLabel.place(x=10, y=1)
        # Creating input bar
        searchBar = tk.Entry(tl_frame, width=40)
        # searchBar.grid(row = 1, column = 0, columnspan=2)
        searchBar.place(x=80, y=7)
        # Search Button
        searchButton = tk.Button(tl_frame, width=20, text = "Search", command = check_valid)
        # searchButton.grid(row = 1, column = 2)
        searchButton.place(x=175, y=30)

        # Checkboxes for artist, songs and playlist
        song_var = tk.IntVar()
        song_chk = tk.Checkbutton(tl_frame, text="Song", variable=song_var, fg="#637da6", bg="#132933", font=("Calibri", 12, "bold"))
        song_chk.select()
        song_chk.place(x=50, y=60)

        playlist_var = tk.IntVar()
        playlist_chk = tk.Checkbutton(tl_frame, text="Playlist", variable=playlist_var, fg="#637da6", bg="#132933", font=("Calibri", 12, "bold"))
        playlist_chk.select()
        playlist_chk.place(x=130, y=60)

        artist_var = tk.IntVar()
        artist_chk = tk.Checkbutton(tl_frame, text="Artist", variable=artist_var, fg="#637da6", bg="#132933", font=("Calibri", 12, "bold"))
        artist_chk.select()
        artist_chk.place(x=230, y=60)



        tl_frame.grid(row=1, column=0)


    # Bottom left
    if True:
        bl_frame = tk.LabelFrame(left_frame, text="Searched Songs", padx=5, pady=5, bg="#132933", border=0)
        bl_frame.config(fg='white', font=("Calibri", 15, 'bold'))
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



        bl_frame.grid(row=2, column=0)

    left_frame.grid(row=0, column=0)


# ===================== Right Side============================================== #

# Right Side
if True:
    right_frame = tk.Frame(root, height="600", width="400", padx=5, pady=5, bg="#132933")
    right_frame.configure(height=right_frame["height"],width=right_frame["width"])
    right_frame.grid_propagate(0)

    # Prerequisite
    if True:

        #Music player
        def playSong():
            try:

                # Clarence
                if True:
                    pass
                
                # if play a single song
                if type(selected_path) == str:
                    pg.mixer.music.load(r"{}".format(selected_path))
                    pg.mixer.music.play(-1)
                    temp_name = entryText_name.get()
                    entryPlayingAudio.set("{}".format(temp_name))
                    pauseButton["text"] = "▮▮"
                
                #if play a playlist
                elif type(selected_path) == list:
                    try:
                        temp_name = selectedPlaylist_name.get()
                        entryPlayingAudio.set("{}".format(temp_name))

                        sql ="select audio_path from audio_tbl where audio_name = '{}';".format(song_in_playlist_now)
                        mycursor.execute(sql)
                        myresult = mycursor.fetchall()
                        for i in myresult:
                            for j in i:
                                song_path_now = j

                        index = selected_path.index(song_path_now)
                        
                        # load selected music
                        pg.mixer.music.load(r"{}".format(selected_path[index]))

                        # remove current, previous from list
                        z = 0
                        while z <= index:
                            selected_path.pop(0)
                            z += 1
                        
                        # play selected
                        pg.mixer.music.play()

                        # load second song
                        pg.mixer.music.queue(selected_path[0])
                        selected_path.pop(0)

                        # set event occur after end of song
                        pg.mixer.music.set_endevent(pg.USEREVENT)
                        
                        pauseButton["text"] = "▮▮"

                        # play whole playlist
                        running = True
                        
                        try:

                            while running:
                                # pg.init()

                                event_get = pg.event.get()

                                # checking if any event has been
                                # hosted at time of playing
                                for event in event_get:
                                    
                                    print("Event here")
                                    print(event)
                                    
                                    # A event will be hosted
                                    # after the end of every song
                                    if event.type == pg.USEREVENT:
                                        print('Song Finished')
                                        
                                        # Checking our playList
                                        # that if any song exist or
                                        # it is empty
                                        if len(selected_path) > 0:
                                            
                                            # if song available then load it in player
                                            # and remove from the player
                                            pg.mixer.music.queue(selected_path[0])
                                            selected_path.pop(0)
                                    # Checking whether the 
                                    # player is still playing any song
                                    # if yes it will return true and false otherwise
                                    if not pg.mixer.music.get_busy():
                                        print("Playlist completed")
                                    # if len(selected_path) ==0:
                                        
                                        # When the playlist has
                                        # completed playing successfully
                                        # we'll go out of the
                                        # while-loop by using break
                                        running = False

                                        # pg.quit()
                                        # pg.mixer.init()

                                        break
                        except:
                            # it will have pygame video not initialist error, but we didnt use that so ..
                            # plus if import all from pygame it will bug
                            pass
                    except:
                        pass



            except NameError:
                print("No item (songs) selected yet")

        def pauseSong():
            if pauseButton["text"] == "▶":
                pauseButton["text"] = "▮▮"
                pauseButton["bg"] = "white"
                pg.mixer.music.unpause()
            else:
                pauseButton["text"] = "▶"
                pauseButton["bg"] = "white"
                pg.mixer.music.pause()

        def stopSong():
            pg.mixer.music.stop()
        
        def volup():
            x = pg.mixer.music.get_volume()
            if (x <= 1.0) and (x >= 0):
                x += 0.1
            if (x <= 1.0) and (x >= 0):
                pg.mixer.music.set_volume(x)
                # x = x * 100
                # int(x)
                # volnowButton["text"] = "{}".format(x)


        def voldown():
            x = pg.mixer.music.get_volume()
            if (x <= 1.0) and (x >= 0):
                x -= 0.1
            if (x <= 1.0) and (x >= 0):
                pg.mixer.music.set_volume(x)
                # x = x * 100
                # int(x)
                # volnowButton["text"] = "{}".format(x)



        def add_to_playlist():
            if guest_user=="":
                login_win()
            else:
                #song name
                tobeadded = entryText_name.get()

                # new window
                root.withdraw()
                cpl = Toplevel()
                cpl.geometry("500x400")
                cpl.title("My Playlist")
                # cpl.resizable(height=False, width=False)

                # get username
                temp_name = guest_user
                #get uid with username 
                searchQuery = "select uid from user_tbl where username = '{}'".format(temp_name)
                mycursor.execute(searchQuery)
                myresult = mycursor.fetchall()
                for i in myresult:
                    for j in i:
                        uid = j

                upframecp = tk.Frame(cpl, height="250", width="500", padx=5, pady=5, bg="#132933")
                upframecp.configure(height=upframecp["height"],width=upframecp["width"])
                upframecp.grid_propagate(0)
                # View own playlist and its song
                if True:

                    def dissam():
                        try:
                            cs = samlistbox.curselection()
                            plsam = samlistbox.get(cs)
                        except (UnboundLocalError, tk.TclError) as Error:
                            pass

                        global pickkplname
                        pickkplname = plsam

                        searchQuery = "select a.audio_name from audio_tbl a, playlist_tbl p, song_in_playlist s where (p.pid = s.pid) and (a.aid = s.aid) and playlist_name = '{}'".format(plsam)
                        mycursor.execute(searchQuery)
                        myresult = mycursor.fetchall()
                        listsg = []
                        for i in myresult:
                            for j in i:
                                listsg.append(j)
                        
                        sam2listbox.delete(0,"end")
                        for i in listsg:
                            sam2listbox.insert("end", i)
                        sam2listbox.grid(row=1, column=1)

                        # remove song selected from previous playlist
                        varsg.set('')

                    lblabel = tk.Label(upframecp, text = "Your playlist", fg='white', bg='#132933', font=("Calibri", 12, 'bold'))
                    lblabel.grid(row=0, column = 0)

                    samlistbox = tk.Listbox(upframecp, height=25, width=40)
                    samlistbox.bind('<<ListboxSelect>>', lambda x: dissam())
                    samlistbox.grid(row=1, column=0) 

                    # fill in playlist name in listbox
                    if True:
                        query = "select playlist_name from playlist_tbl where uid = '{}'".format(uid)
                        mycursor.execute(query)
                        myresult = mycursor.fetchall()
                        listpl = []
                        for i in myresult:
                            for j in i:
                                listpl.append(j)
                        
                        samlistbox.delete(0,"end")
                        for playname in listpl:
                            samlistbox.insert('end', playname)
                        samlistbox.grid(row=1,column=0)
                


                    def dissam2():
                        try:
                            cs = sam2listbox.curselection()
                            plsam2 = sam2listbox.get(cs)
                            
                            varsg.set('{}'.format(plsam2))
                        
                        except (UnboundLocalError, tk.TclError) as Error:
                            pass
                        
                    
                    lb2label = tk.Label(upframecp, text ="Songs in playlist", fg='white', bg='#132933', font=("Calibri", 12, 'bold'))
                    lb2label.grid(row=0, column=1)

                    sam2listbox = tk.Listbox(upframecp, height=25, width=40)
                    sam2listbox.bind('<<ListboxSelect>>', lambda x: dissam2())
                    sam2listbox.grid(row=1,column=1)

                upframecp.grid()

                # Bottom part (functions)
                downframecp = tk.Frame(cpl, height="250", width="500", padx=5, pady=5, bg="#132933")
                downframecp.configure(height=downframecp["height"],width=downframecp["width"])
                downframecp.grid_propagate(0)


                if True:
                    # For create playlist
                    inframe_down3 = tk.LabelFrame(downframecp, bg="#132933", border=0)
                    inframe_down3.place(x=15, y=15)

                    # verify playlist no exist, if suc then insert
                    def createpl():

                        temp_uname = guest_user
                        if guest_user == "":
                            login_win()
                        else:
                            def nice_sub():
                                query ="select uid from user_tbl where username = '{}'".format(temp_uname)
                                mycursor.execute(query)
                                myresult = mycursor.fetchall() 
                                for i in myresult:
                                    for j in i:
                                        uid = i

                                sql = "update user_tbl set subscription = 1 where uid = '{}'".format(uid)
                                mycursor.execute(sql)
                                db.commit()

                            
                            query = "select subscription from user_tbl where username = '{}'".format(temp_uname)
                            mycursor.execute(query)
                            myresult = mycursor.fetchall()
                            for i in myresult:
                                for j in i:
                                    is_sub = j
                            
                            if is_sub == 0:
                                cpl.withdraw()
                                subwin = Toplevel()
                                subwin.geometry("250x200")
                                subwin.title("Subscribe!")
                                subwin.configure(bg='#132933')
                                subwin.resizable(width=False, height=False)

                                subtitlabel = tk.Label(subwin, text="Oops! You are not subscribed... \n  Please Subscribe to Support Us", fg='white', bg='#132933', font=("Calibri", 12, 'bold'))
                                subtitlabel.place(x=10, y=6)

                                label_sample = tk.Label(subwin, text="Payment Details :", fg='white', bg='#132933', font=("Calibri", 10, 'bold'))
                                label_sample.place(x=3, y=70)
                                entry_sample1 = tk.Entry(subwin)
                                entry_sample1.place(x=110, y=70)


                                label_sample2 = tk.Label(subwin, text="Password :", fg='white', bg='#132933', font=("Calibri", 10, 'bold'))
                                label_sample2.place(x=3, y=100)
                                entry_sample2 = tk.Entry(subwin)
                                entry_sample2.place(x=110, y=100)

                                button_sample = tk.Button(subwin, text="Confirm", command=nice_sub)
                                button_sample.place(x=180, y=125)

                                subBackButton = tk.Button(subwin, text="Back", command= lambda: subButton())
                                subBackButton.place(x=135, y=125)

                                def subButton():
                                    subwin.destroy()
                                    cpl.update()
                                    cpl.deiconify()

                            else:
                        
                                execute_cr = False
                                listex = []
                                varplname = entered_name.get()

                                if len(varplname) <= 3:
                                    messagebox.showinfo("Error", "Playlist name cannot be too short!")
                                elif len(varplname) >= 50:
                                    messagebox.showinfo("Error", "Playlist name cannot be too long!")
                                else:
                                    # search existing playlist
                                    searchQuery = "select p.playlist_name from playlist_tbl p"
                                    mycursor.execute(searchQuery)
                                    myresult = mycursor.fetchall()
                                    print(myresult)
                                    for i in myresult:
                                        for j in i:
                                            listex.append(j)
                                    if varplname not in listex:
                                        execute_cr = True
                                    else:
                                        messagebox.showinfo("Error", "Playlist exist!")

                                if execute_cr:
                                    insertnewplaylist = "insert into `playlist_tbl` (uid, playlist_name) values ('{}','{}');".format(uid, varplname)
                                    mycursor.execute(insertnewplaylist)
                                    db.commit()
                                    messagebox.showinfo("Error", "Playlist Created!")

                                    #refresh
                                    query = "select playlist_name from playlist_tbl where uid = '{}'".format(uid)
                                    mycursor.execute(query)
                                    myresult = mycursor.fetchall()
                                    listpl = []
                                    for i in myresult:
                                        for j in i:
                                            listpl.append(j)
                                    
                                    samlistbox.delete(0,"end")
                                    for playname in listpl:
                                        samlistbox.insert('end', playname)
                                    samlistbox.grid(row=1,column=0)

                    # for create new playlsit
                    elabel = tk.Label(inframe_down3, text= 'New Playlist Name: ', fg='white', bg='#132933', font=("Calibri", 12, 'bold'))
                    elabel.grid(row=0, column=1)

                    entered_name = tk.StringVar()
                    entrynew = tk.Entry(inframe_down3, textvariable=entered_name)
                    entrynew.grid(row=1, column=1)

                    create_button = tk.Button(inframe_down3, text="Create", command=createpl)
                    create_button.grid(row=2, column=1, padx=5, pady=5)






                    # For remove song from playlst
                    inframe_down = tk.LabelFrame(downframecp, bg="#132933", border=0)
                    inframe_down.place(x=180, y=15)

                    def remol():

                        plsam = pickkplname
                        query = "select pid from playlist_tbl where playlist_name = '{}';".format(plsam)
                        mycursor.execute(query)
                        myresult = mycursor.fetchall()
                        for i in myresult:
                            for j in i:
                                pid = j
                        

                        remolsgname = entrysg.get()
                        query = "select aid from audio_tbl where audio_name = '{}';".format(remolsgname)
                        mycursor.execute(query)
                        myresult = mycursor.fetchall()
                        for i in myresult:
                            for j in i:
                                aid = j
                        
                        remolsong = "delete from song_in_playlist where pid = '{}' and aid = '{}';".format(pid, aid)
                        mycursor.execute(remolsong)
                        db.commit()
                    
                    # for delete song from playlist
                    labelsg = tk.Label(inframe_down, text = "Song selected :", fg='white', bg='#132933', font=("Calibri", 12, 'bold'))
                    labelsg.grid(row=0, column= 0)

                    global varsg
                    varsg = tk.StringVar()
                    entrysg = tk.Entry(inframe_down, textvariable=varsg, state=DISABLED)
                    entrysg.grid(row=1, column= 0)

                    buttonsg = tk.Button(inframe_down, text="Remove from playlist", command=remol)
                    buttonsg.grid(row=2, column=0, padx=5, pady=5)







                    # add song to playlsit
                    inframe_down2 = tk.LabelFrame(downframecp, bg="#132933", border=0)
                    # inframe_down2.grid(row=0,column=1)
                    inframe_down2.place(x=335, y=15)
                    def addmol():
                        plsam = pickkplname
                        query = "select pid from playlist_tbl where playlist_name = '{}';".format(plsam)
                        mycursor.execute(query)
                        myresult = mycursor.fetchall()
                        for i in myresult:
                            for j in i:
                                pid = j
                        
                        picked_sg = entryText_name.get()
                        query = "select aid from audio_tbl where audio_name = '{}';".format(picked_sg)
                        mycursor.execute(query)
                        myresult = mycursor.fetchall()
                        for i in myresult:
                            for j in i:
                                aid = j
                        print(picked_sg)
                        addmolsong = "insert into song_in_playlist (pid,aid) values({},{});".format(pid, aid)
                        mycursor.execute(addmolsong)
                        db.commit()



                    # add song to playlist
                    labelsg2 = tk.Label(inframe_down2, text = "Song selected :", fg='white', bg='#132933', font=("Calibri", 12, 'bold'))
                    labelsg2.grid(row=0, column= 0)

                    picked_sg = tk.StringVar()
                    
                    picked_sg.set('{}'.format(tobeadded))

                    entrysg2 = tk.Entry(inframe_down2, textvariable=picked_sg, state=DISABLED)
                    entrysg2.grid(row=1, column= 0)

                    buttonsg2 = tk.Button(inframe_down2, text="Add to playlist", command=addmol)
                    buttonsg2.grid(row=2, column=0, padx=5, pady=5)

                    myplaylist_back = tk.Button(downframecp, width=15, text="Back", command= lambda: backButton())
                    myplaylist_back.place(x=190, y=115)

                def backButton():
                    cpl.destroy()
                    root.update()
                    root.deiconify()

            downframecp.grid()



        def like_song():
            if guest_user=="":
                login_win()
            else:
                temp_name = entryText_name.get()
                temp_artist = entryText_artist.get()
                sql ="select a.aid from audio_tbl a, user_tbl u where u.username = '{}' and a.audio_name = '{}'".format(temp_artist, temp_name)
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                for i in myresult:
                    for j in i:
                        aid = j
                sql ="select uid from user_tbl where username = '{}'".format(guest_user)
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                for i in myresult:
                    for j in i:
                        uid = j

                chklikeQuery = "select like_status from like_tbl where aid = '{}' and uid = '{}'".format(aid, uid)
                mycursor.execute(chklikeQuery)
                if mycursor.fetchall() ==[]:
                    likeQuery = "insert into like_tbl (aid, uid, like_status) values({},{},{});".format(aid, uid, '1')
                    mycursor.execute(likeQuery)
                    db.commit() 
                else:
                    likeQuery = "Update like_tbl set like_status = '1' where aid = '{}' and uid ='{}' ".format(aid, uid)
                    mycursor.execute(likeQuery)
                    db.commit()

                searchAudioQuery ="select sum(like_status) from like_tbl where aid = {}".format(aid)
                mycursor.execute(searchAudioQuery)
                myresult = mycursor.fetchall()
                for i in myresult:
                    for j in i:
                        likenum = j
                entryLikenum.set("{}".format(likenum))
                
        
        def dislike_song():
            if guest_user=="":
                login_win()
            else:
                temp_name = entryText_name.get()
                temp_artist = entryText_artist.get()
                sql ="select a.aid from audio_tbl a, user_tbl u where u.username = '{}' and a.audio_name = '{}'".format(temp_artist, temp_name)
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                for i in myresult:
                    for j in i:
                        aid = j
                sql ="select uid from user_tbl where username = '{}'".format(guest_user)
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                for i in myresult:
                    for j in i:
                        uid = j
                dislikeQuery = "Update like_tbl set like_status = '0'  where aid = '{}' and uid ='{}' ".format(aid, uid)
                mycursor.execute(dislikeQuery)
                db.commit()

                searchAudioQuery ="select sum(like_status) from like_tbl where aid = {}".format(aid)
                mycursor.execute(searchAudioQuery)
                myresult = mycursor.fetchall()
                for i in myresult:
                    for j in i:
                        likenum = j
                entryLikenum.set("{}".format(likenum))


        def pick_artist():
            try:
                cs = artist_Listbox.curselection()
                item_picked_artist = artist_Listbox.get(cs)
                entryText_name.set("{}".format(item_picked_artist))

                searchAudioQuery ="select aid, audio_name, uid, audio_path from audio_tbl where audio_name like" + "'%" + item_picked_artist + "%';"
                mycursor.execute(searchAudioQuery)
                myresult = mycursor.fetchall()
                #Artist of the song (uploader)
                for i in myresult:
                    if i[1] == item_picked_artist:
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
                
                searchAudioQuery ="select sum(like_status) from like_tbl where aid = {}".format(item_id)
                mycursor.execute(searchAudioQuery)
                myresult = mycursor.fetchall()
                for i in myresult:
                    for j in i:
                        likenum = j
                entryLikenum.set("{}".format(likenum))
            except (UnboundLocalError, tk.TclError) as Error:
                pass

        def pick_playlist():
            try:
                cs = playlist_Listbox.curselection()
                item_picked_playlist = playlist_Listbox.get(cs)
                entryText_name.set("{}".format(item_picked_playlist))

                searchAudioQuery ="select aid, audio_name, uid, audio_path from audio_tbl where audio_name like" + "'%" + item_picked_playlist + "%';"
                mycursor.execute(searchAudioQuery)
                myresult = mycursor.fetchall()
                #Artist of the song (uploader)
                for i in myresult:
                    if i[1] == item_picked_playlist:
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
                
                searchAudioQuery ="select sum(like_status) from like_tbl where aid = {}".format(item_id)
                mycursor.execute(searchAudioQuery)
                myresult = mycursor.fetchall()
                for i in myresult:
                    for j in i:
                        likenum = j
                entryLikenum.set("{}".format(likenum))
            
            except (UnboundLocalError, tk.TclError) as Error:
                pass
        
        def select_playlist():            
            
            select_Pname = entryPlaylist_name.get()
            select_Puser = entryPlaylist_user.get()
            
            selectedPlaylist_name.set("{}".format(select_Pname))
            # selectedPlaylist_user.set("{}".format(select_Puser))


            searchAudioQuery ="select a.aid, a.audio_name, a.audio_path, a.uid from song_in_playlist s, playlist_tbl p, audio_tbl a where (s.pid = p.pid) and (s.aid = a.aid) and playlist_name = '{}'".format(select_Pname)
            mycursor.execute(searchAudioQuery)
            myresult = mycursor.fetchall()

            list_songs = []
            for songs in myresult:
                songid = songs[0]
                songname = songs[1]
                songpath = songs[2]
                songartist = songs[3]

                list_songs.append(songname)
        
            selected_Listbox.delete(0,"end")
            for audioname in list_songs:
                selected_Listbox.insert('end', audioname)
            selected_Listbox.grid(row=2,column=0)



        def pick_selected_p():

            #playlist name
            # maybe get both playlist owner also to get accurate playlist id, but hey, deadline. (if improve, use pid line1547)
            current_pl_name = selectedPlaylist_name.get()

            #selected_Listbox
            try:
                cs = selected_Listbox.curselection()
                global song_in_playlist_now
                song_in_playlist_now = selected_Listbox.get(cs)
                entryText_name.set("{}".format(song_in_playlist_now))

                searchAudioQuery ="select aid, audio_name, uid, audio_path from audio_tbl where audio_name like" + "'%" + song_in_playlist_now + "%';"
                mycursor.execute(searchAudioQuery)
                myresult = mycursor.fetchall()
                #Artist of the song (uploader)
                for i in myresult:
                    if i[1] == song_in_playlist_now:
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
                
                searchAudioQuery ="select sum(like_status) from like_tbl where aid = {}".format(item_id)
                mycursor.execute(searchAudioQuery)
                myresult = mycursor.fetchall()
                for i in myresult:
                    for j in i:
                        likenum = j
                entryLikenum.set("{}".format(likenum))

                searchAudioQuery ="select a.audio_name, a.audio_path from playlist_tbl p, song_in_playlist s, audio_tbl a where ((p.pid = s.pid) and (a.aid = s.aid)) and p.playlist_name = '{}'".format(current_pl_name)
                mycursor.execute(searchAudioQuery)
                myresult = mycursor.fetchall()
                path_list =[]
                for i in myresult:
                    path_list.append(i[1])
                # print(path_list)
                global selected_path
                selected_path = path_list

            except (UnboundLocalError, tk.TclError) as Error:
                pass



    # #Top & Mid Right
    if True:
        tr_frame = tk.Frame(right_frame, height=380, width=400, bg="#132933")
        tr_frame.configure(height=tr_frame["height"],width=tr_frame["width"])
        tr_frame.grid_propagate(0)

        # top right details
        if True:
            tr_in_frame = tk.LabelFrame(tr_frame, text="Audio Details", padx=100, pady=3, bg='#132933', border=0)
            tr_in_frame.config(fg='white', font=("Calibri", 15, 'bold'))
            # tr_in_frame.configure(height=tr_frame["height"],width=tr_frame["width"])
            # tr_in_frame.grid_propagate(0)
            if True:
                # Labels
                selected_SongName = tk.Label(tr_in_frame, text="Song Name : ", fg='white', bg='#132933', font=("Calibri", 12, 'bold'))
                selected_SongName.grid()

                selected_Artist = tk.Label(tr_in_frame, text="Artist : ", fg='white', bg='#132933', font=("Calibri", 12, 'bold'))
                selected_Artist.grid()

                selected_Category = tk.Label(tr_in_frame, text="Category : ", fg='white', bg='#132933', font=("Calibri", 12, 'bold'))
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

            tr_in_frame.grid(row=1, column=0)

        # Top right like and dislike
        if True:
            tr_in_frame3 = tk.LabelFrame(tr_frame, padx=5, pady=5, bg='#132933', border=0)
            tr_in_frame3.config(fg='white', font=("Calibri", 12, 'bold'))

            addtoPlaylist_Button = tk.Button(tr_in_frame3, text = "Add To Playlist", padx=20, command= add_to_playlist)
            addtoPlaylist_Button.grid(row=0, column=0, padx=20)

            like_Button = tk.Button(tr_in_frame3, text = "Like", padx=10, command = like_song)
            like_Button.grid(row=0, column=1)
            dislike_Button = tk.Button(tr_in_frame3, text = "Disike", padx=10, command = dislike_song)
            dislike_Button.grid(row=0, column=2)

            global entryLikenum
            entryLikenum = tk.StringVar()
            entry_Likenum= tk.Entry(tr_in_frame3, textvariable=entryLikenum, state="disabled", fg="pink", justify=tk.CENTER, width=10)
            entry_Likenum.grid(row=0, column=3, padx=10)

            tr_in_frame3.grid(row=2, column=0)

        # Mid right
        if True:
            mr_frame = tk.Frame(tr_frame, height=230, width=400, bg="#132933")
            mr_frame.configure(height=mr_frame["height"],width=mr_frame["width"])
            mr_frame.grid_propagate(0)



            # Artist from search
            if True:
                tr_in_frame3 = tk.LabelFrame(mr_frame, text="Artist Details", padx=5, pady=5, bg='#132933', border=0)
                tr_in_frame3.config(fg='white', font=("Calibri", 15, 'bold'))

                global entryArtist_name
                global entryArtist_like
                entryArtist_name = tk.StringVar()
                entryArtist_like= tk.StringVar()
                entry_nameMRL = tk.Entry(tr_in_frame3, textvariable=entryArtist_name, state="disabled", fg="pink", justify=tk.CENTER)
                entry_nameMRL.grid(row=0, column=0)
                entry_ArtistMRL= tk.Entry(tr_in_frame3, textvariable=entryArtist_like, state="disabled", fg="pink", justify=tk.CENTER)
                entry_ArtistMRL.grid(row=1, column=0)



                artist_Listbox = tk.Listbox(tr_in_frame3, height=8, width=30)
                artist_Listbox.bind('<<ListboxSelect>>', lambda x: pick_artist())
                artist_Listbox.grid(row=2,column=0)

                eatspace = tk.Label(tr_in_frame3, text="         ", height=2, bg='#132933')
                eatspace.grid(row=3, column=0)

                tr_in_frame3.grid(row=0, column=0)


            # Playlist from search
            if True:
                tr_in_frame2 = tk.LabelFrame(mr_frame, text="Playlist Details", padx=5, pady=5, bg='#132933', border=0)
                tr_in_frame2.config(fg='white', font=("Calibri", 15, 'bold'))

                global entryPlaylist_name
                global entryPlaylist_user
                entryPlaylist_name = tk.StringVar()
                entryPlaylist_user= tk.StringVar()
                entry_nameTR = tk.Entry(tr_in_frame2, textvariable=entryPlaylist_name, state="disabled", fg="pink", justify=tk.CENTER)
                entry_nameTR.grid(row=0, column=0)
                entry_PlaylistTR= tk.Entry(tr_in_frame2, textvariable=entryPlaylist_user, state="disabled", fg="pink", justify=tk.CENTER)
                entry_PlaylistTR.grid(row=1, column=0)



                playlist_Listbox = tk.Listbox(tr_in_frame2, height=8, width=30)
                playlist_Listbox.bind('<<ListboxSelect>>', lambda x: pick_playlist())
                playlist_Listbox.grid(row=2,column=0)

                selectButton = tk.Button(tr_in_frame2, text="Select", height=1, command = select_playlist)
                selectButton.grid(row=3, column=0, pady=5)

                tr_in_frame2.grid(row=0, column=1)

            mr_frame.grid(row=0, column=0)
        # Top right playlist songs


        tr_frame.grid(row=0, column=0)


    # Bottom Right
    if True:

        br_frame = tk.Frame(right_frame, height=220, width=400, bg="#132933")
        br_frame.configure(height=tr_frame["height"],width=tr_frame["width"])
        br_frame.grid_propagate(0)

        # Show music player
        if True:
            global br_in_frame1
            br_in_frame1 = tk.LabelFrame(br_frame, text="Music Player", padx=5, pady=5, bg="#132933")

            playing_Label = tk.Label(br_in_frame1, text="Now Playing: ", bg="#132933")
            playing_Label.grid(row=0, column=0)
            global entryPlayingAudio
            entryPlayingAudio = tk.StringVar()
            playing_entry = tk.Entry(br_in_frame1, textvariable=entryPlayingAudio, state="disabled", justify=tk.CENTER)
            playing_entry.grid(row=0, column=1, columnspan=3)


            # play pause and stop
            if True:
                
                # copied code
                playButton = tk.Button(br_in_frame1, text = "Play", command = playSong)
                playButton.grid(row=1,column=0)

                pauseButton = tk.Button(br_in_frame1, text ='▶', command = lambda:[pauseSong()])
                pauseButton.grid(row=1,column=2)

                stopButton = tk.Button(br_in_frame1, text = "Stop", command = stopSong)
                stopButton.grid(row=1,column=3)


                volupButton = tk.Button(br_in_frame1, text ='🔊', command = lambda:[volup()])
                volupButton.grid(row=0,column=4)

                voldownButton = tk.Button(br_in_frame1, text ='🔉', command = lambda:[voldown()])
                voldownButton.grid(row=1,column=4)
                
                # dont plan on this, cuz it gives decimals, you can try, line 1685 uncomment
                # volnowButton = tk.Button(br_in_frame1, text ='1', state=DISABLED,command = lambda:[])
                # volnowButton.grid(row=1,column=5)

                # prevButton = tk.Button(br_in_frame1, text ='▮◄', command = lambda:[voldown()])
                # prevButton.grid(row=2,column=0)

                # skipButton = tk.Button(br_in_frame1, text ='►▮', command = lambda:[voldown()])
                # skipButton.grid(row=2,column=1)

            br_in_frame1.grid(row=1, column=1)

        # Show Playlist
        if True:
            br_in_frame2 = tk.Frame(br_frame, height=220, width=130, bg="#132933")
            br_in_frame2.configure(height=br_in_frame2["height"],width=br_in_frame2["width"])
            br_in_frame2.grid_propagate(0)

            global selectedPlaylist_name
            # global selectedPlaylist_user
            selectedPlaylist_name = tk.StringVar()
            # selectedPlaylist_user= tk.StringVar()

            labels = tk.Label(br_in_frame2, text = "Selected Playlist")
            labels.grid(row=0, column=0)

            entry_nameBR = tk.Entry(br_in_frame2, textvariable=selectedPlaylist_name, state="disabled", fg="pink", justify=tk.CENTER)
            entry_nameBR.grid(row=1, column=0)
            # entry_PlaylistBR= tk.Entry(br_in_frame2, textvariable=selectedPlaylist_user, state="disabled", fg="pink", justify=tk.CENTER)
            # entry_PlaylistBR.grid(row=1, column=0)

            selected_Listbox = tk.Listbox(br_in_frame2, height=10, width=20)
            selected_Listbox.bind('<<ListboxSelect>>', lambda x: pick_selected_p())
            selected_Listbox.grid(row=2,column=0)

            br_in_frame2.grid(row=1, column=0)



        br_frame.grid()

    right_frame.grid(row=0, column=1)




root.mainloop()