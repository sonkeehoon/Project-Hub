from utils import *
from datetime import datetime
from crawler import (WEATHER, 
                     FINE_DUST, 
                     ULTRAFINE_DUST)

try:
    while True:
        now = datetime.now()
        print()
        print("서울 지역 실시간 날씨, 미세먼지, 초미세먼지 정보를 알려드립니다")
        print("※ 현재 시각:", now.strftime("%Y년 %m월 %d일 %I:%M %p"))
        make_divider(100)
        print("{:<10}| {}".format("날씨", WEATHER))
        make_divider(100)
        print("{:<8}| 현재: {}, 오전: {}, 오후: {}".format("미세먼지", FINE_DUST[1], FINE_DUST[2], FINE_DUST[3]))
        make_divider(100)
        print("{:<7}| 현재: {}, 오전: {}, 오후: {}".format("초미세먼지", ULTRAFINE_DUST[1], ULTRAFINE_DUST[2], ULTRAFINE_DUST[3]))
        make_divider(100)
        print("아무 키나 입력하면 실시간 정보가 업데이트됩니다")
        print("Ctrl + Z를 입력하면 종료됩니다")
        make_divider(100)
        input()
        
except EOFError:
    pass