# 최단거리를 이동하며 중간에 노이즈를 섞은 움직임

import pyautogui
import sys
from random import randint, random, choice

# action
action=[[0,-1], # 상
        [0,1],  # 하
        [-1,0], # 좌
        [1,0]]  # 우

action_dict={0:'(상)', 1:'(하)', 2:'(좌)', 3:'(우)'}



if __name__=="__main__":
   # 화면 전체 크기 확인하기
    window_size=pyautogui.size()
    print('화면 크기 :',window_size)

    window_width, window_height=window_size[0],window_size[1]

    # 그리드 설정
    print('Cell 간 간격 : 100')
    n=100
    grid_x=window_width//n
    grid_y=window_height//n
    
    print('그리드의 크기(가로x세로) : ',grid_x,'X',grid_y,'\n')

    # 누적 비용 확인
    rewardMap=[[0 for _ in range(grid_x+1)] for _ in range(grid_y+1)]
    reward=0
    rewardMap[1][1]=reward

    num=1
    while num<=20: # 전체 10번의 학습으로 costMap을 산출
        first=True
        reward=0
        print('■■■■■■ '+str(num)+'번째 학습 ■■■■■■')

        # 첫 마우스 포인터 위치 (10,10) 시작 - pyautogui 는 코너에서의 움직임을 제한함
        mouse_x=100
        mouse_y=100

        print('첫 마우스 시작 포인트 (',mouse_x,',',mouse_y,')')
        pyautogui.moveTo(mouse_x, mouse_y) # 시작점으로의 이동

        grid=[[False for _ in range(grid_x+1)] for _ in range(grid_y+1)] # 방문 체크
        x,y=1,1
        grid[y][x]=True
        

        # 목표 지점 랜덤 설정
        '''
        target_x=randint(0,grid_x)*n
        target_y=randint(0,grid_y)*n
        '''
        target_x=grid_x*n
        target_y=grid_y*n
        print('목표 지점 (',target_x,',',target_y,')')

        distance=((mouse_x-target_x)**2+(mouse_y-target_y)**2)**(1/2)

        #i=1
        while True:
            if grid[target_y//n][target_x//n]:
                print('목표지점에 도착, 누적 비용 : ',reward,'\n')
                break

            if first:
                a=choice([1,3])
                first=False
            else:
                a=randint(0,3) # 상하좌우 움직임

            #print(str(i)+'번째 이동 == ',action_dict[a])

            if 0<=x+action[a][0]<=grid_x and 0<=y+action[a][1] <= grid_y : # Grid 이내의 움직임일 경우
                if not grid[y+action[a][1]][x+action[a][0]]: # 방문한적이 없다면
                    grid[y+action[a][1]][x+action[a][0]]=True

                    # 움직임이 합리적인지 확인 (거리가 줄어드는지)
                    mouse_x+=action[a][0]*n
                    mouse_y+=action[a][1]*n

                    new_distance=((mouse_x-target_x)**2+(mouse_y-target_y)**2)**(1/2)

                    if distance >= new_distance : # 거리가 줄어들었다면 -> 합리적
                        distance=new_distance

                        x+=action[a][0]
                        y+=action[a][1]

                        reward-=1

                        rewardMap[y][x]=min(rewardMap[y][x], reward)

                        pyautogui.moveTo(mouse_x, mouse_y)

                    else: # 거리가 줄어들지 않았다면
                        # 0.1의 확률로 거리가 줄어들지 않았음에도 이동
                        if random()<=0.1:
                            print('＊＊＊＊＊＊＊＊변수 발생＊＊＊＊＊＊＊＊')
                            distance=new_distance # 새로운 거리를 다시 넣어주어야 다시 최단거리를 찾기위해 움직임

                            x+=action[a][0]
                            y+=action[a][1]

                            reward-=1

                            rewardMap[y][x]=min(rewardMap[y][x], reward)

                            pyautogui.moveTo(mouse_x, mouse_y)

                        else:
                            mouse_x-=action[a][0]*n
                            mouse_y-=action[a][1]*n
                else:
                    grid[y+action[a][1]][x+action[a][0]]=False

        num+=1

    for i in range(1,len(rewardMap)):
        print(*rewardMap[i][1:])
    