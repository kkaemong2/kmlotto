
import streamlit as st

# 무작위 번호 생성 함수 불러오기
from lotto_analysis.lotto_generator import generate_random_games

# 출현 빈도 기반 번호 생성 함수 불러오기
from lotto_analysis.lotto_generator import generate_frequency_games

# 번호별 출현 횟수 계산 함수 불러오기
from lotto_analysis.lotto_statistics import calculate_number_frequencies

# 저장된 로또 데이터 불러오기 함수
from lotto_analysis.lotto_storage import load_lotto_data


# 추천 화면 표시 함수
def show_recommendation():

    # CSS 디자인 설정 (웹 화면의 디자인을 꾸미기 위해 HTML과 CSS 사용)
    # markdown -> streamlit 화면에 markdown이나 html 내용 표시 기능
    st.markdown("""     
        <style>

        /* 번호 6개를 가로로 배치 */
        /*lotto-number-row는 CSS에서 사용하는 이름선언 (CSS에서 #을 쓰면 다른 기능임)*/

        .lotto-number-row {
            display: flex;
            flex-wrap: nowrap;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
            width: 100%;
            padding: 8px 4px 16px 4px;
            box-sizing: border-box;
        }

        /* 로또 번호 공통 디자인 */
        .lotto-number {
            display: flex;
            flex: 0 0 40px;
            width: 40px;
            height: 40px;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            background-color: #e8f5e9;
            color: #1b5e20;
            font-size: 15px;
            font-weight: bold;
        }

        /* 모바일 화면에서는 번호 크기와 간격 축소 */
        @media (max-width: 480px) {

            .lotto-number-row {
                gap: 4px;
                padding: 8px 0 14px 0;
            }

            .lotto-number {
                flex-basis: 34px;
                width: 34px;
                height: 34px;
                font-size: 13px;
            }
        }

        </style>
    """, unsafe_allow_html=True)    # HTML 태그와 CSS를 화면에 적용하도록 허용하는 설정

    # 화면 제목
    st.header("🎲 번호 추천")

    # 추천 방식 안내
    st.write("원하는 추천 방식을 선택하세요.")

    # 추천 게임 수 설정
    game_count = 5

    # 추천 방식별 화면 배치
    col1, col2 = st.columns(2)

    # 무작위 추천 영역
    with col1:
        with st.container(border=True):

            # 제목
            st.subheader("무작위 추천")

            # 설명
            st.write("1부터 45까지의 번호를 무작위로 추천합니다.")

            # 무작위 추천 버튼 (버튼이 눌렸으면 실행)
            if st.button(
                "무작위 번호 생성",
                key="random_recommendation",
                use_container_width=True
            ):

                # 무작위 번호 5게임 생성
                games = generate_random_games(game_count)

                # 생성한 번호 저장
                st.session_state["recommended_games"] = games

                # 추천 방식 저장
                st.session_state["recommendation_type"] = "무작위 추천"

    # 분석 기반 추천 영역
    with col2:
        with st.container(border=True):

            # 제목
            st.subheader("분석 기반 추천")

            # 설명
            st.write("과거 당첨번호의 출현 빈도를 반영합니다.")

            # 분석 기반 추천 버튼
            if st.button(
                "분석 번호 생성",
                key="frequency_recommendation",
                use_container_width=True
            ):

                try:

                    # 저장된 로또 데이터 불러오기
                    lotto_data = load_lotto_data()

                    # 데이터가 없는 경우 안내
                    if not lotto_data:
                        st.warning("분석할 로또 데이터가 없습니다.")

                    else:   # not의 else -> 로또 데이터가 존재할 때 아래 코드 실행

                        # 번호별 출현 횟수 계산
                        frequencies = calculate_number_frequencies(lotto_data)

                        # 출현 빈도를 반영하여 5게임 생성
                        games = generate_frequency_games(
                            frequencies,
                            game_count
                        )

                        # 생성한 번호 저장
                        st.session_state["recommended_games"] = games

                        # 추천 방식 저장
                        st.session_state["recommendation_type"] = "분석 기반 추천"

                except Exception as error:  # 발생한 오류 내용을 error에 넣는다

                    # 오류 발생 시 안내
                    st.error(f"분석 중 오류가 발생했습니다: {error}")

    # 추천 결과가 저장되어 있는지 확인
    if "recommended_games" in st.session_state:

        # 구분선
        st.divider()

        # 추천 결과 제목
        st.subheader("추천 번호")

        # 추천 방식 표시
        st.write(
            f"추천 방식: {st.session_state['recommendation_type']}"
        )

        # 저장된 추천 번호 가져오기 (이렇게 변수 두개로 옮겨가는 이유는 화면 다시 실행 시 이전 값이 유지되지 않아서)
        games = st.session_state["recommended_games"]

        # 추천 게임을 하나씩 표시 (enumberate는 꺼내면서 몇 번째인지도 알려준다 i에는 번째, game에는 데이터)
        for i, game in enumerate(games):

            # 게임별 카드 생성 (상자 만들기)
            with st.container(border=True):

                # 게임 번호 표시 (0번째 부터라서 + 1)
                st.markdown(f"**{i + 1}게임**")

                # 번호 6개를 HTML로 가로 배치 상자 만들기
                # div 화면에 상자를 만드는 HTML 요소, class 상자에 속성, lotto-number-row 상자 이름 (CSS 찾는다)
                number_html = '<div class="lotto-number-row">'

                # 번호를 하나씩 HTML에 추가
                for number in game:

                    number_html += (
                        f'<div class="lotto-number">{number}</div>'
                    )

                # 번호 표시 영역 닫기 (/div)
                number_html += '</div>'

                """                
                완성된 HTML 코드 확인 -> st.code(number_html, language="html")
                ex) <div class="lotto-number">3</div>       (lotto-number는 CSS에서 공 크기, 색상 정보 )
                """

                # 완성된 번호 표시
                st.markdown(
                    number_html,
                    unsafe_allow_html=True  # True : HTML 태그를 실제 HTML로 해석해서 화면에 표시
                )

        # 다시 추천 버튼
        if st.button(
            "다시 추천하기",
            use_container_width=True
        ):

            # 추천 결과 삭제
            del st.session_state["recommended_games"]

            # 추천 방식 정보 삭제
            del st.session_state["recommendation_type"]

            # 화면 새로고침
            st.rerun()
