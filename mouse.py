import pyautogui
import sys
from random import randint

if __name__=="__main__":
    position=pyautogui.position()
   # 화면 전체 크기 확인하기
    print(pyautogui.size())

    # x, y 좌표
    x=position.x
    y=position.y

    i=0
    while i<100:
        rand_x=randint(-1,1)*10
        rand_y=randint(-1,1)*10

        x+=rand_x
        y+=rand_y

        print('(',x,',',y,')')

        pyautogui.moveTo(x,y)

        i+=1
        
    #끝
    sys.exit(0)