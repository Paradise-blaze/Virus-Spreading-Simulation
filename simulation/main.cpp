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
    while(i < borders.size()){
        region_name = borders.at(i).at(0);
        neighbour_name = borders.at(i).at(1);
        while (regions.at(j).getName() != region_name)
            j++;
        Region &region = regions.at(j);
        Region &neighbour = *find_if(regions.begin(), regions.end(),
                [neighbour_name](const Region &r) -> bool {return r.getName() == neighbour_name;});
        region.addConnection(neighbour, 1);
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

    // setting working directory
    fs::path dirPath = getWorkingDirectory();
    fs::path resourcesPath = dirPath / "resources";

    rawData regionsData = loadData(resourcesPath / "Country.csv", ';');
    rawData borders = loadData(resourcesPath / "Borders.csv", ';', false);

    vector<Region> regions = createRegions(regionsData);
    setConnections(regions, borders);

    rawRecord diseaseData;
    if (argc == 3) {  //saved disease
        disease = argv[1];
        initialRegion = argv[2];
        rawData diseasesData = loadData(resourcesPath / "Diseases.csv", ',');
        diseaseData = chooseDisease(diseasesData, disease);
    } else if(argc == 6){  //custom disease
        disease = argv[1];
        initialRegion = "";
        diseaseData.push_back(argv[1]);
        diseaseData.push_back(argv[2]);
        diseaseData.push_back(argv[3]);
        diseaseData.push_back(argv[4]);
        diseaseData.push_back(argv[5]);
    } else {  //no arguments
        disease = "measles";
        initialRegion = "Italy";
        rawData diseasesData = loadData(resourcesPath / "Diseases.csv", ',');
        diseaseData = chooseDisease(diseasesData, disease);
    }
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
