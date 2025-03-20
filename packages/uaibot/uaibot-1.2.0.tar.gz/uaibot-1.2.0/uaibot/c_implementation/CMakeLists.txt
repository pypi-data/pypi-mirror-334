cmake_minimum_required(VERSION 3.5)
project(UAIBOT_CPP_BINDS)


# Add pybind11 
execute_process(
    COMMAND "python3" -c "import pybind11; print(pybind11.get_include())"
    OUTPUT_VARIABLE PYBIND11_INCLUDE_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
)
string(REGEX REPLACE "/include$" "" PYBIND11_DIR "${PYBIND11_INCLUDE_DIR}")
set(pybind11_DIR ${PYBIND11_DIR})
set(pybind11_INCLUDE_DIR ${PYBIND11_INCLUDE_DIR})
set(pybind11_DIR ${PYBIND11_DIR}/share/cmake/pybind11) 
set(CMAKE_PREFIX_PATH ${CMAKE_PREFIX_PATH} ${pybind11_DIR}) 
include_directories(${PYBIND11_INCLUDE_DIR})
find_package(pybind11 REQUIRED)


#Add eigen
set(THIRD_PARTY_DIR ${CMAKE_CURRENT_SOURCE_DIR}/third_party)
set(EIGEN3_INCLUDE_DIR ${THIRD_PARTY_DIR})
include_directories(${EIGEN3_INCLUDE_DIR})

# Add python 3.11
find_package(Python3 3.11 REQUIRED COMPONENTS Interpreter Development)
include_directories(${Python3_INCLUDE_DIRS})
link_directories(${Python3_LIBRARY_DIRS})

# Set C++ standard and optimization flags
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -DEIGEN_MPL2_ONLY -Wno-deprecated-declarations") 

# Define source files 
set(SOURCES
    pybind_main.cpp   
    manipulator.cpp  
    utils.cpp  
    declarations.h  
    gjk.c         
    gjk.h
)

# Define an INTERFACE library for nanoflann (header-only)
add_library(nanoflann INTERFACE)
target_include_directories(nanoflann INTERFACE ${CMAKE_CURRENT_SOURCE_DIR})

# Ensure pybind11 and Eigen are properly included
pybind11_add_module(uaibot_cpp_bind ${SOURCES})

# EXPLICITLY LINK PYTHON 3.11 LIBRARY
target_include_directories(uaibot_cpp_bind PRIVATE ${EIGEN3_INCLUDE_DIR} ${pybind11_INCLUDE_DIR} ${Python3_INCLUDE_DIRS})
target_link_libraries(uaibot_cpp_bind PRIVATE nanoflann ${Python3_LIBRARIES})

# SET RUNTIME SEARCH PATH (Ensures the `.so` file finds dependencies)
set_target_properties(uaibot_cpp_bind PROPERTIES INSTALL_RPATH_USE_LINK_PATH TRUE)
set_target_properties(uaibot_cpp_bind PROPERTIES BUILD_WITH_INSTALL_RPATH TRUE)
set_target_properties(uaibot_cpp_bind PROPERTIES INSTALL_RPATH ${Python3_LIBRARY_DIRS})

# Ensure `.so` is output to the correct directory
# set_target_properties(uaibot_cpp_bind PROPERTIES
#     LIBRARY_OUTPUT_DIRECTORY ../../
# )

execute_process(
    COMMAND python3 -c "import sysconfig; print(sysconfig.get_path('platlib'))"
    OUTPUT_VARIABLE PYTHON_SITE_PACKAGES
    OUTPUT_STRIP_TRAILING_WHITESPACE
)
set_target_properties(uaibot_cpp_bind PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${PYTHON_SITE_PACKAGES}/uaibot
)

# Ensure gjk.c is compiled as C
set_source_files_properties(gjk.c PROPERTIES LANGUAGE C)
