from faulthandler import disable
from glob import glob
from importlib.resources import path
import os
from pathlib import Path
import shutil
from PIL import ImageTk, Image
from tkinter import StringVar, filedialog
from queue import Empty
from select import select
from telnetlib import STATUS
import tkinter as tk
from tkinter import messagebox, Listbox, Toplevel
import re
import tkinter
from turtle import width, window_height
# from cv2 import split
import pygame as pg
from pyparsing import col
from py_SQL import db_connection
# from driveconnector import ImageDownload, ImageUpload

db, mycursor = db_connection()
root = tk.Tk()

guest_user = ""
# initialise pygame mixer
pg.mixer.init()

# ============================= Application Design =============================
# Change Window(Application) Title
root.title("Musicfy")
# Change icon
# root.iconbitmap(r"musicfy.ico")
# # Change Window's size
# root.geometry("800x600")
# Fix window's size
# root.resizable(width=False, height=False)
# ==============================================================================


# jason's code
if True:
    # ===================================== Main =============================================
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

        my_img = ImageTk.PhotoImage(Image.open("img\music logo design.png"))
        img_label = tk.Label(login_left_frame, image= my_img, borderwidth=0, highlightthickness=0)
        img_label.grid()

        main = tk.Frame(login, bg='#132933')
        signup = tk.Frame(login, bg='#132933')

        for frame in (main, signup):
            frame.place(x=500, y=0, width=500, height=500)





        # ===================================== User Main =======================================
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


            # ===================================== first frame insert thing here =====================================


            # main title
            userprofile = tk.Label(profile, text="User Profile")
            userprofile.place(x=150, y=0)
            userprofile.config(fg='white', bg='#132933', font=('Helvatical bold',26, 'bold'))
            # to take select the row containing that username
            selecteduser = 'select * FROM user_tbl WHERE username = "%s"' % username
            mycursor.execute(selecteduser)
            results = mycursor.fetchall()

            # display profile
            # for row in results:
            #     # display profile
            #         path = "image/"+row[7]
            #         print(path)
            #         if os.path.exists(path):
            #             ini_img = Image.open(path)
            #             img = ImageTk.PhotoImage(ini_img.resize((150,150), Image.ANTIALIAS))
            #             label = tk.Label(profile, image = img)
            #             label.place(x=20, y=60)
            #             print(path)
            #         else:#display default profile if databse is none
            #             ini_img = Image.open("image/defaultprofile.jpg")
            #             img = ImageTk.PhotoImage(ini_img.resize((150,150), Image.ANTIALIAS))
            #             label = tk.Label(profile, image = img)
            #             label.place(x=20, y=60)


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

                    upload_quit_button = tk.Button(up_song, text="Quit", command= lambda: upload_quit())
                    upload_quit_button.grid(sticky='E', row=0, column=1)

                def upload_quit():
                    up_song.destroy()
                    top.update()
                    top.deiconify()


                Upload_audio()

            # namtung code
            # def viewownSong():

            #     temp_name = guest_user
            #     searchAudioQuery = "select a.audio_name from audio_tbl a, user_tbl u where (a.uid = u.uid) and username ='{}'".format(temp_name)
            #     mycursor.execute(searchAudioQuery)
            #     myresult = mycursor.fetchall()
            #     print(myresult)


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

                createplaylist_button = tk.Button(profile, text="Create Playlist", command=lambda:())#function here)
                createplaylist_button.place(x=265, y=400)

                viewplaylist_button =tk.Button(profile, text="View Playlist", command=lambda:())#function here)
                viewplaylist_button.place(x=370, y=400)

            def changetoartist():
                # change the user type database from listener to artist
                changeusertype = f'update user_tbl set usertype = "artist" where username = "{username}"'
                mycursor.execute(changeusertype)
                db.commit()
                messagebox.showinfo(title=None, message="You have successfully become an artist")
                profile.update()
                # raise_frame(profile)


            if usertype == "listener":
                createplaylist_button = tk.Button(profile, text="Create Playlist", command=lambda:())#function here)
                createplaylist_button.place(x=70, y=400)

                viewplaylist_button =tk.Button(profile, text="View Playlist", command=lambda:())#function here)
                viewplaylist_button.place(x=220, y=400)

                changetoartist_button =tk.Button(profile, text="Become an Artist", command=lambda:changetoartist())#function here)
                changetoartist_button.place(x=350, y=400)

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
            # print(results[0][2])

            edit_profile_button = tk.Button(profile, text="Edit Profile", command=lambda: raise_frame(edit))
            edit_profile_button.place(x=60, y=220)


            


            # ===================================== second frame insert thing here ===================================== 
            modify = tk.Label(edit, text="Modify Profile")
            modify.place(x=120, y=30)
            modify.config(fg='white', bg='#132933', font=('Helvatical bold',30, 'bold'))




            # ===================================== modify username part =====================================
            # username label
            changeusername = tk.Label(edit, fg='white', bg='#132933', text="Username: *", font=("Calibri", 15, "bold"))
            changeusername.place(x=130, y=100)
            # username entry
            username_entry = tk.Entry(edit, textvariable=changeusername)
            username_entry.place(x=250, y=107)




            # ===================================== modify password part =====================================
            # password label
            changepassword = tk.Label(edit,fg='white', bg='#132933', text="Password: *", font=("Calibri", 15, "bold"))
            changepassword.place(x=130, y=150)
            # password entry
            password_entry = tk.Entry(edit, textvariable=changepassword, show="*")
            password_entry.place(x=250, y=157)




            # ===================================== modify profile image part =====================================
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
                    except:
                        messagebox.showerror("Error", "There is an error on the code")



            # ===================================== button part =====================================
            savebutton = tk.Button(edit, text="Save Changes", command=lambda:check_info())
            savebutton.place(x=250, y=250)

            # # button for edit frame to go back to the main frame
            mainbutton= tk.Button(edit, text="Main", command=lambda: raise_frame(profile))
            mainbutton.place(x=200, y=250)
                    
            # to display the first frame
            raise_frame(profile) 


            user_quit_button = tk.Button(profile, text="Quit", command=lambda: quit(top))
            user_quit_button.place(x=450, y=0)
        



        # ===================================== Admin Main =====================================
        def admin(username):
            login.withdraw()
            top = Toplevel()
            top.geometry("450x460")
            top.configure(bg='#132933')
            top.resizable(height=False, width=False)
            top.title("Admin Page")
            global guest_user
            guest_user = username

            # ============================================= Update Listbox =============================================
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




            # ============================================= Delete =============================================
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




            # ============================================= Banning =============================================
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




            # ============================================= Display User =============================================
            # display all records in user table database
            def showuser():

                showquery = "SELECT uid, usertype, username FROM user_tbl WHERE NOT usertype = 'admin'"
                mycursor.execute(showquery)
                sdresult = mycursor.fetchall()

                list.delete(0, tk.END)

                for row in sdresult:
                    showdata = str(row[0])+ '  |  ' +row[1]+ '  |  ' +row[2]
                    list.insert(list.size()+1, showdata)




            # ============================================= Main =============================================
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
        



        # ===================================== Login =========================================

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
                    messagebox.showinfo("Musicfy", "User Login Successfull!")
                    loguser_entry.delete(0, tk.END)
                    logpass_entry.delete(0, tk.END)
                    login.withdraw()
                    user(username)

                # checks whether usertype "artist" is in list 
                elif 'artist' in results[0]:
                    messagebox.showinfo("Musicfy", "User Login Successfull!")
                    loguser_entry.delete(0, tk.END)
                    logpass_entry.delete(0, tk.END)
                    login.withdraw()
                    user(username)

                # checks whether usertype "admin" is in list
                elif 'admin' in results[0]:
                    messagebox.showinfo("Musicfy", "Admin Login Successfull!")
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




        # ===================================== Sign Up =====================================
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

                    # checks if the length of password is more then 10 characters
                    elif len(passw) > 10:
                        messagebox.showinfo("Error", "Password cant exceed 10 characters")
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
                        messagebox.showinfo("Information", "Registration Successfull!")

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

