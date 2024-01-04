cmake_minimum_required(VERSION 3.13)
include(pico_sdk_import.cmake)
project(tempH_project C CXX ASM)
set(CMAKE_C_STANDARD 11)

set(CMAKE_CXX_STANDARD 17)
pico_sdk_init()

add_executable(tempH
temp_humid.c
)
pico_enable_stdio_usb(tempH 1)
pico_enable_stdio_uart(tempH 1)
pico_add_extra_outputs(tempH)
target_link_libraries(tempH pico_stdlib)