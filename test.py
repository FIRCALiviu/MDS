from customtkinter import CTk,LEFT,CTkButton

# Create the main window
root = CTk()

# Create two buttons
button1 = CTkButton(master=root, text="Button 1")
button2 = CTkButton(master=root, text="Button 2")

# Pack the buttons side-by-side
button1.pack(side=LEFT)
button2.pack(side=LEFT)

root.mainloop()
