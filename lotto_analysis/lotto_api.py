import requests
import time

from .config import BASE_URL, HEADERS

# 특정 회차 데이터 요청
def get_lotto_data(lotto_round):

    url = f"{BASE_URL}/selectPstLt645InfoNew.do"

    # 조회 조건 - 주소 뒷부분에 나옴
    params = {
        "srchDir": "center", # 데이터의 이름(키)
        "srchLtEpsd": lotto_round  # 실제 데이터(값)
    }

    for attempt in range(3):
                try:
                    print(f"요청 회차: {lotto_round}")
                
                # 서버에 데이터를 요청하고 응답 결과를 response 변수에 저장
                    response = requests.get(
                        url,
                        headers=HEADERS,
                        params=params,
                        timeout=30      # 서버 응답을 최대 30초 기다린다
                    )
    
                    # 서버 요청(HTTP)을 실패했다면 오류를 발생시킴 (200 -> 정상, 404 -> 주소 찾을 수 없음, 500 -> 서버 내부 오류)
                    response.raise_for_status()
    
                    # 서버에서 받은 JSON 데이터를 Python 자료형 변환하여 data에 저장
                    data = response.json()
    
                    return data["data"]["list"]
                
                # requests 라이브러리에서 발생하는 오류를 한꺼번에 적은 클래스
                except requests.exceptions.RequestException as e:

                    # 실제 오류 내용 출력
                    print(f"오류 내용: {e}")

                    if attempt == 2:
                        raise

                    print("서버 연결 실패. 5초 후 재시도...")
                    time.sleep(5)
                    if attempt == 2:
                        raise   #재시도하지 않고 오류를 바깥으로 전달
    
                    print("서버 연결 실패. 5초 후 재시도...")
                    time.sleep(5)
