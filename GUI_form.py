import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QFileDialog, QLabel, QLineEdit, QComboBox)

# 引入plot_core.py繪圖功能
from plot_core import load_data, draw_high_freq_plot

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
        
        # first-TOP control bar
        top_layout = QHBoxLayout()
        self.btn_open = QPushButton('Open Excel', self) #self is not required
        self.btn_open.setFixedWidth(100)
        self.btn_open.clicked.connect(self.open_file)
        
        
        self.input_param01 = QLineEdit(self)
        self.input_param01.setText('2')
        self.input_param01.setPlaceholderText('header line number')
        self.input_param01.setFixedWidth(100)

        self.combo_data01 = QComboBox(self)
        self.combo_data01.setFixedWidth(100)
        self.combo_data02 = QComboBox(self)
        self.combo_data02.setFixedWidth(100)

        top_layout.addWidget(self.btn_open)
        top_layout.addWidget(self.input_param01)
        top_layout.addSpacing(100)
        top_layout.addWidget(self.combo_data01)
        top_layout.addWidget(self.combo_data02)
        top_layout.addStretch()

        main_layout.addLayout(top_layout)


        # second-Status Bar
        self.Op_status = QLabel('尚未讀取檔案', self)
        main_layout.addWidget(self.Op_status)
        

        # 初始化 Matplotlib 畫布 (乾淨的畫布)
        self.fig, self.ax1 = plt.subplots(figsize=(12, 6))
        self.canvas = FigureCanvas(self.fig)
        main_layout.addWidget(self.canvas)
        
        # 工具列
        self.toolbar = NavigationToolbar(self.canvas, self)
        main_layout.addWidget(self.toolbar)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, '選擇高頻資料 Excel 檔', '', 'Excel Files (*.xlsx *.xls)'
        )
        
        if file_path:
            filename = file_path.split("/")[-1]
            self.Op_status.setText(f'正在讀取：{filename}')
            QApplication.processEvents()
            
            try:
                # 1. 呼叫核心模組讀取資料
                df = load_data(file_path)
                
                # 2. 呼叫核心模組把圖畫在我們 GUI 的 self.ax1 上
                draw_high_freq_plot(self.ax1, df)
                
                # 3. 通知畫布重新渲染
                self.canvas.draw()
                self.Op_status.setText(f'讀取成功：{filename}')
                
            except Exception as e:
                self.Op_status.setText(f'錯誤：資料處理失敗 ({str(e)})')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PlotApp()
    ex.show()
    sys.exit(app.exec())