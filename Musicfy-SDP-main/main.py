from email import message
from tkinter import *
from tkinter import messagebox
import connect_db

mycursor, sql_db = connect_db.connection()

def raise_frame(frame):
    frame.tkraise()


def login_verify():
    username = username_verify.get()
    password = password_verify.get()

    sql = "SELECT * FROM user_tbl WHERE username = %s and password = %s"
    mycursor.execute(sql, [(username), (password)])
    results = mycursor.fetchall()

    if results:
        messagebox.showinfo("Musicfy", "Login Successfull!")
        mycursor.close()
        sql_db.close()
        return True
    else:
        messagebox.showinfo("Error", "Incorrect Username or Password!")
        return False


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
        sql_db.commit()
        messagebox.showinfo("Information", "Registration Successfull!")

        reg_username.set("")
        reg_password.set("")

# ===================================== Main =====================================
root = Tk()
root.geometry("500x500")


main = Frame(root)
signup = Frame(root)

for frame in (main, signup):
    frame.grid(row=0, column=0, sticky="news")

# main page with musicfy logo
mainlabel = Label(main, text='Musicfy Logo')
mainlabel.pack()


# ===================================== Login =====================================
# set global variables (login)
global username_verify
global password_verify

username_verify = StringVar()
password_verify = StringVar()

# login form code
# username input code
loguser_label = Label(main, text="Username: ", fg="black", font=("Calibri", 12, "bold"))
loguser_label.pack()
# username entry
loguser_entry = Entry(main, textvariable=username_verify)
loguser_entry.pack()
loguser_label1 = Label(main, text="")
loguser_label1.pack()

# password input code
logpass_label = Label(main, text="Password: ", fg="black", font=("Calibri", 12, "bold"))
logpass_label.pack()
# password entry
logpass_entry = Entry(main, textvariable=password_verify, show="*")
logpass_entry.pack()
logpass_label1 = Label(main, text="")
logpass_label1.pack()

# login button in main frame
loginbutton = Button(main, text="Login", command= login_verify)
loginbutton.pack()

# sign up button in main frame
mainbutton = Button(main, text="Sign Up", command=lambda: raise_frame(signup))
mainbutton.pack()

# ===================================== Sign Up =====================================
# sign up section in signup frame
# signup button, navigate to signup frame
signuplabel = Label(signup, text="Sign Up")
signuplabel.pack()

# sign up form 
# set global variables (signup)
global reg_username
global reg_password

reg_username = StringVar()
reg_password = StringVar()

# username label
reguser_label = Label(signup, text="Username: *", font=("Calibri", 12, "bold"))
reguser_label.pack()
# username entry
reguser_entry = Entry(signup, textvariable=reg_username)
reguser_entry.pack()

# password label
regpass_label = Label(signup, text="Password: *", font=("Calibri", 12, "bold"))
regpass_label.pack()
# password entry
regpass_entry = Entry(signup, textvariable=reg_password, show="*")
regpass_entry.pack()
regpass_label1 = Label(signup, text="")
regpass_label1.pack()


signupbutton = Button(signup, text="Confirm", command=reg_verify)
signupbutton.pack()

# button for signup frame to go back to the main frame
signupbuttonb = Button(signup, text="Main", command=lambda: raise_frame(main))
signupbuttonb.pack()

raise_frame(main)
root.mainloop()