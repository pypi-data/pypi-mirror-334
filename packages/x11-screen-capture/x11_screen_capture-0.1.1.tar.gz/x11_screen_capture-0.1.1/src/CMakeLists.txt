cmake_minimum_required(VERSION 3.12)

set(CMAKE_BUILD_TYPE Release)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)

project(screen_capture_module_cpp) # Project name for CMake (different from Python module name)

# Find Python Interpreter and Development components - VERY IMPORTANT for Python extensions!
find_package(Python COMPONENTS Interpreter Development REQUIRED)

# Include Python headers - VERY IMPORTANT!
include_directories(${Python_INCLUDE_DIRS})

find_package(X11 REQUIRED)
find_package(JPEG REQUIRED)
find_package(Threads REQUIRED)

include_directories(${X11_INCLUDE_DIR} ${JPEG_INCLUDE_DIRS})
link_directories(${X11_LIBRARY_DIR} ${JPEG_LIBRARY_DIRS})

add_library(screen_capture_module SHARED
    screen_capture_module.cpp
    xxhash.c
)

target_link_libraries(screen_capture_module
    PUBLIC
    ${PYTHON_LIBRARIES} # Link against Python! VERY IMPORTANT!
    ${X11_LIBRARIES}
    ${JPEG_LIBRARIES}
    Threads::Threads
)

set_target_properties(screen_capture_module PROPERTIES
    PREFIX ""
    SUFFIX ".so"
    OUTPUT_NAME screen_capture_module
)

install(TARGETS screen_capture_module DESTINATION screen_capture)
