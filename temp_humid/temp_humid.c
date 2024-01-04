#include <stdio.h>
#include <math.h>

#include "pico/stdlib.h"
#include "hardware/gpio.h"

#include "dhtInterface.h"

const uint DHT_PIN = 15;
const uint MAX_TIMINGS = 85;



int main(){

    stdio_init_all();
    
    dht_reading reading = dht_init(DHT_PIN);

    while(1){
        sleep_ms(2000);
        
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