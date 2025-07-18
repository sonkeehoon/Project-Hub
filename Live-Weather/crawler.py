import requests
from bs4 import BeautifulSoup


# 날씨
weather_url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%84%9C%EC%9A%B8%EB%82%A0%EC%94%A8'
weather = requests.get(weather_url)

if weather.status_code == 200:
    
    html = weather.text
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.select_one(".temperature_text > strong")
    temperature = temp.get_text()[5:]
    weather_info = soup.select_one(".summary > .weather.before_slash")
    WEATHER = f"{temperature} ({weather_info.get_text().rstrip()})"
    WEATHER = WEATHER.replace("  ", ", ")
    
# 미세먼지
fine_dust_url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EB%AF%B8%EC%84%B8%EB%A8%BC%EC%A7%80"
fine_dust = requests.get(fine_dust_url)

if fine_dust.status_code == 200:
    
    html = fine_dust.text
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.select_one(".tb_scroll > table > tbody > tr:nth-child(1)")
    FINE_DUST: list = temp.get_text().strip().split()

# 초미세먼지
ultrafine_dust_url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%B4%88%EB%AF%B8%EC%84%B8%EB%A8%BC%EC%A7%80"
ultrafine_dust = requests.get(ultrafine_dust_url)

if ultrafine_dust.status_code == 200:
    
    html = ultrafine_dust.text
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.select_one(".tb_scroll > table > tbody > tr:nth-child(1)")
    ULTRAFINE_DUST: list = temp.get_text().strip().split()
    if __name__ == "__main__":
        print(ULTRAFINE_DUST)

