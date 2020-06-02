import tkinter as tk
import xml.etree.ElementTree as et
from PIL import Image, ImageTk
import time


class Window:

    def realize(self, root, to_add):
        if to_add.tag == "Form":
            for sub in to_add:
                self.realize(root, sub)
        else:
            tag = to_add.tag
            constructor = getattr(tk, tag, None)
            if constructor:
                options = to_add.attrib.copy()
                print(tag, options)
                elem = constructor(root, **options)
                if 'command' in options:
                    func = getattr(Window, options['command'], lambda _: None)
                    if func:
                        elem.config(command=lambda: func(self, elem))
                elif tag == "Button":
                    elem.config(command=lambda: self.change_menu(elem))
                for sub in to_add:
                    self.realize(elem, sub)
                elem.pack()

        return root

    def __init__(self, title, xml):
        self.root = self.realize(tk.Tk(), et.parse(xml).getroot())
        self.panel = self.root.nametowidget("content.background")
        self.menu_pack_options = {}
        self.menu_children_config_options = {}
        self.set_options()
        self.menu = self.root.nametowidget("content.menu")
        self.menus = {}
        self.load_menus()
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

    def set_options(self):
        #pack options
        self.menu_pack_options['side'] = tk.LEFT #horizontal alignment
        #configurations
        #self.menu_children_config_options[''] =

    def set_configuration(self, original, copy):
        for config in original.config():
            try:
                copy.config({config: original.cget(config)})
            except:
                pass

    def load_menus(self):
        menu_holder = self.root.nametowidget("menus")
        for menu in menu_holder.winfo_children():
            self.set_configuration(self.menu, menu)
            for child in menu.winfo_children():
                child.pack(**self.menu_pack_options)
            menu.pack_forget() #hides menu
            self.menus[menu.winfo_name()] = menu

    def open(self):
        self.root.title(self.title)
        self.load()
        self.scale()
        self.panel.config(image=self.scaled["background"])
        self.panel.pack(side="bottom", fill="both", expand="yes")

        self.menu = self.menus['initial']
        self.menu.pack()
        self.root.config(menu=self.menu)
        #self.root.resizable(width=False, height=False)
        self.refresh()
        self.root.mainloop()

    def load(self):
        #load images
        for name in ["background", "map"]:
            self.images[name] = Image.open(self.paths[name])

    def scale(self):
        for name in ["background", "map"]:
            image = self.images[name].resize((self.width, self.height), Image.ANTIALIAS)
            self.scaled[name] = ImageTk.PhotoImage(image)

    def change_menu(self, elem):
        self.menu.pack_forget()
        name = elem.winfo_name()
        if name in self.menus:
            self.menu = self.menus[name]

        self.menu.pack()

    def refresh(self):
        self.root.after(1000, self.refresh) #refreshes every second

    # button methods

    def start_button(self, elem):
        self.panel.config(image=self.scaled["map"])
        self.change_menu(elem)

    def close_window(self, _):
        self.root.quit()
