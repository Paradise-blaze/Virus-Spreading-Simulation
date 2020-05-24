//
// Created by proxpxd on 5/22/20.
//

#include "Simulation.h"

#define INFECT_CHANCE 5

Simulation::Simulation() = default;
Simulation::Simulation(vector<Region> &regions, vector<string> &disease_data) {
    disease_name = disease_data.at(0);
    alpha = Region::stod(disease_data.at(1));
    beta = Region::stod(disease_data.at(2));
    gamma1 = Region::stod(disease_data.at(3));
    gamma2 = Region::stod(disease_data.at(4));
    this->regions = move(regions);
    setInitialValues();
    setSavingFrequency(7 * 4);
}

void Simulation::setInitialValues() {
    for(Region &r: regions){
        r.setCoefficients(alpha, beta, gamma1, gamma2);
    }
}

void Simulation::setSavingFrequency(int _days) {
    savingGap = _days;
    for(Region &r: regions)
        r.setHistorySize(savingGap);
}

void Simulation::setMaxDays(long max) {
    maxDays = max;
}

void Simulation::setRegionZero(string &location) {
    regionZeroName = location;
}

bool Simulation::isDiedOut() {
    for(const Region &r: regions) {
        if (r.isExposed())
            return false;
    }
    return true;
}

vector<Region>::iterator Simulation::getRegionIt(string &regionName) {
    auto regionZeroItr = find_if(regions.begin(), regions.end(), [regionName](Region &r)-> bool {return r.getName() == regionName;});
    return regionZeroItr;
}

void Simulation::initialiseRegionZero() {
    auto regionIt = getRegionIt(regionZeroName);
    if (regionIt != regions.end()){
        regionIt->setPatientZero();
    } else {
        Region &initialRegion = regions.at(rand() % regions.size());
        regionZeroName = initialRegion.getName();
        initialRegion.setPatientZero();
        cout << regionZeroName << " has been chosen for a region zero" << endl;
    }
}

void Simulation::simulate() {
    int infect;

    initialiseRegionZero();
    while (!isDiedOut() && (maxDays <= 0 || days < maxDays)){ //optional maximum simulation day setting
        for(Region &r: regions) {
            r.makeSimulationStep();
            infect = random() % INFECT_CHANCE;
            if(infect == 0)
                r.infectOtherCountry(r.getConnections());
            infect = random() % INFECT_CHANCE;
            if(infect == 0)
                r.infectOtherCountry(r.getFlights());
        }
        days++;

        if (days % savingGap == 0) {
            //saveData();
        }
        //cout << getRegionIt(regionZeroName)->getExposed() << " ";
        //cout << getRegionIt(regionZeroName)->getPopulation() << endl;
    }
    //saveData();
}
