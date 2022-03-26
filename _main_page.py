from faulthandler import disable
from glob import glob
from importlib.resources import path
from PIL import ImageTk, Image
from tkinter import filedialog
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
from py_SQL import db_connection
from driveconnector import ImageDownload, ImageUpload

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

            # to declare first frame
            profile = tk.Frame(top)
            #to declare edit profile(second frame)
            edit = tk.Frame(top)


            def raise_frame(frame):
                frame.tkraise()

            for frame in (profile, edit):
                frame.place(x=0, y=0, width=500, height=500)


            # ===================================== first frame insert thing here =====================================

            # main title
            userprofile = tk.Label(profile, text="User Profile")
            userprofile.place(x=0, y=0)
            userprofile.config(font=('Helvatical bold',26))

            # print(username)
            # tk.Label(profile, text="Welcome, " + username ).grid(row=1, column=7) 

            # to take select the row containing that username
            selecteduser = 'select * FROM user_tbl WHERE username = "%s"' % username
            mycursor.execute(selecteduser)
            results = mycursor.fetchall()

            # # display profile
            # for row in results:
            #     # display profile
            #         path = "image/"+row[8]
            #         if os.path.exists(path):
            #             ini_img = Image.open(path)
            #             img = ImageTk.PhotoImage(ini_img.resize((100,150), Image.ANTIALIAS))
            #             label = tk.Label(profile, image = img)
            #             label.place(x=20, y=60)
            #         else:#display default profile if databse is none
            #             ini_img = Image.open("image/defaultprofile.jpg")
            #             img = ImageTk.PhotoImage(ini_img.resize((150,150), Image.ANTIALIAS))
            #             label = tk.Label(profile, image = img)
            #             label.place(x=20, y=60)

            # display other info 
            usertype = results[0][1]
            username = results[0][2]
            subscription = results[0][4]
            uploaded = results[0][5]
            downloaded = results[0][6]

            if usertype == "artist":
                # display button
                uploadsong_button = tk.Button(profile, text="Upload Song", command=lambda:())#function here)
                uploadsong_button.place(x=50, y=400)

                viewownsong_button = tk.Button(profile, text="View Own Song", command=lambda:())#function here)
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
            displayusername.config(font=('Helvatical bold',14))

            displayusertype = tk.Label(profile, text=f"User Type : {usertype}")
            displayusertype.place(x=200, y=140)
            displayusertype.config(font=('Helvatical bold',14))

            if subscription == 0:
                subscription = "Not Subscribed"
            else:
                subscription = "Subscribed"

            displaysubscription = tk.Label(profile, text=f"Subscription : {subscription}")
            displaysubscription.place(x=200, y=200)
            displaysubscription.config(font=('Helvatical bold',14))

            displayuploaded = tk.Label(profile, text=f"Uploaded Songs : {uploaded}")
            displayuploaded.place(x=200, y=260)
            displayuploaded.config(font=('Helvatical bold',14))

            displaydownloaded = tk.Label(profile, text=f"Downloaded Songs : {downloaded}")
            displaydownloaded.place(x=200, y=320)
            displaydownloaded.config(font=('Helvatical bold',14))
            # print(results[0][2])

            edit_profile_button = tk.Button(profile, text="Edit Profile", command=lambda: raise_frame(edit))
            edit_profile_button.place(x=60, y=220)




            # ===================================== second frame insert thing here ===================================== 

            modify = tk.Label(edit, text="Modify Profile")
            modify.pack()
            modify.config(font=('Helvatical bold',28))




            # ===================================== modify username part =====================================
            usernamelabel = tk.Label(edit, text="")
            usernamelabel.pack()

            # username label
            changeusername = tk.Label(edit, text="Username: *", font=("Calibri", 12, "bold"))
            changeusername.pack()
            # username entry
            username_entry = tk.Entry(edit, textvariable=changeusername)
            username_entry.pack()




            # ===================================== modify password part =====================================
            # password label
            changepassword = tk.Label(edit, text="Password: *", font=("Calibri", 12, "bold"))
            changepassword.pack()
            # password entry
            password_entry = tk.Entry(edit, textvariable=changepassword, show="*")
            password_entry.pack()

            regpass_label1 = tk.Label(edit, text="")
            regpass_label1.pack()




            # ===================================== modify profile image part =====================================
            # get user id
            selecteduser = 'select * FROM user_tbl WHERE username = "%s"' % username
            mycursor.execute(selecteduser)
            results = mycursor.fetchall()
            for getid in results:
                user_id=getid[0]
                break

            # upload image button
            changeprofile = tk.Label(edit, text="Change Profile Image:", font=("Calibri", 12, "bold"))
            changeprofile.pack()
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

            button = tk.Button(edit, text='select image here', command=UploadAction)
            button.pack()

            # function to check if username taken/password long enough
            def check_info():
                usern = username_entry.get()
                passw = password_entry.get()
                checkuser = "SELECT username FROM user_tbl WHERE username = %s"
                mycursor.execute(checkuser, (usern, ))
                userexists = mycursor.fetchall()

                check_symbol= re.compile('[@_!#$%^&*()<>?/\|}{~:]')
                # messagebox.showinfo("Message","Username taken please use another username")
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
                            messagebox.showinfo("Information", "Changes is Successfull!")

                            # clears the input box empty after a successful registration process
                            username_entry.delete(0, tk.END)
                            password_entry.delete(0, tk.END)
                            # edit.destroy()
                            # raise_frame(profile)
                    except:
                        print("There is an error")




            # ===================================== button part =====================================

            savebutton = tk.Button(edit, text="Save Changes", command=lambda:check_info())
            savebutton.pack()

            # # button for edit frame to go back to the main frame
            mainbutton= tk.Button(edit, text="Main", command=lambda: raise_frame(profile))
            mainbutton.pack()
                    
            # to display the first frame
            raise_frame(profile) 


            user_quit_button = tk.Button(top, text="Quit", command=lambda: quit(top))
            user_quit_button.place(x=450, y=0)




        # ===================================== Admin Main =====================================
        def admin(username):
            login.withdraw()
            top = Toplevel()
            top.geometry("500x500")
            top.title("Admin Page")

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
            searchUser = tk.Label(top, text="Username | ID: ")
            searchUser.grid(row=2, column=5)

            tk.Label(top, text="Welcome, " +username).grid(row=1, column=7) 
            admin_label = tk.Label(top, text="To ban user, enter their user id")
            admin_label.grid(row=1, column=5)

            userEntry = tk.Entry(top)
            userEntry.bind("<KeyRelease>", check)
            userEntry.grid(row=2, column=6)

            all_data = tk.Button(top, text="Show All Data", command = showuser)
            all_data.grid(row=3, column=5)

            search_button = tk.Button(top, text="Ban", command = banuser)
            search_button.grid(row=3, column=6)

            delete_button = tk.Button(top, text="Delete", command = deleteuser)
            delete_button.grid(row=3, column=7)

            quit_button = tk.Button(top, text="Quit", command=lambda: quit(top))
            quit_button.grid(row=1, column=8)

            list = Listbox(top)
            list.grid(row=4, column=5)

            showuser()



        def quit(top):

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
                        messagebox.showinfo("Error", "Username cant be too long")
                        reguser_entry.delete(0, tk.END)

                    # checks if username contain any special characters
                    elif check_symbol.search(usern):
                        messagebox.showinfo("Error", "Username cant contain any special characters")
                        reguser_entry.delete(0, tk.END)

                    # checks if the length of password is more then 10 characters
                    elif len(passw) > 10:
                        messagebox.showinfo("Error", "Password cant be too long")
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
                    print("There is an error")


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
                for audioname in result_list[0]:
                    result_listbox.insert('end',  "Audio | " + audioname)
                for playlistname in result_list[1]:
                    result_listbox.insert('end', "Playlist | "+ playlistname)
                for artistname in result_list[2]:
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
            global item_picked
            item_picked = result_listbox.get(cs)


            if "Audio" in item_picked:
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

            if "Playlist" in item_picked:
                item_picked = item_picked.replace("Playlist | ","")
                # entryText_name.set("{}".format(item_picked))
            
            if "Artist" in item_picked:
                item_picked = item_picked.replace("Playlist | ","")


