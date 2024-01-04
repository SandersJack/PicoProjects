cmake_minimum_required(VERSION 3.13)
include(pico_sdk_import.cmake)
project(hw_project C CXX ASM)
set(CMAKE_C_STANDARD 11)

set(CMAKE_CXX_STANDARD 17)
pico_sdk_init()

add_executable(hw
hw.c
)

pico_enable_stdio_usb(hw 1)
pico_enable_stdio_uart(hw 0)


pico_add_extra_outputs(hw)

target_link_libraries(hw pico_stdlib)