#include <iostream>
#include <vector>
#include <filesystem>
#include <fstream>
#include "Region.h"

//namespace filesystem = experimental::filesystem;
using namespace std;

vector<string> getPaths(){
    string filesPath = "resources";

    vector<string> paths;
    /*
    for (const auto &file: filesystem::directory_iterator(filesPath)){
        paths.push_back(file.path());
    }
     */
    paths.push_back("../" + filesPath + "/regions.csv"); //temporally
    return paths;
}

string choosePath(vector<string> paths){
    int i = 0;
    cout << "Proszę wybrać numer zarazy" << endl;
    for(string &path: paths){
        cout << i + 1 << " " << path << endl;
    }
    int choice;
    //cin >> choice;
    choice = 1; // for tests
    return paths.at(choice-1);
}

vector<string> stringToVector(string &record, string &sep){
    stringstream ss(record);
    vector<string> result;
    string val;
    while (getline(ss, val,','))
        result.push_back(val);

    return result;
}

vector<vector<string>> loadData(string &path, string &sep){
    vector<vector<string>> initials;
    vector<string> country;
    ifstream file;
    file.open(path, ios::in);

    string line;
    while (getline(file, line)){
        country = stringToVector(line, sep);
    }
    return initials;
}

vector<Region> createRegions(vector<vector<string>> &data){
    vector<Region> regions;
    Region region;
    for(vector<string> d: data){
        // to fill constructor
        // think about all string constructor
        // with conversion inside
        region = Region();
        regions.push_back(region);
    }
    for (int i = 0; i < regions.size(); i++){
        //regions.at(i)
    }

    return regions;
}

int main() {
    string sep = ",";
    vector<string> paths = getPaths();
    string path = choosePath(paths);
    vector<vector<string>> data = loadData(path, sep);
    vector<Region> regions = createRegions(data);
    return 0;
}
