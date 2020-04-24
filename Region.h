//
// Created by szymon on 24.04.2020.
//

#ifndef VIRUS_SPREADING_SIMULATION_REGION_H
#define VIRUS_SPREADING_SIMULATION_REGION_H

#include <string>

enum climateType {
    Tropical,
    Arid,
    Mediterranean,
    Temperate,
    Continental,
    Polar
};

class Region {
    std::string name;
    double averAge;
    double healthCare;
    double transport;
    climateType climate;
    double alpha;        //transfer to exposed
    double beta;         //infectiousness coefficient
    double gamma1;       //recovery coefficient
    double gamma2;       //death coefficient (disease)
    double lambda = 0;   //fertility coefficient
    double mi = 0;       //death coefficient (all cases)
    long int population;
    long int susceptible;
    long int exposed;
    long int infectious;
    long int recovered;
    long int dead;

    Region(std::string &, double, double, double, climateType, double, double, double, double, double, double, long int, long int, long int, long int, long int, long int);
};

#endif //VIRUS_SPREADING_SIMULATION_REGION_H
