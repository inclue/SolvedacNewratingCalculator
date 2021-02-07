import math
import json
from urllib import request

def levelName(level):
    if level == 0:
        return 'Unrated'
    prefix = ['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond', 'Ruby']
    roman = ['I', 'II', 'III', 'IV', 'V']
    return prefix[math.floor((level - 1) / 5)] + ' ' + roman[4 - (level - 1) % 5]

# json data API로 가져오기
id = input('백준 ID를 입력하세요 : ').strip()

res1 = request.urlopen(request.Request('https://api.solved.ac/v2/users/show.json?id=%s' % id))
res2 = request.urlopen(request.Request('https://api.solved.ac/v2/users/problem_stats.json?id=%s' % id))

user_info = json.loads(res1.read().decode('UTF-8'))['result']['user'][0]
problem_stat = json.loads(res2.read().decode('UTF-8'))['result']

# 현재 정보
print('현재 경험치 :', user_info['exp'])
print('현재 티어 :', levelName(user_info['level']), end='\n\n')

# 상위 100개 문제 레이팅 계산
cnt = 0
new_rating = 0
for i in range(30, 0, -1):
    now_cnt = min(100 - cnt, problem_stat[i]['solved'])
    cnt += now_cnt
    new_rating += (now_cnt * i)
print('상위 100 문제 레이팅 :', new_rating)

# 보너스 레이팅 계산
classInfo = user_info['class']
solvedInfo = user_info['solved']
voteInfo = user_info['vote_count']
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
    if new_tier_rating[i] <= new_rating < new_tier_rating[i + 1]:
        new_tier = i
        break

print('새로운 레이팅 :', new_rating)
if new_tier:
    print('새로운 티어 :', levelName(new_tier))
else:
    print('새로운 티어 :', 'Unrated')
