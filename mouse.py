import pyautogui
import sys
from random import randint

if __name__=="__main__":
   # 화면 전체 크기 확인하기
    window_size=pyautogui.size()
    print('화면 크기 :',window_size,'\n')

    window_width, window_height=window_size[0],window_size[1]

    # 그리드 설정
    print('■■■■ Cell 간 간격을 입력하세요 ■■■■')
    n=int(sys.stdin.readline())
    grid_x=window_width//n
    grid_y=window_height//n
    
    print('그리드의 크기(가로x세로) : ',grid_x,'X',grid_y)

    # 방문 체크
    grid=[[False for _ in range(window_width+1)] for _ in range(window_height+1)]

    # 첫 마우스 포인터 위치 랜덤 배치
    mouse_x=randint(0,grid_x)*n
    mouse_y=randint(0,grid_y)*n

    pyautogui.moveTo(mouse_x, mouse_y)
    grid[mouse_y][mouse_x]=True
    print('첫 마우스 시작 포인트 (',mouse_x,',',mouse_y,')')

    # 목표 지점 랜덤 설정
    target_x=randint(0,grid_x)*n
    target_y=randint(0,grid_y)*n
    print('목표 지점 (',target_x,',',target_y,')')

    # action
    action=[[n,0], # 좌
            [-n,0], # 우
            [0,n], # 하
            [0,-n]] # 상

    moved=1
    reward=0
    distance=((mouse_x-target_x)**2+(mouse_y-target_y)**2)**(1/2)

    i=1
    while True:
        if grid[target_y][target_x]:
            print('목표지점에 도착')
            print('누적 보상 : ',reward)
            sys.exit(0)

        if moved==4:
            print('더이상 움직일 수 없습니다')
            print('누적 보상 : ',reward)
            break

        a=randint(0,3)

        print('[',str(i),'] - ',str(moved),'번째 시도')
        moved+=1

        if 0<=mouse_x+action[a][0]<=window_width and 0<=mouse_y+action[a][1]<=window_height:
            if not grid[mouse_y+action[a][1]][mouse_x+action[a][0]]:
                mouse_x+=action[a][0]
                mouse_y+=action[a][1]
                grid[mouse_y][mouse_x]=True

                pyautogui.moveTo(mouse_x,mouse_y,1)
                #pyautogui.dragTo(mouse_x,mouse_y,1,button='left')
                #pyautogui.hotkey('ctrl','c')
                moved=1

                new_distance=((mouse_x-target_x)**2+(mouse_y-target_y)**2)**(1/2)

                if distance < new_distance : # 멀어졌다면
                    reward-=1
                else: # 가까워졌다면
                    reward+=1

                distance = new_distance

                print('=========================>>>',mouse_x,',',mouse_y,'이동, 보상 :',reward)

        i+=1
    