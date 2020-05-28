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
    this->isHistoryEmpty = true;
    initEventHistory();

    setHistorySize(4*7); //4 weeks
    //addDataHistory();
}

void Region::setNaturalGrowth(std::string &Lambda, std::string &Mi){
    this->lambda = stod(Lambda);
    this->mi = stod(Mi);
}

void Region::setCoefficients(double Alpha, double Beta, double Gamma1, double Gamma2) {
    this->alpha = Alpha;
    this->beta = Beta;
    this->gamma1 = Gamma1;
    this->gamma2 = Gamma2;
}

void Region::initEventHistory() {
    this->eventHistory.insert(std::make_pair("setSocialDistancing",false));
    this->eventHistory.insert(std::make_pair("setCurfew",false));
    this->eventHistory.insert(std::make_pair("setParks",false));
    this->eventHistory.insert(std::make_pair("setRestaurants",false));
    this->eventHistory.insert(std::make_pair("setMasks",false));
    this->eventHistory.insert(std::make_pair("setGloves",false));
    this->eventHistory.insert(std::make_pair("setBorders",false));
    this->eventHistory.insert(std::make_pair("setFakeNews",false));
    this->eventHistory.insert(std::make_pair("setEntertainmentCenter",false));
    this->eventHistory.insert(std::make_pair("setPanic",false));
    this->eventHistory.insert(std::make_pair("setSociety",false));
    this->eventHistory.insert(std::make_pair("setSchools",false));
    this->eventHistory.insert(std::make_pair("setShoppingCenter",false));
    this->eventHistory.insert(std::make_pair("setGatherings",false));
    this->eventHistory.insert(std::make_pair("setPlacesOfWorship",false));
    this->eventHistory.insert(std::make_pair("setInfectiousIsolation",false));
    this->eventHistory.insert(std::make_pair("setExposedIsolation",false));
    this->eventHistory.insert(std::make_pair("setScienceDonating",false));
}

bool Region::isExposed() const {
    return getExposed() + getInfectious() > 0;
}

//getters
std::string Region::getName() const { return this->name; }
double Region::getAverAge() const { return this->averAge; }
double Region::getHealthCare() const { return this->healthCare; }
double Region::getTransport() const { return this->transport; }
climateType Region::getClimate() const { return this->climate; }
double Region::getAlpha() const { return this->alpha; }
double Region::getBeta() const { return this->beta; }
double Region::getGamma1() const { return this->gamma1; }
double Region::getGamma2() const { return this->gamma2; }
double Region::getLambda() const { return this->lambda; }
double Region::getMi() const { return this->mi; };
long int Region::getPopulation() const { return this->population; }
long int Region::getSusceptible() const { return this->susceptible; }
long int Region::getExposed() const { return this->exposed; }
long int Region::getInfectious() const { return this->infectious; }
long int Region::getRecovered() const { return this->recovered; }
long int Region::getDead() const { return this->dead; }
std::map<Region,double>& Region::getConnections() const { return this->connections; }
std::map<Region,double>& Region::getFlights() const { return this->flights; }
int ** Region::getHistory() const { return this->history; }
int Region::getHistorySize() const { return this->historySize; }
bool Region::getIsHistoryEmpty() const { return this->isHistoryEmpty; }
int Region::getHistoryDay() const { return this->historyDay; }

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
std::string Region::setSocialDistancing(bool cond) {
    if (cond)
        this->beta *= SOCIAL_C;                 //increase
    else
        this->beta /= SOCIAL_C;                 //decrease
    return __func__;
}
std::string Region::setCurfew(bool cond) {
    if (cond)
        this->beta *= CURFEW_C;                 //introduce
    else
        this->beta /= CURFEW_C;                 //withdraw
    return __func__;
}

std::string Region::setParks(bool cond) {
    if(cond)
        this->beta *= PARK_C;                   //close
    else
        this->beta /= PARK_C;                   //open
    return __func__;
}

std::string Region::setRestaurants(bool cond) {
    if(cond)
        this->beta *= REST_C;                   //close
    else
        this->beta /= REST_C;                   //open
    return __func__;
}

std::string Region::setMasks(bool cond) {
    if(cond)
        this->beta *= MASK_C;                   //introduce
    else
        this->beta /= MASK_C;                   //withdraw
    return __func__;
}

std::string Region::setGloves(bool cond) {
    if(cond)
        this->beta *= GLOVE_C;                  //introduce
    else
        this->beta /= GLOVE_C;                  //withdraw
    return __func__;
}

std::string Region::setBorders(bool cond) {
    if (cond) {                                 //close
        for (auto pair : this->connections)
            pair.second = 1;
        for (auto pair : this->flights)
            pair.second = 1;
    }
    else {                                      //open but carefully
        for (auto pair : this->connections)
            pair.second = 2;
        for (auto pair : this->flights)
            pair.second = 2;
    }
    return __func__;
}

std::string Region::increaseInternalTransport() {
    if (this->transport != MAX_TRANSPORT)
        this->transport++;
    return __func__;
}

std::string Region::decreaseInternalTransport() {
    if (this->transport != 1)
        this->transport--;
    return __func__;
}

std::string Region::increaseExternalTransport() {
    for (auto pair : this->connections)
        if (pair.second != MAX_CONNECT)
            pair.second++;
    return __func__;
}

std::string Region::decreaseExternalTransport() {
    for (auto pair : this->connections)
        if (pair.second != 1)
            pair.second--;
    return __func__;
}

std::string Region::increaseTrade() {
    for (auto pair : this->flights)
        if (pair.second != MAX_FLIGHT)
            pair.second++;
    return __func__;
}

std::string Region::decreaseTrade() {
    for (auto pair : this->flights)
        if (pair.second != 1)
            pair.second--;
    return __func__;
}

