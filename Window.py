import tkinter as tk
import xml.etree.ElementTree as et
from PIL import Image, ImageTk
import time
import csv
import os


class Window:
    translations_path = os.path.join('resources', 'translations.csv')

    @staticmethod
    def get_translations(from_lang, to_lang):
        with open(Window.translations_path) as f:
            translations = csv.DictReader(f)
            dictionary = {}
            for t in translations:
                dictionary[t[from_lang]] = t[to_lang]
        return dictionary

    def realize(self, root, to_add):
        if to_add.tag == "Form":
            for sub in to_add:
                self.realize(root, sub)
        else:
            tag = to_add.tag
            constructor = getattr(tk, tag, None)
            if constructor:
                options = to_add.attrib.copy()
                # print(tag, options)
                elem = constructor(root, **options)
                if 'command' in options:  # Empty function will be executed if no viable name has been typed
                    func = getattr(Window, options['command'], lambda _1, _2: None)
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
        self.root.title(title)
        self.panel = self.root.nametowidget("content.background")
        self.menu_pack_options = {}
        self.menu_children_config_options = {}
        self.current_language = 'english'
        self.menu = None
        self.menus = {}
        self.width = int(720 * 1.618)
        self.height = 720
        self.img = None
        self.paths = {}
        self.images = {}
        self.scaled = {}
        self.dictionary = {}

    def set_title(self, title):
        self.root.title(title)

    def set_data_path(self, path):
        self.paths["data"] = path

    def set_background_path(self, path):
        self.paths["background"] = path

    def set_map_path(self, path):
        self.paths["map"] = path

    def set_dimensions(self, width, height):
        self.width = width
        self.height = height

    def load_menu_options(self):
        # pack options
        self.menu_pack_options['side'] = tk.LEFT  # horizontal alignment
        # configurations
        self.menu_children_config_options['height'] = '3 0'
        pass

    @staticmethod
    def copy_configuration(original, copy):
        for config in original.config():
            try:
                copy.config({config: original.cget(config)})
            except:
                pass

    @staticmethod
    def get_languages_names():
        with open(Window.translations_path) as f:
            langs = f.readline().replace('\n', '').split(',')
        return [lang.title() for lang in langs]

    @staticmethod
    def get_diseases_names():
        names = []
        with open(os.path.join('resources', 'Diseases.csv')) as f:
            f.readline()
            for line in f.readlines():
                names.append(line.split(',', 1)[0])
        return names

    @staticmethod
    def get_custom_names(menu_name):
        if menu_name == 'languages':
            return Window.get_languages_names()
        elif menu_name == 'diseases':
            return Window.get_diseases_names()

    def get_button_function(self, menu_name, button_name):
        if menu_name == 'languages':
            return lambda: self.set_language(button_name)
        elif menu_name == 'diseases':
            return lambda: 0 # to add

    def set_dynamic_buttons(self, menu):
        menu_name = menu.winfo_name()
        if menu_name not in ['languages', 'diseases']:
            return

        names = Window.get_custom_names(menu_name)
        for name in names:
            button = tk.Button(menu, name=name.lower(), text=self.trans(name))
            func = self.get_button_function(menu_name, name.lower())
            button.config(command=func)
            self.set_child_pack_options(button)

        return_button = menu.nametowidget('main')
        return_button.pack(side=tk.RIGHT)
    
    def set_menu_pack_options(self, menu):
        for child in menu.winfo_children():
            self.set_child_pack_options(child)

    def set_child_pack_options(self, child):
        child.pack(**self.menu_pack_options)

    def load_menus(self):
        menu_holder = self.root.nametowidget("menus")
        for menu in menu_holder.winfo_children():
            self.copy_configuration(self.menu, menu)
            self.set_menu_pack_options(menu)
            self.set_dynamic_buttons(menu)

            menu.pack_forget()  # hides menu
            self.menus[menu.winfo_name()] = menu

    def load_images(self):
        for name in ["background", "map"]:
            self.images[name] = Image.open(self.paths[name])
            self.scaled[name] = self.scale_image(self.images[name])

    def scale_image(self, image):
        scaled = image.resize((self.width, self.height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(scaled)

    def load_all(self):
        self.load_images()
        self.load_menu_options()
        self.menu = self.root.nametowidget("content.menu")
        self.load_menus()
        self.menu = self.menus['initial']
    
    def set_all(self):
        self.panel.config(image=self.scaled["background"])
        self.panel.pack(side="bottom", fill="both", expand="yes")
        self.menu.pack()
        self.root.config(menu=self.menu)
        self.set_language('polish')
        # self.root.resizable(width=False, height=False)

    def set_language(self, language):
        self.dictionary = Window.get_translations(self.current_language, language)
        self.translate_gui(self.root)
        self.current_language = language

    def translate_gui(self, node):
        for child in node.winfo_children():
            if isinstance(child, tk.Button):
                child.config(text=self.trans(child['text']))
            self.translate_gui(child)

    def open(self):
        self.load_all()
        self.set_all()

        self.refresh()
        self.root.mainloop()

    def trans(self, word):
        if word in self.dictionary and self.dictionary[word] is not None:
            return self.dictionary[word]
        return word

    def change_menu(self, arg):
        self.menu.pack_forget()
        name = arg if isinstance(arg, str) else arg.winfo_name()
        if name in self.menus:
            self.menu = self.menus[name]

        self.menu.pack()

    def refresh(self):
        self.root.after(1000, self.refresh)  # refreshes every second

    # button methods
    def start_button(self, widget):
        self.panel.config(image=self.scaled["map"])
        self.change_menu(widget)

    def close_window(self, _):
        self.root.quit()
