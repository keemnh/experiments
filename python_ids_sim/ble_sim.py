import time, random

# BLE ping-pong 시뮬: 10~50ms 랜덤 지연
while True:
    t1 = time.time()
    delay = random.uniform(0.01, 0.05)  # 10~50 ms
    time.sleep(delay)
    t2 = time.time()
    rtt_ms = (t2 - t1) * 1000
    print(f"{t2:.3f},BLE, rtt={rtt_ms:.1f}ms")
    time.sleep(0.5)  # 500ms 주기로 ping
