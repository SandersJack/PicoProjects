#include "dhtInterface.h"
 
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include <math.h>

static const uint LED_PIN = 0;


dht_reading dht_init(uint8_t pin) {
    /// Debug LED
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);
    /// 
    gpio_init(pin);
    dht_reading dht;
    dht.pin = pin;
    return dht;
}

static float wait_for(uint8_t pin, uint8_t expect) {
    uint32_t then = time_us_32();
    while (expect != gpio_get(pin)) {
        sleep_us(10);
    }
    return time_us_32() - then;
}

static float word(uint8_t first, uint8_t second) {
    return (float) ((first << 8) + second);
}

int read_from_dht(dht_reading *result){
    int data[5] = {0,0,0,0,0};

    gpio_set_dir(result->pin, GPIO_OUT);
    gpio_put(result->pin, 0);
    sleep_ms(10);
    gpio_put(result->pin, 1);
    sleep_us(40);


    gpio_set_dir(result->pin, GPIO_IN);
    wait_for(result->pin,0);
    wait_for(result->pin,1);
    wait_for(result->pin,0);


    gpio_put(LED_PIN, 1);

    // read sample (40 bits = 5 bytes)
    for (uint8_t bit = 0; bit < 40; ++bit) {
        wait_for(result->pin, 1);
        uint8_t count = wait_for(result->pin, 0);
        data[bit / 8] <<= 1;
        if (count > 50) {
            data[bit / 8] |= 1;
        }
    }
    gpio_set_dir(result->pin, GPIO_OUT);
    gpio_put(result->pin, 1);

    gpio_put(LED_PIN, 0);


    if (data[4] == ((data[0] + data[1] + data[2] + data[3]) & 0xFF)) {
        float humidity = word(data[0], data[1]) / 10;
        float temp = word(data[2] & 0x7F, data[3]) / 10;

        // if the highest bit is 1, temperature is negative
        if (data[2] & 0x80) {
            temp = -temp;
        }

        // check if checksum was OK but something else went wrong
        if (isnan(temp) || isnan(humidity) ||temp == 0) {
            return DHT_ERR_NAN;
        } else {
            result->humidity = humidity;
            result->temp_celsius = temp;
            return DHT_OK;
        }
    } else {
        return DHT_ERR_CHECKSUM;
    }
}
