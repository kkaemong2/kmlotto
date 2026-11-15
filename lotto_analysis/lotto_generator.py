import random

# 무작위 번호 생성
def generate_numbers():

    # 1~45 중 중복 없이 6개 추출
    numbers = random.sample(range(1,46), 6)

    # 번호를 오름차순으로 정렬해서 반환
    return sorted(numbers)


# 무작위 로또 게임 생성
def generate_random_games(game_count):

    # 생성한 게임을 저장할 리스트
    games = []

    # 요청한 게임 수만큼 반복
    for i in range(game_count):

        # 생선한 번호를 게임 목록에 추가
        games.append(generate_numbers())

    return games


# 출현 빈도 기반 번호 생성
def generate_frequency_games(frequencies, game_count):

    # 생성한 게임을 저장할 리스트
    games = []

    # 요청한 게임 수만큼 반복
    for i in range(game_count):

        # 1부터 45까지 번호 준비
        numbers = list(range(1,46))

        # 각 번호의 출현 횟수를 가중치로 설정
        weights = [frequencies.get(number, 0) + 1 for number in numbers]    # 가중치를 계산하고 그 번호를 하나씩 꺼낸다

        # 현재 게임의 번호를 저장할 리스트
        game = []

        # 번호 6개를 선택
        for j in range(6):

            # 출현 빈도를 반영하여 번호 하나 선택
            selected_number = random.choices(numbers, weights=weights, k=1)[0] # 뒤의 [0]은 뽑은 리스트를 숫자만 나오게 한다

            # 선택한 번호를 게임에 추가
            game.append(selected_number)

            # 이미 선택한 번호는 후보 목록에서 제거
            selected_index = numbers.index(selected_number)
            numbers.pop(selected_index)
            weights.pop(selected_index)

        # 번호를 오름차순으로 정렬
        game.sort()

        # 완성된 게임을 전체 게임 목록에 추가
        games.append(game)

    return games
