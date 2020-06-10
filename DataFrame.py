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
            self.end_day = int(lines[len(lines) - 1].split(';')[0])
            self.susceptible = []
            self.exposed = []
            self.infectious = []
            self.recovered = []
            self.dead = []
            self.population = 0

            for line in lines:
                numbers = line.split(';')
                self.susceptible.append(float(numbers[1]))
                self.exposed.append(float(numbers[2]))
                self.infectious.append(float(numbers[3]))
                self.recovered.append(float(numbers[4]))
                self.dead.append(float(numbers[5].strip()))

            self.population = self.susceptible[0] + self.exposed[0] + self.infectious[0] + self.recovered[0] + self.dead[0]

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
        self.result_path = ''
        self.disease = ''
        self.init_region = ''
        self.status = []
        self.frame_list = []
        self.max_day = 0
        self.curr_day = 0
        self.day_step = None
        self.result_directory = ''
        self.world_stats = {'susceptible': [], 'exposed': [], 'infectious': [], 'recovered': [], 'dead': []}

    def set_result_path(self, path):
        self.result_path = path

    def set_day_step(self, day):
        self.day_step = day

    def set_max_day(self, day):
        self.max_day = day

    def set_status(self, member):
        self.status.append(member)

    def set_directory(self, disease, init_region):
        self.disease = disease
        self.init_region = init_region
        self.result_directory = os.path.join(self.result_path, disease, init_region)
        self.max_day = self.load_frames()
        self.gather_global_data()

    def get_directory(self):
        return self.result_directory

    def get_status(self):
        return self.status

    def get_current_day(self):
        return self.curr_day

    def get_max_day(self):
        return self.max_day

    def check_status(self, member):
        return member in self.status

    def generate_maps(self, group, curr_day):
        data_to_map = {'name': [], 'population': [], group: []}

        for frame in self.frame_list:
            data_to_map['name'].append(frame.name)
            data_to_map['population'].append(frame.population)
            data_to_map[group].append(0)

        group_in_countries = pd.DataFrame(data_to_map, columns=['name', 'population', group])
        merged = self.geopandas_countries.set_index('name').join(group_in_countries.set_index('name'))

        self.curr_day = 0
        for step in range(0, self.max_day, self.day_step):
            curr_day.value = step
            self.curr_day = step
            for frame in self.frame_list:
                actual_list = frame.choose_list(group)
                if group == 'susceptible' and step < frame.start_day:
                    merged.loc[frame.name, group] = actual_list[0]
                if frame.start_day <= step <= frame.end_day:
                    merged.loc[frame.name, group] = actual_list[step - frame.start_day]
                elif step > frame.end_day:
                    merged.loc[frame.name, group] = actual_list[-1]
            self.draw_map(merged, step, group)

        self.set_status(group)

    def load_frames(self):
        path = os.path.join(self.result_directory, 'data')
        maximum = 0
        for file in os.listdir(path):
            country = self.DataFrame(os.path.join(path, file))
            if maximum < country.end_day:
                maximum = country.end_day
            self.frame_list.append(country)

        return maximum

    def draw_map(self, data, i, group):
        fg, ax = plt.subplots(figsize=(10, 5))
        fg.set_facecolor('cyan')

        data[group] = data.apply(lambda x: x[group] / x['population'], axis=1)
        max_value = data[group].max()

        data.plot(column=group, ax=ax, cmap='Reds', linewidth=0.5, edgecolor='0.8',
                  missing_kwds={"color": "white"}, vmin=0, vmax=max_value, legend=True)

        results_dir = os.path.join(self.result_directory, 'maps/')

        if not os.path.isdir(results_dir):
            os.makedirs(results_dir)

        plt.axis('off')
        plt.savefig(results_dir + group + str(i) + '.png', facecolor=fg.get_facecolor())
        plt.close(fg)

    def gather_global_data(self):
        for step in range(0, self.max_day):
            self.world_stats['susceptible'].append(0)
            self.world_stats['exposed'].append(0)
            self.world_stats['infectious'].append(0)
            self.world_stats['recovered'].append(0)
            self.world_stats['dead'].append(0)

            for frame in self.frame_list:
                if step < frame.start_day:
                    self.world_stats['susceptible'][step] += frame.susceptible[0]
                    self.world_stats['exposed'][step] += frame.exposed[0]
                    self.world_stats['infectious'][step] += frame.infectious[0]
                    self.world_stats['recovered'][step] += frame.recovered[0]
                    self.world_stats['dead'][step] += frame.dead[0]
                elif frame.start_day <= step < frame.end_day:
                    self.world_stats['susceptible'][step] += frame.susceptible[step - frame.start_day]
                    self.world_stats['exposed'][step] += frame.exposed[step - frame.start_day]
                    self.world_stats['infectious'][step] += frame.infectious[step - frame.start_day]
                    self.world_stats['recovered'][step] += frame.recovered[step - frame.start_day]
                    self.world_stats['dead'][step] += frame.dead[step - frame.start_day]
                elif step >= frame.end_day:
                    self.world_stats['susceptible'][step] += frame.susceptible[frame.end_day - frame.start_day]
                    self.world_stats['exposed'][step] += frame.exposed[frame.end_day - frame.start_day]
                    self.world_stats['infectious'][step] += frame.infectious[frame.end_day - frame.start_day]
                    self.world_stats['recovered'][step] += frame.recovered[frame.end_day - frame.start_day]
                    self.world_stats['dead'][step] += frame.dead[frame.end_day - frame.start_day]

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

        results_dir = os.path.join(self.result_directory, 'plots')

        if not os.path.isdir(results_dir):
            os.makedirs(results_dir)

        plt.savefig(os.path.join(results_dir, 'world_plot.png'))
        plt.close()


    def plot_country(self, country_name):
        country = next((frame for frame in self.frame_list if frame.name == country_name), None)
        if country_name is None:
            return
        time = [i for i in range(0, len(country.dead))]

        plt.plot(time, country.susceptible, label='Susceptible')
        plt.plot(time, country.exposed, label='Exposed')
        plt.plot(time, country.infectious, label='Infectious')
        plt.plot(time, country.recovered, label='Recovered')
        plt.plot(time, country.dead, label='Dead')

        plt.ylabel('Number of people')
        plt.xlabel('Time (in days)')
        plt.legend()

        results_dir = os.path.join(self.result_directory, 'plots')

        if not os.path.isdir(results_dir):
            os.makedirs(results_dir)

        plt.savefig(os.path.join(results_dir, country.name) + '_plot.png')
        plt.close()

