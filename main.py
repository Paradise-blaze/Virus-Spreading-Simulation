from Window import Window


window = Window("Virus Spreading")
window.set_background_path("background.png")
window.set_map_path("map.png")
size = 580
window.set_dimensions(int(size * 1.618), size)
window.open()

'''
img = ImageTk.PhotoImage(Image.open("test.png"))
        panel = tk.Label(root, image=img)

        form = et.parse("ui.xml").getroot()
        frame = realize(root, form)
        frame.pack()

        panel.pack(side="bottom", fill="both", expand="yes")
        root.mainloop()
'''
'''
def realize(master, element):
    if element.tag == "form":
        frame = tk.Frame(master, **element.attrib)
        for subelement in element:
            widget = realize(frame, subelement)
            widget.pack()
        return frame
    else:
        options = element.attrib
        if element:
            options = options.copy()
            for subelement in element:
                options[subelement.tag] = subelement.text
        widget_factory = getattr(tk, element.tag.capitalize())
        return widget_factory(master, **options)
'''