# log_to_csv.py

import pandas as pd

# 1) hall.log 읽기
df = pd.read_csv("hall.log", header=None, names=["state"])

# 2) 시간 컬럼 추가 (0.5초 간격 가정)
df["time_s"] = df.index * 0.5

# 3) CSV로 저장
df.to_csv("hall_states.csv", index=False)

print(f"hall_states.csv 생성됨 ({len(df)}개 레코드)")