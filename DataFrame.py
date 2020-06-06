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

    scriptDir = os.path.dirname(__file__)
    resultsDir = os.path.join(scriptDir, 'maps/')

    if not os.path.isdir(resultsDir):
        os.makedirs(resultsDir)

    plt.axis('off')
    plt.savefig('maps/'+str(i)+'.png', facecolor=fg.get_facecolor())
    plt.close(fg)


def clearDirectory(path):
    if os.path.isdir(path):
        for file in os.scandir(path):
            os.remove(file)


def mergeDataFrames(df1, df2, df3):
    tmp = df1.set_index('name').join(df2.set_index('name'))
    return tmp.join(df3)


def main():             #te instrukcje trzeba będzie przerzucić do main w main.py
    step = 0
    dataFrameList = []
    pandemicCondition = {}    # country/bool pair
    dataToMap = {'name': [], 'dead': []}

    geopandasCountries = gp.read_file(gp.datasets.get_path('naturalearth_lowres'))
    csvCountries = pd.read_csv('resources/Country.csv', header=0, sep=';')
    csvCountries = clearData(csvCountries)

    for file in os.listdir('results/'):
        country = DataFrame('results/'+file)
        dataFrameList.append(country)
        dataToMap['name'].append(country.name)
        dataToMap['dead'].append(0)
        pandemicCondition[file] = True

    deadInCountries = pd.DataFrame(dataToMap, columns=['name', 'dead'])
    deadInCountries = deadInCountries.set_index('name')
    merged = mergeDataFrames(geopandasCountries, csvCountries, deadInCountries)

    clearDirectory(os.path.dirname(__file__)+"/maps/")

    while True in pandemicCondition.values():
        for frame in dataFrameList:
            if step in range(frame.startDay, frame.endDay+1):
                deadInCountries.loc[frame.name]['dead'] = frame.deadList[step-frame.startDay]
                merged = mergeDataFrames(geopandasCountries, csvCountries, deadInCountries)
            if step > frame.endDay:
                pandemicCondition[frame.name] = False
            drawMap(merged, step)
            step += 1


if __name__ == "__main__":
    main()
