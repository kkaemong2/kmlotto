
import streamlit as st

# 로또 데이터 자동 갱신에 필요한 함수 불러오기
from lotto_analysis.lotto_collector import (
    get_latest_lotto_round,
    get_lotto_rounds,
    collect_lotto_data
)

from lotto_analysis.lotto_storage import (
    load_lotto_data,
    save_lotto_data,
    get_last_saved_round
)

# 홈 화면 함수 불러오기
from web.home import show_home

# 추천 화면 함수 불러오기
from web.recommendation import show_recommendation

# 데이터 화면 함수 불러오기
from web.data_view import show_data_view

# 통계 화면 함수 불러오기
from web.statistics import show_statistics

# 설정 화면 함수 불러오기
from web.settings import show_settings

# 게시판 화면 함수 불러오기
from web.community import show_community


# 웹사이트 기본 설정 (이 설정은 파일에서 Streamlit 명령 중 가장 먼저 실행되어야 함)
st.set_page_config(
    page_title="kmlotto",      # 페이지 이름
    layout="wide"               # 화면 너비 넓게
)

# 로또 데이터 자동 갱신 함수
def update_lotto_data():

    # 동행복권 서버에서 최신 회차 확인
    latest_round = get_latest_lotto_round()

    # 현재 저장된 마지막 회차 확인
    last_round = get_last_saved_round()

    # 최신 회차 확인에 실패한 경우
    if latest_round <= 0:
        raise ValueError("최신 회차를 확인하지 못했습니다.")

    # 이미 최신 데이터가 저장되어 있는 경우
    if latest_round <= last_round:
        return f"현재 최신 데이터는 {latest_round}회 입니다. "

    # 새롭게 수집해야 하는 회차 목록 생성
    lotto_rounds = get_lotto_rounds(
        last_round + 1,
        latest_round
    )

    # 누락된 회차 데이터 수집
    new_data = collect_lotto_data(lotto_rounds)

    # 새로운 데이터가 없는 경우
    if not new_data:
        raise ValueError("새로운 로또 데이터를 수집하지 못했습니다.")

    # 기존 데이터 불러오기
    existing_data = load_lotto_data()

    # 기존 데이터를 회차 번호를 기준으로 딕셔너리로 변환
    combined_data = {
        item["ltEpsd"]: item
        for item in existing_data
    }

    # 새로 수집한 데이터를 기존 데이터에 추가
    for item in new_data:
        combined_data[item["ltEpsd"]] = item

    # 회차 순서대로 정렬
    updated_data = [
        combined_data[round_number]
        for round_number in sorted(combined_data)
    ]

    # 합쳐진 전체 데이터를 JSON 파일에 저장
    save_lotto_data(updated_data)

    # 실제 저장된 마지막 회차 확인
    updated_last_round = max(
        item["ltEpsd"] for item in updated_data
    )

    # 최신 회차까지 모두 수집했는지 확인
    if updated_last_round < latest_round:
        return (
            f"일부 데이터만 갱신되었습니다. "
            f"현재 저장된 마지막 회차: {updated_last_round}회"
        )

    return (
        f"데이터 갱신 완료! "
        f"최신회차가 {last_round}회에서 {updated_last_round}회로 변경되었습니다."
    )


# 앱 세션에서 최초 한 번만 자동 갱신 실행
if "data_update_checked" not in st.session_state:

    # 중복 실행 방지를 위해 먼저 실행 여부 기록
    st.session_state["data_update_checked"] = True

    try:
        # 자동 갱신 실행
        update_message = update_lotto_data()

        # 갱신 결과 저장
        st.session_state["data_update_status"] = "success"
        st.session_state["data_update_message"] = update_message

    except Exception as e:

        # 오류가 발생한 상태 기록
        st.session_state["data_update_status"] = "error"

        # 실제 오류 내용도 함께 저장
        st.session_state["data_update_message"] = (
            f"최신 데이터 확인에 실패했습니다.\n\n"
            f"오류 내용: {type(e).__name__}: {e}\n\n"
            f"기존에 저장된 데이터로 화면을 표시합니다."
    )

        # 로그에도 오류 내용 출력
        print(f"로또 데이터 자동 갱신 오류: {type(e).__name__}: {e}")

