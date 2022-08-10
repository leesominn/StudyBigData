import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
# from PyQt5.QtCore import Qt

# 클래스 OOP
class QTemplate(QWidget):
    # 생성자
    def __init__ (self) -> None: 
        super().__init__() 
        self.initUI()
    
    # 화면정의를 위해 만든 사용자 함수
    def initUI(self) -> None:
        self.addControls()
        self.setGeometry(300, 100, 640, 400) 
        self.setWindowTitle('QLabel')
        self.show()

    def addControls(self) -> None:
        self.setWindowIcon(QIcon('./pyqt01/image/lion.png')) # 윈도우창의 title에 아이콘 넣기
        label1= QLabel('', self)
        label2= QLabel('', self)
        label1.setStyleSheet(
            ('border-width: 3px;'
             'border-style: solid;'
             'border-color: blue;'
             'image: url(./pyqt01/image/image1.png)') # image경로는 절대경로로
        )
        label2.setStyleSheet(
            ('border-width: 3px;'
             'border-style: dot-dot-dash;'
             'border-color: red;'
             'image: url(./pyqt01/image/image2.png)') 
        )    

        box = QHBoxLayout() # H는 가로방향, V는 세로방향
        box.addWidget(label1)
        box.addWidget(label2)
        
        self.setLayout(box)
        
   
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ins = QTemplate()
    app.exec_()