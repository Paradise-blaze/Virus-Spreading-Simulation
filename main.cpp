#include <iostream>
#include <vector>
#include <filesystem>
#include <fstream>
#include <iterator>

//namespace filesystem = std::experimental::filesystem;

std::vector<std::string> getPaths(){
    std::string filesPath = "resource";
    std::vector<std::string> paths;
    for (const auto &file: std::filesystem::directory_iterator(filesPath)){
        paths.push_back(file.path());
    }
    return paths;
}

std::string choosePath(std::vector<std::string> paths){
    int i = 0;
    std::cout << "Proszę wybrać numer zarazy" << std::endl;
    for(std::string &path: paths){
        std::cout << i + 1 << path << std::endl;
    }
    int choice;
    std::cin >> choice;
    return paths.at(choice-1);
}

std::vector<std::string> stringToVector(std::string &string, std::string &sep){
    std::stringstream ss(string);
    std::istream_iterator<std::string> beg(ss);
    std::istream_iterator<std::string> end;
    std::vector<std::string> result(beg, end);
    std::copy(result.begin(), result.end(), std::ostream_iterator<std::string>(ss, ","));
    for (const std::string &res: result){
        std::cout << res << std::endl;
    }
    return result;
}

std::vector<std::vector<std::string>> loadData(std::string &path, std::string &sep){
    std::vector<std::vector<std::string>> initials;
    std::vector<std::string> country;
    std::ifstream file;
    file.open(path, std::ios::in);
    std::string line;
    while (std::getline(file, line)){
        country = stringToVector(line, sep);
    }
    return initials;
}

int main() {
    std::string sep = ",";
    std::vector<std::string> paths = getPaths();
    std::string path = choosePath(paths);
    std::vector<std::vector<std::string>> data = loadData(path, sep);
    return 0;
}
