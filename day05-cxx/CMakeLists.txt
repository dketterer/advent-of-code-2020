cmake_minimum_required(VERSION 3.10)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

project(day05)

find_package(Boost 1.71.0 COMPONENTS)


include_directories(${Boost_INCLUDE_DIRS})
add_executable(day05 main.cpp)
target_link_libraries(day05 ${Boost_LIBRARIES})
