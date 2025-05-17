# plot_hall.py

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("hall_states.csv")

plt.plot(
    df["time_s"],
    df["state"],
    drawstyle="steps-pre",  # 'pre' 면 해당 시점까지 이전 값 유지
    marker="o",
    markersize=6,
    linewidth=2
)

plt.xlabel("Time (s)")
plt.ylabel("Hall State (0 = LOW, 1 = HIGH)")
plt.title("Hall Sensor Toggle Over Time")
plt.ylim(-0.1, 1.1)
plt.grid(True)
plt.tight_layout()
plt.show()