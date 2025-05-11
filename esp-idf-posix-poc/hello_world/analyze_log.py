import re

log_path = 'hello_log.txt'
with open(log_path) as f:
    lines = f.readlines()

data = []
for line in lines:
    m = re.match(r"Restarting in (\d+) seconds\.\.\.", line)
    if m:
        data.append(int(m.group(1)))

print(f"'Restarting in' 메시지 개수: {len(data)}")
print(f"카운트다운 값 목록: {data}")