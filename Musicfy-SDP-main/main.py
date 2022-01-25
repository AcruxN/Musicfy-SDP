from email import message
from tkinter import *
from tkinter import messagebox

import connect_db

mycursor, sql_db = connect_db.connection()


def login_verify():
    
    username = username_verify.get()
    password = password_verify.get()

    sql = "SELECT * FROM user_tbl WHERE username = %s and password = %s"
    mycursor.execute(sql, [(username), (password)])
    results = mycursor.fetchall()

    if results:
        messagebox.showinfo("", "Login Success")
        root.destroy()
        return True
    else:
        messagebox.showinfo("Error", "Incorrect Username or Password")
        return False


def register_completion():

    reg_username = username.get()
    reg_email = email.get()
    reg_password = password.get()


    if reg_username == "":
        messagebox.showinfo("Error","All fields are required...")
    elif reg_email == "":
        messagebox.showinfo("Error", "All fields are required...")
    elif reg_password == "":
        messagebox.showinfo("Error", "All fields are required...")
    else:
        mycursor.execute("SELECT * FROM user_tbl WHERE username = '" + username.get() + "'")
        if mycursor.fetchone() is not None:
            messagebox.showinfo("Error", "Username is already taken!")
        else:
            reg_info = "INSERT INTO user_tbl (usertype, username, email, password) VALUES ('user', %s, %s, %s)"
            mycursor.execute(reg_info)
            sql_db.commit()
            messagebox.showinfo("Success", "Registration Successfull!")
        mycursor.close()
        sql_db.close()

    # # validation of entered data
    # if(len(password) < 15): # length of password minimum 15 char
    #     validation = False
    #     msg = msg + "Password minimum 20 char"

    # # username between 10 and 15
    # if(len(username) < 10 or len(username) < 15 or not username.isalnum()):
    #     validation = False
    
    # else:
    #     # execute query
    #     query = "SELECT username, password, email FROM user_tbl WHERE email=%s"
    #     r_set = cursordb.execute(query, email)
    #     r_set = r_set.fetchall()
    #     no = len(r_set) 
    

def register():

        global counter

        if counter < 2:

            # set global variables
            global username 
            global email
            global password

            global register_screen

            # use toplevel widget to create a window on top of all other
            register_screen = Toplevel()
            register_screen.title("Musicfy 2.0") 
            register_screen.geometry("300x250")

            Label(register_screen, text="Registration", bg="#0059b3", width="300", height="2", font=("Calibri", 13)).pack()
            Label(register_screen, text="").pack()


            # text variables
            username = StringVar()
            email = StringVar()
            password = StringVar()

            # username label
            username_label = Label(register_screen, text = "Username * ", font=("Calibri", 12, 'bold'))
            username_label.pack()

            # username entry 
            # entry widget, a standard tkinter widget used to enter or display a somgle line of text
            username_entry = Entry(register_screen, textvariable = username)
            username_entry.pack()

            # email label 
            email_label = Label(register_screen, text = "Email * ", font=("Calibri", 12, 'bold'))
            email_label.pack()

            # email entry 
            email_entry = Entry(register_screen, textvariable = email)
            email_entry.pack()


            # password label
            password_label = Label(register_screen, text = "Password * ", font=("Calibri", 12, 'bold'))
            password_label.pack()

            # password entry
            password_entry = Entry(register_screen, textvariable = password, show = '*')
            password_entry.pack()

            Label(register_screen, text = "").pack()

            # register button
            Button(register_screen, text = "Register", width = 10, height = 1, command = register_completion).pack()

            counter += 1
        else:
            messagebox.showinfo("Error", "Window is already opened")



root = Tk()
root.title("Musicfy 2.0") # Title of GUI Window
root.geometry("400x350") # Set size of the GUI Window


def login():

    # counter to limit the number of windows opened, currently set only 1 window is 
    # opened when button is clicked
    global counter 
    counter = 1

    # logo / title 
    Label(text="Musicfy Logo", bg="#0059b3", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()

    global username_verify 
    global password_verify 

    username_verify = StringVar()
    password_verify = StringVar()

    # login code 
    Label(text="Username:", fg="black", font=("Calibri", 12, 'bold')).pack()
    Entry(textvariable = username_verify).pack()
    Label(text="").pack()

    Label(text="Password:", fg="black", font=("Calibri", 12, 'bold')).pack()
    Entry(textvariable = password_verify, show="*").pack()
    Label( text="").pack()

    Button(text = "Login", width = 10, height = 1, command = login_verify).pack()

    # register button
    Button(text="Sign Up", height="2", width="30", command = register).pack()

login()
root.mainloop()
