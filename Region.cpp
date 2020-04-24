//
// Created by szymon on 24.04.2020.
//

#include "Region.h"

Region::Region() = default;

Region::Region(std::string &name, double averAge, double healthCare, double transport, climateType climate, double alpha, double beta, double gamma1, double gamma2, double lambda, double mi, long int population, long int susceptible, long int exposed, long int infectious, long int recovered, long int dead) {
    this->name = name;
    this->averAge = averAge;
    this->healthCare = healthCare;
    this->transport = transport;
    this->climate = climate;
    this->alpha = alpha;
    this->beta = beta;
    this->gamma1 = gamma1;
    this->gamma2 = gamma2;
    this->lambda = lambda;
    this->mi = mi;
    this->population = population;
    this->susceptible = susceptible;
    this->exposed = exposed;
    this->infectious = infectious;
    this->recovered = recovered;
    this->dead = dead;
}