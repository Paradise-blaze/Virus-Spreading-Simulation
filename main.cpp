#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include "Region.h"

using namespace std;
using rawData = vector<vector<string>>;
using rawRecord = vector<string>;

const string regionsPath = "/home/proxpxd/Desktop/moje_programy/simulations/Virus-Spreading-Simulation/resources/Country.csv";
const string diseasesPath = "/home/proxpxd/Desktop/moje_programy/simulations/Virus-Spreading-Simulation/resources/Diseases.csv";
const string bordersPath = "/home/proxpxd/Desktop/moje_programy/simulations/Virus-Spreading-Simulation/resources/Borders.csv";


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
    Region neighbour, region = regions.at(j);
    while(i < borders.size()){
        region_name = borders.at(i).at(0);
        neighbour_name = borders.at(i).at(1);
        while (region.getName() != region_name)
            region = regions.at(++j);

        neighbour = *find_if(regions.begin(), regions.end(), [neighbour_name](const Region &r) -> bool {return r.getName() == neighbour_name;});
        region.addConnection(neighbour, 1); // check the default value
        //cout << region_name << neighbour_name << "\n" << region.getName() << neighbour.getName() << endl;
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
    // Loading data
    rawData diseasesData = loadData(diseasesPath, ',');
    rawData regionsData = loadData(regionsPath, ';');
    rawData borders = loadData(bordersPath, ';');

    rawRecord diseaseData = chooseDisease(diseasesData);
    vector<Region> regions = createRegions(regionsData);
    setConnections(regions, borders);

    // Creating simulation
    // potentially in the future
    //Simulation simulation = Simulation(regions, diseaseData);
    return 0;
}
