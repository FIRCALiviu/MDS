import os
import customtkinter as ctk
import mysql.connector
# Initialize the CustomTkinter app
app = ctk.CTk()

# Set window size and title
app.geometry("1000x500")
app.title("Budgeting app launcher")

def show_error(app, message):
    app.error_label.configure(text=message)
    try:
        app.error_label.show()
    except AttributeError:
        app.error_label.pack()
    app.after(2000, hide_error)


def hide_error():
        app.error_label.configure(text="")
        app.error_label.pack_forget()


# Define function to handle login
def login():
    username = entry_username.get()
    password = entry_password.get()
    
    try:
        mydb = mysql.connector.connect(
            
            host="localhost",
            user=username,
            password=password,
            database=username+"db"
            )
        mydb.close()
        
    except Exception:
        show_error(app,"Invalid password or account!")
        return
    command = f"echo {username} {password} | python paidapp.py  "
    os.system(command)
    
# Create and place username label and entry
label_username = ctk.CTkLabel(app, text="Username")
label_username.pack(pady=10)
entry_username = ctk.CTkEntry(app)
entry_username.pack(pady=5)

app.error_label = ctk.CTkLabel(
            app , text="", text_color="red", font=("Arial", 12)
        )
# Create and place password label and entry
label_password = ctk.CTkLabel(app, text="Password")
label_password.pack(pady=10)
entry_password = ctk.CTkEntry(app, show="*")
entry_password.pack(pady=5)

# Create and place login button
button_login = ctk.CTkButton(app, text="Login", command=login)
button_login.pack(pady=20)

# Run the app
app.mainloop()
