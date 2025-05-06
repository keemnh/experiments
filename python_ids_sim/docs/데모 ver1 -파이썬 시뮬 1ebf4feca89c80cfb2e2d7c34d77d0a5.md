# 데모 ver1 -파이썬 시뮬

> “하드웨어 없이 데이터 흐름 감 잡기”
> 
> - 센서 데이터 생성
> - BLE 지연 생성
> - 그걸 합쳐서 탐지·로깅하는 흐름
> 
> → 까다로운 IDF 설치나 빌드 오류에 막히지 않고
> 
> → 진짜 하드웨어 없이도 “내가 설계한 파이프라인이 동작하긴 하네”를 바로 확인
> 
> <목표>
> 
> - **하드웨어 없이**
> - **전체 IDS 파이프라인(센서→탐지→로깅→알림)** 을
> - **가짜 데이터**로 빠르게 돌려 보자

## **1️⃣ : 센서 태스크 시뮬 (sensor_sim.py)**

1. 터미널 열고 파이썬 버전 및 설치 확인
    
    `python3 —version`
    

1. 작업파일이 저장될 장소로 이동
    
    `cd ~/Downloads`
    

1. 텍스트 에디터를 열고 코드 저장
    
    `nano sensor_sim.py`
    
    ```python
    import time, random
    
    while True:
        t = time.time()   # Unix epoch 기준 현재 시각 초 단위
        hall = random.choice([0, 1])
        imu  = abs(random.gauss(0, 0.2)) # 0주변,  표준편차 0.2, 항상 양수(abs)
        print(f"{t:.3f},SENSOR, hall={hall}, imu={imu:.2f}")
        time.sleep(0.01)    # 1초=1,000ms, 1,000 ms÷10 ms = 100Hz
    ```
    
    **`Ctrl+O** (Write Out)`
    
    → 누르면 화면 아래에 File Name to Write: sensor_sim.py 라고 뜸
    → 그냥 엔터 치면 저장 완료
    
    → **Ctrl+X** 누르면 nano 에디터가 종료되고 다시 터미널 프롬프트로 돌아감
    
    ![스크린샷 2025-05-06 오후 1.57.53.png](%E1%84%83%E1%85%A6%E1%84%86%E1%85%A9%20ver1%20-%E1%84%91%E1%85%A1%E1%84%8B%E1%85%B5%E1%84%8A%E1%85%A5%E1%86%AB%20%E1%84%89%E1%85%B5%E1%84%86%E1%85%B2%E1%86%AF%201ebf4feca89c80cfb2e2d7c34d77d0a5/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA_2025-05-06_%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE_1.57.53.png)
    

4. 3번에서 저장한 파일 실행

`python3 sensor_sim.py`

1. 결과 확인하고 `Ctrl + C`로 멈추기
    
    ![스크린샷 2025-05-06 오후 2.00.41.png](%E1%84%83%E1%85%A6%E1%84%86%E1%85%A9%20ver1%20-%E1%84%91%E1%85%A1%E1%84%8B%E1%85%B5%E1%84%8A%E1%85%A5%E1%86%AB%20%E1%84%89%E1%85%B5%E1%84%86%E1%85%B2%E1%86%AF%201ebf4feca89c80cfb2e2d7c34d77d0a5/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA_2025-05-06_%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE_2.00.41.png)
    

