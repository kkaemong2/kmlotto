
import streamlit as st      # streamlit 웹사이트를 만들 때 사용하는 라이브러리


# 메뉴 이동 함수
def go_to_menu(menu_name):

    # 선택한 메뉴를 세션에 저장
    st.session_state["selected_menu"] = menu_name   # 임시공간에 key, value 값으로 임시 저장


# 홈 화면 표시 함수
def show_home():

    # 홈 화면 제목
    st.header("🏠 홈")

    # 주요 기능 안내 (일반적인 내용 작성)
    st.write("kmlotto")

    # 화면에 구분선 표시
    st.divider()

    # 홈 화면을 세 개의 세로 공간으로 나눔(1열, 2열, 3열)
    col1, col2, col3 = st.columns(3)

    # 번호 추천 카드
    with col1:
        with st.container(border=True):     # 하나의 영역(container)으로 묶어 테두리(border)를 표시하라

            # 테두리 안에 표시됨

            st.subheader("🎲 번호 추천")            # subheader 중간 제목

            st.write("무작위 및 분석 기반 추천")     # 일반 내용

            # 화면에 버튼을 만드는 기능
            st.button(
                "추천 화면으로 이동",            # 버튼에 표시할 글자
                key="home_recommendation",      # 버튼을 구분하기 위한 key 이름
                use_container_width=True,       # width="stretch" 방식과 같음, 버튼 영역의 너비를 가득 채움
                on_click=go_to_menu,            # 클릭했을 때 실행할 함수
                args=("추천",)                  # args는 함수에 전달할 추가적인 인자로  go_to_menu("추천") 이런식으로 반영됨
                                                 
            )

    # 데이터 조회 카드
    with col2:
        with st.container(border=True):

            st.subheader("📂 데이터 조회")

            st.write("당첨번호 및 저장 게임")

            # 데이터 화면으로 이동하는 버튼
            st.button(
                "데이터 화면으로 이동",
                key="home_data",
                use_container_width=True,
                on_click=go_to_menu,
                args=("데이터",)
            )

    # 통계 분석 카드
    with col3:
        with st.container(border=True):

            st.subheader("📊 통계 분석")

            st.write("번호별 출현 통계")

            # 통계 화면으로 이동하는 버튼
            st.button(
                "통계 화면으로 이동",
                key="home_statistics",
                use_container_width=True,
                on_click=go_to_menu,
                args=("통계",)
            )
