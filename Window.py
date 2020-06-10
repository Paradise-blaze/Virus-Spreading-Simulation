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

        self.colors = {
            "field_background": "#333333",
            "field_text": "white"
        }

        self.disease_choice = ''
        self.region_choice = ''
        self.map_type_choice = None
        self.slide_num = 0
        self.day_step = 1
        self.simulation_process = None
        self.generator_process = None
        self.max_day = 0
        self.current_day = 0
        self.images_not_found = 0

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
        self.menu_pack_options['fill'] = tk.BOTH  #
        self.menu_pack_options['expand'] = True  #
        # configurations
        #self.menu_children_config_options['fill'] = '3 0'
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
        tk.Frame().winfo_children()
        for child in self.menus["custom"].winfo_children()[1].winfo_children():
            child.pack(expand=True, fill=tk.BOTH) #modifying custom's name label
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
            return lambda: self.set_language(button_name.lower())
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
                frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
            purified_name = Window.purify_name(name)
            button = tk.Button(frame, name=purified_name, text=self.trans(name))
            func = self.get_button_function(menu_name, name)
            button.config(command=func)
            self.set_child_pack_options(button)
            i += 1

        if with_return:
            #return_button = self.get_return_button(menu, "main")
            return_button = menu.nametowidget('main')
            return_button.pack(side=tk.RIGHT)

    def get_return_button(self, parent, destiny):
        return_btn = tk.Button(parent, name=destiny, text=self.trans("Return"))
        return return_btn

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
        names = ["region", "disease", "type"]
        to_translate = [self.region_choice, self.disease_choice, self.map_type_choice]
        self.hided_children["map"] = []
        for i in range(len(names)):
            if to_translate[i] is not  None:
                elem = tk.Entry(self.menu, name=names[i])
                elem.insert(tk.INSERT, self.trans(to_translate[i]))
                self.set_child_pack_options(elem)
                elem.config(state="disabled",
                            disabledbackground=self.colors["field_background"],
                            disabledforeground=self.colors["field_text"]) #  font=("Arial", 16)
                elem.pack(side=tk.LEFT)
                self.hided_children["map"].append(elem)

        for child in self.menu.winfo_children():
            if child.winfo_name() in ['main', 'diseases']:
                child.pack(side=tk.RIGHT)

    def region_generator_factory(self, name):
        return lambda: self.generate_region_plot(name)

    def create_plot_menu(self):
        menu = self.menus['plots']
        regions = list(set([self.region_choice, "Poland", "United States of America", "China", "Germany", "France", "Russia"]))
        for region in regions:
            button = tk.Button(menu, name=self.purify_name(region), text=self.trans(region))
            button.config(command=self.region_generator_factory(region))
            self.set_child_pack_options(button)

    def trans(self, word):
        if word in self.dictionary and self.dictionary[word] is not None and self.dictionary[word] != '':
            return self.dictionary[word]
        return word

    @staticmethod
    def destroy_children(widget, dont=""):
        for child in widget.winfo_children():
            if child.winfo_name() != dont:
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
        if name in ['main', 'return']:
            self.panel.config(image=self.scaled['map'])
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
            if isinstance(child, tk.Button) or isinstance(child, tk.Label):
                child.config(text=self.trans(child['text']))
            elif isinstance(child, tk.Scale):
                child.config(label=self.trans(child["label"]))
            self.translate_gui(child)

    def choose_disease(self, disease_name):
        self.disease_choice = disease_name
        self.display_regions()

    def choose_region(self, region_name):
        self.region_choice = region_name
        self.change_menu('confirmation')
        self.create_animation_widgets()

    def clear_choice(self, widget):
        self.disease_choice = ''
        self.region_choice = ''
        self.change_menu(widget)

    # Handlig custom simulation
    def set_custom_simulation(self, _):
        name = self.get_custom_name()
        coefficients = self.get_coefficients()
        args = [name]
        args.extend(coefficients)
        #self.run_simulation(args) # not working yet, we should see in C

    def get_custom_name(self):
        return self.menus['custom'].winfo_children()[1].winfo_children()[1]["text"]

    def get_coefficients(self):
        return [str(child.get()) for child in self.menus['custom'].winfo_children() if isinstance(child, tk.Scale)]

    # running and displaying simulation
    def run_simulation(self, args):
        all_args = [self.paths['program']]
        all_args.extend(args)
        self.simulation_process = subprocess.Popen(all_args)
        self.change_menu("simulation")
        self.wait_for_simulation()

    def confirm_and_run(self, _):
        self.run_simulation([self.disease_choice, self.region_choice])

    def wait_for_simulation(self):
        if self.simulation_process is not None and self.simulation_process.poll() is not None:
            self.map_generator.set_directory(self.disease_choice, self.region_choice)
            self.max_day = self.map_generator.get_max_day()
            self.simulation_process = None
        else:
            self.root.after(100, self.wait_for_simulation)

    def exists_simulation(self):
        return os.path.exists(os.path.join(self.paths['animation'], self.map_type_choice + "0.png"))

    def select_type(self, widget):
        self.map_type_choice = widget.winfo_name()
        self.paths['animation'] = os.path.join(self.paths['results'], self.disease_choice, self.region_choice, 'maps')
        if self.exists_simulation():
            self.change_menu("map")
            self.begin_display()
        else:
            self.current_day = mp.Value('i', 0)  # i stands for int
            self.generator_process = mp.Process(target=self.map_generator.generate_maps,
                                                args=(self.map_type_choice, self.current_day,))
            self.generator_process.start()
            self.change_menu("map")
            self.wait_for_generator()

    def wait_for_generator(self):
        if self.max_day - self.current_day.value <= self.day_step:
            self.begin_display()
        else:
            self.update_loading_status()
            self.root.after(1000, self.wait_for_generator)

    def update_loading_status(self):
        status = 100*self.current_day.value/self.max_day
        self.menu.nametowidget("main").config(text=self.trans("Generating") + " {:.2f}%".format(status))

    def begin_display(self):
        self.slide_num = 0
        self.create_animation_widgets()
        self.menu.nametowidget("main").config(text="return", command=lambda: self.change_menu("main"))
        self.display()

    def display(self):
        file = os.path.join(self.paths['animation'], "{}{}.png".format(self.map_type_choice, self.slide_num))
        self.slide_num += self.day_step
        if False and os.path.exists(file): # False to delete
            self.images_not_found = 0
            image = self.scale_image(Image.open(file))
            self.panel.config(image=image)
            self.panel.image = image
            self.root.after(100, self.display)
        elif self.images_not_found <= 11:
            self.images_not_found += 1
            self.root.after(1, self.display)
        else:
            self.destroy_children(self.menu, 'main')
            self.create_plot_menu()
            self.change_menu("plots")

    def generate_world_plot(self, _):
        self.map_generator.plot_world()
        self.display_plot("world")

    def generate_region_plot(self, name):
        self.map_generator.plot_country(name)
        self.display_plot(name)

    def display_plot(self, name):
        file = "{}_plot.png".format(name)
        path = os.path.join(self.paths["results"], self.disease_choice, self.region_choice, "plots", file)
        image = self.scale_image(Image.open(path))
        self.panel.config(image=image)
        self.panel.image = image
