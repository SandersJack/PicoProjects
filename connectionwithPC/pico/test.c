#include "wirelessConnection.h"

#include <stdio.h>
#include <string.h>

#include "pico/stdlib.h"
#include "pico/cyw43_arch.h"

#include "lwip/pbuf.h"
#include "lwip/udp.h"
#include "lwip/ip_addr.h"

#include "Constants.h"

void send_udp_data(const char *data);

void send_udp_data(const char *data) {
    struct udp_pcb *udp_conn = udp_new();
    if (!udp_conn) {
        printf("Error creating UDP connection\n");
        return;
    }

    ip_addr_t server_addr;
    if (!ipaddr_aton(SERVER_IP, &server_addr)) {
        printf("Error parsing server IP address\n");
        udp_remove(udp_conn);
        return;
    }

    err_t err = udp_connect(udp_conn, &server_addr, 5000);
    if (err != ERR_OK) {
        printf("Error connecting to server\n");
        udp_remove(udp_conn);
        return;
    }

    // Create a pbuf to hold the data
    struct pbuf *p = pbuf_alloc(PBUF_TRANSPORT, strlen(data), PBUF_RAM);
    if (!p) {
        printf("Error allocating pbuf\n");
        udp_remove(udp_conn);
        return;
    }

    // Copy data into the pbuf
    memcpy(p->payload, data, p->len);

    // Send the pbuf over UDP
    err = udp_send(udp_conn, p);
    if (err != ERR_OK) {
        printf("Error sending data over UDP\n");
    }

    // Free the pbuf
    pbuf_free(p);

    // Close the UDP connection
    udp_remove(udp_conn);
}


int main(){

    stdio_init_all();

    printf("Startup\n");

    wirelessConnection setup;
    strcpy(setup.ssid, W_SSID);
    strcpy(setup.pass, W_PASS);

    while(connect(&setup) != 0);
    printf("Start of Loop\n");
    while (1){
        sleep_ms(2000);
        float temperature = 25.5;
        float humidity = 50.0;

        // Create a string with the sensor data
        char data_to_send[128];
        snprintf(data_to_send, sizeof(data_to_send), "temperature=%.2f&humidity=%.2f", temperature, humidity);
        printf(data_to_send);
        printf("\n");
        // Send data over UDP
        send_udp_data(data_to_send);
    }
    
}