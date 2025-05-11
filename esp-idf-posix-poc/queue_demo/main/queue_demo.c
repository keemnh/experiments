#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "esp_log.h"
#include <stdlib.h>

#define TAG "queue_demo"
static QueueHandle_t q;

void producer(void *arg)     // producer 태스크
{
    int count = 0;
    while (count < 10) {     // 0부터 9까지 숫자를 0.5초마다 Queue에 넣으면서
        xQueueSend(q, &count, portMAX_DELAY);
        ESP_LOGI(TAG, "Produced: %d", count); // “Produced: X” 로그 남김
        count++;
        vTaskDelay(pdMS_TO_TICKS(500));
    }
    ESP_LOGI(TAG, "Producer done. Exiting.");
    exit(0);
}

void consumer(void *arg)   // consumer 태스크
{
    int value;
    while (1) {     // Queue에 숫자가 들어올 때마다 꺼내서
        if (xQueueReceive(q, &value, portMAX_DELAY) == pdTRUE) {
            ESP_LOGI(TAG, "Consumed: %d", value); // “Consumed: X” 로그 찍음
        }
    }
}

void app_main(void)
{
    q = xQueueCreate(5, sizeof(int));    // 큐가 최대 5개의 int 값 담을 수 있음
    xTaskCreate(producer, "producer", 2048, NULL, 5, NULL);
    xTaskCreate(consumer, "consumer", 2048, NULL, 5, NULL);
}