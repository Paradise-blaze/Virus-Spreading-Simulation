from Window import Window


window = Window("Virus Spreading", "gui.xml")
window.set_background_path("background.png")
window.set_map_path("map.png")
size = 580
window.set_dimensions(int(size * 1.618), size)
window.open()
'''
<LabelFrame text='Hello World' borderwidth='2' relief='groove' column='0' row='0' columnspan='2'>
        <Label text='Entry:' column='0' row='0'/>
        <Checkbutton name='check' text='checkbutton' column='1' row='0'/>
        <Entry name='entry' bg='gold' width='30' column='0' row='1' columnspan='2'/>
    </LabelFrame>
    <Button name='ok' text='OK' column='0' row='1'/>
    <Button name='cancel' text='Cancel' column='1' row='1'/>
'''
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