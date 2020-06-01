from Window import Window

window = Window("Virus Spreading", "gui.xml")
window.set_background_path("background.png")
window.set_map_path("map.png")
size = 580
window.set_dimensions(int(size * 1.618), size)
window.open()
