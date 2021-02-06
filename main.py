import math
import json
import requests
from bs4 import BeautifulSoup

def levelName(level):
    prefix = ['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond', 'Ruby']
    roman = ['I', 'II', 'III', 'IV', 'V']
    return prefix[math.floor((level - 1) / 5)] + ' '  + roman[4 - (level - 1) % 5]

# json data 만들기
id = input('백준 ID를 입력하세요 : ').strip()
req = requests.get('https://solved.ac/profile/' + id)
soup = BeautifulSoup(req.text, 'html.parser')
jsonData = json.loads(soup.find('script', {'type':'application/json'}).string)['props']['pageProps']

# 현재 정보
print('현재 경험치 :', jsonData['user']['result']['user'][0]['exp'])
print('현재 티어 :', levelName(jsonData['user']['result']['user'][0]['level']), end='\n\n')

# 상위 100개 문제 레이팅 계산
cnt = 0
new_rating = 0
for i in range(30, 0, -1):
    now_cnt = min(100 - cnt, jsonData['solvedStats']['result'][i]['solved'])
    cnt += now_cnt
    new_rating += (now_cnt * i)
print('상위 100 문제 레이팅 :', new_rating)

# 보너스 레이팅 계산
classInfo = jsonData['user']['result']['user'][0]['class']
solvedInfo = jsonData['user']['result']['user'][0]['solved']
voteInfo = jsonData['user']['result']['user'][0]['vote_count']
classRatingInfo = [0, 25, 50, 100, 150, 200, 210, 220, 230, 240, 250]

classRating = classRatingInfo[classInfo]
solvedRating = round(150 * (1 - pow(0.995, solvedInfo)))
voteRating = round(50 * (1 - pow(0.99, voteInfo)))
new_rating += classRating + solvedRating + voteRating

print('클래스 레이팅 :', classRating)
print('푼 문제 레이팅 :', solvedRating)
print('투표 문제 레이팅 :', voteRating)

# 새로운 티어 계산
new_tier_rating = [0, 30, 60, 90, 120, 150,
                   200, 300, 400, 500, 650,
                   800, 950, 1100, 1250, 1400,
                   1600, 1750, 1900, 2000, 2100,
                   2200, 2300, 2400, 2500, 2600,
                   2700, 2800, 2850, 2900, 2950]

new_tier = 30
for i in range(30):
    if new_rating >= new_tier_rating[i] and new_rating < new_tier_rating[i + 1]:
        new_tier = i
        break

print('새로운 레이팅 :', new_rating)
if new_tier:
    print('새로운 티어 :', levelName(new_tier))
else:
    print('새로운 티어 :', 'Unrated')
