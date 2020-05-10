#include "Region.h"

//Static members

//String converters
double Region::stod(std::string &str) {
    double value;
    try {value = std::stod(str);} catch (...) {value = 0.0;}
    return value;
}

int Region::stoi(std::string &str) {
    int value;
    try {value = std::stoi(str);} catch (...) {value = 0;}
    return value;
}

long Region::stol(std::string &str) {
    long value;
    try {value = std::stol(str);} catch (...) {value = 0;}
    return value;
}

//Non static members

//initialize
Region::Region() = default;
Region::Region(std::string &name, std::string &averAge, std::string &healthCare, std::string &transport, std::string &climate,  std::string &population) {
    this->name = name;
    this->averAge = stod(averAge);
    this->healthCare = stod(healthCare);
    this->transport = stod(transport);
    this->climate = (climateType) stoi(climate);
    this->population = stol(population);
}

void Region::setNaturalGrowth(std::string &Lambda, std::string &Mi){
    this->lambda = stod(Lambda);
    this->mi = stod(Mi);
}

void Region::setCoefficients(std::string &Alpha, std::string &Beta, std::string &Gamma1, std::string &Gamma2) {
    this->alpha = stod(Alpha);
    this->beta = stod(Beta);
    this->gamma1 = stod(Gamma1);
    this->gamma2 = stod(Gamma2);
}


//getters
std::string Region::getName() const { return this->name; }
double Region::getAverAge() const { return this->averAge; }
double Region::getHealthCare() const { return this->healthCare; };
double Region::getTransport() const { return this->transport; };
climateType Region::getClimate() const { return this->climate; };
double Region::getAlpha() const { return this->alpha; };
double Region::getBeta() const { return this->beta; };
double Region::getGamma1() const { return this->gamma1; };
double Region::getGamma2() const { return this->gamma2; };
double Region::getLambda() const { return this->lambda; };
double Region::getMi() const { return this->mi; };
long int Region::getPopulation() const { return this->population; };
long int Region::getSusceptible() const { return this->susceptible; };
long int Region::getExposed() const { return this->exposed; };
long int Region::getInfectious() const { return this->infectious; };
long int Region::getRecovered() const { return this->recovered; };
long int Region::getDead() const { return this->dead; };

//relations between regions
void Region::addConnection(Region &region, int val) {
    if (!this->checkConnection(region))
        this->connections.insert(std::make_pair(region, val));
}

bool Region::checkConnection(Region &region) const { return this->connections.count(region); }

void Region::addFlight(Region &region, int val) {
    if (!this->checkFlight(region))
        this->flights.insert(std::make_pair(region, val));
}

bool Region::checkFlight(Region &region) { return this->flights.count(region); }

//reactions
void Region::introduceSocialDistancing() { this->beta *= SOCIAL_C; }
void Region::withdrawSocialDistancing() { this->beta /= SOCIAL_C; }
void Region::introduceCurfew() { this->beta *= CURFEW_C; }
void Region::withdrawCurfew() { this->beta /= CURFEW_C; }
void Region::closeParks() { this->beta *= PARK_C; }
void Region::openParks() { this->beta /= PARK_C; }
void Region::closeRestaurants() { this->beta *= REST_C; }
void Region::openRestaurants() { this->beta /= REST_C; }
void Region::introduceMasks() { this->beta *= MASK_C; }
void Region::withdrawMasks() { this->beta /= MASK_C;}
void Region::introduceGloves() { this->beta *= GLOVE_C; }
void Region::withdrawGloves() { this->beta /= GLOVE_C; }

void Region::closeBorders() {
    for (auto pair : this->connections)
        pair.second = 1;
    for (auto pair : this->flights)
        pair.second = 1;
}

void Region::openBorders() {
    for (auto pair : this->connections)
        pair.second = 2;
    for (auto pair : this->flights)
        pair.second = 2;
}

void Region::increaseInternalTransport() {
    if (this->transport != MAX_TRANSPORT)
        this->transport++;
}

void Region::decreaseInternalTransport() {
    if (this->transport != 1)
        this->transport--;
}

void Region::decreaseExternalTransport() {
    for (auto pair : this->connections)
        if (pair.second != 1)
            pair.second--;
}

void Region::increaseExternalTransport() {
    for (auto pair : this->connections)
        if (pair.second != MAX_CONNECT)
            pair.second++;
}

void Region::increaseTrade(){
    for (auto pair : this->flights)
        if (pair.second != MAX_FLIGHT)
            pair.second++;
}

void Region::decreaseTrade() {
    for (auto pair : this->flights)
        if (pair.second != 1)
            pair.second--;
}

void Region::spreadFakeNews() {
    this->beta /= FAKE_NEWS_C;
    this->gamma1 *= FAKE_NEWS_C;
    this->gamma2 /= FAKE_NEWS_C;
}

void Region::fightWithFakeNews() {
    this->beta *= FAKE_NEWS_C;
    this->gamma1 /= FAKE_NEWS_C;
    this->gamma2 *= FAKE_NEWS_C;
}

void Region::closeEntertainmentCenter() {
    this->beta *= ENTERTAINMENT_C;
}

void Region::openEntertainmentCenter() {
    this->beta /= ENTERTAINMENT_C;
}

void Region::causePanic() {
    this->alpha /= PANIC_C;
    this->beta /= PANIC_C;
    this->gamma1 *= PANIC_C;
    this->gamma2 /= PANIC_C;
    this->lambda /= PANIC_C;
}

void Region::reducePanic() {
    this->alpha *= PANIC_C;
    this->beta *= PANIC_C;
    this->gamma1 /= PANIC_C;
    this->gamma2 *= PANIC_C;
    this->lambda *= PANIC_C;
}

void Region::educateSociety() {
    this->beta *= EDUCATION_C;
    this->gamma1 /= EDUCATION_C;
    this->gamma2 *= EDUCATION_C;
}

void Region::foolSociety() {
    this->beta /= EDUCATION_C;
    this->gamma1 *= EDUCATION_C;
    this->gamma2 /= EDUCATION_C;
}

void Region::closeSchools() { this->beta *= SCHOOL_C; }
void Region::openSchools() { this->beta /= SCHOOL_C; }
void Region::closeShoppingCenter() { this->beta *= SHOP_C; }
void Region::openShoppingCenter() { this->beta /= SHOP_C; }
void Region::forbidGatherings() { this->beta *= GATHER_C; }
void Region::permitGatherings() { this->beta /= GATHER_C; }
void Region::openPlacesOfWorship() { this->beta *= WORSHIP_C; }
void Region::closePlacesOfWorship() { this->beta /= WORSHIP_C; }
void Region::isolateInfectious() { this->beta *= INFECTIOUS_C; }
void Region::doNotIsolateInfectious() { this->beta /= INFECTIOUS_C; }
void Region::isolateExposed() { this->beta *= EXPOSED_C; }
void Region::doNotIsolateExposed() { this->beta /= EXPOSED_C; }

void Region::donateHealthCare() {
    if (this->healthCare != MAX_HEALTH)
        this->healthCare++;
}

void Region::cutExpensesOnHealthCare() {
    if (this->healthCare != 1)
        this->healthCare--;
}

void Region::donateScience() {
    this->gamma1 /= SCIENCE_C;
    this->gamma2 *= SCIENCE_C;
    this->lambda *= SCIENCE_C;
}

void Region::cutExpensesOnScience() {
    this->gamma1 *= SCIENCE_C;
    this->gamma2 /= SCIENCE_C;
    this->lambda /= SCIENCE_C;
}

//operators
bool operator<(const Region &region1, const Region &region2) { return region1.name < region2.name; }