# Left Side
if True:
    left_frame = tk.Frame(root, height="600", width="400", padx=5, pady=5, bg="red")
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
            global item_picked
            item_picked = result_listbox.get(cs)


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

            if "Playlist | " in item_picked:
                item_picked = item_picked.replace("Playlist | ","")
                entryPlaylist_name.set("{}".format(item_picked))

                for i in search_result_2:
                    if item_picked == i[0]:
                        entryPlaylist_user.set(i[1])
                
                searchAudioQuery ="select a.aid, a.audio_name, a.audio_path, a.uid from song_in_playlist s, playlist_tbl p, audio_tbl a where (s.pid = p.pid) and (s.aid = a.aid) and playlist_name = '{}'".format(item_picked)
                mycursor.execute(searchAudioQuery)
                myresult = mycursor.fetchall()
                
                print(myresult)


            if "Artist | " in item_picked:
                item_picked = item_picked.replace("Playlist | ","")


    # top top left
    if True:
        top_frame = tk.Frame(left_frame,width="400", padx=5, pady=5, bg="purple")

        profileButton = tk.Button(top_frame, text="Profile", command = lambda: check_username(guest_user))
        profileButton.grid(row=0, column=0)
        quitButton = tk.Button(top_frame, text="Quit", command= lambda: quit())
        quitButton.grid(row=0, column=1) 

        def check_username(guest_user):
            if guest_user == "":
                login_win()
                print(guest_user+"<-username printed")
            else:
                print(guest_user)

        def quit():

            root.destroy()

        top_frame.grid(row=0, column=0)


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

        # user_var = tk.IntVar()
        # user_chk = tk.Checkbutton(tl_frame, text="User", variable=user_var)
        # user_chk.select()
        # user_chk.grid(row=2, column = 3)

        #Get Checkbox value by


        tl_frame.grid(row=1, column=0)


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



        bl_frame.grid(row=2, column=0)

    left_frame.grid(row=0, column=0)


