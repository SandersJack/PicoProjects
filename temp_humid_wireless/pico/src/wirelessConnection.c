#include "wirelessConnection.h"

#include <stdio.h>

#include "pico/stdlib.h"
#include "pico/cyw43_arch.h"
#include "hardware/gpio.h"

/*
#include "lwip/pbuf.h"
#include "lwip/udp.h"
#include "lwip/ip_addr.h"
*/

#include "Constants.h"

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

void send_http_post_request(const char *data) {
    /*
    int sockfd = lwip_socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

    if (sockfd < 0) {
        printf("Error creating socket\n");
        return;
    }

    struct sockaddr_in server_address;
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(SERVER_PORT);
    inet_pton(AF_INET, SERVER_IP, &server_address.sin_addr);

    if (lwip_connect(sockfd, (struct sockaddr*)&server_address, sizeof(server_address)) < 0) {
        printf("Error connecting to server\n");
        lwip_close(sockfd);
        return;
    }

    // Construct the HTTP request
    char request[512];
    snprintf(request, sizeof(request), "POST %s HTTP/1.1\r\n"
                                       "Host: %s\r\n"
                                       "Content-Type: application/x-www-form-urlencoded\r\n"
                                       "Content-Length: %d\r\n\r\n%s",
             RESOURCE_PATH, SERVER_IP, (int)strlen(data), data);

    // Send the HTTP request
    lwip_send(sockfd, request, strlen(request), 0);

    // Receive and print the server's response (optional)
    char response[512];
    int received = lwip_recv(sockfd, response, sizeof(response) - 1, 0);

    if (received > 0) {
        response[received] = '\0';
        printf("Server response:\n%s\n", response);
    }

    // Close the socket
    lwip_close(sockfd);
    */
}