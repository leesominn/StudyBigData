import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt

# 클래스 OOP
class qTemplate(QWidget):
    # 생성자
    def __init__ (self) -> None: 
        super().__init__() 
        self.initUI()
    
    # 화면정의를 위해 만든 사용자 함수
    def initUI(self) -> None:
        self.setGeometry(300, 100, 640, 400) 
        self.setWindowTitle('QTemplate!')
        self.text = 'What a wonderful world'
        self.show()
   
    # Qwidget안에 원래 속해있는 함수위젯
    def paintEvent(self, event) -> None: 
        paint = QPainter()
        paint.begin(self)
        # 그리는 함수를 추가해줘야함
        self.drawText(event, paint)
        paint.end()

    # text를 그리기 위해 만든 사용자 함수
    def drawText(self, event, paint):
        paint.setPen(QColor(50,50,50))
        paint.setFont(QFont('Impact', 20))
        paint.drawText(105, 100, 'HELL WORLD') # label로 text를 넣은게 아니라 drawText로 text를 넣은 것
        paint.setPen(QColor(0,250,50))
        paint.setFont(QFont('NanumGothic', 15))
        paint.drawText(event.rect(), Qt.AlignCenter, self.text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ins = qTemplate()
    app.exec_()