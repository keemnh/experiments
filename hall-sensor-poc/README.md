# Hall 센서 PoC

- 시스템 구조
    
    ```bash
    [물리적 하드웨어]
    └─ MCU (ESP32 같은 보드)
        └─ 펌웨어 (firmware)
            └─ 커널 (RTOS 등)
                └─ 개발환경 (ESP-IDF / Arduino 등)
                    └─ 네가 작성하는 코드
    ```
    
    - 하드웨어 (mcu; ESP32 보드)
    - 펌웨어 (Firmware)
        - ESP32는 보통 펌웨어 = FreeRTOS + 드라이버들이라고 보면 됨
    - 커널 (RTOS, Real-Time OS)
        - 펌웨어 안에 있는 작은 운영체제 커널
        - ESP32는 기본적으로 FreeRTOS를 커널로 씀
        - Task 스케줄링, 우선순위 제어, 인터럽트 대응 등 처리
    - 개발환경 (ESP-IDF / Arduino)
        - 실제로 코드를 짜는 공간
        - ESP32는 다양한 개발환경을 선택할 수 있음
            - ESP-IDF (정식), Arduino (간이), Micropython 등
    - 사용자 코드
        - app_main()이나 loop()에 쓰는 코드
        - 이 코드는 개발환경을 통해 빌드되고, 커널이 스케줄링해서 MCU 위에서 돌게 됨
        
- 펌웨어란?
    
    < 펌웨어는 소프트웨어다. >
    
    - 펌웨어는 결국 C 코드, 어셈블리 코드로 작성된 프로그램이야.
    - 근데 이 프로그램은 PC가 아닌 MCU(예: ESP32) 위에서 실행돼.
    - **OS 없이도 돌아갈 수 있음**. 하지만 대부분은 작은 OS(=RTOS) 위에서 실행됨.
    - 실행되려면 머신코드(binary) 형태로 컴파일돼서 **MCU의 플래시에 올라가야 함.**
        
        > 요약: 소프트웨어지만, 하드웨어의 일부처럼 동작하는 특수 목적 코드
        > 
        
        > 그래서 이름도 “firm + ware” → 하드웨어처럼 고정된 소프트웨어
        > 
        
- esp 칩
    
    ```bash
    [ESP32 칩 내부 구성]
    ┌──────────────────────────────┐
    │  CPU (Xtensa 코어 1~2개)      │  ← 명령 실행 (펌웨어 실행 주체)
    ├──────────────────────────────┤
    │  ROM (고정 부트로더)         │  ← 부팅 시 항상 실행됨
    ├──────────────────────────────┤
    │  RAM (SRAM)                  │  ← 실행 중 데이터 저장
    ├──────────────────────────────┤
    │  Flash (외부 연결)           │  ← 펌웨어 저장소 (코드 + 리소스)
    ├──────────────────────────────┤
    │  주변 장치 (GPIO, UART, I²C 등) │  ← 드라이버가 제어하는 물리 장치
    └──────────────────────────────┘
    ```
    
    ---
    
    ### 실행 흐름 (**ROM → Flash → RAM → CPU 실행** 구조)
    
    ```bash
    (1) 전원 인가 → 칩 부팅 시작
    ↓
    (2) ROM에 있는 Bootloader가 실행됨 (변경 불가)
    ↓
    (3) 외부 Flash에서 펌웨어(.bin) 코드 로드
    ↓
    (4) 펌웨어 시작점 (app_main, 혹은 Arduino의 setup())이 RAM에 복사됨
    ↓
    (5) CPU가 RAM에 올라간 코드를 실행함
    ↓
    (6) 코드에서 RTOS 초기화 → Task 등록 → Loop or Scheduler 실행
    ```
    
    ---
    
    ### **🔄 요약: MCU 위에서 펌웨어가 돌아간다는 건**
    
    | **계층** | **역할** |
    | --- | --- |
    | **Flash** | 펌웨어 저장소 (.bin) |
    | **Boot ROM** | 부팅 시 펌웨어 로딩 |
    | **RAM** | 펌웨어 실행 위치 |
    | **CPU** | RAM의 펌웨어 코드를 명령어 단위로 실행 |
    | **드라이버** | 하드웨어 레지스터 접근을 포장 |
    | **RTOS** | Task 관리, 인터럽트 분배 등 |
    | **네 코드** | 결국 RTOS 위에서 동작하는 하나의 Task |
    
    ---
    
    ### **📌 그래서 물리적으로 어떻게 연결되어 있냐?**
    
    ```bash
    [Flash ↔ ROM ↔ RAM ↔ CPU]  
    ↑                  ↑
    드라이버        사용자 코드
    ↑
    GPIO, I²C, UART 등 물리 장치
    ```
    
    → **펌웨어는 하드웨어를 직접 제어할 수 있는 특수한 소프트웨어이고**,
    
    → **RTOS는 그 소프트웨어가 여러 일을 효율적으로 처리하게 도와주는 운영체제 커널**
    
    ---
    
