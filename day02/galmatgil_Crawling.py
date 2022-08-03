## 부산 갈맷길 정보 API 크롤링


import os
import sys
import urllib.request
import datetime
import time
import json
import pandas as pd
import pymysql


ServiceKey = 'Ujsa%2BxyfB2mRN3knWyRXupD7DWtbgxxz8mOXJB4ezhCNrj9MWSdDTjgPb%2FAd4d%2BOxPUq6go7f54boPeSxXN9EQ%3D%3D'

# url 접속 요청 후 응답리턴 함수
def getRequestUrl(url):
    req = urllib.request.Request(url)

    try:
        res = urllib.request.urlopen(req)
        if res.getcode() == 200: # 200대=ok, 400대=error, 500대=server error
            print(f'[{datetime.datetime.now()}] Url Request success') # f포맷팅 사용
            return res.read().decode('utf-8')
    except Exception as e:
        print(e)
        print(f'[{datetime.datetime.now()}] Error for URL : {url}')
        return None


def getGalmatgilInfo(): 
    service_url = 'http://apis.data.go.kr/6260000/fbusangmgcourseinfo/getgmgcourseinfo'
    params = f'?serviceKey={ServiceKey}' 
    params += f'&numOfRows=10'
    params += f'&pageNo=1'
    params += f'&resultType=json'
    url = service_url + params

    print(url)
    retData = getRequestUrl(url)

    if retData == None:
        return None
    else:
        return json.loads(retData)

'''
"seq": 1,
"course_nm": "1코스",
"gugan_nm": "1코스 1구간",
"gm_range": "11.9km",
"gm_degree": "중",
"start_pls": "임랑해수욕장",
"start_addr": "부산광역시 기장군 장안읍 임랑리 145-5",
"middle_pls": "일광해수욕장",
"middle_adr": "부산광역시 기장군 일광면 삼성리 115-28",
"end_pls": "기장군청",
"end_addr": "부산광역시 기장군 기장읍 청강리 3-3",
"gm_course": "임랑해수욕장-칠암파출소-부경대학교 수산과학연구소-일광해수욕장-기장체육관-기장군청",
"gm_text": "옛부터 아홉 개의 포구가 있어 기장구포로 불렸는데,
'''

# 데이터수집요청하기 함수
def getGalmatgilService():
    result = []

    jsonData = getGalmatgilInfo()
    # print(jsonData)
    if jsonData['getgmgcourseinfo']['header']['code'] == '00' :
        if jsonData['getgmgcourseinfo']['item'] == '':
            print('서비스 오류!')
        else:
            for item in jsonData['getgmgcourseinfo']['item']:
                # print(item)
                seq = item['seq']
                course_nm = item['course_nm']
                gugan_nm = item['gugan_nm']
                gm_range = item['gm_range']
                gm_degree = item['gm_degree']
                start_pls = item['start_pls']
                start_addr = item['start_addr']
                middle_pls = item['middle_pls']
                middle_adr = item['middle_adr']
                end_pls = item['end_pls']
                end_addr = item['end_addr']
                gm_course = item['gm_course']
                gm_text = item['gm_text']

                result.append([seq, course_nm, gugan_nm, gm_range, gm_degree, start_pls, start_addr, middle_pls, 
                                middle_adr, end_pls, end_addr, gm_course, gm_text])
    
    return result


def main():
    reuslt = []

    print('부산 갈맷길코스 조회합니다')
    result = getGalmatgilService()

    if len(result) > 0:
        # 파일저장(csv)
        columns = ['seq', 'course_nm', 'gugan_nm', 'gm_range', 'gm_degree', 'start_pls', 'start_addr', 'middle_pls', 
                    'middle_adr', 'end_pls', 'end_addr', 'gm_course', 'gm_text']
        result_df = pd.DataFrame(result, columns=columns)
        result_df.to_csv(f'./부산갈맷길정보.csv', index=False, encoding='utf-8')

        print('csv파일 저장완료!')

        # DB저장
        connection = pymysql.connect(host='localhost',
                                    user='root',
                                    password='1234',
                                    db='crawling_data')
        cursor = connection.cursor() # cursor객체가 있어야 제대로 실행이 가능

        # column명 동적으로 만들기
        cols = '`,`'.join([str(i) for i in result_df.columns.tolist()])

        for i, row in result_df.iterrows():
            sql = 'INSERT INTO `galmatgil_info` (`' + cols + '`) VALUES ('+ '%s, '*(len(row)-1) +'%s)'
            cursor.execute(sql, tuple(row))

        connection.commit()
        connection.close()

        print('DB 저장완료!') 

if __name__ == '__main__':
    main()