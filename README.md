# HFD-Plotsys
High-Frequency-Data Plot system
Since Excel cannot directly plot data sets with more than 20,000 records, I created a simple program to generate the charts.
Currently, I’m primarily using two libraries: PyQT6 and matplotlib.


## Files

- `Main_GUI.py` — 主要執行的程式
- `plot_core.py` — 畫圖的子程式
- `print_fist.py` — 過渡的測試檔案,不用理會

## Requirements

- Python 3.9+
- PyQt6
- pandas
- matplotlib
- openpyxl (讀取 .xlsx 檔案需要)

## Installation

安裝所需套件:

```bash
pip install PyQt6 pandas matplotlib openpyxl
```
## How to Run
在專案資料夾內執行:
```bash
python Main_GUI.py
```
## Usage
1. 點擊 **Open Excel** 按鈕,選擇你的資料檔案
2. 從下拉選單選擇要繪製的欄位
3. 圖表會自動顯示在畫面中