- 깃허브 업로드 구조
    
    ```bash
    hall-sensor-poc/
    ├── esp-idf/
    │   ├── main/
    │   │   └── gpio_example_main.c
    │   ├── CMakeLists.txt
    │   ├── .wokwi/
    │   │   └── project.json
    │   └── wokwi.toml (있으면)
    ├── arduino/            ← 나중에 여기로 hall.ino 따로 만들면 됨
    │
    ├── python/             ← 로그 분석 파이프라인
    ```
    

**< 이번 주 과제 >**

1. **ESP32 + Hall 센서 시뮬레이션 (Wokwi에서)**
2. **Python으로 로그 시뮬레이션 → 분석 파이프라인 실행**

<aside>

> **전체 흐름 요약**
> 
1. Wokwi에서 회로 구성
2. 펌웨어 작성하고 빌드 (센서값 읽고 출력)
3. 시뮬레이터 실행해서 콘솔 로그 확인
4. 로그 저장 → Python 코드들 실행
5. 결과 CSV/그래프 정리
</aside>

---

# < ESP-IDF 로그 >

# 💥  1. 로그 확인

- 리셋하고 다시 시작…

## 1) 프로젝트 템플릿 자동 생성

```bash
# cd [원하는 경로로 이동]
idf.py create-project hall_test
cd hall_test
```

```bash
hall_test/
├── CMakeLists.txt
├── sdkconfig.defaults
└── main/
    └── example_main.c
```

## 2) 센서 로그 코드 작성

main/hall_test.c 제목 수정 → gpio_example_main.c

```c
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
```

## 3) 빌드

```bash
idf.py set-target esp32   # 최초 한 번
idf.py build
```

## 4) **헤드리스 시뮬레이션 & 로그 캡처**

```bash
wokwi-cli run \
  --elf build/app.elf \
  --timeout 0 \
  --capture hall.log
```

→ 로그 생성 안 돼서 터미널 스크립트로 로그 찍어냄…

```bash
rm -f hall.log
for i in {0..5}; do
  state=$(( i % 2 ))   # i 가 0부터 5까지일 때, 0→1→0→1… 반복
  echo "$state" >> hall.log
  sleep 0.5            # 0.5초 대기
done
```

# 💥 **2. 로그 → CSV 변환 → 그래프**

- pip install pandas
- log_to_csv.py 생성

```python
# log_to_csv.py

import pandas as pd

# 1) hall.log 읽기
df = pd.read_csv("hall.log", header=None, names=["state"])

# 2) 시간 컬럼 추가 (0.5초 간격 가정)
df["time_s"] = df.index * 0.5

# 3) CSV로 저장
df.to_csv("hall_states.csv", index=False)

print(f"hall_states.csv 생성됨 ({len(df)}개 레코드)")
```

- 같은 위치에 plot_hall.py 파일 생성
- pip install matplotlib

```python
# plot_hall.py

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("hall_states.csv")

plt.plot(
    df["time_s"],
    df["state"],
    drawstyle="steps-pre",  # 'pre' 면 해당 시점까지 이전 값 유지
    marker="o",
    markersize=6,
    linewidth=2
)

plt.xlabel("Time (s)")
plt.ylabel("Hall State (0 = LOW, 1 = HIGH)")
plt.title("Hall Sensor Toggle Over Time")
plt.ylim(-0.1, 1.1)
plt.grid(True)
plt.tight_layout()
plt.show()
```

---

# < ESP- IDF  + Wokwi 시뮬 시도 >

# ✅ 1. Wokwi 회로 구성

## 1) .wokwi 폴더 생성 (project.json)

> 시뮬레이터용 회로 정보를 담을 .wokwi 폴더
> 

```markdown
mkdir -p .wokwi
cd .wokwi
```

## **2) project.json 파일 생성 (**.wokwi/project.json)

> 회로를 정의할 JSON 파일
> 

