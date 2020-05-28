#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <cstdlib>
#include <ctime>
#include "Region.h"
#include "Simulation.h"

#define MAX_DAYS 5000
#define FREQUENCY 30

using namespace std;
using rawData = vector<vector<string>>;
using rawRecord = vector<string>;

const string PiDisPath = "/home/proxpxd/Desktop/moje_programy/simulations/Virus-Spreading-Simulation/resources/Diseases.csv";
const string PiCouPath = "/home/proxpxd/Desktop/moje_programy/simulations/Virus-Spreading-Simulation/resources/Country.csv";
const string PiBorPath = "/home/proxpxd/Desktop/moje_programy/simulations/Virus-Spreading-Simulation/resources/Borders.csv";
const string SzDisPath = "/home/szymon/Pulpit/Programowanie/C++/Virus-Spreading-Simulation/resources/Diseases.csv";
const string SzCouPath = "/home/szymon/Pulpit/Programowanie/C++/Virus-Spreading-Simulation/resources/Country.csv";
const string SzBorPath = "/home/szymon/Pulpit/Programowanie/C++/Virus-Spreading-Simulation/resources/Borders.csv";
const string JaDisPath = "D:/Studia/Virus-Spreading-Simulation/resources/Diseases.csv";
const string JaCouPath = "D:/Studia/Virus-Spreading-Simulation/resources/Country.csv";
const string JaBorPath = "D:/Studia/Virus-Spreading-Simulation/resources/Borders.csv";

rawRecord stringToVector(string &record, char delim){
    stringstream ss(record);
    rawRecord values;
    string val;
    while (getline(ss, val, delim))
        values.push_back(val);

    return values;
}

rawData loadData(const string &path, char delim, bool header=true){
    rawData data;
    rawRecord  values;
    ifstream file;
    file.open(path, ios::in);

    string line;
    if (header)
        file.ignore(numeric_limits<streamsize>::max(), '\n');

    while (getline(file, line)) {
        values = stringToVector(line, delim);
        data.push_back(values);
    }
    return data;
}

rawRecord chooseDisease(rawData data){
    int i = 0;
    cout << "Proszę wybrać numer zarazy:" << endl;
    for(rawRecord &record: data){
        cout << i + 1 << ": " << record.at(0) << endl;
        i++;
    }
    int choice;
    //cin >> choice;
    choice = 1; // for tests
    return data.at(choice-1);
}

void setConnections(vector<Region> regions, rawData borders){
    // creating connections between regions
    int i = 0, j = 0;
    string neighbour_name, region_name;
    Region region = regions.at(j);
    while(i < borders.size()){
        region_name = borders.at(i).at(0);
        neighbour_name = borders.at(i).at(1);
        while (region.getName() != region_name)
            region = regions.at(++j);

        Region &neighbour = *find_if(regions.begin(), regions.end(), [neighbour_name](const Region &r) -> bool {return r.getName() == neighbour_name;});
        region.addConnection(neighbour, 1); // check the default value
        i++;
    }
}

vector<Region> createRegions(rawData &data){
    vector<Region> regions;
    Region region;
    for(rawRecord d: data){
        region = Region(d.at(0), d.at(1), d.at(2), d.at(3), d.at(4), d.at(7));
        region.setNaturalGrowth(d.at(5), d.at(6));
        regions.push_back(region);
    }
    return regions;
}

int main() {
    srand(time(nullptr));
    // Loading data
    rawData diseasesData = loadData(JaDisPath, ',');
    rawData regionsData = loadData(JaCouPath, ';');
    rawData borders = loadData(JaBorPath, ';');

    rawRecord diseaseData = chooseDisease(diseasesData);
    vector<Region> regions = createRegions(regionsData);
    setConnections(regions, borders);

    // Creating and setting simulation
    Simulation simulation = Simulation(regions, diseaseData);
    simulation.setSavingFrequency(FREQUENCY);
    simulation.setMaxDays(MAX_DAYS);

    //turning simulation on
    simulation.simulate();
    return 0;
}
