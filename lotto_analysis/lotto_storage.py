import json
import os       # 운영체제와 상호작용하는 도구

from .config import DATA_FILE

# 저장된 로또 데이터 불러오기
def load_lotto_data():

    # 저장 파일이 존재하는지 확인
    if not os.path.exists(DATA_FILE):
        return []

    # JSON 파일을 읽기 모드로 열기
    with open(DATA_FILE,"r", encoding="utf-8") as file:

        # JSON 데이터를 파이썬 자료형으로 변환
        lotto_data = json.load(file)

    return lotto_data


# 로또 데이터 저장하기
def save_lotto_data(lotto_data):

    # 저장할 폴더가 없으면 폴더 생성
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    # JSON 파일을 쓰기 모드로 열기
    with open(DATA_FILE, "w", encoding="utf-8") as file:

        # 파이썬 데이터를 JSON 형식으로 저장
        json.dump(lotto_data, file, ensure_ascii=False, indent = 4)


# 마지막으로 저장된 회차 확인
def get_last_saved_round():

    # 저장된 로또 데이터 불러오기
    lotto_data = load_lotto_data()

    # 저장된 데이터가 없다면 0 반환
    if not lotto_data:
        return 0

    # 데이터 중 가장 높은 회차 번호 반환
    last_round = max(item["ltEpsd"] for item in lotto_data)

    return last_round