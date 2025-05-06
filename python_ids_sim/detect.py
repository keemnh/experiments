import csv

# 1) sensor.log와 ble.log 파일을 각각 한 줄씩 읽어 들여,
events = []
for line in open('sensor.log'):
    # a. 한 줄 예시: "1746500000.123,SENSOR, hall=1, imu=0.05"
    t_str, _type, rest = line.strip().split(',', 2)
    # - split(',',2): 앞의 두 콤마까지 잘라서 세 부분으로 분리
    #   t_str="1746500000.123", _type="SENSOR", rest=" hall=1, imu=0.05"
    events.append((float(t_str), 'sensor', rest))

for line in open('ble.log'):
    # 한 줄 예시: "1746500000.623,BLE, rtt=23.4ms"
    t_str, _type, rest = line.strip().split(',', 2)
    events.append((float(t_str), 'ble', rest))

# 2) 시간순으로 정렬  
events.sort(key=lambda x: x[0])

# 3) merged.csv 파일에 쓰기  
with open('merged.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    # CSV 첫 줄: 컬럼 이름(header)
    writer.writerow(['time', 'type', 'val1', 'val2'])
    for t, typ, rest in events:
        if typ == 'sensor':
            # rest: " hall=1, imu=0.05"
            hall_str, imu_str = [s.strip() for s in rest.split(',')]
            # hall_str="hall=1", imu_str="imu=0.05"
            hall = hall_str.split('=')[1]
            imu  = imu_str.split('=')[1]
            writer.writerow([t, 'sensor', hall, imu])
        else:
            # rest: " rtt=23.4ms"
            rtt_str = rest.strip().split('=')[1]
            # rtt_str="23.4ms"
            # 숫자만 떼어내려면 끝의 'ms' 제거
            rtt = rtt_str.replace('ms','')
            writer.writerow([t, 'ble', rtt, ''])
