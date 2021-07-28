from GridWorld import *
from Agent import *

if __name__=="__main__":
    env=GridWorld()
    agent=Agent()

    gamma=1.0
    alpha=0.1 # 새로 들어오는 정보를 얼만큼 수용할 것인가

    reward_grid=[[0 for _ in range(env.grid_x+1)] for _ in range(env.grid_y+1)]

    for k in range(5): # 20번의 에피소드 진행
        print(str(k+1)+'번째 에피소드 진행중')
        done=False
        history=list()

        while not done:
            action=agent.select_action() # action random 선택
            (x,y), reward, done= env.step(action)
            history.append((x,y,reward))
        
        env.reset()

        # 에피소드가 끝난 뒤 테이블 업데이트
        cum_reward=0
        
        for transition in history[::-1]:
            x,y,reward=transition
            reward_grid[y][x]+=alpha*(cum_reward-reward_grid[y][x])
            cum_reward+=gamma*reward

    # 결과
    for row in reward_grid:
        print([round(i,2) for i in row])