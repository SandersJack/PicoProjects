#ifndef dhtInterface_HPP
#define dhtInterface_HPP


#include "pico/stdlib.h"

#define DHT_OK              0
#define DHT_ERR_CHECKSUM    10
#define DHT_ERR_NAN         11

typedef struct {
    uint pin;
    float humidity;
    float temp_celsius;
} dht_reading;

dht_reading dht_init(uint8_t pin);
int read_from_dht(dht_reading *result);

#endif