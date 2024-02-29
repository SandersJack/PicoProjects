// NeoPixel Ring simple sketch (c) 2013 Shae Erisson
// Released under the GPLv3 license to match the rest of the
// Adafruit NeoPixel library

#include "pico/stdio.h"
#include "pico/time.h"
#include <tusb.h>
#include "Adafruit_NeoPixel.hpp"

// Which pin on the Arduino is connected to the NeoPixels?
#define PIN        0 // On Trinket or Gemma, suggest changing this to 1

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS 16 // Popular NeoPixel ring size

#define DELAYVAL 200 // Time (in milliseconds) to pause between pixels

void example() {
  Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
  
  pixels.begin(); // INITIALIZE NeoPixel strip object (REQUIRED)
  
  for (int l ; l <4 ; l++) {
  pixels.clear(); // Set all pixel colors to 'off'
   printf("cleared pixels 1\n"); 
  for(int i=0; i<NUMPIXELS; i++) { // For each pixel...

    // Here we're using a moderately bright green color:
    pixels.setPixelColor(i, pixels.Color((i%3)*150,((i+1)%3)*150 ,((i+2)%3)*150));
    pixels.show();   // Send the updated pixel colors to the hardware.

    sleep_ms(DELAYVAL); // Pause before next pass through loop
  }
  }
};
  

uint8_t halfdimmed(uint8_t val) {
  return ((val * neopixels_gamma8(126))>>8) ;
}

uint8_t notdimmed(uint8_t val) {
  return val;
}

Adafruit_NeoPixel myPixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);


int main () {
	
  stdio_init_all();
  
  //while (!tud_cdc_connected()) {sleep_ms(100);}
  //printf("Starting simple\n"); 
  example() ;
  //printf ("Ending example\n");
  example() ;
  //printf("Ending 2nd example\n");
  sleep_ms(5000);

}