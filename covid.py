from bs4 import BeautifulSoup
import requests

url = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13&ncvContSeq=&contSeq=&board_id=&gubun=' #이 링크에서 크롤링
res = requests.get(url)
res.raise_for_status()
soup = BeautifulSoup(res.text, 'lxml')

all = soup.select_one('#content > div > div.data_table.midd.mgt24 > table > tbody > tr.sumline > td:nth-child(5)').text #전체 확진자 수
today = soup.select_one('#mapAll > div > ul > li:nth-child(6) > div:nth-child(2) > span').text #오늘 확진자 수
die = soup.select_one('#mapAll > div > ul > li:nth-child(1) > div:nth-child(2) > span').text #사망자 수
die_plus = soup.select_one('#mapAll > div > ul > li:nth-child(2) > div:nth-child(2) > span').text #전일대비 사망자 증가율
date = soup.select_one('#content > div > div.timetable > p > span').text #최종 갱신일
#covid19_date = covid19_date.replace('.', '-') #최종 갱신일에서 .을 -로 바꿈
