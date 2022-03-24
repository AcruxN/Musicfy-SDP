# Import Python Public module
import tkinter as tk
import pygame as pg
from email import message
from tkinter import messagebox


# Import Local Module
from py_SQL import db_connection

# Connect Database
db, mycursor = db_connection()

# Initialise tkinter
root = tk.Tk()

# initialise pygame mixer
pg.mixer.init()

# ============================= Application  =====================================
# Change Window(Application) Title
root.title("Musicfy")
# Change icon
# root.iconbitmap(r"musicfy.ico")
# Change Window's size
root.geometry("500x500")
# Fix window's size
root.resizable(width=False, height=False)

#                   ========== Frames ============
def raise_frame(frame):
    frame.tkraise()

login_f = tk.Frame(root)
signup_f = tk.Frame(root)
search_f = tk.Frame(root)

for f in (login_f, signup_f, search_f):
    # f.grid(row=0, column=0, sticky="news")
    f.pack()
# ------------------- Button to change application Size ------------------------
# def resize():
#     w = 400
#     h = 400
#     root.geometry(f"{w}x{h}") 

# resizeButton = tk.Button(root, text="Resize to 400 x 400", command = resize)
# resizeButton.grid(row=2, column=2)
# ------------------------------------------------------------------------------


# ==============================================================================


# ===================================== Login =====================================

def login_verify():
    username = username_verify.get()
    password = password_verify.get()

    sql = "SELECT * FROM user_tbl WHERE username = %s and password = %s"
    mycursor.execute(sql, [(username), (password)])
    results = mycursor.fetchall()

    if results:
        messagebox.showinfo("Musicfy", "Login Successfull!")
        
        raise_frame(search_f)
        search()

        # Why close database? If DB closed cant 2nd login will get error / Do other stuff need reopen
        # mycursor.close()
        # db.close()

        # What for?
        # return True
    else:
        messagebox.showinfo("Error", "Incorrect Username or Password!")
        # return False

def login():

    raise_frame(login_f)

    # set global variables (login)
    global username_verify
    global password_verify

    username_verify = tk.StringVar()
    password_verify = tk.StringVar()

    # login form code
    # username input code
    loguser_label = tk.Label(login_f, text="Username: ", fg="black", font=("Calibri", 12, "bold"))
    loguser_label.pack()
    # username entry
    loguser_entry = tk.Entry(login_f, textvariable=username_verify)
    loguser_entry.pack()
    loguser_label1 = tk.Label(login_f, text="")
    loguser_label1.pack()

    # password input code
    logpass_label = tk.Label(login_f, text="Password: ", fg="black", font=("Calibri", 12, "bold"))
    logpass_label.pack()
    # password entry
    logpass_entry = tk.Entry(login_f, textvariable=password_verify, show="*")
    logpass_entry.pack()
    logpass_label1 = tk.Label(login_f, text="")
    logpass_label1.pack()

    # login button in main frame
    loginbutton = tk.Button(login_f, text="Login", command= login_verify)
    loginbutton.pack()

    # sign up button in main frame
    signupbutton = tk.Button(login_f, text="Sign Up", command=lambda: raise_frame(signup_f))
    signupbutton.pack()

    # Button for guest
    continueAsGuest = tk.Button(login_f, text="Continue as Guest", command=search)
    continueAsGuest.pack()



# ===================================== Sign Up =====================================

def reg_verify():
    usern = reg_username.get()
    passw = reg_password.get()
    checkusername = mycursor.execute("SELECT username FROM user_tbl WHERE usern = %(username)s", (usern,))
    userexists = mycursor.fetchall()

    if usern in userexists:
        messagebox.showinfo("Error", "Username Already Exists!")
    

    # if usern == "" or passw == "":
    #     messagebox.showinfo("Error", "All Fields Are Required!")
    #     if checkusername == 0:
    #         messagebox.showinfo("Error", "Username already exist!")

    else:
        reg_sql = "INSERT INTO user_tbl (usertype, username, password) VALUES (%s, %s, %s)"
        reg_val = ("user", usern, passw)
        mycursor.execute(reg_sql, reg_val)
        db.commit()
        messagebox.showinfo("Information", "Registration Successfull!")

        reg_username.set("")
        reg_password.set("")

def signup():
    # sign up section in signup frame
    # signup button, navigate to signup frame
    signuplabel = tk.Label(signup_f, text="Sign Up")
    signuplabel.pack()

    # sign up form 
    # set global variables (signup)
    global reg_username
    global reg_password

    reg_username = tk.StringVar()
    reg_password = tk.StringVar()

    # username label
    reguser_label = tk.Label(signup_f, text="Username: *", font=("Calibri", 12, "bold"))
    reguser_label.pack()
    # username entry
    reguser_entry = tk.Entry(signup_f, textvariable=reg_username)
    reguser_entry.pack()

    # password label
    regpass_label = tk.Label(signup_f, text="Password: *", font=("Calibri", 12, "bold"))
    regpass_label.pack()
    # password entry
    regpass_entry = tk.Entry(signup_f, textvariable=reg_password, show="*")
    regpass_entry.pack()
    regpass_label1 = tk.Label(signup_f, text="")
    regpass_label1.pack()


    signupbutton = tk.Button(signup_f, text="Confirm", command=reg_verify)
    signupbutton.pack()

    # button for signup frame to go back to the main frame
    signupbuttonb = tk.Button(signup_f, text="Main", command=lambda: raise_frame(login_f))
    signupbuttonb.pack()


# ===================================== Search =====================================

def search():
    login_f.destroy()
    raise_frame(search_f)

    # Creating label for search bar
    searchLabel = tk.Label(search_f, text = "Search Audio: ", font = ('Italic', 14), fg="dark blue")
    # Creating input bar
    searchBar = tk.Entry(search_f)
    # Display Search bar & Input Bar
    # searchLabel.grid(row = 0, column = 0)
    # searchBar.grid(row = 0, column = 1)
    searchLabel.pack()
    searchBar.pack()



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
            searchValid = tk.Label(search_f, text = f"Invalid Search")
            # searchValid.grid(row=2,column=1)
            searchValid.pack()
        else:
            # Valid
            searchValid = tk.Label(search_f, text = f"Displaying Search Result for: {u_search}")
            # searchValid.grid(row=2,column=1)
            searchValid.pack()
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
            audioLabel = tk.Label(search_f, text = f"Audio Name = {a_name}")
            # audioLabel.grid(row=3+audio_num, column=1) # row 0 = search bar, row 1= search button, row 2 = Displaying Search Result for:
            audioLabel.pack()

            # Play Audio
            #
            # Issue - Play the last song on all button,
            # Solution probably use list, call list
            audioButton = tk.Button(search_f, text = "Play", command = lambda:[playSong(a_path)])
            # audioButton.grid(row=3+audio_num, column=2)
            audioButton.pack()

        # Display number of results after loop
        numLabel = tk.Label(search_f, text = f"Number of Result {audio_num}")
        # numLabel.grid(row=4+audio_num, column=1)
        numLabel.pack()


    # Search Button
    searchButton = tk.Button(search_f, text = "Search", command = check_valid)
    # Display search button
    # searchButton.grid(row = 1, column = 0)
    searchButton.pack()



login()
root.mainloop()