# 데이터 불러오기 및 저장 관련 함수
from .lotto_storage import load_lotto_data
from .lotto_storage import save_lotto_data
from .lotto_storage import get_last_saved_round

# 로또 데이터 수집 관련 함수
from .lotto_collector import get_latest_lotto_round
from .lotto_collector import get_lotto_rounds
from .lotto_collector import collect_lotto_data

# 로또 통계 분석 관련 함수
from .lotto_statistics import calculate_number_frequencies
from .lotto_statistics import get_frequency_ranking

# 로또 번호 생성 관련 함수
from .lotto_generator import generate_random_games
from .lotto_generator import generate_frequency_games

# 프로그램 실행
def main():

    # 기존에 저장된 로또 데이터 불러오기
    lotto_data = load_lotto_data()

    # 마지막으로 저장된 회차 확인
    last_saved_round = get_last_saved_round()

    print(f"마지막 저장 회차: {last_saved_round}")

    # 동행복권 서버에서 최신 회차 확인
    latest_round = get_latest_lotto_round()

    print(f"현재 최신 회차: {latest_round}")

    # 새롭게 수집해야 할 회차 목록 생성
    new_rounds = get_lotto_rounds(
        last_saved_round + 1,
        latest_round
    )

    # 새로운 당첨번호 데이터 수집
    new_data = collect_lotto_data(new_rounds)

    # 새로 수집한 데이터가 있다면 기존 데이터에 추가
    if new_data:
        lotto_data.extend(new_data)

        # 전체 로또 데이터 저장
        save_lotto_data(lotto_data)

        print(f"새로 수집한 회차 수: {len(new_data)}")

    else:
        print("새로운 당첨번호가 없습니다.")

    # 저장된 로또 데이터가 있는지 확인
    if not lotto_data:
        print("분석할 로또 데이터가 없습니다.")
        return

    # 번호별 출현 횟수 계산
    frequencies = calculate_number_frequencies(lotto_data)

    # 출현 횟수가 높은 순서대로 정렬
    ranking = get_frequency_ranking(frequencies)

    print("\n===== 번호별 출현 순위 TOP 10 =====")

    # 상위 10개 번호 출력
    for number, count in ranking[:10]:
        print(f"{number}번: {count}회")

    # 무작위 로또 5게임 생성
    random_games = generate_random_games(5)

    print("\n===== 무작위 번호 생성 =====")

    # 무작위 번호 출력
    for i in range(len(random_games)):
        print(f"{i + 1}게임: {random_games[i]}")

    # 출현 빈도 기반 로또 5게임 생성
    frequency_games = generate_frequency_games(frequencies, 5)

    print("\n===== 출현 빈도 기반 번호 생성 =====")

    # 출현 빈도 기반 번호 출력
    for i in range(len(frequency_games)):
        print(f"{i + 1}게임: {frequency_games[i]}")


# 이 파일을 직접 실행했을 때만 main() 실행
if __name__ == "__main__":
    main()
