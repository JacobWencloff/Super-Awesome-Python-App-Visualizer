# Algo-Viz
### A Algorithm Vizualizer 

Algo-Viz is a desktop application intended to provide a visual representation of the inner workings of commonly used algorithms. 

## Current Features
---
- A completely maluable data set
    - Size
    - Top range
    - Bottom range
- Ability to hot swap algorithms
- Ability to increase / decrease the speed of an animation
- Acess to view to source algorithm being used
- Reset feature, letting the user reset the algorithm and graph 

## Supporting Libraries 
---
Algo-Viz has two dependecies that attribute all of the programs functionality. PyImGUI allows for the creation of the entire user interface, this library is supported by the OpenGL, the second library. The launcher for the Algo-Viz application is created via a python packaged called PyInstaller, this software interprets the project file, and constructs a executable file based on the dependencies and child files attached to it.

## Supported Algorithms 
- Merge Sort
- Quick Sort
- A* Path finding 

## INSTRUCTIONS !!!
---
This project is currently not a production build ! that means the file has no executable, and must be launched from the terminal!

#### Directions
- Ensure you have python installed on your PC
    - open your terminal and type ```$python3 --version``` or ```$Spython --version``` to ensure you have python on your local machine
    - If python is not installed, please install it like so
        - MAC -> ```$ brew install python```
        - Linux -> ```$ sudo apt install python3 ```
        - Windows -> https://www.python.org/downloads/

- Once python has been varified on your local machine, please install pyimgui using your terminal
    - ```$ pip install pyimgui[full] ```
    - this will install all dependencies needed for the program to operate 

- Lastly, please navigate to the directory storing the project on your local storage within your terminal, and run the command ```$ python3 ./main.py```

