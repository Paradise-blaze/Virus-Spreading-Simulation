import os
from Window import Window

base_dir = 'simulation'
Window.set_translations_path(os.path.join(base_dir, 'resources', 'translations.csv'))

window = Window("Virus Spreading", os.path.join(base_dir, "resources", "gui.xml"))
window.set_background_path(os.path.join(base_dir, "images", "background.png"))
window.set_map_path(os.path.join(base_dir, "images", "map.png"))
window.set_diseases_path(os.path.join(base_dir, 'resources', 'Diseases.csv'))
window.set_regions_path(os.path.join(base_dir, 'resources', 'Country.csv'))
size = 580
window.set_dimensions(int(size * 1.618), size)
window.open()
