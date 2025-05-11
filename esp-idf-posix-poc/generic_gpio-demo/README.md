# Generic GPIO Blink Example (POSIX 시뮬레이션)

ESP-IDF 내장 GPIO 토글 예제를 macOS/Linux POSIX 환경에서 빌드·실행하는 방법

## 요구 사항
- ESP-IDF 개발 환경이 설치되어 있어야 함
- `idf.py` 명령이 PATH에 등록되어 있어야 함

## 빌드 및 실행

```bash
cd ~/git/experiments/esp-idf-posix-poc/generic_gpio-demo
idf.py --preview set-target linux
idf.py --preview build
./build/generic_gpio.elf

	•	터미널에 LED ON / LED OFF 메시지가 0.5초 간격으로 반복 출력되면 성공
	•	Ctrl+C 로 종료
