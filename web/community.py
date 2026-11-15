
import streamlit as st
from datetime import datetime       # 날짜, 시간 관련 기능을 불러옴


# 게시판 화면 표시 함수
def show_community():

    # 화면 제목
    st.header("💬 게시판")

    st.write("로또 추천 번호와 분석 결과를 자유롭게 공유해 보세요.")

    # 게시글 저장 공간 초기화
    if "community_posts" not in st.session_state:
        st.session_state["community_posts"] = []

    # 게시글 작성 영역
    with st.expander("✏️ 새 게시글 작성", expanded=False):  # 접었다 펼 수 있는 영역을 만든다. 펼치는 영역의 제목, False = 처음에는 접힌 상태

        # 게시글 작성 폼
        with st.form("community_post_form", clear_on_submit=True):  # form 여러 입력 항목을 하나의 제출 단위로 묶음
                                                                    # 이름을 community_post_form, True = 제출하면 입력창 비움
            
            # 작성자 입력
            author = st.text_input(     # 한 줄 짜리 입력창 생성
                "작성자",
                placeholder="작성자 이름"   # 입력하기 전 회색으로 표시되는 문구
            )

            # 제목 입력
            title = st.text_input(
                "제목",
                placeholder="게시글 제목을 입력하세요."
            )

            # 내용 입력
            content = st.text_area(     # 여러 줄의 입력창
                "내용",
                placeholder="게시글 내용을 입력하세요.",
                height=150              # 입력창의 높이는 150픽셀
            )

            # 게시글 등록 버튼
            submitted = st.form_submit_button(      # 폼을 제출하는 버튼
                "게시글 등록",                      # 버튼에 표시할 글자
                width="stretch"                     # 버튼을 사용할 수 있는 가로 공간에 맞춰 늘려 줌
            )

            # 등록 버튼을 눌렀을 때
            if submitted:

                # 필수 입력 확인
                if not author.strip() or not title.strip() or not content.strip():  # strip = 문자열 앞뒤 공백은 제거, 
                                                                                    # not -> 입력이 비어있거나 공백이면 참이되어 실행됨
                    st.warning("작성자, 제목, 내용을 모두 입력해 주세요.")              # warning은 노란 경고창으로 나옴

                else:

                    # 새로운 게시글 생성
                    new_post = {
                        "id": len(st.session_state["community_posts"]) + 1,         # 게시글 번호, 개수를 세고 + 1을 해서 신규작성
                        "author": author.strip(),                                   # 작성자
                        "title": title.strip(),                                     # 제목
                        "content": content.strip(),                                 # 내용
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),          # 작성 날짜
                        "comments": []                                              # 댓글 목록
                    }

                    # 게시글 목록에 추가
                    st.session_state["community_posts"].append(new_post)

                    # 화면 새로고침
                    st.rerun()

    st.divider()

    # 게시글 목록 제목
    st.subheader("게시글 목록")

    # 저장된 게시글 가져오기
    posts = st.session_state["community_posts"]

    # 게시글이 없는 경우
    if not posts:

        st.info("아직 등록된 게시글이 없습니다.")

    else:

        # 최신 게시글부터 표시
        for post in reversed(posts):        # reversed는 역순으로 읽는 기능이라 최신부터 표시

            with st.container(border=True): # 게시글 하나를 컨테이너영역 감싸기

                # 게시글 제목
                st.markdown(f"**{post['title']}**")

                # 작성자와 작성 날짜
                st.caption(
                    f"작성자: {post['author']} | {post['date']}"
                )

                # 게시글 내용
                st.write(post["content"])

                # 댓글 개수
                st.caption(
                    f"댓글 {len(post['comments'])}개"
                )

    # 게시글이 존재하는 경우 댓글 기능 표시
    if posts:

        st.divider()

        st.subheader("댓글 작성")

        # 게시글 선택 목록 생성
        post_options = {
            f"{post['id']}번 | {post['title']}": post["id"] # 사용자는 제목을 보고 선택하지만 프로그램은 게시글 번호로 탐색
            for post in posts
        }

        # 댓글을 작성할 게시글 선택
        selected_title = st.selectbox(          # 여러 항목중 선택하는 드롭다운 메뉴
            "댓글을 작성할 게시글을 선택하세요.",
            list(post_options.keys())
        )

        # 선택한 게시글 번호
        selected_id = post_options[selected_title]

        # 선택한 게시글 찾기
        selected_post = next(
            post for post in posts
            if post["id"] == selected_id
        )

        # 댓글 작성 폼
        with st.form("community_comment_form", clear_on_submit=True):

            # 댓글 작성자
            comment_author = st.text_input(
                "작성자",
                placeholder="작성자 이름"
            )

            # 댓글 내용
            comment_content = st.text_input(
                "댓글 내용",
                placeholder="댓글을 입력하세요."
            )

            # 댓글 등록 버튼
            comment_submitted = st.form_submit_button(
                "댓글 등록",
                width="stretch"
            )

            # 댓글 등록 처리
            if comment_submitted:

                # 입력값 확인
                if not comment_author.strip() or not comment_content.strip():

                    st.warning("작성자와 댓글 내용을 입력해 주세요.")

                else:

                    # 댓글 데이터 생성
                    new_comment = {
                        "author": comment_author.strip(),
                        "content": comment_content.strip(),
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }

                    # 선택한 게시글에 댓글 추가
                    selected_post["comments"].append(new_comment)

                    # 화면 새로고침
                    st.rerun()

        # 선택한 게시글의 댓글 목록
        st.subheader("댓글 목록")

        if selected_post["comments"]:

            for comment in selected_post["comments"]:

                with st.container(border=True):

                    st.write(comment["content"])

                    st.caption(
                        f"{comment['author']} | {comment['date']}"
                    )

        else:

            st.info("아직 댓글이 없습니다.")
