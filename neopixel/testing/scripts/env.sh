#!/bin/bash

cp ../../pico-sdk/external/pico_sdk_import.cmake .

export PICO_SDK_PATH=../../../pico-sdk

mkdir -p build

alias make_clean="rm build/* -r"

alias make="cmake -S . -B build; cmake --build build"
