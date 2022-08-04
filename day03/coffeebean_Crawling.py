## Selenium 사용하여 웹페이지 크롤링

# 패키지 로드
from bs4 import BeautifulSoup
import pandas as pd 
import time
from selenium import webdriver

def getCoffeeBeanInfo(result):
    # chrome webdrvier 객체 생성
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])    
    wd = webdriver.Chrome('./day03/chromedriver.exe', options=options) # jupyter와 경로가 다름(day03추가)
    
    for i in range(1, 11):
        wd.get('https://www.coffeebeankorea.com/store/store.asp') 
        time.sleep(1) # 팝업 표시후에 크롤링이 안돼서 브라우저가 닫히는 걸 방지하는 용도
        
        try:
            wd.execute_script(f"storePop2('{i}')")

            time.sleep(0.5)  
            html = wd.page_source
            soup = BeautifulSoup(html, 'html.parser')
            # print(soup.prettify())

            store_name = soup.select('div.store_txt > h2')[0].string
            print(store_name)
            store_info = soup.select('table.store_table > tbody > tr > td')
            store_addr_list = list(store_info[2])
            store_addr = store_addr_list[0].strip()
            store_contact = store_info[3].string
        
            result.append([store_name] + [store_addr] + [store_contact])
        except Exception as e:
            print(e)
            continue 

def main():
    result = []
    print('커피빈 매장 크롤링 >>> ')
    getCoffeeBeanInfo(result)

    # pandas Dateframe 생성
    columns = ['store', 'address', 'phone']
    coffeebean_df = pd.DataFrame(result, columns=columns)

    # csv 저장
    coffeebean_df.to_csv('./coffeebean_shop_info.csv', index=True, encoding='utf-8') 
    print('저장 완료!')

    del result[:]

if __name__ == '__main__':
    main()