1. 의미 해석
    - (Unix epoch 기준) 1970년 1월 1일 0시부터 흐른 “현재 시각”을 초 단위 실수로 보여줌
    - SENSOR 태그는 “이 줄이 센서 이벤트”라는 표시
    - hall=0/1 은 Hall 센서가 “잠금 상태(0) vs 열린 상태(1)”
    - imu=숫자 는 “진동·가속도 세기”
    
    → 센서 태스크가 100Hz로 데이터를 읽는 모습 (1초에 100번 
    

## **2️⃣ : BLE 시뮬 (ble_sim.py)**

> 네트워크 지연(RTT)을 가짜로 만들어보는 시뮬레이션
> 

1. 텍스트 에디터를 열고 코드 저장
    
    `nano ble_sim.py`
    
    ```python
    import time, random
    
    # BLE ping-pong 시뮬: 10~50ms 랜덤 지연
    while True:
        t1 = time.time()
        delay = random.uniform(0.01, 0.05)  # 10~50ms 사이의 실수 하나를 랜덤 선택
        time.sleep(delay) # 지연을 흉내
        t2 = time.time()  # pong 받은 시점 기록
        rtt_ms = (t2 - t1) * 1000  # t2–t1은 왕복지연(sec단위), *1000은 ms단위로 
        print(f"{t2:.3f},BLE, rtt={rtt_ms:.1f}ms") 
        time.sleep(0.5)  # 500ms 주기로 ping
    ```
    
    **`Ctrl+O** (Write Out)`
    
    → 누르면 화면 아래에 File Name to Write: sensor_sim.py 라고 뜸
    → 그냥 엔터 치면 저장 완료
    
    → **Ctrl+X** 누르면 nano 에디터가 종료되고 다시 터미널 프롬프트로 돌아감
    
2. 파일 실행 →  결과 확인하고 **Ctrl+C** 눌러서 멈추기
    
    `python3 ble_sim.py`
    
    ![스크린샷 2025-05-06 오후 2.34.40.png](%E1%84%83%E1%85%A6%E1%84%86%E1%85%A9%20ver1%20-%E1%84%91%E1%85%A1%E1%84%8B%E1%85%B5%E1%84%8A%E1%85%A5%E1%86%AB%20%E1%84%89%E1%85%B5%E1%84%86%E1%85%B2%E1%86%AF%201ebf4feca89c80cfb2e2d7c34d77d0a5/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA_2025-05-06_%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE_2.34.40.png)
    

1. 데이터 분석
    - (Unix epoch 기준) 현재 시각
    - BLE 태그
    - RTT 통신 지연 시간 (요청(Ping) 보낸 시점부터 응답(Pong) 받은 시점까지 걸린 시간)

<aside>
💡

### **오탐(false positive) 위험**

사용자 주변 환경(신호 세기 약함·장애물·폰 성능 저하) 때문에 실제로는 공격이 아닌데 RTT가 일시적으로 올라가서 “공격”으로 잘못 감지할 수 있음

- 보완
    1. **다중 비교**
        - 한 번이 아니라 연속 N회(rtt > T) 조건 부여
        - ex) “3회 연속 20 ms 초과” 일 때만 탐지
    2. **센서 퓨전**
        - BLE RTT 외에 Hall/IMU 센서 이벤트와 **함께** 판정
        - ex) rtt>20 ms AND imu>RMS_threshold AND hall==LOCKED
    3. **동적 임계치 조정**
        - 평소 평균 RTT + α·표준편차 방식으로 가변 임계치 사용
    4. **환경 보정**
        - 신호 강도(RSSI) 정보도 같이 보고, RSSI가 너무 낮으면 “신호 약함”으로 분류
</aside>

## **3️⃣ : 로그 합치고 rule-based 탐지 구현**

- **로그 합치기** → 센서·네트워크 이벤트를 시간 순으로 나란히 비교
- **룰 기반 탐지** → 간단한 조건으로 “이럴 때 공격”을 빠르게 걸러 보고, 기준값을 잡기

### **A. 로그 파일 준비하기**

1. 센서 로그 수집
    1. sensor_sim.py를 실행하면서 출력 결과를 파일에 저장
        
        `python3 sensor_sim.py > sensor.log`
        
    2. 몇 초간(예: 5초) 그대로 둔 뒤, Ctrl+C 로 멈추고 sensor.log에 저장된 데이터 확인
2. ble 로그 수집
    1. 다른 터미널 열고
    2. ble_sim.py 실행하고 출력 결과 파일에 저장
        
        `python3 ble_sim.py > ble.log`
        
        ![스크린샷 2025-05-06 오후 3.39.30.png](%E1%84%83%E1%85%A6%E1%84%86%E1%85%A9%20ver1%20-%E1%84%91%E1%85%A1%E1%84%8B%E1%85%B5%E1%84%8A%E1%85%A5%E1%86%AB%20%E1%84%89%E1%85%B5%E1%84%86%E1%85%B2%E1%86%AF%201ebf4feca89c80cfb2e2d7c34d77d0a5/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA_2025-05-06_%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE_3.39.30.png)
        

