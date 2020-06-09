import geopandas as gp
import matplotlib.pyplot as plt
import pandas as pd
import os


class MapGenerator:
    def __init__(self):
        self.geopandas_countries = gp.read_file(gp.datasets.get_path('naturalearth_lowres'))
        self.csv_countries = None
        self.path = ''
        self.status = []

    def get_status(self):
        return self.status

    def check_status(self, member):
        return member in self.status

    def set_path(self, path):
        self.path = path
        self.csv_countries = pd.read_csv(path, header=0, sep=';')

    def get_path(self):
        return self.path

    def clear_data(self):
        to_drop = ['Antarctica', 'Falkland Is.', 'Fr. S. Antarctic Lands', 'N. Cyprus', 'Palestine', 'Taiwan',
                   'eSwatini', 'W. Sahara']

        for i in to_drop:
            self.csv_countries = self.csv_countries[self.csv_countries.name != i]

    def generate_maps(self, group, frame_list):
        step = 0
        pandemic_condition = {}  # country/bool pair
        data_to_map = {'name': [], group: []}

        for frame in frame_list:
            data_to_map['name'].append(frame.name)
            data_to_map[group].append(0)
            pandemic_condition[frame.name] = True

        dead_in_countries = pd.DataFrame(data_to_map, columns=['name', group])
        dead_in_countries = dead_in_countries.set_index('name')
        merged = merge_data_frames(self.geopandas_countries, self.csv_countries, dead_in_countries)

        while True in pandemic_condition.values():
            for frame in frame_list:
                actual_list = frame.choose_list(group)
                if step in range(frame.start_day, frame.end_day + 1):
                    dead_in_countries.loc[frame.name][group] = actual_list[step - frame.start_day]
                    merged = merge_data_frames(self.geopandas_countries, self.csv_countries, dead_in_countries)
                elif step > frame.end_day:
                    pandemic_condition[frame.name] = False
            draw_map(merged, step, group)
            step += 1

        set_status(self.status, group)


class DataFrame:
    def __init__(self, path):
        file = open(path)
        lines = file.readlines()

        self.name = os.path.basename(path).split(';')[0]
        self.start_day = int(lines[0].split(';')[0])
        self.end_day = int(lines[len(lines)-1].split(';')[0])

        self.susceptible = []
        self.exposed = []
        self.infectious = []
        self.recovered = []
        self.dead = []

        for line in lines:
            numbers = line.split(';')
            self.susceptible.append(int(numbers[1]))
            self.exposed.append(int(numbers[2]))
            self.infectious.append(int(numbers[3]))
            self.recovered.append(int(numbers[4]))
            self.dead.append(int(numbers[5].strip()))

    def choose_list(self, name):
        if name == 'susceptible':
            return self.susceptible
        elif name == 'exposed':
            return self.exposed
        elif name == 'infectious':
            return self.infectious
        elif name == 'recovered':
            return self.recovered
        else:  # name == 'dead'
            return self.dead


def set_status(array, member):
    array.append(member)


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


def merge_data_frames(df1, df2, df3):
    tmp = df1.set_index('name').join(df2.set_index('name'))
    return tmp.join(df3)


def clear_directory(path):
    if os.path.isdir(path):
        for file in os.scandir(path):
            os.remove(file)


def load_data(frame_list):
    for file in os.listdir('results/'):
        country = DataFrame('results/'+file)
        frame_list.append(country)


def gather_global_data(frame_list):
    dictionary = {'susceptible': [], 'exposed': [], 'infectious': [], 'recovered': [], 'dead': []}
    step = 0
    pandemic_condition = {}  # country/bool pair

    for frame in frame_list:
        pandemic_condition[frame.name] = True

    while True in pandemic_condition.values():
        dictionary['susceptible'].append(0)
        dictionary['exposed'].append(0)
        dictionary['infectious'].append(0)
        dictionary['recovered'].append(0)
        dictionary['dead'].append(0)

        for frame in frame_list:
            if step in range(frame.start_day, frame.end_day+1):
                dictionary['susceptible'][step] += frame.susceptible[step-frame.start_day]
                dictionary['exposed'][step] += frame.exposed[step-frame.start_day]
                dictionary['infectious'][step] += frame.infectious[step-frame.start_day]
                dictionary['recovered'][step] += frame.recovered[step-frame.start_day]
                dictionary['dead'][step] += frame.dead[step-frame.start_day]
            elif step > frame.end_day:
                pandemic_condition[frame.name] = False
                dictionary['susceptible'][step] += frame.susceptible[frame.end_day]
                dictionary['exposed'][step] += frame.exposed[frame.end_day]
                dictionary['infectious'][step] += frame.infectious[frame.end_day]
                dictionary['recovered'][step] += frame.recovered[frame.end_day]
                dictionary['dead'][step] += frame.dead[frame.end_day]

        step += 1

    dictionary['susceptible'].pop(len(dictionary['susceptible'])-1)
    dictionary['exposed'].pop(len(dictionary['exposed'])-1)
    dictionary['infectious'].pop(len(dictionary['infectious'])-1)
    dictionary['recovered'].pop(len(dictionary['recovered'])-1)
    dictionary['dead'].pop(len(dictionary['dead'])-1)

    return dictionary


def plot_world(world):
    time = [i for i in range(0, len(world['dead']))]

    plt.plot(time, world['susceptible'], label='Susceptible')
    plt.plot(time, world['exposed'], label='Exposed')
    plt.plot(time, world['infectious'], label='Infectious')
    plt.plot(time, world['recovered'], label='Recovered')
    plt.plot(time, world['dead'], label='Dead')

    plt.ylabel('Number of people')
    plt.xlabel('Time (in days)')
    plt.legend()

    script_dir = os.path.dirname(__file__)
    results_dir = os.path.join(script_dir, 'plots/')

    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)

    plt.savefig('plots/world_plot.png')
    plt.close()


def plot_country(country):
    time = [i for i in range(0, len(country.dead))]

    plt.plot(time, country.susceptible, label='Susceptible')
    plt.plot(time, country.exposed, label='Exposed')
    plt.plot(time, country.infectious, label='Infectious')
    plt.plot(time, country.recovered, label='Recovered')
    plt.plot(time, country.dead, label='Dead')

    plt.ylabel('Number of people')
    plt.xlabel('Time (in days)')
    plt.legend()

    script_dir = os.path.dirname(__file__)
    results_dir = os.path.join(script_dir, 'plots/')

    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)

    plt.savefig('plots/'+country.name+'_plot.png')
    plt.close()


if __name__ == "__main__":
    data_frame_list = []            #tutaj będą zapisywane dane z plików
    load_data(data_frame_list)

    mapGen = MapGenerator()
    mapGen.set_path('resources/Country.csv')
    mapGen.clear_data()
    worldStats = gather_global_data(data_frame_list)       #słownik do generowania wykresu dla całego świata

    clear_directory(os.path.dirname(__file__)+"/maps/")         #ta funkcja czyści cały folder, być może będzie potrzebna implementacja kasująca wybrany rodzaj map
    clear_directory(os.path.dirname(__file__) + "/plots/")

    mapGen.generate_maps('susceptible', data_frame_list)
    print(mapGen.get_status())
    print(mapGen.check_status('susceptible'))
    #mapGen.generate_maps('exposed', data_frame_list)
    #mapGen.generate_maps('infectious', data_frame_list)
    #mapGen.generate_maps('recovered', data_frame_list)
    #mapGen.generate_maps('dead', data_frame_list)

    print(mapGen.get_path())

    plot_world(worldStats)

    for frame in data_frame_list:
        plot_country(frame)
