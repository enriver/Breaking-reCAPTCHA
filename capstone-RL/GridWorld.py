import pyautogui

class GridWorld():
    def __init__(self): # (10,10) 시작
        self.x=0 # x좌표
        self.y=0 # y좌표
        self.cell=100 # 셀 간격

        window_size=pyautogui.size()
        self.width=window_size[0] # 윈도우 가로
        self.height=window_size[1] # 윈도우 세로

        self.grid_x=self.width//self.cell
        self.grid_y=self.height//self.cell

        self.mouse_x=10
        self.mouse_y=10

        self.visit_grid=[[False for _ in range(self.grid_x+1)] for _ in range(self.grid_y+1)]
        self.visit_grid[self.y][self.x]=True

        pyautogui.moveTo(self.mouse_x,self.mouse_y,1)

    def step(self, a):

        if a==0:
            reward=self.move_up()
        elif a==1:
            reward=self.move_down()
        elif a==2:
            reward=self.move_left()
        elif a==3:
            reward=self.move_right()

        done=self.is_done()
        
        return (self.x, self.y), reward, done

    def move_up(self):
        self.y-=1

        if self.y < 0:
            self.y+=1
        else:
            if not self.visit_grid[self.y][self.x]:
                self.visit_grid[self.y][self.x]=True

                self.mouse_y-=self.cell

                if self.mouse_y < 0:
                    self.mouse_y+=self.cell
                    self.y+=1

                    return 0
                
                pyautogui.moveTo(self.mouse_x,self.mouse_y)

                return -1
            
        return 0

    def move_down(self):
        self.y+=1

        if self.y > self.grid_y:
            self.y-=1
        else:
            if not self.visit_grid[self.y][self.x]:
                self.visit_grid[self.y][self.x]=True

                self.mouse_y+=self.cell

                if self.mouse_y > self.height:
                    self.mouse_y+=self.cell
                    self.y-=1

                    return 0

                pyautogui.moveTo(self.mouse_x, self.mouse_y)

                return -1
        return 0

    def move_left(self):
        self.x-=1

        if self.x < 0:
            self.x+=1
        else:
            if not self.visit_grid[self.y][self.x]:
                self.visit_grid[self.y][self.x]=True

                self.mouse_x-=self.cell

                if self.mouse_x < 0 :
                    self.mouse_x+=self.cell
                    self.x+=1
                    
                    return 0

                pyautogui.moveTo(self.mouse_x, self.mouse_y)

                return -1
        return 0

    def move_right(self):
        self.x+=1

        if self.x > self.grid_x:
            self.x-=1
        else:
            if not self.visit_grid[self.y][self.x]:
                self.visit_grid[self.y][self.x]=True

                self.mouse_x+=self.cell

                if self.mouse_x > self.width:
                    self.mouse_x-=self.cell
                    self.x-=1

                    return 0

                pyautogui.moveTo(self.mouse_x, self.mouse_y)

                return -1
        return 0

    def is_done(self):
        if self.x==self.grid_x and self.y==self.grid_y:
            return True
        else:
            return False

    def get_state(self):
        return (self.x, self.y)

    def reset(self):
        self.x=0
        self.y=0
        
        self.mouse_x=10
        self.mouse_y=10

        self.visit_grid=[[False for _ in range(self.grid_x+1)] for _ in range(self.grid_y+1)]
        self.visit_grid[self.y][self.x]=True

        pyautogui.moveTo(self.mouse_x,self.mouse_y,1)

        return (self.x, self.y)