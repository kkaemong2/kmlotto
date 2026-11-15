import requests # 인터넷 서버에 데이터를 요청할 때 사용하는 라이브러리

# https://www.dhlottery.co.kr/lt645/selectPstLt645InfoNew.do?srchDir=center&srchLtEpsd=1249&_=1794116699277

# https://www.dhlottery.co.kr/lt645 -> 공통으로 사용하는 기본 주소
# selectPstLt645InfoNew.do -> 실제 데이터를 요청할 경로
# ?srchDir=center&srchLtEpsd=1249&_=1794116699277 -> 추가 요청 조건의 쿼리 파라미터


BASE_URL = "https://www.dhlottery.co.kr/lt645"

# 요청 헤더 (요청할 때 함께 전달하는 정보)
HEADERS = {
    "User-Agent": "Mozilla/5.0",                            # 어떤 프로그램을 통해 요청중인지
    "Referer": "https://www.dhlottery.co.kr/lt645/result"   # 어느 페이지에서 이 데이터를 요청했는지
}


DATA_FILE = r"C:\Users\gusco\Desktop\Work\Ex1\data\lotto_data.json" # 당첨번호를 저장할 파일 위치