#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include "Region.h"

using namespace std;
using rawData = vector<vector<string>>;
using rawRecord = vector<string>;

const string regionsPath = "/home/proxpxd/Desktop/moje_programy/simulations/Virus-Spreading-Simulation/resources/Country.csv";
const string diseasesPath = "/home/proxpxd/Desktop/moje_programy/simulations/Virus-Spreading-Simulation/resources/diseases.csv";


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

vector<Region> createRegions(rawData &data){
    vector<Region> regions;
    Region region;
    for(rawRecord d: data){
        // to fill constructor
        // think about all string constructor
        // with conversion inside
        region = Region();
        regions.push_back(region);
    }
    // creating connections between regions
    for (int i = 0; i < regions.size(); i++){
        //regions.at(i);
    }

    return regions;
}


int main() {
    // Choosing and loading disease to simulate
    rawData diseasesData = loadData(diseasesPath, ',');
    rawRecord diseaseData = chooseDisease(diseasesData);

    // Loading default regions' data
    rawData regionsData = loadData(regionsPath, ';');
    vector<Region> regions = createRegions(regionsData);

    // Creating simulation
    // potentially in the future
    //Simulation simulation = Simulation(regions, diseaseData);
    return 0;
}