# ===================== Right Side==============================================

# Right Side
if True:
    right_frame = tk.Frame(root, height="600", width="400", padx=5, pady=5, bg="black")
    right_frame.configure(height=right_frame["height"],width=right_frame["width"])
    right_frame.grid_propagate(0)

    # Prerequisite
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
        tr_frame = tk.Frame(right_frame, height=380, width=400, bg="purple")
        tr_frame.configure(height=tr_frame["height"],width=tr_frame["width"])
        tr_frame.grid_propagate(0)

        # top right details
        if True:
            tr_in_frame = tk.LabelFrame(tr_frame, text="Audio Details", padx=100, pady=5)
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

            tr_in_frame.grid(row=0, column=0)

        # Top right like and dislike
        if True:
            tr_in_frame3 = tk.LabelFrame(tr_frame, padx=5, pady=5)

            addtoPlaylist_Button = tk.Button(tr_in_frame3, text = "Add To Playlist", padx=20)
            addtoPlaylist_Button.grid(row=0, column=0, padx=20)

            like_Button = tk.Button(tr_in_frame3, text = "Like", padx=10)
            like_Button.grid(row=0, column=1)
            dislike_Button = tk.Button(tr_in_frame3, text = "Disike", padx=10)
            dislike_Button.grid(row=0, column=2)

            global entryLikenum
            entryLikenum = tk.StringVar()
            entry_Likenum= tk.Entry(tr_in_frame3, textvariable=entryLikenum, state="disabled", fg="pink", justify=tk.CENTER, width=10)
            entry_Likenum.grid(row=0, column=3)

            tr_in_frame3.grid(row=1, column=0)


        # Top right playlist songs
        if True:
            tr_in_frame2 = tk.LabelFrame(tr_frame, text="Playlist Details", padx=5, pady=5)

            global entryPlaylist_name
            global entryPlaylist_user
            entryPlaylist_name = tk.StringVar()
            entryPlaylist_user= tk.StringVar()
            entry_nameTR = tk.Entry(tr_in_frame2, textvariable=entryPlaylist_name, state="disabled", fg="pink", justify=tk.CENTER)
            entry_nameTR.grid(row=0, column=0)
            entry_PlaylistTR= tk.Entry(tr_in_frame2, textvariable=entryPlaylist_user, state="disabled", fg="pink", justify=tk.CENTER)
            entry_PlaylistTR.grid(row=1, column=0)



            playlist_Listbox = tk.Listbox(tr_in_frame2, height=5, width=5)
            # playlist_Listbox.bind('<<ListboxSelect>>', lambda x: pick_from_list())
            playlist_Listbox.grid(row=2,column=0)

            tr_in_frame2.grid(row=2, column=0)
        



        tr_frame.grid(row=0, column=0)


    # Bottom Right
    if True:

        br_frame = tk.Frame(right_frame, height=220, width=400, bg="orange")
        br_frame.configure(height=tr_frame["height"],width=tr_frame["width"])
        br_frame.grid_propagate(0)

        # Show music player
        if True:
            global br_in_frame1
            br_in_frame1 = tk.LabelFrame(br_frame, text="Music Player", padx=5, pady=5, bg="green")

            playing_Label = tk.Label(br_in_frame1, text="Now Playing: ", bg="green")
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
            br_in_frame2 = tk.LabelFrame(br_frame, text = "Selcted Playlist", padx= "5", pady = "5", bg="grey")

            global selectedPlaylist_name
            global selectedPlaylist_user
            selectedPlaylist_name = tk.StringVar()
            selectedPlaylist_user= tk.StringVar()

            entry_nameBR = tk.Entry(br_in_frame2, textvariable=selectedPlaylist_name, state="disabled", fg="pink", justify=tk.CENTER)
            entry_nameBR.grid(row=0, column=0)
            entry_PlaylistBR= tk.Entry(br_in_frame2, textvariable=selectedPlaylist_user, state="disabled", fg="pink", justify=tk.CENTER)
            entry_PlaylistBR.grid(row=1, column=0)



            br_in_frame2.grid(row=1, column=0)

        # Show Playlist
        # if True:
        #     global br_in_frame2
        #     br_in_frame2 = tk.LabelFrame(right_frame, text="Playlist Details", padx=5, pady=5, bg="white")

        #     example = tk.Button(br_in_frame2, text="Test")
        #     example.grid()


        #     # playlist_Listbox = tk.Listbox(br_in_frame2, height=5, width=5)
        #     # # playlist_Listbox.bind('<<ListboxSelect>>', lambda x: pick_from_list())
        #     # playlist_Listbox.grid(row=2,column=0)

        #     br_in_frame2.grid(row=1, column=1)

        br_frame.grid()

    right_frame.grid(row=0, column=1)




root.mainloop()