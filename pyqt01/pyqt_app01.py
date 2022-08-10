# 가장 간단한 PyQt 실행방법
from PyQt5 import QtWidgets as qw 

def run():
    app = qw.QApplication([]) # (기본)
    wnd = qw.QMainWindow() # (기본)윈도우창 만들기
    label = qw.QLabel('Hello Qt!') # (옵션)label에 text적기
    wnd.setCentralWidget(label) # (옵션)내가 만든 윈도우창에 label을 중앙에 위치시키기
    wnd.show() # (기본)
    app.exec_() # (기본)

if __name__ == '__main__':
    run()
