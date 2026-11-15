from .lotto_api import get_lotto_data

# 로또 최신 회차 확인
def get_latest_lotto_round():

    start_round = 1
    end_round = 9999
    latest_round = 0

    while start_round <= end_round:

        middle_round = (start_round + end_round) // 2   # 이진 탐색 방법, // -> 정수 몫 연산자 (나눗셈 후 소수점 이하 버림)

        data = get_lotto_data(middle_round)

        if any(item["ltEpsd"] == middle_round for item in data):    # 서버에서 받은 데이터 안에 내가 요청한 회차가 있는지 확인
            latest_round = middle_round     # 현재 확인한 회차를 최신 회차 후보로 지정
            start_round = middle_round + 1

        else:       # 데이터가 없으면 더 낮은 회차를 탐색하도록 끝값을 내림
            end_round = middle_round - 1

    return latest_round


# 로또 회차 목록 생성
def get_lotto_rounds(start_round, end_round):

    lotto_rounds = []

    for lotto_round in range(start_round, end_round + 1): # range의 범위가 이상-미만이라 +1 반영
        lotto_rounds.append(lotto_round)

    return lotto_rounds


# 당첨번호 수집
def collect_lotto_data(lotto_rounds):

    collected_data = {}

    # 10회차 단위로 서버에 요청
    for i in range(0, len(lotto_rounds), 10):

        # 이번에 요청할 회차
        lotto_round = lotto_rounds[i]

        # 서버에서 주변 10회차 데이터 가져오기
        data = get_lotto_data(lotto_round)

        # 서버에서 받은 데이터를 하나씩 확인
        for item in data:

            # 이미 수집한 회차가 아니라면 저장
            collected_data[item["ltEpsd"]] = item

    # 회차 순서대로 정렬해서 리스트로 반환
    return [collected_data[round_number]
            for round_number in lotto_rounds
            if round_number in collected_data]


"""
# 당첨번호 수집
def collect_lotto_data(lotto_rounds):

    collected_data = []

    for lotto_round in lotto_rounds:
        data = get_lotto_data(lotto_round)

        for item in data:
            if item["ltEpsd"] == lotto_round:
                collected_data.append(item)

                break

    return collected_data
"""