std::string Region::setFakeNews(bool cond) {
    if(cond) {
        this->beta *= FAKE_NEWS_C;
        this->gamma1 /= FAKE_NEWS_C;
        this->gamma2 *= FAKE_NEWS_C;
    }
    else {
        this->beta /= FAKE_NEWS_C;
        this->gamma1 *= FAKE_NEWS_C;
        this->gamma2 /= FAKE_NEWS_C;
    }
    return __func__;
}

std::string Region::setEntertainmentCenter(bool cond) {
    if(cond)
        this->beta *= ENTERTAINMENT_C;
    else
        this->beta /= ENTERTAINMENT_C;
    return __func__;
}

std::string Region::setPanic(bool cond) {
    if(cond) {
        this->alpha *= PANIC_C;
        this->beta *= PANIC_C;
        this->gamma1 /= PANIC_C;
        this->gamma2 *= PANIC_C;
        this->lambda *= PANIC_C;
    }
    else {
        this->alpha /= PANIC_C;
        this->beta /= PANIC_C;
        this->gamma1 *= PANIC_C;
        this->gamma2 /= PANIC_C;
        this->lambda /= PANIC_C;
    }
    return __func__;
}

std::string Region::setSociety(bool cond) {
    if (cond) {                         //educate
        this->beta *= EDUCATION_C;
        this->gamma1 /= EDUCATION_C;
        this->gamma2 *= EDUCATION_C;
    }
    else {                              //fool
        this->beta /= EDUCATION_C;
        this->gamma1 *= EDUCATION_C;
        this->gamma2 /= EDUCATION_C;
    }
    return __func__;
}

std::string Region::setSchools(bool cond) {
    if(cond)                            //close
        this->beta *= SCHOOL_C;
    else                                //open
        this->beta /= SCHOOL_C;
    return __func__;
}

std::string Region::setShoppingCenter(bool cond) {
    if(cond)
        this->beta *= SHOP_C;           //close
    else
        this->beta /= SHOP_C;           //open
    return __func__;
}

std::string Region::setGatherings(bool cond) {
    if(cond)
        this->beta *= GATHER_C;         //forbid
    else
        this->beta /= GATHER_C;         //permit
    return __func__;
}

std::string Region::setPlacesOfWorship(bool cond) {
    if(cond)
        this->beta *= WORSHIP_C;        //close
    else
        this->beta /= WORSHIP_C;        //open
    return __func__;
}

std::string Region::setInfectiousIsolation(bool cond) {
    if(cond)
        this->beta *= INFECTIOUS_C;     //isolate
    else
        this->beta /= INFECTIOUS_C;     //don't isolate
    return __func__;
}

std::string Region::setExposedIsolation(bool cond) {
    if(cond)
        this->beta *= EXPOSED_C;        //isolate
    else
        this->beta /= EXPOSED_C;        //don't isolate
    return __func__;
}

std::string Region::donateHealthCare() {
    if (this->healthCare != MAX_HEALTH)
        this->healthCare++;
    return __func__;
}

std::string Region::cutExpensesOnHealthCare() {
    if (this->healthCare != 1)
        this->healthCare--;
    return __func__;
}

std::string Region::setScienceDonating(bool cond) {
    if (cond) {                         //donate
        this->gamma1 /= SCIENCE_C;
        this->gamma2 *= SCIENCE_C;
        this->lambda *= SCIENCE_C;
    }
    else {                              //cut expenses
        this->gamma1 *= SCIENCE_C;
        this->gamma2 /= SCIENCE_C;
        this->lambda /= SCIENCE_C;
    }
    return __func__;
}

//spreading methods
void Region::infectOtherCountry(std::map<Region, double> & countryMap) const {
    if(this->infectious > 0) {
        int neighbourCount, neighbourNumber;
        auto it = countryMap.begin();

        neighbourCount = countryMap.size();
        neighbourNumber = static_cast<int>(rand()) % neighbourCount;

        for (int i = 0; i < neighbourNumber; ++i) {
            it++;
        }

        if (it->first.infectious == 0)
            it->first.infectious = 1;
    }
}

//simulation methods
void Region::makeSimulationStep(long day) {
    //if (!isExposed() && dead > 0)
    //    addDataHistory();
    if (!isExposed())
        return;
    double b_I_S = beta * (double)infectious * (double)susceptible / (double)population;
    d_susceptible = (lambda - mi) * (double)susceptible - b_I_S;
    d_exposed = b_I_S - (mi + alpha) * (double)exposed;
    d_infectious = alpha * (double)exposed - (gamma1 + gamma2 + mi) * (double)infectious;
    d_recovered = gamma1 * (double)infectious - mi * (double)recovered;
    d_dead = gamma2 * (double)infectious;

    susceptible += (long int)d_susceptible;
    exposed += (long int)d_exposed;
    infectious += (long int)d_infectious;
    recovered += (long int)d_recovered;
    dead += (long int)d_dead;
    population -= dead;

    addDataHistory(day);
}

void Region::setPatientZero() {
    exposed = 1;
}

void Region::setHistorySize(int size) {
    historySize = size;
    history = new int*[size];
    for(int i = 0; i < size; i++)
        history[i] = new int[5];
}


void Region::addDataHistory(long day) {
    isHistoryEmpty = false;
    if (historyDay >= historySize){
        return;
    }
    history[historyDay][0] = day;
    history[historyDay][1] = susceptible;
    history[historyDay][2] = exposed;
    history[historyDay][3] = infectious;
    history[historyDay][4] = recovered;
    history[historyDay][5] = dead;
    historyDay++;
}

//operators
bool operator<(const Region &region1, const Region &region2) { return region1.name < region2.name; }