# ==============================================================================


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
            cs = result_listbox.curselection()
            item_picked = result_listbox.get(cs)

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
                print(guest_user)

        def quit():

            root.destroy()

        top_frame.grid(row=0, column=0)


    # Top left
    if True:
        tl_frame = tk.LabelFrame(left_frame, text="Search", padx=5, pady=5, bg="#132933")

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



        tl_frame.grid(row=1, column=0)


    # Bottom left
    if True:
        bl_frame = tk.LabelFrame(left_frame, text="Result", padx=5, pady=5, bg="#132933")
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


# ===================== Right Side==============================================

# Right Side
if True:
    right_frame = tk.Frame(root, height="600", width="400", padx=5, pady=5, bg="#132933")
    right_frame.configure(height=right_frame["height"],width=right_frame["width"])
    right_frame.grid_propagate(0)

    # Prerequisite
    if True:

        #Music player
        def playSong():
            print(selected_path)
            try:

                # Clarence
                if True:
                    pass

                if type(selected_path) == str:
                    pg.mixer.music.load(r"{}".format(selected_path))
                    pg.mixer.music.play(-1)
                    temp_name = entryText_name.get()
                    entryPlayingAudio.set("{}".format(temp_name))
                    
                elif type(selected_path) == list:
                    num_index = len(selected_path) - 1
                    index = 0
                    while index <= num_index:
                        pg.mixer.music.load(r"{}".format(selected_path[index]))
                        pg.mixer.music.play(-1)
                        print(index)
                        index +=1
            except NameError:
                print("No item (songs) selected yet")

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
        
        def add_to_playlist():
            pass

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
            

        def pick_playlist():
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
            cs = selected_Listbox.curselection()
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
            print(path_list)
            global selected_path
            selected_path = path_list
            # for i in myresult:
            #     for j in i:
            #         global selected_path
            #         selected_path = j
            #         print(selected_path)

    # #Top & Mid Right
    if True:
        tr_frame = tk.Frame(right_frame, height=380, width=400, bg="#132933")
        tr_frame.configure(height=tr_frame["height"],width=tr_frame["width"])
        tr_frame.grid_propagate(0)

        # top right details
        if True:
            tr_in_frame = tk.LabelFrame(tr_frame, text="Audio Details", padx=100, pady=15)
            # tr_in_frame.configure(height=tr_frame["height"],width=tr_frame["width"])
            # tr_in_frame.grid_propagate(0)
            if True:
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

            tr_in_frame.grid(row=1, column=0)

        # Top right like and dislike
        if True:
            tr_in_frame3 = tk.LabelFrame(tr_frame, padx=5, pady=5)

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
                tr_in_frame3 = tk.LabelFrame(mr_frame, text="Artist Details", padx=5, pady=5)

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

                eatspace = tk.Label(tr_in_frame3, text="         ", height= 2)
                eatspace.grid(row=3, column=0)

                tr_in_frame3.grid(row=0, column=0)


            # Playlist from search
            if True:
                tr_in_frame2 = tk.LabelFrame(mr_frame, text="Playlist Details", padx=5, pady=5)

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

            # copied code
            playButton = tk.Button(br_in_frame1, text = "Play", command = playSong)
            playButton.grid(row=1,column=0)

            pauseButton = tk.Button(br_in_frame1, text = "Pause", command = lambda:[pauseSong(),changeButton_pause()])
            pauseButton.grid(row=1,column=2)

            unpauseButton = tk.Button(br_in_frame1, text = "Unpause", command = lambda:[unpauseSong(),changeButton_unpause()])
            unpauseButton.grid(row=2,column=2)

            stopButton = tk.Button(br_in_frame1, text = "Stop", command = stopSong)
            stopButton.grid(row=1,column=3)

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