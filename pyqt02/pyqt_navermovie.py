from os import link
from re import search # Pyqt위한 import
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from urllib.parse import quote # 네이버 openAPI위한 import
import urllib.request
import json
import webbrowser

# 클래스 OOP
class qTemplate(QWidget):
    # 생성자
    def __init__ (self) -> None: # 생성자
        super().__init__() 
        uic.loadUi('./pyqt02/navermovie.ui', self)
        self.initUI()
    
    def initUI(self) -> None:
        self.addControls()
        self.show()
    
    # 위젯 정의, 이벤트(signal) 처리
    def addControls(self) -> None:
        self.btnSearch.clicked.connect(self.btnSearchClicked)
        self.txtSearch.returnPressed.connect(self.btnSearchClicked) # enter키로 검색 실행하기
        self.tblResult.itemSelectionChanged.connect(self.tblResultSelected)

    # tblResult창 클릭하면 해당 기사링크로 이동하는 함수
    def tblResultSelected(self) -> None:
        selected = self.tblResult.currentRow() # 현재 선택된 열의 인덱스
        link = self.tblResult.item(selected, 2).text() # tblResult창에서 index[1]인 주소를 가져오는 것
        webbrowser.open(link)     

    def btnSearchClicked(self) -> None: # 슬롯(이벤트핸들러) 
        jsonResult = []
        totalResult = []
        keyword = 'movie'
        search_word = self.txtSearch.text()
        display_count = 100

        # QMessageBox.information(self, '결과', search_word)
        jsonResult = self.getNaverSearch(keyword, search_word, 1, display_count)
        # print(jsonResult)

        for post in jsonResult['items']:
            totalResult.append(self.getPostData(post))
        # print(totalResult)
        self.makeTable(totalResult)
        return 

    # 테이블위젯 설정
    def makeTable(self, result):
        self.tblResult.setSelectionMode(QAbstractItemView.SingleSelection) #pyqtDesigner에서 처리해도 가능
        self.tblResult.setColumnCount(3) # 2 -> 3
        self.tblResult.setRowCount(len(result)) # result가 50개면 50개 출력(displayCount에 따라서 변경, 현재는 50개로 고정)
        self.tblResult.setHorizontalHeaderLabels(['영화제목', '상영년도', '뉴스링크']) # 제목 추가
        self.tblResult.setColumnWidth(0, 250)
        self.tblResult.setColumnWidth(1, 100)
        self.tblResult.setColumnWidth(2, 100) # 세번째 column 설정 추가
        self.tblResult.setEditTriggers(QAbstractItemView.NoEditTriggers) # read only(읽기만 가능)

        i = 0
        for item in result:
            title = self.strip_tag(item[0]['title'])
            subtitle = self.strip_tag(item[0]['subtitle'])
            pubDate = item[0]['pubDate']
            link = item[0]['link']
            self.tblResult.setItem(i, 0, QTableWidgetItem(f'{title} / {subtitle}'))
            self.tblResult.setItem(i, 1, QTableWidgetItem(pubDate))
            self.tblResult.setItem(i, 2, QTableWidgetItem(link))
            i += 1

    # html tag 없애는 함수
    def strip_tag(self, title):
        ret = title.replace('&lt;', '<')
        ret = ret.replace('&gt;', '>')
        ret = ret.replace('&quot;', '"')
        ret = ret.replace('&apos;', "'")
        ret = ret.replace('&amp;', '&')
        ret = ret.replace('<b>', '')
        ret = ret.replace('</b>', '')
        return ret

    def getPostData(self, post):
        temp = []
        title= post['title']
        subtitle= post['subtitle']
        link = post['link']
        pubDate = post['pubDate']

        temp.append({'title':title, 'subtitle':subtitle, 'link':link, 'pubDate':pubDate})

        return temp 

    # 핵심함수(Naver API 크롤링을 위한 함수)
    def getNaverSearch(self, keyword, search, start, display):
        url = f'https://openapi.naver.com/v1/search/{keyword}.json' \
              f'?query={quote(search)}&start={start}&display={display}'
        print(url)
        req = urllib.request.Request(url)
        # 네이버 인증 추가
        req.add_header('X-Naver-Client-Id', 'w2SrjIcbPlRew2exM0l8')
        req.add_header('X-Naver-Client-Secret', 'ZAkULrp9Ve')

        res = urllib.request.urlopen(req)
        if res.getcode() == 200:
            print('URL request Succeed')
        else:
            print('URL request Failed')

        ret = res.read().decode('utf-8')
        if ret == None:
            return None
        else:
            return json.loads(ret)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ins = qTemplate()
    app.exec_()