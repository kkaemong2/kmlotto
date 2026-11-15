
import streamlit as st
import pandas as pd

# 저장된 로또 데이터 불러오기
from lotto_analysis.lotto_storage import load_lotto_data

# 번호별 출현 횟수 계산
from lotto_analysis.lotto_statistics import calculate_number_frequencies

# 번호별 출현 횟수 순위 계산
from lotto_analysis.lotto_statistics import get_frequency_ranking


# 통계 화면 표시 함수
def show_statistics():

    # 화면 제목
    st.header("📊 통계 분석")

    st.write("저장된 역대 당첨번호를 바탕으로 번호별 출현 통계를 확인합니다.")

    # 저장된 로또 데이터 불러오기
    lotto_data = load_lotto_data()

    # 저장된 데이터가 없는 경우
    if not lotto_data:

        st.warning("분석할 로또 데이터가 없습니다.")

        st.write("먼저 데이터 화면에서 로또 데이터를 확인해 주세요.")

        return      # 데이터가 없으면 여기서 함수를 끝낸다 

    # 번호별 출현 횟수 계산
    frequencies = calculate_number_frequencies(lotto_data)

    # 출현 횟수 순위 계산
    ranking = get_frequency_ranking(frequencies)

    # 전체 당첨번호 개수
    total_draws = len(lotto_data)

    # 저장된 데이터의 가장 오래된 회차와 최신 회차
    first_round = min(item["ltEpsd"] for item in lotto_data)
    last_round = max(item["ltEpsd"] for item in lotto_data)

    # 가장 많이 나온 번호
    most_number = ranking[0]        # 위에서 ranking이 (3,190)처럼 튜플 형태라 ranking[0] 이렇게 불러온다

    # 가장 적게 나온 번호
    least_number = ranking[-1]

    st.divider()

    # 통계 요약 제목
    st.subheader("전체 통계")

    # 요약 정보 배치
    col1, col2, col3 = st.columns(3)

    # 분석한 회차 수
    with col1:

        # metric은 숫자나 주요 정보를 강조해서 보여줌
        st.metric(
            label="분석 회차",  # 표시할 정보의 이름
            value=f"{total_draws:,}회"  # 표시할 정보
        )

    # 가장 많이 나온 번호
    with col2:

        st.metric(
            label="최다 출현 번호",
            value=f"{most_number[0]}번",            # 튜플의 번호와 횟수를 나타냄
            delta=f"{most_number[1]}회 출현"    # delta는 주요 숫자와 함께 표현되는 보조 정보로 기능 자체에 자체 기본적인 디자인 포함되어 있음
        )

    # 가장 적게 나온 번호
    with col3:

        st.metric(
            label="최소 출현 번호",
            value=f"{least_number[0]}번",
            delta=f"{least_number[1]}회 출현"
        )

    st.divider()

    # 번호별 출현 횟수 그래프
    st.subheader("번호별 출현 횟수")

    # 1번부터 45번까지 출현 횟수 데이터 생성
    chart_data = pd.DataFrame([
        {
            "번호": number,
            "출현 횟수": frequencies.get(number, 0)     # get(찾을 키, 없을 때 사용할 값)
        }
        for number in range(1, 46)
    ])

    # 출현 횟수 막대그래프 표시
    st.bar_chart(
        chart_data,
        x="번호",
        y="출현 횟수"
    )

    st.caption(f"{first_round}회부터 {last_round}회까지의 당첨번호를 분석한 결과입니다.")

    st.divider()

    # 출현 순위 표시
    st.subheader("출현 순위")

    # 상위 번호와 하위 번호 배치
    col1, col2 = st.columns(2)

    # 가장 많이 나온 번호 TOP 10
    with col1:

        st.markdown("**많이 나온 번호 TOP 10**")

        top_data = pd.DataFrame(
            ranking[:10],                   # ranking의 데이터 앞에서부터 10개 가져옴
            columns=["번호", "출현 횟수"]
        )

        top_data.index = range(1, len(top_data) + 1)    # Pandas는 표를 만들면 기본적으로 행이 0부터라 1부터 (10 + 1) 미만까지 지정해준다

        st.dataframe(
            top_data,
            width="stretch"
        )

    # 가장 적게 나온 번호 TOP 10
    with col2:

        st.markdown("**적게 나온 번호 TOP 10**")

        bottom_data = pd.DataFrame(
            ranking[-10:],
            columns=["번호", "출현 횟수"]
        )

        # 적게 나온 번호부터 표시
        bottom_data = bottom_data.sort_values(
            by="출현 횟수",     # 출현 횟수 열을 기준으로 정렬
            ascending=True      # 작은 값부터 큰 값 순서로 정렬
        )

        bottom_data.index = range(1, len(bottom_data) + 1)

        st.dataframe(
            bottom_data,
            width="stretch"
        )

    st.divider()

    # 전체 번호별 출현 횟수
    st.subheader("전체 번호 통계")

    # 전체 번호 순위 데이터 생성
    all_ranking = pd.DataFrame(
        ranking,
        columns=["번호", "출현 횟수"]
    )

    # 출현 횟수 기준 내림차순 정렬
    all_ranking = all_ranking.sort_values(
        by=["출현 횟수", "번호"],
        ascending=[False, True]     # 출현 횟수는 높은 횟수 부터, 번호가 작은 것 부터
    )

    # 순위 번호 추가 (테이터프레임.insert(위치, 열 이름, 넣을 데이터))
    all_ranking.insert(
        0,
        "순위",
        range(1, len(all_ranking) + 1)
    )

    # 전체 통계 표 표시
    st.dataframe(
        all_ranking,
        width="stretch",
        hide_index=True     # Pandas가 기본적으로 가지고 있는 행 번호를 숨기는 옵션, 우리가 위에서 이미 만들어서 숨김
    )
