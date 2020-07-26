cmake_minimum_required(VERSION 3.10.2)
project(EMCAServerSmallpt
    VERSION 1.0.0    
    DESCRIPTION "EMCA example with smallpt"
    LANGUAGES CXX)

include(GNUInstallDirs)

# use old compiler version due to strange behavior on top of rendered image
set(CMAKE_CXX_COMPILER  "g++-5")
set(CXX_FLAG            "-O3 -std=c++11")
set(OPENMP              "-fopenmp")
set(NARROWING           "-Wno-narrowing")

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGX} ${CXX_FLAG} ${OPENMP} ${NARROWING}")

add_executable(${PROJECT_NAME} smallpt.cpp)
target_link_libraries(${PROJECT_NAME} emca)