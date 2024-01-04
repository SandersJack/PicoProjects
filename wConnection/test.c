#include "wirelessConnection.h"

#include <stdio.h>
#include <string.h>

#include "pico/stdlib.h"
#include "pico/cyw43_arch.h"

#include "Constants.h"

int main(){

    stdio_init_all();

    wirelessConnection setup;
    strcpy(setup.ssid, W_SSID);
    strcpy(setup.pass, W_PASS);

    connect(&setup);
}