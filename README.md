# kmlotto 실행
-pip install -r requirements.txt
-python -m streamlit run app.py

## app.py
- Streamlit 웹 애플리케이션 실행
- 웹사이트 제목 및 메뉴 구성
- 각 화면 파일 연결 및 실행
- 사용자 화면 이동 관리

## README.md
- 프로젝트 소개 및 기본 안내

## 1. lotto_analysis
로또 관련 파이썬 코드와 데이터를 관리하는 폴더

### main.py
- 프로그램 실행 및 전체 흐름 관리

### config.py
- BASE_URL : 동행복권 API 기본 주소 <br>
- HEADERS : 서버 요청 헤더 <br>
- DATA_FILE : 데이터 저장 경로 

### lotto_api.py 
- get_lotto_data() : 특정 회차 당첨번호 데이터 요청

### lotto_collector.py
- get_latest_lotto_round() : 최신 회차 확인 <br>
- get_lotto_rounds() : 지정한 범위의 회차 목록 생성 <br>
- collect_lotto_data() : 신규 당첨번호 수집 

### lotto_storage.py
- load_lotto_data() : 저장된 데이터 불러오기 <br>
- save_lotto_data() : 데이터 저장 <br>
- get_last_saved_round() : 마지막 저장 회차 확인 

### lotto_statistics.py
- calculate_number_frequencies() : 번호별 출현 횟수 계산 <br>
- get_frequency_ranking() : 출현 횟수 순위 정렬

### lotto_generator.py
- generate_numbers() : 무작위 번호 생성 <br>
- generate_random_games() : 무작위 로또 게임 생성
- generate_frequency_games() : 출현 빈도 기반 번호 생성


## 2. web
웹 화면 및 사용자 인터페이스를 관리하는 폴더

### home.py
- 웹사이트 메인 화면 구성

### recommendation.py
- 무작위 번호 추천 화면
- 분석 기반 번호 추천 화면

### data_view.py
- 전체 당첨번호 목록 조회
- 저장한 게임 목록 조회
- 회차별 당첨번호 조회

### statistics.py
- 번호별 출현 통계 화면
- 출현 빈도 순위 화면
- 통계 분석 결과 표시

### settings.py
- 환경 설정 화면
- 서버 연결 상태 확인
- 온라인 / 오프라인 모드 설정

### community.py
- 게시판 화면 구성
- 게시글 작성 및 조회
- 댓글 작성 및 조회