→ Wokwi 시뮬레이터는 어떤 보드에 어떤 부품을 어떻게 연결할지 알아야 회로를 그려주고 동작하게 함

→ 해당 정보를 JSON 파일에 넣는 것

(JSON(JavaScript Object Notation) 파일은 “키”와 “값” 쌍으로 데이터를 구조화해서 저장하는 텍스트 형식)

- project.json 파일
    
    Wokwi 시뮬레이터한테 “어떤 부품을 어디에 놓고, 어떻게 연결해야 할지” 알려 주는 회로도 설정 파일.
    
    - **parts** 배열: ESP32 보드나 버튼 같은 부품 목록
    - **connections** 배열: 부품 핀 끼리 이어 줄 와이어 정보
    - **simulation.firmware**: 어느 ELF(펌웨어)를 실행할지 경로 지정

```markdown
touch project.json
open -a TextEdit project.json
```

```json
{
  "version": 1,
  "name": "hall-sensor-poc",
  "files": ["main/gpio_example_main.c"],       // 어느 소스 파일을 펌웨어로 쓸지
  "devices": [     //  부품 종류·위치 
    { "id":"esp32", "type":"wokwi-esp32-devkit-v1", "top":-50, "left":0 },
    { "id":"hall",  "type":"wokwi-pushbutton",      "top":30,  "left":-100, "rotate":90,
      "attrs":{"color":"green","label":"HALL"} }
  ],
  "connections": [     // 부품 간 전선 연결 정보
    ["hall:1.l","esp32:0","green"],
    ["hall:2.r","esp32:GND","black"]
  ]
}
```

# ✅ 2. 펌웨어 작성 & 빌드

## 1) 프로젝트 루트에서 main/gpio_example_main.c 작성

> ESP32에서 특정 핀(GPIO0)에 연결된 센서(버튼)를 읽어서,
> 
> 
> 상태가 바뀔 때마다(0→1, 1→0) 터미널에 HALL=0 또는 HALL=1 로그를 찍어주는 펌웨어 로직을 짜는 거
> 
> - main/gpio_example_main.c 파일
>     1. **main/gpio_example_main.c**
>         - app_main() 함수(FreeRTOS 진입점) 안에
>             - GPIO0을 입력 풀업 모드로 세팅
>             - 무한루프 돌면서 버튼(푸시버튼 대체) 눌림↔떼어짐 감지
>             - 변화가 있을 때마다 printf("HALL=%d\n", level)로 로그 출력
>     2. **빌드 과정**
>         - idf.py build 명령이 이 C 파일과 main/CMakeLists.txt를 읽어서
>         - build/hall_sensor_poc.elf (실행 파일)·.bin (플래시 이미지)를 생성
>         - 이 ELF가 “펌웨어”다. 시뮬레이터나 실제 보드에 올려서 실행되는 바로 그 프로그램.
>     3. **펌웨어 vs. 시뮬 설정**
>         - main/gpio_example_main.c : **펌웨어 코드**
>         - .wokwi/project.json, wokwi.toml : **시뮬레이션 회로·환경 설정**
>         - 두 파일이 합쳐져야, “회로에서 버튼 누르면 펌웨어가 반응”하는 흐름이 완성돼.
> - main/gpio_example_main.c → 펌웨어 → 빌드 → ELF
>     - idf.py build 하면 이 C 코드가 컴파일(→ 어셈블리→기계어) 해서
>     - build/hall_sensor_poc.elf 라는 실행 파일(ELF 포맷)로 변환됨

→ Hall 센서 = 원래 자기장(magnetic field)을 감지하는 센서

→ A3144 같은 디지털 Hall 센서는 자석이 가까워지면 내부 트랜지스터가 동작하면서 출력이 LOW(0)로 바뀌고, 자석이 멀어지면 ****다시 HIGH(1)으로 돌아감

```bash
cd ~/dev/repos/rif-sandbox/demos/keem/hall-sensor-poc   # 프로젝트 루트로 이동
mkdir main                                             # main 폴더 생성
touch main/gpio_example_main.c                         # 이제 파일 생성 가능
open -a "TextEdit" main/gpio_example_main.c            # TextEdit으로 열기
```

→ ESP-IDF 빌드 시스템(CMake 기반)이 main/ 디렉터리를 기본 소스 폴더로 인식

→ main/이 없으면 idf.py build가 “빌드할 소스가 없다”거나 “어디서 코드를 읽어야 할지 모르겠다” 하고 오류날 수 있음

