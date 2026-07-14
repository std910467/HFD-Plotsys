import pandas as pd

def load_data(file_path):
    """讀取 Excel 資料"""
    return pd.read_excel(file_path, header=1)

def draw_high_freq_plot(ax1, df, col1, col2):
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
        df[col1],
        color="blue",
        linewidth=0.1,
        label= col1
    )
    ax1.set_ylabel(col1, color="blue")
    ax1.tick_params(axis='y', labelcolor="blue")
    ax1.grid(True)

    # --- 建立右側 Y 軸 (F(KG)) ---
    ax2 = ax1.twinx()
    ax2.plot(
        df[col2],
        color="red",
        linewidth=0.1,
        label=col2
    )
    ax2.set_ylabel(col2, color="red")
    ax2.tick_params(axis='y', labelcolor="red")

    # 自動緊湊排版
    fig.tight_layout()

def change_ax1(ax1, df, col1):
    if not col1: #選單空的就不畫
        return    
    ax1.lines  #裡面的線全部移除
    while ax1.lines:
        ax1.lines[0].remove()
        
    # 畫上新的左邊資料
    ax1.plot(
        df[col1],
        color="blue",
        linewidth=0.1,
        label=col1
    )
    
    # 重新設定左邊 Y 軸的標籤與自動縮放
    ax1.set_ylabel(col1, color="blue")
    ax1.tick_params(axis='y', labelcolor="blue")
    ax1.relim()          # 重新計算資料邊界
    ax1.autoscale_view() # 自動縮放左邊 Y 軸的範圍
    


def change_ax2(ax1, df, col2 ):
    if not col2:
        return
    ax2 = None
    fig = ax1.get_figure()
    for extra_ax in fig.axes:
        if extra_ax is not ax1:
            ax2=extra_ax
            break

    if ax2==None: #測試有沒有建立ax2
        ax2 = ax1.twinx()
    else:
        while ax2.lines:
            ax2.lines[0].remove()

    # 畫上新的右邊資料
    ax2.plot(
        df[col2],
        color="red",  # 換個顏色區分
        linewidth=0.1,
        label=col2
    )
    
    # 重新設定右邊 Y 軸的標籤與自動縮放
    ax2.set_ylabel(col2, color="red")
    ax2.tick_params(axis='y', labelcolor="red")
    ax2.relim()
    ax2.autoscale_view()