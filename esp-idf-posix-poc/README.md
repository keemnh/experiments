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


## 🔧 파일 설명
- install_idf.sh / export_idf.sh
ESP-IDF 설치와 환경변수(export) 스크립트
- hello_log.txt
hello_world 예제 실행 결과 로그
- analyze_log.py
hello_log.txt에서 “Restarting in N seconds…” 카운트다운을 파싱해 개수와 값 리스트 출력
- sdkconfig.example
idf.py menuconfig 후 기본 설정을 기록한 예제 파일
- queue_demo
FreeRTOS Queue(Producer/Consumer) 예제 코드와 빌드 설정
- generic_gpio-demo
ESP-IDF 내장 GPIO 깜빡이 예제 복원본과 빌드 설정