→ `gpio_example_main.c`는  ESP32 펌웨어 로직의 진입점(entry point) 역할을 함. 즉, 이 파일 안에 있는 app_main() 함수가 ESP32 부팅 후 제일 먼저 실행되는 코드임.

```c
// gpoi_example_main.c

#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"

#define HALL_GPIO  GPIO_NUM_0   // JSON에서 GPIO0에 연결했으니

void app_main(void)
{
    // 입력 + 내부 풀업 설정(안 누르면 자동으로 HIGH)
    gpio_config_t io = {
        .pin_bit_mask = 1ULL << HALL_GPIO,
        .mode         = GPIO_MODE_INPUT,
        .pull_up_en   = GPIO_PULLUP_ENABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type    = GPIO_INTR_DISABLE
    };
    gpio_config(&io);

    int prev = gpio_get_level(HALL_GPIO);
    while (1) {
        int level = gpio_get_level(HALL_GPIO);
        if (level != prev) {
            printf("HALL=%d\n", level);  // 0 → 눌림, 1 → 떼어짐
            prev = level;
        }
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}
```

## **2) ESP-IDF 환경 로드** + 환경변수 설정 (툴체인 셸 설정)

- `export.sh` 를 실행해서
    - IDF_PATH, PATH, PYTHONPATH 같은 ESP-IDF 전용 환경변수를 셸에 등록해 주지 않으면
    - idf.py, cmake, xtensa-esp-elf-gcc 같은 툴을  찾을 수가 없음
- `~/.zshrc`에 source ~/dev/idf/esp-idf/export.sh 한 줄 추가는
    - 터미널을 켤 때마다 ESP-IDF 환경이 자동으로 활성화되도록 해 주는 거
    - 매번 수동으로 source 안 쳐도 되게 함

```bash
# ESP-IDF 환경 로드
# 예시: esp-idf가 ~/dev/idf/esp-idf에 설치된 경우
source ~/dev/idf/esp-idf/export.sh
```

```bash
# ESP-IDF 경로 환경변수 설정
open -a TextEdit ~/.zshrc
source ~/dev/idf/esp-idf/export.sh
source ~/.zshrc
idf.py --version       # 동작 확인(버전 잘 뜨는지 확인)
```

## 3)  최상위 **CMakeLists.txt 생성**

- CMakeLists.txt, wokwi.toml
    - **최상위 CMakeLists.txt**: 프로젝트 루트에 있어야 함. 빌드 시스템이 “여기부터 빌드 시작” 이라고 명령
    - **main/CMakeLists.txt**: main/ 폴더 안에 있어야, “여기 있는 C 파일들(main.c 등)을 컴포넌트로 빌드해”라고 알려 주는 역할.
    - **wokwi.toml**: JSON은 회로·핀맵 정의, TOML은 “어떤 펌웨어(ELF)를 시뮬에 올릴지”만 담는 파일인데, wokwi.toml 은 **프로젝트 루트**(hall-sensor-poc/)에 놓는 게 맞음
        
        .wokwi/project.json 과 같은 레벨이지, .wokwi/ 밖에 있어야 CLI(wokwi-cli run .)가 잘 찾음
        
- 최상위 CMakeLists.txt
    - ESP-IDF 툴체인이 이 파일을 보고
        - IDF_PATH(ESP-IDF 설치 경로)를 불러오고
        - project(<name>)으로 프로젝트 이름을 설정한 뒤
        - 하위 컴포넌트들을 찾아서 빌드하도록 초기 설정을 해줌
    - **없으면 ESP-IDF가 “어디서부터 빌드해야 할지” 모르는 상태가 됨**

```bash
# CMakeLists.txt 생성 - 1
cd ~/dev/repos/rif-sandbox/demos/keem/hall-sensor-poc
touch CMakeLists.txt
open -a "TextEdit" CMakeLists.txt
```

```bash
# CMakeLists.txt 생성 - 2 (파일에 복붙)
cmake_minimum_required(VERSION 3.16)

include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(hall_sensor_poc)
```

## 4) **main/CMakeLists.txt 생성 + 빌드**

- main/CMakeLists.txt
    - main/ 폴더를 하나의 ****컴포넌트(component) 로 인식시키는 역할
    - idf_component_register() 호출을 통해
        - 소스 파일들(SRCS)을 명시하고
        - 필요하다면 헤더 검색 경로(INCLUDE_DIRS)도 지정해줌
    - 이 한 줄이 없으면 “main 컴포넌트” 자체가 빌드 대상에서 빠져 버려서, **gpio_example_main.c 코드가 전혀 컴파일되지 않음**

