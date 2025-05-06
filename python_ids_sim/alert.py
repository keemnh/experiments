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