### **B. 로그 합치기 스크립트 만들기 (detect.py)**

> merged.csv에 멀티모달 데이터가 잘 정리됐는지 확인하고, 그 위에 탐지 룰을 적용
> 
1. 새 파이썬 파일 생성
    
    `nano detect.py`
    
    - sensor.log와 ble.log를 읽어서
        1. 타임스탬프 기준으로 정렬
        2. merged.csv라는 하나의 표(시간·타입·값1·값2)로 저장
2. 코드 붙여넣고 저장 
    
    → 붙여넣고 → Ctrl + O → enter → Ctrl + x
    
    ```python
    import csv
    
    # 1) sensor.log와 ble.log 파일을 각각 한 줄씩 읽어 들여,
    events = []   # 로그 이벤트를 모두 담을 빈 리스트 마련
    for line in open('sensor.log'):
        t_str, _type, rest = line.strip().split(',', 2)  # 시간·타입·나머지(값)로 분리
        events.append((float(t_str), 'sensor', rest)) 
        # 리스트에 (시간, 종류, 나머지 문자열) 튜플로 저장
    
    for line in open('ble.log'): # BLE 로그도 같은 방식으로 이벤트에 저장
        t_str, _type, rest = line.strip().split(',', 2)
        events.append((float(t_str), 'ble', rest))
    
    # 2) 시간순으로 정렬  
    events.sort(key=lambda x: x[0])
    
    # 3) merged.csv 파일에 쓰기  
    # merged.csv'라는 이름으로 새 파일을 만들거나, 이미 있으면 덮어쓰기 모드('w')
    with open('merged.csv', 'w', newline='') as f:
        writer = csv.writer(f)   #  한 줄씩 CSV 형식으로 작성
        writer.writerow(['time', 'type', 'val1', 'val2']) # CSV 첫 줄: 컬럼 이름
        for t, typ, rest in events:
            if typ == 'sensor': # 센서로그이면
                # 출력 포맷 정리
                hall_str, imu_str = [s.strip() for s in rest.split(',')]
                hall = hall_str.split('=')[1]
                imu  = imu_str.split('=')[1]
                writer.writerow([t, 'sensor', hall, imu])
            else:   # ble 로그이면
                # 출력 포맷 정리
                rtt_str = rest.strip().split('=')[1]
                rtt = rtt_str.replace('ms','')
                writer.writerow([t, 'ble', rtt, ''])
    ```
    
3. detect.py와 alert.py를 분리한 이유
    - 로그 합치기(시뮬데이터 통합)는 **탐지 로직과는 별개의 작업**이어서
    - “데이터 준비” 단계 → “탐지” 단계
    - 책임을 분리하면 유지보수·디버깅이 쉬워짐

### **C. 합치고 실행해 보기 (merged.csv)**

> sensor.log와 ble.log에 저장된 이벤트들을 “시간순으로” 한 파일에 엮어 놓은 CSV(표) 파일
> 
> 
> → 센서 이벤트와 BLE 이벤트를 **동시에 비교**해야만 “멀티모달” 탐지가 가능
> 

1. 터미널에서 실행
    
    `python3 detect.py`
    

1. 해당 경로로 가면 merged.csv 파일 생성되어 있음
    
    ![merged-csv 결과.png](%E1%84%83%E1%85%A6%E1%84%86%E1%85%A9%20ver1%20-%E1%84%91%E1%85%A1%E1%84%8B%E1%85%B5%E1%84%8A%E1%85%A5%E1%86%AB%20%E1%84%89%E1%85%B5%E1%84%86%E1%85%B2%E1%86%AF%201ebf4feca89c80cfb2e2d7c34d77d0a5/merged-csv_%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA.png)
    
    ![스크린샷 2025-05-06 오후 4.34.27.png](%E1%84%83%E1%85%A6%E1%84%86%E1%85%A9%20ver1%20-%E1%84%91%E1%85%A1%E1%84%8B%E1%85%B5%E1%84%8A%E1%85%A5%E1%86%AB%20%E1%84%89%E1%85%B5%E1%84%86%E1%85%B2%E1%86%AF%201ebf4feca89c80cfb2e2d7c34d77d0a5/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA_2025-05-06_%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE_4.34.27.png)
    

