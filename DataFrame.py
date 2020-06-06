import geopandas as gp
import matplotlib.pyplot as plt
import pandas as pd
import os


class DataFrame:
    def __init__(self, path):
        file = open(path)
        lines = file.readlines()

        self.name = os.path.basename(path).split(';')[0]
        self.start_day = int(lines[0].split(';')[0])
        self.end_day = int(lines[len(lines)-1].split(';')[0])

        self.dead_list = []

        for line in lines:
            numbers = line.split(';')
            self.dead_list.append(int(numbers[(len(numbers)-1)].strip()))


def clear_data(gp_data):
    to_drop = ['Antarctica', 'Falkland Is.', 'Fr. S. Antarctic Lands', 'N. Cyprus', 'Palestine', 'Taiwan', 'eSwatini',
              'W. Sahara']

    for i in to_drop:
        gp_data = gp_data[gp_data.name != i]

    return gp_data.sort_values(by=['name'])


def draw_map(data, i, group):
    fg, ax = plt.subplots(figsize=(10, 5))
    fg.set_facecolor('cyan')
    data.plot(column=group, ax=ax, cmap='Reds', linewidth=0.5, edgecolor='0.8',
              missing_kwds={"color": "white"})

    script_dir = os.path.dirname(__file__)
    results_dir = os.path.join(script_dir, 'maps/')

    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)

    plt.axis('off')
    plt.savefig('maps/'+group+str(i)+'.png', facecolor=fg.get_facecolor())
    plt.close(fg)


def clear_directory(path):
    if os.path.isdir(path):
        for file in os.scandir(path):
            os.remove(file)


def merge_data_frames(df1, df2, df3):
    tmp = df1.set_index('name').join(df2.set_index('name'))
    return tmp.join(df3)


def map_generator(group):             #te instrukcje trzeba będzie przerzucić do main w main.py
    step = 0
    data_frame_list = []
    pandemic_condition = {}    # country/bool pair
    data_to_map = {'name': [], group: []}

    geopandas_countries = gp.read_file(gp.datasets.get_path('naturalearth_lowres'))
    csv_countries = pd.read_csv('resources/Country.csv', header=0, sep=';')
    csv_countries = clear_data(csv_countries)

    for file in os.listdir('results/'):
        country = DataFrame('results/'+file)
        data_frame_list.append(country)
        data_to_map['name'].append(country.name)
        data_to_map[group].append(0)
        pandemic_condition[file] = True

    dead_in_countries = pd.DataFrame(data_to_map, columns=['name', group])
    dead_in_countries = dead_in_countries.set_index('name')
    merged = merge_data_frames(geopandas_countries, csv_countries, dead_in_countries)

    while True in pandemic_condition.values():
        for frame in data_frame_list:
            if step in range(frame.start_day, frame.end_day+1):
                dead_in_countries.loc[frame.name][group] = frame.dead_list[step-frame.start_day]
                merged = merge_data_frames(geopandas_countries, csv_countries, dead_in_countries)
            if step > frame.end_day:
                pandemic_condition[frame.name] = False
            draw_map(merged, step, group)
            step += 1


if __name__ == "__main__":
    clear_directory(os.path.dirname(__file__)+"/maps/")
    map_generator('exposed')
    map_generator('dead')
