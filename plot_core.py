import pandas as pd

def load_data(file_path):
    """讀取 Excel 資料"""
    return pd.read_excel(file_path, header=1)

def draw_high_freq_plot(ax1, df):
    """
    核心繪圖邏輯。
    接收一個外部傳入的 ax1，並在其上繪製雙 Y 軸圖表。
    """
    # 清除舊圖表內容
    ax1.clear()
    
    # 處理可能存在的舊右側 Y 軸
    # 檢查 ax1 的 figure 中是否已經有 twinx 產生的第二個 axes
    fig = ax1.get_figure()
    for extra_ax in fig.axes:
        if extra_ax is not ax1:
            extra_ax.clear()
            fig.delaxes(extra_ax)

    # --- 左側 Y 軸 (PWM) ---
    ax1.plot(
        df["PWM(us)"],
        color="blue",
        linewidth=0.3,
        label="PWM"
    )
    ax1.set_ylabel("PWM", color="blue")
    ax1.tick_params(axis='y', labelcolor="blue")
    ax1.grid(True)

    # --- 建立右側 Y 軸 (F(KG)) ---
    ax2 = ax1.twinx()
    ax2.plot(
        df["F(KG)"],
        color="red",
        linewidth=0.1,
        label="F(KG)"
    )
    ax2.set_ylabel("F(KG)", color="red")
    ax2.tick_params(axis='y', labelcolor="red")

    # 自動緊湊排版
    fig.tight_layout()