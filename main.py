import os
from Window import Window

window = Window("Virus Spreading", os.path.join("resources", "gui.xml"))
window.set_background_path(os.path.join("images", "background.png"))
window.set_map_path(os.path.join("images", "map.png"))
window.set_diseases_path(os.path.join('resources', 'Diseases.csv'))
window.set_regions_path(os.path.join('resources', 'Country.csv'))
size = 580
window.set_dimensions(int(size * 1.618), size)
window.open()
