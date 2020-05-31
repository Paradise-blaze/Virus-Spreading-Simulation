import tkinter as tk
import xml.etree.ElementTree as et
from PIL import Image, ImageTk
import time


def realize(master, element):
    lf = tk.LabelFrame()
    print(element.tag, element.attrib)
    for sub in element:
        realize(master, sub)
    return lf


class Window:

    def __init__(self, title):
        self.root = tk.Tk()
        self.title = title
        self.width = int(720 * 1.618)
        self.height = 720
        self.img = None
        self.paths = {}
        self.images = {}
        self.scaled = {}

    def set_title(self, title):
        self.title = title

    def set_data_path(self, path):
        self.paths["data"] = path

    def set_background_path(self, path):
        self.paths["background"] = path

    def set_map_path(self, path):
        self.paths["map"] = path

    def set_dimensions(self, width, height):
        self.width = width
        self.height = height

    def open(self):
        self.root.title(self.title)
        self.load()
        self.scale()
        panel = tk.Label(self.root, image=self.scaled["background"])
        panel.pack(side="bottom", fill="both", expand="yes")
        self.root.resizable(width=False, height=False)
        self.refresh()
        self.root.mainloop()

    def load(self):
        for name in ["background", "map"]:
            self.images[name] = Image.open(self.paths[name])

    def scale(self):
        for name in ["background", "map"]:
            image = self.images[name].resize((self.width, self.height), Image.ANTIALIAS)
            self.scaled[name] = ImageTk.PhotoImage(image)

    def refresh(self):
        print(time.asctime())
        self.root.after(1000, self.refresh) #refreshes every second

