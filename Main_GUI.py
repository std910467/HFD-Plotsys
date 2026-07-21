import sys
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QFileDialog, QLabel, 
                             QLineEdit, QComboBox, QSpinBox,QAbstractSpinBox  )
from PyQt6.QtCore import Qt 
from PyQt6.QtGui import QAction

# 引入plot_core.py繪圖功能
from plot_core import load_data, draw_high_freq_plot, change_ax1, change_ax2

class PlotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('High-Frequency Data Plot')
        self.setGeometry(100, 100, 1000, 700) 
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        #設定 menu bar
        menubar = self.menuBar()
        settings_menu = menubar.addMenu('設定')

        open_settings_action = QAction('繪圖參數設定', self)
        open_settings_action.triggered.connect(self.open_settings_dialog)
        settings_menu.addAction(open_settings_action)



        # first-TOP control bar
        top_layout = QHBoxLayout()

        ##設定輸入標頭的地方
        self.label_header = QLabel('Header:', self)
       # self.label_header.setFixedWidth(50)
        self.input_param01 = QSpinBox(self)
        self.input_param01.setValue(2)
        self.input_param01.setKeyboardTracking(False) #關閉鍵盤追蹤，這樣輸入完才會作動
        self.input_param01.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons) #關閉旁邊內建的上下箭頭。
        self.input_param01.setToolTip('請輸入 Excel 資料的標頭行數 (Header Line Number)') #浮動顯示輸入說明。
        self.input_param01.setFixedWidth(40)

        ##開啟檔案的按鈕
        self.btn_open = QPushButton('Open Excel', self) #self is not required
        self.btn_open.setFixedWidth(100)
        self.btn_open.clicked.connect(self.open_file)
        

        ##設定下拉選單
        self.combo_data01 = QComboBox(self)
        self.combo_data01.setFixedWidth(100)
        self.combo_data02 = QComboBox(self)
        self.combo_data02.setFixedWidth(100)
        
        self.combo_data01.currentTextChanged.connect(self.combo01_changed)
        self.combo_data02.currentTextChanged.connect(self.combo02_changed)

        top_layout.addWidget(self.label_header)
        top_layout.addWidget(self.input_param01)
        top_layout.addWidget(self.btn_open)  
        top_layout.addSpacing(100)      
        top_layout.addWidget(self.combo_data01)
        top_layout.addWidget(self.combo_data02)
        top_layout.addStretch()

        main_layout.addLayout(top_layout) #裝入第一排


        # second-Status Bar
        self.Op_status = QLabel('尚未讀取檔案', self)
        self.Op_status.setFixedHeight(25)
        self.Op_status.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        main_layout.addWidget(self.Op_status)
        

        # 初始化 Matplotlib 畫布 (乾淨的畫布)
        self.fig, self.ax1 = plt.subplots(figsize=(12, 6))
        self.canvas = FigureCanvas(self.fig)
        main_layout.addWidget(self.canvas)
        
        # 工具列
        self.toolbar = NavigationToolbar(self.canvas, self)
        main_layout.addWidget(self.toolbar)

    def open_file(self):  #開啟檔案
        file_path, _ = QFileDialog.getOpenFileName(
            self, '選擇高頻資料 Excel 檔', '', 'Excel Files (*.xlsx *.xls)'
        )
        
        if file_path:
            filename = file_path.split("/")[-1]
            header_row = self.input_param01.value()
            self.Op_status.setText(f'正在讀取：{filename}')
            QApplication.processEvents()
            
            try:
                # 1. 讀取資料
                self.df = load_data(file_path,header_row)
                
                ##更新下拉選單
                self.Update_Combo(self.df.columns.tolist())
                col_count = len(self.df.columns.tolist())

                def_col1=1 if col_count > 1 else 0
                def_col2=6 if col_count > 6 else (col_count-1)                

                # 2. 圖畫在我們 GUI 的 self.ax1 上
                draw_high_freq_plot(self.ax1, self.df, self.df.columns[def_col1] , self.df.columns[def_col2])
                
                # 3. 通知畫布重新渲染
                self.canvas.draw()
                self.Op_status.setText(f'讀取成功：{filename}')
                
            except Exception as e:
                self.Op_status.setText(f'ERROR：資料處理失敗 ({str(e)})')
        
    def Update_Combo(self, columns):   #更新下拉選單
        self.combo_data01.blockSignals(True)
        self.combo_data02.blockSignals(True)

        self.combo_data01.clear()
        self.combo_data02.clear()
        self.combo_data01.addItems(columns)
        self.combo_data02.addItems(columns)
        
        col_count = len(columns)

        def_col1=1 if col_count > 1 else 0
        def_col2=6 if col_count > 6 else (col_count-1)
        self.combo_data01.setCurrentIndex(def_col1)
        self.combo_data02.setCurrentIndex(def_col2)
        self.combo_data01.blockSignals(False)
        self.combo_data02.blockSignals(False)

    
    def combo01_changed(self, col1):
        change_ax1(self.ax1, self.df, col1)
        self.fig.canvas.draw_idle()

    def combo02_changed(self, col2):
        change_ax2(self.ax1, self.df, col2)
        self.fig.canvas.draw_idle()
    
    def open_settings_dialog(self):
        print("功能建立中")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PlotApp()
    ex.show()
    sys.exit(app.exec())