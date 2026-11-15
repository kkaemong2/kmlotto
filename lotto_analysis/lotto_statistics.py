# 번호별 출현 횟수 계산
def calculate_number_frequencies(lotto_data):

    # 번호별 출현 횟수를 저장할 딕셔너리
    frequencies = {}

    # 수집한 회차 데이터를 하나씩 확인
    for item in lotto_data:

        # 당첨번호 6개를 하나씩 확인
        for i in range(1,7):

            # 현재 당첨번호 가져오기
            number = item[f"tm{i}WnNo"]

            # 해당 번호가 처음 등장했다면 0으로 초기화
            if number not in frequencies:
                frequencies[number] = 0

            # 해당 번호의 출현 횟수 1 증가
            frequencies[number] += 1

    return frequencies


# 번호별 출현 횟수 순위 정렬
def get_frequency_ranking(frequencies):

    # 출현 횟수가 높은 순서대로 정렬
    ranking = sorted(
        frequencies.items(),        # 딕셔너리의 번호와 출현 횟수를 한 쌍으로 가져옴
        key=lambda item: item[1],   # 0은 로또번호, 1은 출현횟수 -> 출현횟수 기준으로 정렬
        reverse=True                # True는 큰 숫자부터 작은 숫자, False는 반대
    )

    return ranking