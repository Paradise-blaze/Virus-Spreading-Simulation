import geopandas as gp
import matplotlib.pyplot as plt
import pandas as pd
import os


class MapGenerator:
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

    def __init__(self):
        self.geopandas_countries = gp.read_file(gp.datasets.get_path('naturalearth_lowres'))
        self.csv_countries = None
        self.csv_path = ''
        self.disease = ''
        self.init_region = ''
        self.status = []
        self.frame_list = []
        self.result_directory = ''
        self.world_stats = {'susceptible': [], 'exposed': [], 'infectious': [], 'recovered': [], 'dead': []}

    def set_status(self, member):
        self.status.append(member)

    def set_directory(self, disease, init_region):
        self.disease = disease
        self.init_region = init_region
        self.result_directory = 'results/'+disease+'/'+init_region+'/'
        self.load_frames()
        self.gather_global_data()

    def get_directory(self):
        return self.result_directory

    def get_status(self):
        return self.status

    def check_status(self, member):
        return member in self.status

    def set_csv_path(self, path):
        self.csv_path = path
        self.csv_countries = pd.read_csv(path, header=0, sep=';')

    def get_csv_path(self):
        return self.csv_path

    def clear_data(self):
        to_drop = ['Antarctica', 'Falkland Is.', 'Fr. S. Antarctic Lands', 'N. Cyprus', 'Palestine', 'Taiwan',
                   'eSwatini', 'W. Sahara']

        for i in to_drop:
            self.csv_countries = self.csv_countries[self.csv_countries.name != i]

    def generate_maps(self, group):
        step = 0
        pandemic_condition = {}  # country/bool pair
        data_to_map = {'name': [], group: []}

        for frame in self.frame_list:
            data_to_map['name'].append(frame.name)
            data_to_map[group].append(0)
            pandemic_condition[frame.name] = True

        dead_in_countries = pd.DataFrame(data_to_map, columns=['name', group])
        dead_in_countries = dead_in_countries.set_index('name')
        merged = merge_data_frames(self.geopandas_countries, self.csv_countries, dead_in_countries)

        while True in pandemic_condition.values():
            for frame in self.frame_list:
                actual_list = frame.choose_list(group)
                if step in range(frame.start_day, frame.end_day + 1):
                    dead_in_countries.loc[frame.name][group] = actual_list[step - frame.start_day]
                    merged = merge_data_frames(self.geopandas_countries, self.csv_countries, dead_in_countries)
                elif step > frame.end_day:
                    pandemic_condition[frame.name] = False
            self.draw_map(merged, step, group)
            step += 1

        self.set_status(group)

    def load_frames(self):
        path = 'results/'+self.disease+'/'+self.init_region+'/sim_files/'
        for file in os.listdir(path):
            country = self.DataFrame(path + file)
            self.frame_list.append(country)

    def draw_map(self, data, i, group):
        fg, ax = plt.subplots(figsize=(10, 5))
        fg.set_facecolor('cyan')
        data.plot(column=group, ax=ax, cmap='Reds', linewidth=0.5, edgecolor='0.8',
                  missing_kwds={"color": "white"})

        results_dir = os.path.join(self.result_directory, 'maps/')

        if not os.path.isdir(results_dir):
            os.makedirs(results_dir)

        plt.axis('off')
        plt.savefig(results_dir + group + str(i) + '.png', facecolor=fg.get_facecolor())
        plt.close(fg)

    def gather_global_data(self):
        step = 0
        pandemic_condition = {}  # country/bool pair

        for frame in self.frame_list:
            pandemic_condition[frame.name] = True

        while True in pandemic_condition.values():
            self.world_stats['susceptible'].append(0)
            self.world_stats['exposed'].append(0)
            self.world_stats['infectious'].append(0)
            self.world_stats['recovered'].append(0)
            self.world_stats['dead'].append(0)

            for frame in self.frame_list:
                if step in range(frame.start_day, frame.end_day + 1):
                    self.world_stats['susceptible'][step] += frame.susceptible[step - frame.start_day]
                    self.world_stats['exposed'][step] += frame.exposed[step - frame.start_day]
                    self.world_stats['infectious'][step] += frame.infectious[step - frame.start_day]
                    self.world_stats['recovered'][step] += frame.recovered[step - frame.start_day]
                    self.world_stats['dead'][step] += frame.dead[step - frame.start_day]
                elif step > frame.end_day:
                    pandemic_condition[frame.name] = False
                    self.world_stats['susceptible'][step] += frame.susceptible[frame.end_day]
                    self.world_stats['exposed'][step] += frame.exposed[frame.end_day]
                    self.world_stats['infectious'][step] += frame.infectious[frame.end_day]
                    self.world_stats['recovered'][step] += frame.recovered[frame.end_day]
                    self.world_stats['dead'][step] += frame.dead[frame.end_day]

            step += 1

        self.world_stats['susceptible'].pop(len(self.world_stats['susceptible']) - 1)
        self.world_stats['exposed'].pop(len(self.world_stats['exposed']) - 1)
        self.world_stats['infectious'].pop(len(self.world_stats['infectious']) - 1)
        self.world_stats['recovered'].pop(len(self.world_stats['recovered']) - 1)
        self.world_stats['dead'].pop(len(self.world_stats['dead']) - 1)

    def plot_world(self):
        time = [i for i in range(0, len(self.world_stats['dead']))]

        plt.plot(time, self.world_stats['susceptible'], label='Susceptible')
        plt.plot(time, self.world_stats['exposed'], label='Exposed')
        plt.plot(time, self.world_stats['infectious'], label='Infectious')
        plt.plot(time, self.world_stats['recovered'], label='Recovered')
        plt.plot(time, self.world_stats['dead'], label='Dead')

        plt.ylabel('Number of people')
        plt.xlabel('Time (in days)')
        plt.legend()

        results_dir = os.path.join(self.result_directory, 'plots/')

        if not os.path.isdir(results_dir):
            os.makedirs(results_dir)

        plt.savefig(results_dir + 'world_plot.png')
        plt.close()

    def plot_country(self, country):
        time = [i for i in range(0, len(country.dead))]

        plt.plot(time, country.susceptible, label='Susceptible')
        plt.plot(time, country.exposed, label='Exposed')
        plt.plot(time, country.infectious, label='Infectious')
        plt.plot(time, country.recovered, label='Recovered')
        plt.plot(time, country.dead, label='Dead')

        plt.ylabel('Number of people')
        plt.xlabel('Time (in days)')
        plt.legend()

        results_dir = os.path.join(self.result_directory, 'plots/')

        if not os.path.isdir(results_dir):
            os.makedirs(results_dir)

        plt.savefig(results_dir + country.name + '_plot.png')
        plt.close()


def merge_data_frames(df1, df2, df3):
    tmp = df1.set_index('name').join(df2.set_index('name'))
    return tmp.join(df3)


if __name__ == "__main__":
    mapGen = MapGenerator()
    mapGen.set_csv_path('resources/Country.csv')
    mapGen.set_directory('measles', 'Solomon Is.')
    mapGen.clear_data()

    mapGen.generate_maps('susceptible')
    mapGen.generate_maps('exposed')
    mapGen.generate_maps('infectious')
    mapGen.generate_maps('recovered')
    mapGen.generate_maps('dead')

    print(mapGen.get_status())
    print(mapGen.check_status('susceptible'))

    print(mapGen.get_csv_path())
    print(mapGen.get_directory())

    mapGen.plot_world()

    for frame in mapGen.frame_list:
        mapGen.plot_country(frame)
