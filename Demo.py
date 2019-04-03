'''
This file is just to show the demo of Color Bar widget
'''

if __name__ == "__main__":
    from tkinter import *
    from ColorBar import Colorscale

    root = Tk()
    root.config({"bg":"black"})
    root.geometry("320x250+100+100")
    root.title("Tkinter Color Bar")

    L = Frame(root, bg="white", width=150, height=150)
    L.pack(padx=10, pady=(30, 10))

    CS = Colorscale(
                    width=300,                              # Width of the Widget
                    height=30,                              # Height of the Widget
                    value="hex",                            # Value either "hex" or "rgb"
                    mousewheel=0,                           # Mousewheel disabled
                    command=lambda hex: L.config(bg=hex)    # Function with a parameter to get the value
                    )

    CS.pack(side="bottom", padx=10, pady=(5))
    
    # Mousewheel Enabled
    CS.configure(mousewheel=1)
    
    root.mainloop()
