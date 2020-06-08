import tkinter as tk
import xml.etree.ElementTree as et
from PIL import Image, ImageTk
import time
import csv
import subprocess
import os


class Window:
    translations_path = os.path.join('resources', 'translations.csv')
    languages_names = None
    diseases_names = None
    regions_names = None

    @staticmethod
    def get_translations(from_lang, to_lang):
        from_lang = from_lang.lower()
        to_lang = to_lang.lower()
        with open(Window.translations_path) as f:
            translations = csv.DictReader(f)
            dictionary = {}
            for t in translations:
                dictionary[t[from_lang]] = t[to_lang]
        return dictionary

    @staticmethod
    def translate(dictionary, word):
        if word in dictionary and dictionary[word] is not None and dictionary[word] != '':
            return dictionary[word]
        return word

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

    @staticmethod
    def load_languages_names():
        with open(Window.translations_path) as f:
            langs = f.readline().replace('\n', '').split(',')
        Window.languages_names = [lang.title() for lang in langs]

    @staticmethod
    def load_diseases_names():
        names = []
        with open(os.path.join('resources', 'Diseases.csv')) as f:
            f.readline()
            for line in f.readlines():
                names.append(line.split(',', 1)[0])
        Window.diseases_names = names

    @staticmethod
    def load_regions_names():
        names = []
        with open(os.path.join('resources', 'Country.csv')) as f:
            f.readline()
            for line in f.readlines():
                names.append(line.split(';', 1)[0])
        Window.regions_names = names

    @staticmethod
    def get_custom_names(menu_name):
        if menu_name == 'languages':
            if Window.languages_names is None:
                Window.load_languages_names()
            return Window.languages_names
        elif menu_name == 'diseases':
            if Window.diseases_names is None:
                Window.load_diseases_names()
            return Window.diseases_names
        elif menu_name == 'panel':
            if Window.regions_names is None:
                Window.load_regions_names()
            return Window.regions_names

    def __init__(self, title, xml):
        self.root = self.realize(tk.Tk(), et.parse(xml).getroot())
        self.root.title(title)
        self.panel = self.root.nametowidget("content.panel")
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
        self.disease_choice = ''
        self.region_choice = ''
        self.process = None

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

    def set_menu_options(self):
        # pack options
        self.menu_pack_options['side'] = tk.LEFT  # horizontal alignment
        # configurations
        #self.menu_children_config_options['height'] = '3 0'
        pass

    def load_images(self):
        for name in ["background", "map"]:
            self.images[name] = Image.open(self.paths[name])
            self.scaled[name] = self.scale_image(self.images[name])

    def scale_image(self, image):
        scaled = image.resize((self.width, self.height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(scaled)

    def load_all(self):
        self.load_images()
        self.set_menu_options()
        self.menu = self.root.nametowidget("content.menu")
        self.load_menus()
        self.menu = self.menus['initial']

    def set_all(self):
        self.panel.config(image=self.scaled["background"])
        #self.panel.pack(side="bottom", fill="both", expand="yes")
        self.menu.pack()
        self.root.config(menu=self.menu)
        self.set_language('polish')
        # self.root.resizable(width=False, height=False)

    @staticmethod
    def copy_configuration(original, copy):
        for config in original.config():
            try:
                copy.config({config: original.cget(config)})
            except:
                pass

    def get_button_function(self, menu_name, button_name):
        if menu_name == 'languages':
            return lambda: self.set_language(button_name)
        elif menu_name == 'diseases':
            return lambda: self.choose_disease(button_name)
        elif menu_name == 'panel':
            return lambda: self.choose_region(button_name)

    # To use there should exist:
    # -get_custom_names
    # -get_button_function
    # methods for a menu name
    def set_dynamic_buttons(self, menu, with_return=True):
        menu_name = menu.winfo_name()
        if menu_name not in ['languages', 'diseases', 'panel']:
            return

        names = Window.get_custom_names(menu_name)
        i = 0
        max_in_row = 10
        frame = None
        for name in names:
            if i % max_in_row == 0:
                frame = tk.Frame(menu, name='frame{}'.format(i//max_in_row))
                frame.pack(side=tk.TOP)
            button = tk.Button(frame, name=Window.purify_name(name), text=self.trans(name))
            func = self.get_button_function(menu_name, name.lower())
            button.config(command=func)
            self.set_child_pack_options(button)
            i += 1

        if with_return:
            return_button = menu.nametowidget('main')
            return_button.pack(side=tk.RIGHT)

    @staticmethod
    def purify_name(name):
        new_name = name.lower()\
            .replace('.', '')
        return new_name

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

    def open(self):
        self.load_all()
        self.set_all()

        self.refresh()
        self.root.mainloop()

    def trans(self, word):
        return Window.translate(self.dictionary, word)

    def clear_panel(self):
        for child in self.panel.winfo_children():
            child.destroy()

    def change_menu(self, arg):
        self.menu.pack_forget()
        name = arg if isinstance(arg, str) else arg.winfo_name()
        if name in self.menus:
            self.menu = self.menus[name]
        self.clear_panel()
        self.menu.pack()

    def refresh(self):
        self.root.after(1000, self.refresh)  # refreshes every second

    def display_regions(self):
        self.set_dynamic_buttons(self.panel, False)

    # Button functions
    def start_button(self, widget):
        self.panel.config(image=self.scaled["map"])
        self.change_menu(widget)

    def close_window(self, _):
        self.root.quit()

    def set_language(self, language):
        if self.current_language != 'english' and language != 'english':
            self.set_language('english')
        self.dictionary = Window.get_translations(self.current_language, language)
        self.translate_gui(self.root)
        self.current_language = language

    def translate_gui(self, node):
        for child in node.winfo_children():
            if isinstance(child, tk.Button):
                child.config(text=self.trans(child['text']))
            self.translate_gui(child)

    def choose_disease(self, disease_name):
        self.disease_choice = disease_name
        if len(self.panel.winfo_children()) == 0:
            self.panel.pack_forget()
            self.display_regions()
            self.panel.pack()

    def choose_region(self, region_name):
        self.region_choice = region_name
        self.change_menu('confirmation')

    def clear_choice(self, widget):
        self.disease_choice = ''
        self.region_choice = ''
        self.change_menu(widget)

    def run_simulation(self, widget):
        program = os.path.join('cmake-build-debug', 'Virus_Spreading_Simulation')
        self.process = subprocess.Popen([program, self.disease_choice, self.region_choice])
        self.change_menu(widget)

