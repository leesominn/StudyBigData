import sys
from PyQt5.QtWidgets import QApplication, QWidget

# 클래스 OOP
class qTemplate(QWidget):
    # 생성자
    def __init__ (self) -> None: # 여기서 self는 qTemplate를 말하는 것
        # 생성자는 기본적으로 return할 값이 없기 때문에 None이 되는 것
        # 만약 __str__이었다면 문자열을 return해줘야 함
        super().__init__() # qTemplate의 상속받은 QWidget를 의미
        self.initUI()
    
    def initUI(self) -> None:
        self.setGeometry(300, 100, 640, 400) # Qwidget안에 원래 속해있는 값
        # setGeometry(x축,y축,너비,높이) <-- 윈도우창의 좌표를 의미
        self.setWindowTitle('QTemplate!')
        self.show()
   
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ins = qTemplate()
    app.exec_()