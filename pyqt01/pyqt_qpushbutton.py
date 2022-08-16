import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# 클래스 OOP
class qTemplate(QWidget):
    # 생성자
    def __init__ (self) -> None: 
        super().__init__() 
        self.initUI()
    
    def initUI(self) -> None:
        self.addControls()
        self.setGeometry(300, 100, 640, 400) 
        self.setWindowTitle('QPushButton 예제')
        self.show()

    def addControls(self) -> None:
        self.label = QLabel('메시지 : ', self)
        self.label.setGeometry(10,10,600,40)
        self.btnl = QPushButton('Click', self)
        self.btnl.setGeometry(510, 350, 120, 40)
        self.btnl.clicked.connect(self.btnl_clicked) # signal 연결
        # clicked=클릭하고 손을 떼는 순간 / click=클릭하는 순간 
        
    # event = signal(python) <-- ex. 버튼을 클릭하는 것 
    def btnl_clicked(self):
        self.label.setText('메시지 : btnl 버튼 클릭!') # Click버튼을 누르면 실행됨
        QMessageBox.information(self, 'Signal', 'Button Clicked!') # 일반정보창
        
        # QMessageBox.warning(self, 'Signal', 'Button Clicked!') # 경고창
        # QMessageBox.critical(self, 'Signal', 'Button Clicked!') # 에러창
   
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ins = qTemplate()
    app.exec_()