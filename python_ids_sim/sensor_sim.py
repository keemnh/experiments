import time, random

while True:
    t = time.time()
    hall = random.choice([0, 1])
    imu  = abs(random.gauss(0, 0.2))
    print(f"{t:.3f},SENSOR, hall={hall}, imu={imu:.2f}")
    time.sleep(0.01)
