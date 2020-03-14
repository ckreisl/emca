# EMCA — Explorer of Monte-Carlo based Algorithms
![EMCA](https://github.com/ckreisl/emca/blob/readme/images/emca.jpg)
## About
EMCA is a framework for the visualization of Monte Carlo-based algorithms more precisely it is designed to visualize and analyze unidirectional path tracing algorithms. It consists of two parts, a server part, which serves as an interface for the respective rendering system and a client, which takes over the pure visualization. The client is written in Python and offers the possibility to visualize and analyze the path tracing algorithm. EMCA works on a pixel basis, which means that instead of pre-computing and saving all the necessary data of the whole rendered image, everything is calculated at run-time. The data is collected and generated according to the selected pixel by the user.

This framework was developed as Master thesis 03/2019 at the University of Tübingen (Germany). Special thanks goes to Prof. Hendrik Lensch, Sebastian Herholz (supervisor), Tobias Rittig and Lukas Ruppert who made this work possible.

Currently this framework only runs on **Linux** systems. It was tested and developed on Ubuntu 16.04, 18.04 and 19.10.

## Server Interface
During the development of emca [mitsuba](https://github.com/mitsuba-renderer/mitsuba) was used as render system. For this purpose an interface was implemented to allow data transfer between mitsuba and the emca framework. Code modifications to mitsuba can be found here: https://github.com/ckreisl/mitsuba/tree/emca (branch emca).

### Setup
If you never worked with mitsuba before please download and read the documentation about how to configure and compile mitsuba. In the next steps I assume that mitsuba has already been set up.

1. Clone or pull the changes from the mitsuba emca branch.
1. In your *config.py* add `-DDETERMINISTIC` as compile flag for CXX. This will allow for determinisitic renderings in order to analyze and debug path tracing algorithms with emca.
1. Compile mitsuba
1. Start the server with the following command: `mtsutil emca <path_to_scene.xml>`

## EMCA Client
Clone this repository and use the Python virtual enviroment in the 'env' folder to start EMCA (emca.py).

### Documentation
(TODO)
