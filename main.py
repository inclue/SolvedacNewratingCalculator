#-*- coding:utf-8 -*-
import math
import json
import ssl

from urllib import request

def levelName(level):
    if level == 0:
        return 'Unrated'
    if level == 31:
        return 'Master'
    prefix = ['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond', 'Ruby']
    roman = ['I', 'II', 'III', 'IV', 'V']
    return prefix[math.floor((level - 1) / 5)] + ' ' + roman[4 - (level - 1) % 5]

#아이디 입력 받기
id = input('백준 아이디를 입력하세요 : ').strip()

try:
    # json data API로 가져오기
    ssl_context = ssl._create_unverified_context()
    res1 = request.urlopen(
        request.Request('https://api.solved.ac/v2/users/show.json?id=%s' % id), context = ssl_context)
    res2 = request.urlopen(
        request.Request('https://api.solved.ac/v2/users/problem_stats.json?id=%s' % id), context = ssl_context)

    user_info = json.loads(res1.read().decode('UTF-8'))['result']['user'][0]
    problem_stat = json.loads(res2.read().decode('UTF-8'))['result']

    # 현재 정보
    print('현재 경험치 :', "{:,}".format(user_info['exp']))
    print('현재 티어 :', levelName(user_info['level']), end='\n\n')

    # 상위 100개 문제 레이팅 계산
    cnt = 0
    higher_rating = 0
    for i in range(30, 0, -1):
        now_cnt = min(100 - cnt, problem_stat[i]['solved'])
        cnt += now_cnt
        higher_rating += (now_cnt * i)
    print('상위 100 문제 레이팅 :', higher_rating)

    # 보너스 레이팅 계산
    class_info = user_info['class']
    solved_info = user_info['solved']
    vote_count_info = user_info['vote_count']
    
    class_rating_table = [0, 25, 50, 100, 150, 200, 210, 220, 230, 240, 250]
    class_rating = class_rating_table[class_info]
    solved_rating = round(175 * (1 - pow(0.995, solved_info)))
    vote_count_rating = round(25 * (1 - pow(0.9, vote_count_info)))

    print('클래스 레이팅 :', class_rating)
    print('문제 수 레이팅 :', solved_rating)
    print('기여 레이팅 :', vote_count_rating, end='\n\n')

    # 새로운 티어 계산
    new_rating = higher_rating + class_rating + solved_rating + vote_count_rating
    new_tier = 31
    new_tier_table = [0, 30, 60, 90, 120, 150,
                       200, 300, 400, 500, 650,
                       800, 950, 1100, 1250, 1400,
                       1600, 1750, 1900, 2000, 2100,
                       2200, 2300, 2400, 2500, 2600,
                       2700, 2800, 2850, 2900, 2950, 3000]
    for i in range(31):
        if new_tier_table[i] <= new_rating < new_tier_table[i + 1]:
            new_tier = i
            break

    print('새로운 레이팅 :', new_rating)
    print('새로운 티어 :', levelName(new_tier))
except Exception as e:
    print('아이디를 찾을 수 없습니다. 아이디를 다시 한번 확인해주세요.')
    print(e)
