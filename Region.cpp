//
// Created by szymon on 24.04.2020.
//

#include "Region.h"

Region::Region() = default;
Region::Region(std::string &name, std::string &averAge, std::string &healthCare, std::string &transport, std::string &climate, std::string &alpha, std::string &beta, std::string &gamma1, std::string &gamma2, std::string &lambda, std::string &mi, std::string &population, std::string &susceptible, std::string &exposed, std::string &infectious, std::string &recovered, std::string &dead) {
    this->name = name;
    this->averAge = std::stod(averAge);
    this->healthCare = std::stod(healthCare);
    this->transport = std::stod(transport);
    this->climate = (climateType) std::stoi(climate);
    this->alpha = std::stod(alpha);
    this->beta = std::stod(beta);
    this->gamma1 = std::stod(gamma1);
    this->gamma2 = std::stod(gamma2);
    this->lambda = std::stod(lambda);
    this->mi = std::stod(mi);
    this->population = std::stol(population);
}

void Region::addConnection(Region &region, double val) {
    /*if (!connections.contains(region)){
        //connections.insert_or_assign(region, val);
    }*/
}