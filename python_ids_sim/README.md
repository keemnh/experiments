# experiments

Python으로 IDS(센서→BLE→탐지→로깅) 전체 흐름 시뮬레이션

## python_ids_sim
- sensor_sim.py : 100Hz 센서 데이터 생성
- ble_sim.py    : 500ms BLE RTT 시뮬레이션
- detect.py     : sensor.log + ble.log → merged.csv 생성
- alert.py      : 룰 기반 이상 이벤트 탐지

## data (샘플 로그)
- sensor.log
- ble.log
- merged.csv
