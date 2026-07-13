import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("高频数据-2026‘02’09-15‘58’12.xlsx",header=1)

# 建立圖表
fig, ax1 = plt.subplots(figsize=(12,6))

# 左側Y軸
ax1.plot(
    df["PWM(us)"],
    color="blue",
    linewidth=0.3,
    label="PWM"
)

ax1.set_ylabel("PWM")

# 建立右側Y軸
ax2 = ax1.twinx()

ax2.plot(
    df["F(KG)"],
    color="red",
    linewidth=0.1,
    label="F(KG)"
)

ax2.set_ylabel("F(KG)")

plt.grid(True)

plt.show()