```bash
# main/CMakeLists.txt 생성 - 1
cd main
touch CMakeLists.txt
open -a "TextEdit" CMakeLists.txt
```

```bash
# main/CMakeLists.txt 생성 - 2 (복붙)
idf_component_register(
  SRCS "gpio_example_main.c"
  INCLUDE_DIRS ""
)
```

```bash
## 빌드
cd ..
idf.py build
```

# ✅ 3. 시뮬레이션 실행 **& 로그 캡처 (중단)**

## 1) **.wokwi/project.json 수정**

```bash
##  **.wokwi/project.json**

{
  "version": 1,
  "editor": "arduino",
  "parts": [
    {
      "type": "wokwi-esp32-devkit-v1", "id": "esp32",
      "top": -50, "left": 0
    },
    {
      // “Hall 센서 대신 쓸 디지털 입력”
      "type": "wokwi-digital-input", 
      "id": "hall", 
      "top":  32, "left": -80,
      "attrs": { "color": "green", "label": "HALL" }
    },
    {
      "type": "wokwi-serial-monitor","id":"uart","top":-180,"left":260
    }
  ],
  "connections": [
    ["hall:1",   "esp32:0",    "green", []],  // hall 핀1 → GPIO0
    ["hall:2",   "esp32:GND",  "black", []]   // hall 핀2 → GND
  ],
  "simulation": {
    "firmware": "build/hall_sensor_poc.elf"
  }
}
```

# < Arduino + Wokwi 시뮬 시도 >

# 🔮 1.  아두이노 개발 (중단)

## 1) 아두이노 개발 환경

| **항목** | **설명** |
| --- | --- |
| **아두이노 개발환경** | Arduino 보드용 펌웨어를 작성하는 방식 (.ino 파일 + setup() / loop() 함수 구조) |
| **Arduino core for ESP32** | ESP32를 Arduino 문법으로 제어할 수 있게 해주는 라이브러리 |
| **Wokwi 시뮬레이터** | Arduino 코드(.ino)를 ESP32 보드에 연결해 시뮬할 수 있는 온라인/로컬 시뮬 환경 |

## 2) **hall.ino 생성 (펌웨어 코드)**

→ 프로젝트 로컬(루트) 레벨에 생성

`touch hall.ino
open -a "TextEdit" hall.ino`

```c
 //  hall.ino (펌웨어 코드)
 
const int hallPin = 0;  // GPIO0에 연결

void setup() {
  pinMode(hallPin, INPUT_PULLUP);  // 풀업 설정 → 버튼 안 누르면 HIGH
  Serial.begin(115200);
}

void loop() {
  static int prev = HIGH;
  int level = digitalRead(hallPin);
  if (level != prev) {
    Serial.print("HALL=");
    Serial.println(level);
    prev = level;
  }
  delay(100);  // 디바운싱 겸 polling delay
}
```

## 3) 설정 파일들 **생성**

```toml
## **arduino/wokwi.toml** 
[wokwi]
project = ".wokwi/project.json"
```

```json
//  .vscode/settings.json
{
  "wokwi.mode": "arduino"
}
```

```json
//vscode/arduino.json 파일

{
  "sketch": "hall.ino",
  "board": "esp32:esp32:esp32dev"
}
```

## 4) **.wokwi/project.json (시뮬 회로 설정)**

`mkdir .wokwi
touch .wokwi/project.json
open -a "TextEdit" .wokwi/project.json`

```json
{
  "version": 1,
  "description": "Arduino Hall Sensor PoC",
  "files": ["hall.ino"],
  "devices": [
    {
      "type": "wokwi-esp32-devkit-v1",
      "id": "esp",
      "top": -50,
      "left": 0
    },
    {
      "type": "wokwi-pushbutton",
      "id": "hall",
      "top": 40,
      "left": -120,
      "rotate": 90,
      "attrs": { "color": "green", "label": "HALL" }
    },
    {
      "type": "wokwi-serial-monitor",
      "id": "uart",
      "top": -200,
      "left": 250
    }
  ],
  "connections": [
    ["hall:1", "esp:GPIO0", "green"],
    ["hall:2", "esp:GND", "black"],
    ["esp:TX0", "uart:RX", "gray"],
    ["esp:RX0", "uart:TX", "gray"]
  ]
}
```
