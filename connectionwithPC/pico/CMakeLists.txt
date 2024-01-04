cmake_minimum_required(VERSION 3.13)
set(PICO_BOARD pico_w)
include(pico_sdk_import.cmake)
project(wtest_project C CXX ASM)
set(CMAKE_C_STANDARD 11)

set(CMAKE_CXX_STANDARD 17)
pico_sdk_init()

file(GLOB SOURCES src/*.c)
include_directories(include)

add_executable(wtest test.c ${SOURCES})

pico_enable_stdio_usb(wtest 1)
pico_enable_stdio_uart(wtest 1)

pico_add_extra_outputs(wtest)

target_link_libraries(wtest pico_cyw43_arch_lwip_threadsafe_background pico_stdlib)