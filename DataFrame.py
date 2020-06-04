import geopandas as gp
import matplotlib.pyplot as plt
import pandas as pd
import os


class DataFrame:
    def __init__(self, path):
        file = open(path)
        lines = file.readlines()

        self.name = os.path.basename(path).split(';')[0]
        self.startDay = int(lines[0].split(';')[0])
        self.endDay = int(lines[len(lines)-1].split(';')[0])

        self.deadList = []

        for line in lines:
            numbers = line.split(';')
            self.deadList.append(int(numbers[(len(numbers)-1)].strip()))


def clearData(gp_data):
    toDrop = ['Antarctica', 'Falkland Is.', 'Fr. S. Antarctic Lands', 'N. Cyprus', 'Palestine', 'Taiwan', 'eSwatini',
              'W. Sahara']

    for i in toDrop:
        gp_data = gp_data[gp_data.name != i]

    return gp_data.sort_values(by=['name'])


def drawMap(data, i):
    fg, ax = plt.subplots(figsize=(10, 5))
    fg.set_facecolor('cyan')
    data.plot(column='dead', ax=ax, cmap='Reds', linewidth=0.5, edgecolor='0.8',
              missing_kwds={"color": "white"})

    script_dir = os.path.dirname(__file__)
    results_dir = os.path.join(script_dir, 'maps/')

    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)

    plt.axis('off')
    plt.savefig('maps/'+str(i)+'.png', facecolor=fg.get_facecolor())
    plt.close(fg)


def main():             #te instrukcje trzeba będzie przerzucić do main w main.py
    step = 0
    dataFrameList = []
    pandemyDict = {}
    currentDead = {'name': [], 'dead': []}

    world = gp.read_file(gp.datasets.get_path('naturalearth_lowres'))
    countries = pd.read_csv('resources/Country.csv', header=0, sep=';')
    countries = clearData(countries)

    for file in os.listdir('results/'):
        country = DataFrame('results/'+file)
        dataFrameList.append(country)
        currentDead['name'].append(country.name)
        currentDead['dead'].append(0)
        pandemyDict[file] = True

    df = pd.DataFrame(currentDead, columns=['name', 'dead'])
    df = df.set_index('name')
    tmp = world.set_index('name').join(countries.set_index('name'))
    merged = tmp.join(df)

    while True in pandemyDict.values():
        for frame in dataFrameList:
            if step in range(frame.startDay, frame.endDay+1):
                df.loc[frame.name]['dead'] = frame.deadList[step-frame.startDay]
                tmp = world.set_index('name').join(countries.set_index('name'))
                merged = tmp.join(df)
            if step > frame.endDay:
                pandemyDict[frame.name] = False
            drawMap(merged, step)
            step += 1


if __name__ == "__main__":
    main()
