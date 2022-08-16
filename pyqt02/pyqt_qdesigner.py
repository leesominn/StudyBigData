import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# 클래스 OOP
class qTemplate(QWidget):
    # 생성자
    def __init__ (self) -> None: 
        super().__init__() 
        uic.loadUi('./pyqt02/basic01.ui', self)
        self.initUI()
    
    def initUI(self) -> None:
        self.addControls()
        
        self.show()

    def addControls(self) -> None:
        self.btn1.clicked.connect(self.btn1_clicked)

    def btn1_clicked(self):
        self.label.setText('메모 : btnl 버튼 클릭!') # Click버튼을 누르면 실행됨
        QMessageBox.warning(self, 'Signal', 'Button Clicked!')
       

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ins = qTemplate()
    app.exec_()