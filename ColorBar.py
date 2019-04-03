'''
MIT License

Copyright (c) 2019 Saad Mairaj

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Version: 0.0.1

Repository:
https://github.com/Saadmairaj/Tkinter-Color-Bar

'''

from tkinter import *
from PIL import Image, ImageTk
from tkinter.font import Font
from tkinter import font
import numpy as np


# Round Soild square for the canvas
def create_rounded(self, x1, y1, x2, y2, r, color="black",**kw):
    self.create_arc(x1,  y1,  x1+r,   y1+r, start= 90, extent=90, style=PIESLICE, outline="", **kw)
    self.create_arc(x2-r-1, y1, x2-1, y1+r, start=  0, extent=90, style=PIESLICE, outline="", **kw)
    self.create_arc(x1, y2-r-1, x1+r, y2-1, start=180, extent=90, style=PIESLICE, outline="", **kw)
    self.create_arc(x2-r, y2-r, x2-1, y2-1, start=270, extent=90, style=PIESLICE, outline="", **kw)
    self.create_rectangle(x1+r/2, y1, x2-r/2, y2, width=0, **kw)
    self.create_rectangle(x1, y1+r/2, x2, y2-r/2, width=0, **kw)
Canvas.create_rounded = create_rounded

# Round Rectanle for the canvas
def rounded_rect(self, x, y, w, h, c, fill="black", linetags=None, arctags=None, **kw):
    self.create_arc(x,   y,   x+2*c,   y+2*c,   start= 90, extent=90, style="arc", outline=fill, **kw)
    self.create_arc(x+w-2*c, y+h-2*c, x+w, y+h, start=270, extent=90, style="arc", outline=fill, **kw)
    self.create_arc(x+w-2*c, y,   x+w, y+2*c,   start=  0, extent=90, style="arc", outline=fill, **kw)
    self.create_arc(x,   y+h-2*c, x+2*c,   y+h, start=180, extent=90, style="arc", outline=fill, **kw)
    self.create_line(x+c, y,   x+w-c, y    , fill=fill, **kw)
    self.create_line(x+c, y+h, x+w-c, y+h  , fill=fill, **kw)
    self.create_line(x,   y+c, x,     y+h-c, fill=fill, **kw)
    self.create_line(x+w, y+c, x+w,   y+h-c, fill=fill, **kw)
Canvas.create_roundsqaure = rounded_rect



class Colorscale(Canvas):
    """
        Color Scale for tkinter
        Use mousewheel to be presice
        "mousewheel" = False    # Disabled
        "mousewheel" = True     # Enabled

        Returns hexcode or RGB 
        if value = "hex" or value = "rgb" respectively
    """
    def __init__(self, *arg, **kw):
        
        self.val = kw.get("value", "rgb")
        self.command = kw.get("command")
        self.width = kw.get("width", 200)
        self.height = kw.get("height", 24)
        self._Mw_bool = kw.get("mousewheel", True)

        kw.pop("value", None)
        kw.pop("command", None)
        kw.pop("mousewheel", None)

        Canvas.__init__(self, *arg, **kw)
        self.config(highlightthickness=0)
        self.config(width=self.width, height=self.height)

        self._im = np.load("colorscale.npy")
        self._im = Image.fromarray(self._im)
        self._im = np.array(self._im)
        self._im = Image.fromarray(self._im)
        self._im = self._im.resize((self.width, self.height))
        self.pixels = self._im.load()
        self._im = ImageTk.PhotoImage(self._im)

        self.create_image(self.width/2,self.height/2, image=self._im)
        self.image = self._im

        self.create_roundsqaure(self.width/3 ,2, 5, self.height-4, 2, width=2, 
            fill="white", tags="marker")

        self.bind("<B1-Motion>", self.move_marker)
        self.bind("<ButtonRelease-1>", self.Release,"+")
        if self._Mw_bool:
            self.bind("<MouseWheel>", self.MouseWheel)
        self.xaxis = int(self.width/3)

    def configure(self, cnf=None, **kw):
        self.val = kw.get("value", self.val)
        self.command = kw.get("command", self.command)
        self.width = kw.get("width", self.width)
        self.height = kw.get("height", self.height)
        self._Mw_bool = kw.get("mousewheel", self._Mw_bool)

        kw.pop("value", None)
        kw.pop("command", None)
        kw.pop("mousewheel", None)

        if self._Mw_bool:
            self.bind("<MouseWheel>", self.MouseWheel)
        else: 
            self.unbind("<MouseWheel>")

        return super().configure(cnf=cnf, **kw)
    
    def config(self, cnf=None, **kw):
        self.val = kw.get("value", self.val)
        self.command = kw.get("command", self.command)
        self.width = kw.get("width", self.width)
        self.height = kw.get("height", self.height)
        self._Mw_bool = kw.get("mousewheel", self._Mw_bool)

        kw.pop("value", None)
        kw.pop("command", None)
        kw.pop("mousewheel", None)

        if self._Mw_bool:
            self.bind("<MouseWheel>", self.MouseWheel)
        else: 
            self.unbind("<MouseWheel>")

        return super().config(cnf=cnf, **kw)

    def Release(self, evt=None):
        "Internal function."
        self.delete("info")
        self.delete("markerbg")

    def RGBtoHEX(self, R,G,B):
        "Internal function."
        return '#%02x%02x%02x' % (R, G, B)

    def move_marker(self, evt, mw=None): 
        "Internal function."
        if mw: 
            evt.x = mw
            evt.y = 10
            self.count = 10
        
            def close():
                if self.count <= 0:
                    self.Release()
                    return
                self.count-=1
                self.after(500, close)
            close()

        if (evt.x>0 and evt.y>0 and evt.x<self.width and evt.y<self.height):
            if not mw: self.xaxis = evt.x
            RGB = self.pixels[evt.x,evt.y][:-1]
            hexcode = self.RGBtoHEX(RGB[0], RGB[1], RGB[2])

            if self.val == "rgb":
                spacer = 50
                spacbg = 40
                text = str(RGB)
                self.Return_value(RGB)
            elif self.val == "hex":
                spacer = 35
                spacbg = 25
                text = hexcode
                self.Return_value(hexcode)

            self.delete("marker")
            self.delete("markerbg")
            self.delete("info")
            self.create_roundsqaure(evt.x ,2, 5, self.height-4, 2, width=2, 
                fill="white",tags="marker")

            if evt.x < self.width-100:
                self.create_rounded(evt.x+spacer-spacbg, self.height/2-6, evt.x+spacer+spacbg, 
                    self.height/2+7, 6,fill="white", tags="markerbg")
                self.create_text(evt.x+spacer, self.height/2, text=text, 
                    font=Font(size=10), tags="info", fill=hexcode)
            else: 
                self.create_rounded(evt.x-spacer-spacbg, self.height/2-6, evt.x-spacer+spacbg, 
                    self.height/2+7, 6, fill="white", tags="markerbg")
                self.create_text(evt.x-spacer, self.height/2, text=text, 
                    font=Font(size=10), tags="info", fill=hexcode)

            self.update_idletasks()

    def Return_value(self, val):
        "Internal function."
        if self.command:
            return self.command(val)

    def MouseWheel(self, evt=None):
        "Internal function."
        if evt.delta <= -1 and self.xaxis < self.width:
            self.xaxis += 1
            self.move_marker(evt, mw=self.xaxis)
        
        if evt.delta >= 1 and self.xaxis > 1:
            self.xaxis -= 1
            self.move_marker(evt, mw=self.xaxis)


# Testing and demo
if __name__ == "__main__":
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