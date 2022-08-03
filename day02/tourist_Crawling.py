## 데이터포털 API 크롤링

from asyncio.proactor_events import _ProactorBaseWritePipeTransport
import os
from pyexpat import native_encoding
import sys
import urllib.request
import datetime
import time
import json
from mysqlx import Column
import pandas as pd


# 저자 키 값 : Ody77GLuYeR%2FeFqbpduMN2Bi4Cka2fztbgnj6E2Eux1kUhy3e4epR28XKBUaObiqPoVzAizxXMBPXtMyuC9v9Q%3D%3D

ServiceKey = 'Ody77GLuYeR%2FeFqbpduMN2Bi4Cka2fztbgnj6E2Eux1kUhy3e4epR28XKBUaObiqPoVzAizxXMBPXtMyuC9v9Q%3D%3D'

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

def getTourismStatsItem(yyyymm, nat_cd, ed_cd): # 연월, 국가코드, 출입구구분코드(ex. 201201,112,D)
    service_url = 'http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList'
    params = f'?_type=json&serviceKey={ServiceKey}' # 인증키
    # ?는 앞에 한번만, 그다음부턴 &로 연결, key={value}형태
    params += f'&YM={yyyymm}'
    params += f'&NAT_CD={nat_cd}'
    params += f'&ED_CD={ed_cd}'
    url = service_url + params

    # print(url)
    retData = getRequestUrl(url)

    if retData == None:
        return None
    else:
        return json.loads(retData)

# 데이터수집요청하기 함수
def getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear):
    jsonResult = []
    result = []
    natName = ''
    dataEnd = f'{nEndYear}{12:0>2}' # 년도 마지막 끝자리가 2자리가 넘어가면 0으로 처리
    isDataEnd = False # 데이터 끝 확인용 플래그

    for year in range(nStartYear, nEndYear+1):
        for month in range(1, 13):
            if isDataEnd == True: break

            yyyymm = f'{year}{month:0>2}' # :0>2를 안하면 2022 1월이 202201이 아닌 20221이 돼버림
            jsonData = getTourismStatsItem(yyyymm, nat_cd, ed_cd)

            if jsonData['response']['header']['resultMsg'] == 'OK':
                # 데이터가 없는 경우라면 break(서비스 종료)
                if jsonData['response']['body']['items'] == '':
                    isDataEnd = True
                    dataEnd = f'{year}{month-1:0>2}'
                    print(f'제공되는 데이터는 {year}년 {month-1}월까지 입니다')
                    break

            print(json.dumps(jsonData, indent=4, sort_keys=True, ensure_ascii=False))
            natName = jsonData['response']['body']['items']['item']['natKorNm']
            natName = natName.replace(' ', '') #ex.중  국 -> 중국으로 공백 없애주기
            num = jsonData['response']['body']['items']['item']['num']
            ed = jsonData['response']['body']['items']['item']['ed']

            jsonResult.append({'nat_name': natName, 'nat_cd': nat_cd, 'yyyymm': yyyymm, 'visit_cnt': num })
            result.append([natName, nat_cd, yyyymm, num])

    return(jsonResult, result, natName, ed, dataEnd)


def main():
    jsonResult = []
    result = []
    natName = ''
    ed = ''
    dataEnd = ''

    print('<< 국내 입국한 외국인 통계데이터를 수집합니다 >>')
    nat_cd = input('국가코드를 입력하세요 (중국: 112 / 일본: 130 / 미국: 275) > ')
    nStartYear = int(input('데이터를 몇 년부터 수집할까요? '))
    nEndYear = int(input('데이터를 몇 년까지 수집할까요? '))
    ed_cd = 'E' # D:한국인외래관광객, E:방한외국인

    (jsonResult, result, natName, ed, dataEnd) = \
        getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear)

    if natName == '':
        print('데이터 전달 실패. 공공데이터포털 서비스 확인요망')
    else:
        # 파일저장(csv)
        columns = ['입국국가', '국가코드', '입국연월', '입국자수']
        result_df = pd.DataFrame(result, columns=columns)
        result_df.to_csv(f'./{natName}_{ed}_{nStartYear}_{dataEnd}.csv', index=False, encoding='cp949')
        #한글 윈도우에서 작업하고 싶다면 encoding을 cp949로, 데이터 분석을 위해 작업하고 싶다면 encoding을 utf8로

        print('csv파일 저장완료!')

if __name__ == '__main__':
    main()