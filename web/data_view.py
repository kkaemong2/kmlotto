
import streamlit as st
import pandas as pd     # 데이터를 저장하고 표 형태로 다루는 라이브러리

# 저장된 로또 데이터 불러오기
from lotto_analysis.lotto_storage import load_lotto_data

# 마지막으로 저장된 회차 확인
from lotto_analysis.lotto_storage import get_last_saved_round


# 데이터 화면 표시 함수
def show_data_view():

    # 화면 제목
    st.header("📂 데이터 조회")

    # 저장된 로또 데이터 불러오기
    lotto_data = load_lotto_data()

    # 마지막 저장 회차 확인
    latest_round = get_last_saved_round()

    # 저장된 데이터가 없는 경우
    if not lotto_data:
        st.warning("저장된 로또 데이터가 없습니다.")
        st.write("먼저 로또 데이터를 수집해야 합니다.")
        return      # 현재 실행중인 함수를 종료한다는 뜻 (아무것도 없는데 무언가 만들면 문제)

    # 저장된 데이터 개수 확인
    total_count = len(lotto_data)

    # 데이터 요약 영역
    st.subheader("데이터 현황")

    # 요약 정보 3개 배치
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("전체 회차", f"{total_count:,}회")    # :, 숫자 천 단위 쉼표

    with col2:
        st.metric("최신 회차", f"{latest_round:,}회")

    with col3:
        oldest_round = min(item["ltEpsd"] for item in lotto_data)
        st.metric("최초 회차", f"{oldest_round:,}회")

    # 구분선
    st.divider()

    # 하나의 화면 안에서 탭 만들기 (2개)
    tab1, tab2 = st.tabs(["당첨번호 조회", "전체 데이터"])

    # 당첨번호 조회 화면
    with tab1:

        # 탭 안에 소제목
        st.subheader("회차별 당첨번호 조회")

        # 조회할 회차 입력받기
        search_round = st.number_input(
            "조회할 회차를 입력하세요.",
            min_value=1,                    # 입력할 수 있는 최소
            max_value=max(1, latest_round), # 입력할 수 있는 최대
            value=max(1, latest_round),     # 처음 입력창에 표시할 기본 숫자 (max는 가장 큰 값 반환)
            step=1                          # 숫자 변경 시 증감 단위
        )

        # 조회 버튼
        if st.button("당첨번호 조회", width="stretch"):     # width="stretch" : 버튼이 사용할 수 있는 영역의 너비에 맞춰 표시

            # 입력한 회차와 일치하는 데이터 찾기
            found_data = next(   # next는 반복 가능한 데이터에서 값을 가져오는 역할
                (
                    item for item in lotto_data
                    if item["ltEpsd"] == search_round
                ),
                None            # 가져올 데이터가 없으면 none 반환
            )

            # 조회 결과 저장
            st.session_state["searched_lotto"] = found_data

        # 이전에 조회한 결과가 있는지 확인 (session_state 안에 "searched_lotto"라는 저장 항목이 만들어져 있는지 확인)
        if "searched_lotto" in st.session_state:

            # 조회 결과 가져오기
            found_data = st.session_state["searched_lotto"]

            if found_data is None:
                st.error("해당 회차의 저장된 데이터가 없습니다.")

            else:

                # 조회한 회차 표시
                st.subheader(f"{found_data['ltEpsd']}회 당첨번호")

                # 당첨번호 6개 가져오기 ( 반복되어 각각의 6개를 하나의 리스트까지 만든다)
                winning_numbers = [
                    found_data[f"tm{i}WnNo"]
                    for i in range(1, 7)
                ]

                # 번호 6개를 표시할 HTML 영역 만들기
                number_html = """
                <div style="
                    display: flex;              /* 내부 요소를 유연 배치 */
                    flex-direction: row;        /* 가로 방향 */
                    flex-wrap: nowrap;          /* 공간 부족 시 다음 줄로 넘어가지 않음*/
                    gap: 8px;                   /* 번호 사이 간격 8px */
                    align-items: center;        /* 세로 방향 가운데 정렬 */
                    overflow-x: auto;           /* 가로 부족하면 좌우 스크롤 허용 */
                    padding: 12px 2px 16px 2px; /* 영역 안 여백 설정 */
                ">
                """

                # 번호를 하나씩 HTML에 추가
                for number in winning_numbers:
                    number_html += f"""
                    <div style="
                        flex: 0 0 38px;
                        width: 38px;
                        height: 38px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        border-radius: 50%;
                        background-color: #e8f5e9;
                        color: #1b5e20;
                        font-size: 14px;
                        font-weight: bold;
                    ">
                        {number}
                    </div>
                    """

                # HTML 영역 종료
                number_html += "</div>"

                # HTML을 화면에 표시
                st.html(number_html)

                # 보너스 번호 표시
                st.markdown(
                    f"**보너스 번호: {found_data['bnsWnNo']}**"
                )

                # 추첨 날짜 표시
                st.write(
                    f"추첨일: {found_data.get('ltRflYmd', '정보 없음')}"    # 혹시 해당 항목이 없으면 '정보 없음'을 반환하여 오류 예방
                )

    # 전체 데이터 화면
    with tab2:

        # 제목
        st.subheader("저장된 전체 당첨번호")

        # 회차별 데이터 정렬
        sorted_data = sorted(
            lotto_data,
            key=lambda item: item["ltEpsd"],    # 정렬 기준 설정 
            reverse=True                        # True = 큰 회차부터 작은 회차, False = 작은 회차부터 큰 회차
        )
        # 표에 표시할 데이터 준비
        table_data = []

        for item in sorted_data:

            # 당첨번호 6개 가져오기
            numbers = [
                item[f"tm{i}WnNo"]
                for i in range(1, 7)
            ]

            # 표에 추가할 데이터 (맨 왼쪽의 문자열은 표의 열 제목이 됨)
            table_data.append({                             # 리스트에 새로운 데이터 추가
                "회차": item["ltEpsd"],
                "추첨일": item.get("ltRflYmd", ""),
                "당첨번호": ", ".join(map(str, numbers)),   # 숫자를 문자열로 바꾸고 join문자열 연결 기능 사용
                "보너스": item["bnsWnNo"]
            })

        # 데이터프레임 생성
        df = pd.DataFrame(table_data)

        # 데이터 표 표시
        st.dataframe(
            df,                 # 표시할 데이터
            width="stretch",    # 화면의 너비에 맞게 조정
            hide_index=True     # 왼쪽의 행 번호 표시하지 않음
        )

        # 데이터 개수 표시
        st.caption(             # 일반 글자보다 작고 보조적인 설명할때 사용
            f"총 {total_count:,}개 회차의 데이터가 저장되어 있습니다."
        )
