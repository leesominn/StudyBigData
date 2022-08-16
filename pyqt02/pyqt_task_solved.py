import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time

# UI 스레드와 작업스레드 분리
class Worker(QThread): 
    # QThread는 UI(화면)를 컨트롤할 권한이 없음 
    # 대신 통신을 통해서 UI스레드를 컨트롤할 수 있도록 해줌 
    valChangeSignal = pyqtSignal(int) 

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.working = True # 클래스 내부 변수 working을 지정

    def run(self):
        while self.working:
            for i in range(0,1000000):
                print(f'출력 : {i}')
                # self.pgbTask.setValue(i)
                # self.txbLog.append(f'출력 >>> {i}')
                self.valChangeSignal.emit(i) # UI 스레드가 화면을 그릴 수 있게 해줌
                time.sleep(0.0001) # 1micro sec정도 시간을 멈춤
       

# 클래스 OOP
class qTemplate(QWidget):
    # 생성자
    def __init__ (self) -> None: 
        super().__init__() 
        uic.loadUi('./pyqt02/ttask.ui', self)
        self.initUI()
    
    def initUI(self) -> None:
        self.addControls()
        
        self.show()

    def addControls(self) -> None:
        self.btnStart.clicked.connect(self.btn1_clicked)
        # Worker 클래스 생성
        self.worker = Worker(self)
        self.worker.valChangeSignal.connect(self.updateProgress) 
        # 스레드에서 받은 signal은 updateProgress함수에서 처리해줌

    @pyqtSlot(int)
    def updateProgress(self, val): # val이 Worker스레드에서 전달받은 반복값
        self.pgbTask.setValue(val)
        self.txbLog.append(f'출력 >>> {val}')
        if val == 999999:
            self.worker.working = False
        

    def btn1_clicked(self):
        self.txbLog.append('실행!!')
        self.pgbTask.setRange(0,999999) # 응답없음 발생
        self.worker.start()
        self.worker.working = True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ins = qTemplate()
    app.exec_()