# 웹사이트 디자인 설정  (CSS코드로 화면 모양을 조절)
st.markdown("""
    <style>

    /* PC 화면 여백 */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* PC 왼쪽 메뉴 버튼 */
    section[data-testid="stSidebar"] .stButton button {
        width: 100%;
        min-height: 48px;
        border-radius: 10px;
        text-align: left;
        font-weight: 600;
    }

    /* PC 메뉴 간격 */
    section[data-testid="stSidebar"] .stButton {
        margin-bottom: 7px;
    }

    /* 모바일 메뉴 숨기기 */
    .st-key-mobile_nav {
        display: none;
    }

    /* 모바일 화면 디자인 */
    @media (max-width: 768px) {

        /* 왼쪽 사이드바 숨기기 */
        section[data-testid="stSidebar"] {
            display: none;
        }

        /* 사이드바 열기 버튼 숨기기 */
        button[data-testid="stSidebarCollapsedControl"] {
            display: none !important;
        }

        /* 모바일 화면 여백 */
        .block-container {
            padding-top: 2rem;
            padding-left: 1rem;
            padding-right: 1rem;
            padding-bottom: 1rem;
        }

        /* 모바일 메뉴 표시 */
        .st-key-mobile_nav {
            display: block;
        }

        /* 모바일 메뉴 버튼 */
        .st-key-mobile_nav .stButton button {
            width: 100%;
            height: 100px;
            min-height: 100px;
            border-radius: 14px;
            font-size: 15px;
            font-weight: 600;
            white-space: normal;
            padding: 0.5rem;
        }

        /* 모바일 메뉴 가로 간격 */
        .st-key-mobile_nav [data-testid="stHorizontalBlock"] {
            gap: 0.8rem;
        }

        /* 모바일 메뉴 열 너비 */
        .st-key-mobile_nav [data-testid="column"] {
            min-width: 0;
        }

        /* 모바일 제목 크기 */
        h1 {
            font-size: 1.8rem !important;
        }
    }

    </style>
""", unsafe_allow_html=True)


# 웹사이트 제목
st.title("kmlotto")

# 화면 구분선
st.divider()

# 자동 갱신 결과 표시
if st.session_state.get("data_update_status") == "success":

    st.success(st.session_state["data_update_message"])

elif st.session_state.get("data_update_status") == "error":

    st.warning(st.session_state["data_update_message"])

# 메뉴 목록 (왼쪽은 메뉴 버튼에 표시할 이름, 오른쪽은 프로그램 내부에서 사용할 이름)
menu_list = {
    "🏠\n홈": "홈",
    "🎲\n추천": "추천",
    "📂\n데이터": "데이터",
    "📊\n통계": "통계",
    "⚙️\n설정": "설정",
    "💬\n게시판": "게시판"
}   # \n은 줄바꿈이지만 나중에 replace로 공백으로 바꿈


# 최초 실행 시 기본 메뉴 설정
if "selected_menu" not in st.session_state:
    st.session_state["selected_menu"] = "홈"


# 메뉴 선택 함수
def select_menu(menu_value):

    # 선택한 메뉴 저장
    st.session_state["selected_menu"] = menu_value


# 현재 선택된 메뉴 확인
selected_menu = st.session_state["selected_menu"]


# PC 왼쪽 메뉴 생성
for menu_name, menu_value in menu_list.items():

    # 현재 선택된 메뉴인지 확인
    is_selected = selected_menu == menu_value

    # PC 메뉴 버튼 생성
    st.sidebar.button(
        menu_name.replace("\n", " "),   # 줄바꿈을 공백기능으로 바꿈
        key=f"menu_{menu_value}",
        use_container_width=True,
        type="primary" if is_selected else "secondary",
        on_click=select_menu,
        args=(menu_value,)
    )


# 모바일 정사각형 메뉴 생성
with st.container(key="mobile_nav"):

    # 메뉴 목록을 리스트로 변환
    menu_items = list(menu_list.items())

    # 첫 번째 메뉴 줄
    col1, col2, col3 = st.columns(3)

    # 첫 번째 줄 메뉴 버튼
    for col, (menu_name, menu_value) in zip(
        [col1, col2, col3],
        menu_items[:3]
    ):

        with col:

            # 현재 선택된 메뉴인지 확인
            is_selected = selected_menu == menu_value

            # 모바일 메뉴 버튼 생성
            st.button(
                menu_name,
                key=f"mobile_menu_{menu_value}",
                use_container_width=True,
                type="primary" if is_selected else "secondary",
                on_click=select_menu,
                args=(menu_value,)
            )

    # 두 번째 메뉴 줄 위쪽에 여백 추가
    st.markdown(
        "<div style='height: 30px;'></div>",
        unsafe_allow_html=True
    )

    # 두 번째 메뉴 줄
    col4, col5, col6 = st.columns(3)

    # 두 번째 줄 메뉴 버튼
    for col, (menu_name, menu_value) in zip(
        [col4, col5, col6],
        menu_items[3:]
    ):

        with col:

            # 현재 선택된 메뉴인지 확인
            is_selected = selected_menu == menu_value

            # 모바일 메뉴 버튼 생성
            st.button(
                menu_name,
                key=f"mobile_menu_{menu_value}",
                use_container_width=True,
                type="primary" if is_selected else "secondary",
                on_click=select_menu,
                args=(menu_value,)
            )


# 현재 선택된 메뉴에 따라 화면 표시
selected_menu = st.session_state["selected_menu"]

if selected_menu == "홈":
    show_home()

elif selected_menu == "추천":
    show_recommendation()

elif selected_menu == "데이터":
    show_data_view()

elif selected_menu == "통계":
    show_statistics()

elif selected_menu == "설정":
    show_settings()

elif selected_menu == "게시판":
    show_community()


# 실행 -> python -m streamlit run app.py
