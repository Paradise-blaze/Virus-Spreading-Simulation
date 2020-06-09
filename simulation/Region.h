//
// Created by szymon on 24.04.2020.
//

#ifndef VIRUS_SPREADING_SIMULATION_REGION_H
#define VIRUS_SPREADING_SIMULATION_REGION_H

#include <iostream>
#include <string>
#include <map>
#include <functional>

#define SOCIAL_C 0.1
#define CURFEW_C 0.3
#define PARK_C 0.8
#define REST_C 0.7
#define MASK_C 0.3
#define GLOVE_C 0.5
#define FAKE_NEWS_C 0.2
#define ENTERTAINMENT_C 0.4
#define PANIC_C 0.2
#define EDUCATION_C 0.5
#define SCHOOL_C 0.6
#define SHOP_C 0.4
#define GATHER_C 0.2
#define WORSHIP_C 0.5
#define INFECTIOUS_C 0.1
#define EXPOSED_C 0.1
#define SCIENCE_C 0.4

#define MAX_HEALTH 5
#define MAX_FLIGHT 5
#define MAX_TRANSPORT 5
#define MAX_CONNECT 5

enum climateType {
    Tropical,
    Arid,
    Mediterranean,
    Temperate,
    Continental,
    Polar
};


class Region {
private:
    std::string name;
    double averAge;
    double healthCare;
    double transport;
    climateType climate;
    double alpha = 0;           //transfer to exposed
    double beta = 0;            //infectiousness coefficient
    double gamma1 = 0;          //recovery coefficient
    double gamma2 = 0;          //death coefficient (disease)
    double lambda = 0;          //fertility coefficient
    double mi = 0;              //death coefficient (all cases)
    long population;
    double susceptible;
    double exposed = 0;
    mutable double infectious = 0;
    double recovered = 0;
    double dead = 0;
    double d_susceptible = 0;
    double d_exposed = 0;
    double d_infectious = 0;
    double d_recovered = 0;
    double d_dead = 0;
    mutable std::map<Region, double> connections;
    mutable std::map<Region, double> flights;
    std::map<std::string, bool> eventHistory;
    int **history = nullptr;
    int historyDay = 0;
    int historySize = 0;
    int historyWidth = 0;
    bool isHistoryEmpty = true;
    double transportCoef;

public:
    //initialize
    Region();
    Region(std::string &, std::string &, std::string &, std::string &, std::string &, std::string &);
    void setCoefficients(double, double, double, double);
    void setNaturalGrowth(std::string &, std::string &);
    void initEventHistory();
    void setHistorySize(int);

    //converters
    static double stod(std::string &);
    static int stoi(std::string &);
    static long stol(std::string &);

    //getters
    /*[[nodiscard]]*/ std::string getName() const;              //nodiscard - CLion rzuca ostrzeżenia, gdy nie ma tego znacznika //Jasiu - a mi wywala gdzies warning kiedy jest xD 
    [[nodiscard]] double getAverAge() const;                //const - jak wyżej, później można usunąć
    [[nodiscard]] double getHealthCare() const;
    [[nodiscard]] double getTransport() const;
    [[nodiscard]] climateType getClimate() const;
    [[nodiscard]] double getAlpha() const;
    [[nodiscard]] double getBeta() const;
    [[nodiscard]] double getGamma1() const;
    [[nodiscard]] double getGamma2() const;
    [[nodiscard]] double getLambda() const;
    [[nodiscard]] double getMi() const;
    [[nodiscard]] long int getPopulation() const;
    [[nodiscard]] long int getSusceptible() const;
    [[nodiscard]] long int getExposed() const;
    [[nodiscard]] long int getInfectious() const;
    [[nodiscard]] long int getRecovered() const;
    [[nodiscard]] long int getDead() const;
    std::map<Region, double>& getConnections() const;
    std::map<Region, double>& getFlights() const;
    int ** getHistory() const;
    int getHistorySize() const;
    int getHistoryWidth() const;
    bool getIsHistoryEmpty() const;
    int getHistoryDay() const;

    //relations between regions
    void addConnection(Region &, int);
    bool checkConnection(Region &) const;
    void addFlight(Region &, int);
    bool checkFlight(Region &region);

    //reactions
    std::string setSocialDistancing(bool);                             //bool arg: true - positive effect, false - negative effect
    std::string setCurfew(bool);
    std::string setParks(bool);
    std::string setRestaurants(bool);
    std::string setMasks(bool);
    std::string setGloves(bool);
    std::string setBorders(bool);
    std::string increaseInternalTransport();                           //transport
    std::string decreaseInternalTransport();
    std::string increaseExternalTransport();                           //connections
    std::string decreaseExternalTransport();
    std::string increaseTrade();                                       //flights
    std::string decreaseTrade();
    std::string setFakeNews(bool);
    std::string setEntertainmentCenter(bool);
    std::string setPanic(bool);
    std::string setSociety(bool);
    std::string setSchools(bool);
    std::string setShoppingCenter(bool);
    std::string setGatherings(bool);
    std::string setPlacesOfWorship(bool);
    std::string setInfectiousIsolation(bool);
    std::string setExposedIsolation(bool);
    std::string donateHealthCare();
    std::string cutExpensesOnHealthCare();
    std::string setScienceDonating(bool);

    //spreading methods
    void infectOtherCountryByLand(std::map<Region, double> &) const;
    void infectOtherCountryByAir(std::vector<Region> &,Region &) const;
    bool getInfectionChance() const;

    //simulation methods
    [[nodiscard]] bool isExposed() const;
    void makeSimulationStep();
    void addDataHistory(long day);
    void setPatientZero();
    void clearHistory();

    //operators
    friend bool operator<(const Region &, const Region &);
};

#endif //VIRUS_SPREADING_SIMULATION_REGION_H
