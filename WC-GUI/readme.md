# 네이버 검색 결과 크롤링 & 워드클라우드 생성기
===============================================

## 📖 소개
이 프로젝트는 네이버 검색 결과를 크롤링하여 텍스트 데이터를 수집하고, 빈도수 분석 및 워드클라우드를 생성하는 Python 기반 애플리케이션입니다.

## 🚀 주요 기능
- 네이버 검색 결과 크롤링 (키워드 입력)
- 수집한 데이터에서 키워드 빈도수 분석
- 워드클라우드 시각화
- 결과 데이터 저장 (txt파일)

## 🛠 사용 기술
- **언어:** Python
- **GUI 인터페이스:** `tkinter`
- **크롤링:** `requests`, `BeautifulSoup`  
- **데이터 분석:** `numpy` 
- **시각화:** `matplotlib`
- **이미지 처리:** `PIL (Pillow)`
- **워드클라우드:** `wordcloud`, `konlpy`

## 🔧 설치 방법
1. 프로젝트를 클론합니다
   ```
   git clone https://github.com/your-username/repository-name.git
   cd repository-name
2. 필요한 패키지를 설치합니다
    ```
    pip install -r requirements.txt
3. 프로그램을 실행합니다
    ```
    python app.py
    또는
    python3 app.py
