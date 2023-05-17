import pygame
import numpy as np
from tqdm import tqdm


def play_episodes(n_episodes=10_000, max_epsilon=1.0, min_epsilon=0.05, decay_rate=0.0001, gamma=0.99, learn=True, viz=False, human=False, log=False):
    global ball_change_x
    global ball_change_y
    global ball_size_to_sides
    global ball_x
    global ball_y
    global rect_x
    global rect_y
    global rect_change_x
    global rect_change_y
    global state_to_id
    global clock

    rewards = []
    epsilon_history = []

    # Végignézzük az epizódokat
    for episode in tqdm(range(n_episodes)):
        done = False

        # Epszilon csökkentése
        epsilon = min_epsilon + (max_epsilon - min_epsilon) * \
                np.exp(-decay_rate * episode)

        # Környezet visszaállítása
        total_reward = 0
        reset()

        # Első állapot beállítása
        state = encode_state(ball_x, ball_y, rect_x, rect_y, ball_change_x, ball_change_y)
        if state not in state_to_id:
            state_to_id[state] = len(state_to_id)

        while not done:
            reward = 0
            
            # Háttér színének beállítása
            screen.fill(BLACK)

            if not human:
                # Az Agent-től akciót kérünk, és ennek megfelelően állítjuk be a játékos mozgását
                action = agent.act(state=state_to_id[state], epsilon=epsilon)
                action_name = ACTIONS[action]

                if action_name == ACTION_LEFT:
                    rect_change_x = -1
                elif action_name == ACTION_RIGHT:
                    rect_change_x = 1
                elif action_name == ACTION_IDLE:
                    rect_change_x = 0
                else:
                    print("Error, unknwon action", action)
                    exit(-1)
            else:
                # Emberi inputot is tudunk kezelni
                action=0
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            rect_change_x = -1
                        elif event.key == pygame.K_RIGHT:
                            rect_change_x = 1   
                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                            rect_change_x = 0
                        elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                            rect_change_y = 0

            # Megváltoztatjuk a játékos és a labda helyzetét a végrehajtott akciónak megfelelően.
            rect_x += rect_change_x
            rect_y += rect_change_y

            # Labda mozgsásának kezelése
            if ball_x<0:
                ball_x=0
                ball_change_x = ball_change_x * -1
            elif ball_x>SPACE_SIZE[0]:
                ball_x=SPACE_SIZE[0]
                ball_change_x = ball_change_x * -1
            elif ball_y<0:
                ball_y=0
                ball_change_y = ball_change_y * -1
            # Amikor a labda és a játékos ütközik, növeljük a jutalmat és megváltoztatjuk a pályát
            elif ball_x + ball_size_to_sides >= rect_x - rect_size_to_sides_x and ball_x - ball_size_to_sides<=rect_x + rect_size_to_sides_x and ball_y==SPACE_SIZE[1]-1:
                ball_change_y = ball_change_y * -1
                reward = 1
            # Akkor fejezzük be az epizódot, amikor a játékos nem találja el a labdát
            elif ball_y> SPACE_SIZE[1] - 1:
                ball_change_y = ball_change_y * -1
                done = True
                reward = -1

            # Most új állapotba kerültünk, mert megtettünk egy bizonyos intézkedést
            new_state = encode_state(ball_x, ball_y, rect_x, rect_y, ball_change_x, ball_change_y)
            if new_state not in state_to_id:
                state_to_id[new_state] = len(state_to_id)

            ball_x += ball_change_x
            ball_y += ball_change_y

            # Ha az Agent túllép a képernyőn (mindkét oldalon), akkor megszakítjuk az epizódot
            if rect_x - rect_size_to_sides_x < 0:
                rect_x = 0 + rect_size_to_sides_x
                reward = -1
                done = True
            if rect_x > SPACE_SIZE[0] - rect_size_to_sides_x - 1:
                rect_x = SPACE_SIZE[0] - rect_size_to_sides_x - 1 
                reward = -1
                done = True
            
            # Vizualizáljuk a környezetet
            if viz:
                # Labda            
                pygame.draw.rect(screen,WHITE,[(ball_x - ball_size_to_sides) * ZOOM_SIZE, (ball_y - ball_size_to_sides) * ZOOM_SIZE, ZOOM_SIZE * ball_size_to_sides, ZOOM_SIZE * ball_size_to_sides])
                
                drawrect(screen,rect_x,rect_y)
                pygame.display.flip()         
                clock.tick(60)
            
            # Frissítjük a Q-table
            if learn:
                agent.learn(state_to_id[state], action, reward, state_to_id[new_state], gamma)

            # A következő időlépés aktuális állapota az aktuális new_state lesz
            state = new_state
            total_reward += reward

        if log:
            print("Total reward:", total_reward)
            
        rewards.append(total_reward)
        epsilon_history.append(epsilon)
    
    return rewards, epsilon_history