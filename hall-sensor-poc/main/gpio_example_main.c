#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include <stdio.h>

#define INTERVAL_MS 500

void app_main(void) {
    int state = 0;
    printf("=== START TOGGLE ===\n");
    while (1) {
        state = !state;
        printf("%d\n", state);
        vTaskDelay(pdMS_TO_TICKS(INTERVAL_MS));
    }
}