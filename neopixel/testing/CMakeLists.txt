cmake_minimum_required(VERSION 3.13)
set(PICO_BOARD pico_w)
include(pico_sdk_import.cmake)
project(wtest_project C CXX ASM)
set(CMAKE_C_STANDARD 11)

set(CMAKE_CXX_STANDARD 17)
pico_sdk_init()

file(GLOB SOURCES src/*.cc)
include_directories(include)

add_executable(neoP neo.cc ${SOURCES})

pico_enable_stdio_usb(neoP 1)
pico_enable_stdio_uart(neoP 1)

pico_add_extra_outputs(neoP)

add_subdirectory(../neopixelTools build)

target_link_libraries(neoP pico_stdlib pico_neopixel)