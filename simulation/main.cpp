#include <iostream>
#include <vector>
#include <filesystem>
#include <cstdlib>
#include <ctime>
#include "Region.h"
#include "Simulation.h"

#define MAX_DAYS 5000
#define FREQUENCY 30
#define PROJECT_NAME "Virus-Spreading-Simulation"

using namespace std;
namespace fs = std::filesystem;
using rawData = vector<vector<string>>;
using rawRecord = vector<string>;


rawRecord stringToVector(string &record, char delim){
    stringstream ss(record);
    rawRecord values;
    string val;
    while (getline(ss, val, delim))
        values.push_back(val);

    return values;
}

rawData loadData(const fs::path &path, char delim, bool header=true){
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

rawRecord chooseDisease(rawData data, string &choice){
    int i = 0;
    for(rawRecord &record: data){
        if (record.at(0) == choice)
            return data.at(i);
        i++;
    }
    return data.at(0);
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

fs::path getWorkingDirectory(){
    fs::path path = fs::current_path();
    while(path.filename().compare(PROJECT_NAME))
        path = path.parent_path();
    return path / "simulation";
}

int main(int argc, char *argv[]) {
    srand(time(nullptr));

    // Arguments
    string disease;
    string initialRegion;
    if (argc == 3) {
        disease = argv[1];
        initialRegion = argv[2];
    } else {
        disease = "measles";
        initialRegion = "Italy";
    }
    // Loading data
    fs::path dirPath = getWorkingDirectory();
    fs::path resourcesPath = dirPath / "resources";

    rawData diseasesData = loadData(resourcesPath / "Diseases.csv", ',');
    rawData regionsData = loadData(resourcesPath / "Country.csv", ';');
    rawData borders = loadData(resourcesPath / "Borders.csv", ';');

    rawRecord diseaseData = chooseDisease(diseasesData, disease);
    vector<Region> regions = createRegions(regionsData);
    setConnections(regions, borders);

    // Creating and setting simulation
    Simulation simulation = Simulation(regions, diseaseData);
    simulation.setSavingFrequency(FREQUENCY);
    simulation.setMaxDays(MAX_DAYS);
    simulation.setRegionZero(initialRegion);
    simulation.setSavingDirectory(dirPath / "results" / disease / initialRegion / "data");
    //turning simulation on
    simulation.simulate();
    return 0;
}
