
import streamlit as st


# 설정 화면 표시 함수
def show_settings():

    # 화면 제목
    st.header("⚙️ 환경 설정")

    st.write("kmlotto 의 사용 환경을 설정할 수 있습니다.")

    st.divider()

    # 사용 모드 설정
    st.subheader("사용 모드")

    # 기존에 선택한 모드 불러오기
    if "lotto_mode" not in st.session_state:                # 데이터를 임시로 기억하는 공간에 "lotto_mode"라는 이름으로 사용 모드를 기억 
        st.session_state["lotto_mode"] = "오프라인 모드"    # "lotto_mode" 없으면 오프라인 모드를 기본값 설정

    # 사용 모드 선택
    selected_mode = st.radio(               #radio는 여러 항목 중 하나만 선택할 수 있는 버튼 기능
        "사용할 모드를 선택하세요.",
        ["오프라인 모드", "서버 모드 (연동 준비 중)"], #라이오 버튼 위에 표시할 안내 문구
        index=None,
        key="lotto_mode"
    )


    # 선택한 모드에 따라 안내 표시
    if selected_mode == "오프라인 모드":

        st.success("오프라인 모드를 선택했습니다.")

        st.write("""
        - 무작위 번호 추천 기능을 사용할 수 있습니다.
        - 이미 저장된 로또 데이터를 이용할 수 있습니다.
        - 라즈베리파이 서버 기능은 사용할 수 없습니다.
        """)

    else:

        st.info("서버 모드는 현재 연동 준비 중입니다.")

        st.write("""
        서버 연결이 완료되면 다음 기능을 사용할 수 있도록 만들 예정입니다.

        - 라즈베리파이에 저장된 데이터 조회
        - 새로운 로또 데이터 수집 및 저장
        - 추천 번호 저장
        - 저장한 번호 다시 불러오기
        """)

    st.divider()

    # 프로그램 정보
    st.subheader("프로그램 정보")

    st.write("**프로그램 이름:** kmlotto")
    st.write("**프로그램 버전:** 1.0.0")
    st.write("**개발 환경:** Python / Streamlit")

    st.divider()

    # 안내
    st.caption("kmlotto - 로또 번호 분석 및 추천 프로그램") # 일반 글씨보다 더 작고 은은한 글씨로 보임
