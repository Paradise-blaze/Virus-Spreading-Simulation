# Virus-Spreading-Simulation
## Origin 
This app is a project for Discrete Simulation of Complex Systems classes. We have decided to create a simulation of a pandemic according to novel coronavirus outbreak in Wuhan. In order to do it with the most efficiency, we implemented the SEIR model - a mathematical description of pandemic. The idea is to divide population into four separate groups. Every letter stands for their names:
- Susceptible  
  People that could potentially get infected by pathogen
- Exposed  
  People in stage between susceptible and infectious; pathogen is present in their bodies but does not cause any symptoms
- Infectious  
  People with all kind of symptoms (mild, medium, serious); the presence of foreign body is clearly noticable
- Removed  
  People who either got rid of pathogen and gained an immunity or died due to illness
  
  
We have decided to enhance that model and split Removed into Recovered and Dead to make it more accurate.
## Implementation 
After several discussions we came up with an idea of writing this app in two programming languages - Python and C++. The first task of program is to create large number of files containing number of 5 groups from our model.
### C++
The low-level traits of this language are widely beneficial for our venture - the essential part of code (simulating spread of pathogen all around the world) is based on two C++ classes - Simulation and Region.
### Python
Famous for various number of graphical libraries, Python is a vital part of our GUI. Using Tkinter we can easily display the results of simulation.

The more detailed information about source code is in "doc" directory.
## How to use
### Running
The preferred way of running this app is using PyCharm. After cloning repo, set Python interpreter as "Python3.6 (venv)" - that file is located in project - and run program with "main" configuration.
### Features
There are two modes of using this app - either choosing one of predefined diseases or creating a new one. In both scenarios user should choose a "region zero" (so the country where the spread begins) from list of available ones. After setting crucial options, simulation is ready to start. When the loading is done properly, there is one more decision to be made - which group of people ought to be displayed in animation. User should make a choice and then they can watch a short animation ilustrating how pathogen travelled around the world. After that there is a possibility to return and see another set of maps or display a plot for every infected country or whole Earth. If the users get bored, they can return to title page and start again with another disease and region zero.
