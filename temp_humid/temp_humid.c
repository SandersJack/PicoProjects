#include <stdio.h>
#include <math.h>

#include "pico/stdlib.h"
#include "hardware/gpio.h"

const uint LED_PIN = PICO_DEFAULT_LED_PIN;

const uint DHT_PIN = 15;
const uint MAX_TIMINGS = 85;

typedef struct {
    float humidity;
    float temp_celsius;
} dht_reading;

int read_from_dht(dht_reading *result);
float wait_for(uint8_t pin, uint8_t expect);
float word(uint8_t first, uint8_t second);

float wait_for(uint8_t pin, uint8_t expect) {
    uint32_t then = time_us_32();
    while (expect != gpio_get(pin)) {
        sleep_us(10);
    }
    return time_us_32() - then;
}

float word(uint8_t first, uint8_t second) {
    return (float) ((first << 8) + second);
}

int read_from_dht(dht_reading *result){
    int data[5] = {0,0,0,0,0};

    gpio_set_dir(DHT_PIN, GPIO_OUT);
    gpio_put(DHT_PIN, 0);
    sleep_ms(10);
    gpio_put(DHT_PIN, 1);
    sleep_us(40);


    gpio_set_dir(DHT_PIN, GPIO_IN);
    wait_for(DHT_PIN,0);
    wait_for(DHT_PIN,1);
    wait_for(DHT_PIN,0);


    gpio_put(LED_PIN, 1);

    // read sample (40 bits = 5 bytes)
    for (uint8_t bit = 0; bit < 40; ++bit) {
        wait_for(DHT_PIN, 1);
        uint8_t count = wait_for(DHT_PIN, 0);
        data[bit / 8] <<= 1;
        if (count > 50) {
            data[bit / 8] |= 1;
        }
    }
    gpio_set_dir(DHT_PIN, GPIO_OUT);
    gpio_put(DHT_PIN, 1);

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
            return 11;
        } else {
            result->humidity = humidity;
            result->temp_celsius = temp;
            return 0;
        }
    } else {
        printf("Bad data\n");
        return 10;
    }
}


int main(){

    stdio_init_all();
    gpio_init(LED_PIN);
    gpio_init(DHT_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);

    while(1){
        sleep_ms(2000);
        dht_reading reading;
        int out = read_from_dht(&reading);
        if(out == 0){
            float temp = reading.temp_celsius;
            float humid = reading.humidity;
            printf("Humidity = %.1f%%, Temperature = %.1fC \n", humid, temp);
        } else if(out == 10){
            printf("Bad data (checksum)\n");
        } else {
            printf("Bad data (NaN)\n");
        }
    }

}