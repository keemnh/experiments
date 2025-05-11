# ESP-IDF POSIX PoC

ESP-IDF 기반 FreeRTOS PoC를 보드 없이 macOS/Linux POSIX 환경에서 시뮬레이션해 보는 예제 모음입니다.  
오늘 실습한 내용(hello_world, Queue 데모, GPIO 예제 복원)과 로그 분석 스크립트를 한 곳에 정리했습니다.

---

## 📂 폴더 구조
```  
esp-idf-posix-poc/
├── README.md
├── env-setup/
│   ├── install_idf.sh
│   └── export_idf.sh
├── hello_world/
│   ├── hello_log.txt
│   ├── analyze_log.py
│   └── sdkconfig.example
├── queue_demo/
│   ├── CMakeLists.txt
│   └── main/
│       ├── queue_demo.c
│       └── CMakeLists.txt
└── generic_gpio-demo/
    ├── CMakeLists.txt
    ├── README.md
    └── main/
        ├── gpio_example_main.c
        └── CMakeLists.txt
```  

---

## 🚀 빠른 시작

1. **ESP-IDF 설치**  
   ```bash
   cd env-setup
   bash install_idf.sh
   bash export_idf.sh

2. **hello_world 시뮬레이션 & 로그 분석**
   ```bash
	cd ../hello_world
	idf.py --preview set-target linux
	idf.py --preview build
	./build/hello_world.elf > hello_log.txt
	python3 analyze_log.py

3. **Queue 데모 실행**  
   ```bash
   cd ../queue_demo
   idf.py --preview set-target linux
   idf.py --preview build
   ./build/queue_demo.elf

## 🔧 파일 설명

- **env-setup/install_idf.sh**  
  ESP-IDF 설치 스크립트 (홈브루 설치 → 레포 클론 → `install.sh` 실행)

- **env-setup/export_idf.sh**  
  환경변수 설정 스크립트 (`export.sh` 를 실행해서 `IDF_PATH` 등 등록)

- **hello_world/hello_log.txt**  
  `hello_world` 예제 POSIX 시뮬레이션 실행 결과 로그

- **hello_world/analyze_log.py**  
  `hello_log.txt`에서 “Restarting in N seconds…” 카운트다운 메시지를 파싱해  
  - 메시지 개수  
  - 카운트다운 값 목록  
  출력하는 파이썬 분석 스크립트

- **hello_world/sdkconfig.example**  
  `idf.py menuconfig` 후 생성된 `sdkconfig` 파일을 복사해 둔  
  “샘플 빌드 설정” 템플릿 파일

- **queue_demo/CMakeLists.txt**  
  `queue_demo` 프로젝트 루트 CMake 보일러플레이트

- **queue_demo/main/queue_demo.c**  
  FreeRTOS Queue Producer/Consumer 예제 코드  
  - `xQueueCreate(5, sizeof(int))`  
  - producer 태스크(0~9 숫자 전송)  
  - consumer 태스크(숫자 수신)  

- **queue_demo/main/CMakeLists.txt**  
  `queue_demo` 메인 컴포넌트 등록 설정 (`freertos`, `log` 의존)

- **generic_gpio-demo/CMakeLists.txt**  
  `generic_gpio-demo` 프로젝트 루트 CMake 보일러플레이트

- **generic_gpio-demo/README.md**  
  GPIO 예제 빌드·실행 방법 요약 (POSIX 시뮬레이션)

- **generic_gpio-demo/main/gpio_example_main.c**  
  ESP-IDF 내장 GPIO 토글(LED blink) 예제 코드  
  - `gpio_reset_pin`  
  - `gpio_set_direction`  
  - `gpio_set_level`  
  - FreeRTOS 태스크에서 500ms 주기 토글

- **generic_gpio-demo/main/CMakeLists.txt**  
  GPIO 예제 메인 컴포넌트 등록 설정 (`driver` 의존)

- **README.md** (루트 및 `esp-idf-posix-poc/README.md`)  
  전체 프로젝트 개요, 폴더 구조, 빠른 시작 가이드 등 빌드 설정
- **generic_gpio-demo**  
  ESP-IDF 내장 GPIO 깜빡이 예제 복원본과 빌드 설정
