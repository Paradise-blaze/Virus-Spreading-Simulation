import tkinter as tk
import xml.etree.ElementTree as et
from PIL import Image, ImageTk
import time
import csv
import subprocess
import multiprocessing as mp
import os
from DataFrame import MapGenerator


class Window:
    translations_path = ''
    languages_names = None
    diseases_names = None
    regions_names = None

    @staticmethod
    def set_translations_path(path):
        Window.translations_path = path

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

    @staticmethod
    def load_languages_names():
        with open(Window.translations_path) as f:
            langs = f.readline().replace('\n', '').split(',')
        Window.languages_names = [lang.title() for lang in langs]

    def load_diseases_names(self):
        names = []
        with open(self.paths['diseases']) as f:
            f.readline()
            for line in f.readlines():
                names.append(line.split(',', 1)[0])
        Window.diseases_names = names

    def load_regions_names(self):
        names = []
        with open(self.paths['regions']) as f:
            f.readline()
            for line in f.readlines():
                names.append(line.split(';', 1)[0])
        Window.regions_names = names

    def get_custom_names(self, menu_name):
        if menu_name == 'languages':
            if Window.languages_names is None:
                Window.load_languages_names()
            return Window.languages_names
        elif menu_name == 'diseases':
            if Window.diseases_names is None:
                self.load_diseases_names()
            return Window.diseases_names
        elif menu_name == 'regions':
            if Window.regions_names is None:
                self.load_regions_names()
            return Window.regions_names

    def __init__(self, title, xml):
        self.root = self.realize(tk.Tk(), et.parse(xml).getroot())
        self.root.title(title)
        self.panel = self.root.nametowidget("content.panel")
        self.menu_pack_options = {}
        self.menu_children_config_options = {}
        self.current_language = 'english'
        self.map_generator = MapGenerator()
        self.menu = None
        self.menus = {}
        self.hided_children = {}
        self.width = int(720 * 1.618)
        self.height = 720
        self.img = None
        self.paths = {}
        self.images = {}
        self.scaled = {}
        self.dictionary = {}

        self.disease_choice = ''
        self.region_choice = ''
        self.map_type_choice = None
        self.slide_num = 0
        self.day_step = 1
        self.simulation_process = None
        self.generator_process = None
        self.max_day = 0
        self.current_day = 0

    def set_title(self, title):
        self.root.title(title)

    def set_data_path(self, path):
        self.paths["data"] = path

    def set_background_path(self, path):
        self.paths["background"] = path

    def set_map_path(self, path):
        self.paths["map"] = path

    def set_regions_path(self, path):
        self.paths["regions"] = path

    def set_diseases_path(self, path):
        self.paths["diseases"] = path

    def set_program_path(self, path):
        self.paths["program"] = path

    def set_results_path(self, path):
        self.paths["results"] = path

    def set_dimensions(self, width, height):
        self.width = width
        self.height = height

    def set_menu_options(self):
        # pack options
        self.menu_pack_options['side'] = tk.LEFT  # horizontal alignment
        # configurations
        #self.menu_children_config_options['height'] = '3 0'
        pass

    def set_day_step(self, step):
        self.day_step = step

    def load_images(self):
        for name in ["background", "map"]:
            self.images[name] = Image.open(self.paths[name])
            self.scaled[name] = self.scale_image(self.images[name])

    def scale_image(self, image):
        scaled = image.resize((self.width, self.height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(scaled)

    def load_panel_menus(self):
        self.set_dynamic_buttons(self.panel, False, 'regions')
        Window.hide_children(self.panel)

    def load_all(self):
        self.load_images()
        self.set_menu_options()
        self.menu = self.root.nametowidget("content.menu")
        self.load_menus()
        self.load_panel_menus()
        self.menu = self.menus['initial']

    def set_all(self):
        self.panel.config(image=self.scaled["background"])
        self.menu.pack()
        self.root.config(menu=self.menu)
        self.set_language('polish')
        self.set_generator()
        # self.root.resizable(width=False, height=False)

    def set_generator(self):
        self.map_generator.set_result_path(self.paths['results'])
        self.map_generator.set_day_step(self.day_step)

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
        elif menu_name == 'regions':
            return lambda: self.choose_region(button_name)

    # To use there should exist:
    # -get_custom_names
    # -get_button_function
    # methods for a menu name
    def set_dynamic_buttons(self, menu, with_return=True, name=None):
        menu_name = menu.winfo_name() if name is None else name
        if menu_name not in ['languages', 'diseases', 'regions']:
            return
        self.hided_children[menu_name] = []
        names = self.get_custom_names(menu_name)
        i = 0
        max_in_row = 10
        frame = None
        for name in names:
            if i % max_in_row == 0:
                frame = tk.Frame(menu, name='frame{}'.format(i//max_in_row))
                self.hided_children[menu_name].append(frame)
                frame.pack(side=tk.TOP)
            purified_name = Window.purify_name(name)
            button = tk.Button(frame, name=purified_name, text=self.trans(name))
            func = self.get_button_function(menu_name, name)
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
        '''
        #Example of animation at the start
        self.disease_choice = "SARS"
        self.region_choice = "United States of America"
        self.map_type_choice = "exposed"
        self.paths['animation'] = os.path.join(self.paths['results'], self.disease_choice, self.region_choice, 'maps')
        self.display()
        '''

        self.root.mainloop()

    def create_animation_widgets(self):
        pass#r = tk.Text(self.menu, name="region", text=self.region_choice)
        #d = tk.Text(self.menu, name="disease", text=self.disease_choice)
        #t = tk.Text(self.menu, name="type", text=self.map_type_choice)
        #self.hided_children["map"] = [r, d, t]

    def trans(self, word):
        if word in self.dictionary and self.dictionary[word] is not None and self.dictionary[word] != '':
            return self.dictionary[word]
        return word

    @staticmethod
    def destroy_children(widget):
        for child in widget.winfo_children():
            child.destroy()

    @staticmethod
    def hide_children(widget):
        for child in widget.winfo_children():
            child.pack_forget()

    def change_menu(self, arg):
        self.menu.pack_forget()
        name = arg if isinstance(arg, str) else arg.winfo_name()
        if name in self.menus:
            self.menu = self.menus[name]
        Window.hide_children(self.panel)
        self.menu.pack()

    def display_regions(self):
        for child in self.hided_children['regions']:
            child.pack(side=tk.TOP)

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
        self.display_regions()

    def choose_region(self, region_name):
        self.region_choice = region_name
        self.change_menu('confirmation')

    def clear_choice(self, widget):
        self.disease_choice = ''
        self.region_choice = ''
        self.change_menu(widget)

    def select_type(self, widget):
        self.map_type_choice = widget.winfo_name()
        self.change_menu("map")

    # running and displaying simulation
    def run_simulation(self, widget):
        self.simulation_process = subprocess.Popen([self.paths['program'], self.disease_choice, self.region_choice])
        self.change_menu(widget)
        self.wait_for_simulation()

    def wait_for_simulation(self):
        if self.simulation_process is not None and self.simulation_process.poll() is not None:
            self.map_generator.set_directory(self.disease_choice, self.region_choice)
            self.max_day = self.map_generator.get_max_day()
            self.simulation_process = None
            self.wait_for_map_type_choice()
        else:
            self.root.after(100, self.wait_for_simulation)

    def wait_for_map_type_choice(self):
        if self.map_type_choice is not None:
            self.current_day = mp.Value('i', 0)  # i stands for int
            self.generator_process = mp.Process(target=self.map_generator.generate_maps, args=(self.map_type_choice, self.current_day,))
            self.generator_process.start()
            self.wait_for_generator()
        else:
            self.root.after(1000, self.wait_for_map_type_choice)

    def wait_for_generator(self):
        if self.max_day - self.current_day.value < self.day_step:
            self.paths['animation'] = os.path.join(self.paths['results'], self.disease_choice, self.region_choice, 'maps')
            self.slide_num = 0
            self.create_animation_widgets()
            self.menu.nametowidget("main").config(text="return", command=lambda: self.change_menu("main"))
            self.display()
        else:
            self.update_loading_status()
            self.root.after(1000, self.wait_for_generator)

    def update_loading_status(self):
        status = 100*self.current_day.value/self.max_day
        self.menu.nametowidget("main").config(text=self.trans("Generating") + " {:.2f}%".format(status))

    def display(self):
        file = os.path.join(self.paths['animation'], "{}{}.png".format(self.map_type_choice, self.slide_num))
        if os.path.exists(file):
            self.slide_num += self.day_step
            print(self.slide_num)
            image = self.scale_image(Image.open(file))
            self.panel.config(image=image)
            self.panel.image = image
            self.root.after(100, self.display)