1. 데이터 분석
    - time: 이벤트 발생 시각
    - type: 이벤트 종류(sensor/ble)
    - val1: sensor → hall값, ble → rtt(ms)
    - val2: sensor → imu값, ble → (빈칸)

### **D. 룰 기반 탐지 적용하기 (alert.py)**

> 간단한 룰로 이상 감지 해보기
→ merged.csv를 읽고 “룰 기반 탐지”를 실제로 수행해서
→ **이상 이벤트** 목록을 뽑아 터미널에 출력하는 스크립트
> 
1. 터미널에 새로 파일 생성해서 아래 코드 저장 
    - `nano alert.py`
        
        → Ctrl+o → enter → Ctrl+x
        
    
    ```python
    # 1) CSV 모듈 불러오기
    import csv
    
    # 2) 이상 탐지 결과를 모아 둘 빈 리스트 준비
    alerts = []
    
    # 3) merged.csv 파일을 헤더(첫 줄) 기준으로 읽어 들이기
    with open('merged.csv', newline='') as f:
        reader = csv.DictReader(f)
        
        # 4) 한 줄씩 순회하면서
        for row in reader:
            # 5) CSV 각 칼럼을 변수에 저장
            #    row['time']   : 문자열로 된 시간 정보
            #    row['type']   : 'sensor' 또는 'ble'
            #    row['val1']   : hall 값 또는 rtt 값
            #    row['val2']   : imu 값 (BLE는 빈 문자열)
            t   = float(row['time'])            # 문자열 → 숫자(소수)
            typ = row['type']                   # 'sensor' 아니면 'ble'
            v1  = float(row['val1'])            # val1을 숫자로 변환
            v2  = float(row['val2']) if row['val2'] else None  
                                                 # val2가 있으면 숫자로, 없으면 None
    
            # 6) 룰 1: BLE(rtt) 이 20 ms 초과하면 이상 판정
            if typ == 'ble' and v1 > 20.0:
                # 이상이면 alerts 리스트에 (시간, 라벨, 값) 추가
                alerts.append((t, 'HighRTT', v1))
    
            # 7) 룰 2: Sensor(imu) 이 0.5 초과하면 이상 판정
            if typ == 'sensor' and v2 is not None and v2 > 0.5:
                alerts.append((t, 'HighIMU', v2))
    
    # 8) 최종 이상 이벤트를 출력
    for atime, label, val in alerts:
        print(f"ALERT at {atime:.3f}: {label} = {val}")
    ```
    

1. 터미널에서 실행
    
    `python3 alert.py`
    
    ![alert.py 결과.png](%E1%84%83%E1%85%A6%E1%84%86%E1%85%A9%20ver1%20-%E1%84%91%E1%85%A1%E1%84%8B%E1%85%B5%E1%84%8A%E1%85%A5%E1%86%AB%20%E1%84%89%E1%85%B5%E1%84%86%E1%85%B2%E1%86%AF%201ebf4feca89c80cfb2e2d7c34d77d0a5/alert.py_%E1%84%80%E1%85%A7%E1%86%AF%E1%84%80%E1%85%AA.png)
    
2. 결과 분석
    - merged.csv를 읽어서 알림 로그를 출력
    - 데이터 준비(merged.csv 생성)와 **탐지 알고리즘**(alert 판정)을 분리하면
        - 탐지 규칙을 바꿀 때마다 데이터 합치기 코드를 손대지 않아도 됨
        - 후에 ML 기반 탐지 모델로 교체해도, 데이터 준비 파이프라인은 그대로 재사용 가능