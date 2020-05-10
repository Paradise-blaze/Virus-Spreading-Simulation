//
// Created by szymon on 24.04.2020.
//

#ifndef VIRUS_SPREADING_SIMULATION_REGION_H
#define VIRUS_SPREADING_SIMULATION_REGION_H

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
    long int population;
    long int susceptible = 0;
    long int exposed = 0;
    long int infectious = 0;
    long int recovered = 0;
    long int dead = 0;
    std::map<Region, double> connections;
    std::map<Region, double> flights;

    static double stod(std::string &);
    static int stoi(std::string &);
    static long stol(std::string &);
public:
    //initialize
    Region();
    Region(std::string &, std::string &, std::string &, std::string &, std::string &, std::string &);
    void setCoefficients(std::string &, std::string &, std::string &, std::string &);
    void setNaturalGrowth(std::string &, std::string &);

    //getters
    [[nodiscard]] std::string getName() const;              //nodiscard - CLion rzuca ostrzeżenia, gdy nie ma tego znacznika
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

    //relations between regions
    void addConnection(Region &, int);
    bool checkConnection(Region &) const;
    void addFlight(Region &, int);
    bool checkFlight(Region &region);

    //reactions
    void introduceSocialDistancing();
    void withdrawSocialDistancing();
    void introduceCurfew();
    void withdrawCurfew();
    void closeParks();
    void openParks();
    void closeRestaurants();
    void openRestaurants();
    void introduceMasks();
    void withdrawMasks();
    void introduceGloves();
    void withdrawGloves();
    void closeBorders();
    void openBorders();
    void decreaseInternalTransport();                             //transport
    void increaseInternalTransport();
    void decreaseExternalTransport();                             //connections
    void increaseExternalTransport();
    void increaseTrade();                                       //flights
    void decreaseTrade();
    void spreadFakeNews();
    void fightWithFakeNews();
    void closeEntertainmentCenter();
    void openEntertainmentCenter();
    void causePanic();
    void reducePanic();
    void educateSociety();
    void foolSociety();
    void closeSchools();
    void openSchools();
    void closeShoppingCenter();
    void openShoppingCenter();
    void forbidGatherings();
    void permitGatherings();
    void openPlacesOfWorship();
    void closePlacesOfWorship();
    void isolateInfectious();
    void doNotIsolateInfectious();
    void isolateExposed();
    void doNotIsolateExposed();
    void donateHealthCare();
    void cutExpensesOnHealthCare();
    void donateScience();
    void cutExpensesOnScience();

    //operators
    friend bool operator<(const Region &, const Region &);

};

#endif //VIRUS_SPREADING_SIMULATION_REGION_H
