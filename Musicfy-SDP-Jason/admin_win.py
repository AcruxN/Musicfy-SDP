import tkinter as tk
from tkinter import Listbox, messagebox

from py_SQL import db_connection

db, mycursor = db_connection()

root = tk.Tk()
root.title("Admin")
root.geometry("350x350")



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
searchUser = tk.Label(root, text="Username | ID: ")
searchUser.grid(row=2, column=5)

admin_label = tk.Label(root, text="To ban user, enter their user id")
admin_label.grid(row=1, column=5)

userEntry = tk.Entry(root)
userEntry.bind("<KeyRelease>", check)
userEntry.grid(row=2, column=6)

all_data = tk.Button(root, text="Show All Data", command = showuser)
all_data.grid(row=3, column=5)

search_button = tk.Button(root, text="Ban", command = banuser)
search_button.grid(row=3, column=6)

delete_button = tk.Button(root, text="Delete", command = deleteuser)
delete_button.grid(row=3, column=7)

list = Listbox(root)
list.grid(row=4, column=5)

showuser()
root.mainloop()