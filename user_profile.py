# ===================================== User Main =====================================

import re
from select import select
import tkinter as tk
from tkinter import messagebox
from driveconnector import ImageUpload
from driveconnector import ImageDownload
# from loginsignup_2 import login_MC

from py_SQL import db_connection
from PIL import ImageTk, Image
import os

from tkinter import filedialog

# database connection 
db, mycursor = db_connection()

# the app size and title
root = tk.Tk()
root.geometry("500x500")
root.title("Musicfy")


# to declare second frame
profile = tk.Frame(root)
#to declare edit profile(third frame)
edit = tk.Frame(root)


def raise_frame(frame):
    frame.tkraise()

for frame in (profile, edit):
    frame.place(x=0, y=0, width=500, height=500)

# selection either listener or artist (to upload songs)

# first frame code here

# from id check database and display the username

import loginsignup_2

userNameooo = loginsignup_2.userName

print(userNameooo)
tk.Label(profile, text="Welcome, " +userNameooo).grid(row=1, column=7) 

# second frame insert thing here

# main title
userprofile = tk.Label(profile, text="User Profile")
userprofile.place(x=0, y=0)
userprofile.config(font=('Helvatical bold',28))

username = "admin"
print(username)
tk.Label(profile, text="Welcome, " + username ).grid(row=1, column=7) 

# to take select the row containing that username
selecteduser = 'select * FROM user_tbl WHERE username = "%s"' % username
mycursor.execute(selecteduser)
results = mycursor.fetchall()

# display profile
for row in results:
    # display profile
        path = "image/"+row[8]
        if os.path.exists(path):
            ini_img = Image.open(path)
            img = ImageTk.PhotoImage(ini_img.resize((100,150), Image.ANTIALIAS))
            label = tk.Label(profile, image = img)
            label.place(x=20, y=60)
        else:#display default profile if databse is none
            ini_img = Image.open("image/defaultprofile.jpg")
            img = ImageTk.PhotoImage(ini_img.resize((100,150), Image.ANTIALIAS))
            label = tk.Label(profile, image = img)
            label.place(x=20, y=60)

# display other info 



edit_profile_button = tk.Button(profile, text="edit profile", command=lambda: raise_frame(edit))
edit_profile_button.place(x=30, y=200)


# third frame here

# main title
modify = tk.Label(edit, text="Modify Profile")
modify.pack()
modify.config(font=('Helvatical bold',28))

# ======================modify username part=====================
usernamelabel = tk.Label(edit, text="")
usernamelabel.pack()

# username label
changeusername = tk.Label(edit, text="Username: *", font=("Calibri", 12, "bold"))
changeusername.pack()
# username entry
username_entry = tk.Entry(edit, textvariable=changeusername)
username_entry.pack()

# still to do verification again and compare to make sure the same username is not used

# ======================modify password part=====================
# password label
changepassword = tk.Label(edit, text="Password: *", font=("Calibri", 12, "bold"))
changepassword.pack()
# password entry
password_entry = tk.Entry(edit, textvariable=changepassword, show="*")
password_entry.pack()

regpass_label1 = tk.Label(edit, text="")
regpass_label1.pack()

# need to do the same thing for pass prolly can reuse the code


# ======================modify profile image part=====================
# get user id
selecteduser = 'select * FROM user_tbl WHERE username = "%s"' % username
mycursor.execute(selecteduser)
results = mycursor.fetchall()
for getid in results:
    user_id=getid[0]
    break

# upload button
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
    messagebox.showinfo("Message","Username taken please use another username")
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
                reg_sql = 'UPDATE user_tbl SET username =  "{usern}", password =  "{passw}", WHERE username= "{username}"'
                mycursor.execute(reg_sql)
                db.commit()
                messagebox.showinfo("Information", "Registration Successfull!")

                username_entry.set("")
                password_entry.set("")

                # clears the input box empty after a successful registration process
                username_entry.delete(0, tk.END)
                password_entry.delete(0, tk.END)
                raise_frame(profile)
        except:
            print("There is an error")
# ======================button part=====================
# button for edit
savebutton = tk.Button(edit, text="Save Changes", command=check_info())

savebutton.pack()

# button for edit frame to go back to the main frame
mainbutton= tk.Button(edit, text="Main", command=lambda: raise_frame(profile))
mainbutton.pack()
        
# to display the first frame
raise_frame(profile)

root.mainloop()