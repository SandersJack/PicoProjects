#include "wirelessConnection.h"

#include <stdio.h>

#include "pico/stdlib.h"
#include "pico/cyw43_arch.h"

int connect(wirelessConnection *input){

    if (cyw43_arch_init_with_country(CYW43_COUNTRY_UK)) {
        printf("failed to initialise\n");
        return W_ERR_INIT;
    }
    printf("initialised\n");

    cyw43_arch_enable_sta_mode();

    if (cyw43_arch_wifi_connect_timeout_ms(input->ssid, input->pass, CYW43_AUTH_WPA2_AES_PSK, 10000)) {
        printf("failed to connect\n");
        return W_ERR_FTC;
    }
    printf("connected\n");
    return W_OK;
}