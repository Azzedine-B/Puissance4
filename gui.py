from tkinter import *

"""
everything is a widget
"""

root = Tk()

# title of the application
title = Label(root, text="Puissance 4")
title.pack()

"""
Button parameters
state : DISABLE, ENABLE
padx : value
pady : value
command : nameofthefunction
"""

# create a function for that button mode
myButton = Button(root, text="Mode Joueur-Joueur", padx= 25, pady= 25)
myButton.pack()

root.mainloop()
