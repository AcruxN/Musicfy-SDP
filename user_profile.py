# bring forth the data from login
# need to make the modify profile function work
# add function to the buttons
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


# to declare first frame
profile = tk.Frame(root)
#to declare edit profile(second frame)
edit = tk.Frame(root)


def raise_frame(frame):
    frame.tkraise()

for frame in (profile, edit):
    frame.place(x=0, y=0, width=500, height=500)


# ======================first frame insert thing here======================

# main title
userprofile = tk.Label(profile, text="User Profile")
userprofile.place(x=0, y=0)
userprofile.config(font=('Helvatical bold',26))

username = "imlistener"
# print(username)
# tk.Label(profile, text="Welcome, " + username ).grid(row=1, column=7) 

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
            img = ImageTk.PhotoImage(ini_img.resize((150,150), Image.ANTIALIAS))
            label = tk.Label(profile, image = img)
            label.place(x=20, y=60)

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


# ======================second frame insert thing here======================

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


# ======================modify password part=====================
# password label
changepassword = tk.Label(edit, text="Password: *", font=("Calibri", 12, "bold"))
changepassword.pack()
# password entry
password_entry = tk.Entry(edit, textvariable=changepassword, show="*")
password_entry.pack()

regpass_label1 = tk.Label(edit, text="")
regpass_label1.pack()


# ======================modify profile image part=====================
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
                reg_sql = f'UPDATE INTO user_tbl  set username = "{usern}", password = "{passw}" WHERE username ="{username}"'
                mycursor.execute(reg_sql)
                db.commit()
                messagebox.showinfo("Information", "Registration Successfull!")

                username_entry.set("")
                password_entry.set("")

                # clears the input box empty after a successful registration process
                username_entry.delete(0, tk.END)
                password_entry.delete(0, tk.END) 
        except:
            print("There is an error")

# ======================button part=====================

savebutton = tk.Button(edit, text="Save Changes", command=lambda:check_info())
savebutton.pack()

# # button for edit frame to go back to the main frame
mainbutton= tk.Button(edit, text="Main", command=lambda: raise_frame(profile))
mainbutton.pack()
        
# to display the first frame
raise_frame(profile)

root.mainloop()