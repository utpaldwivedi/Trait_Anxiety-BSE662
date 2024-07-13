import pygame
import random
import pandas as pd
import time
import numpy as np
# Initialize pygame
pygame.init()

# Set window size
width=800
height=600
screen = pygame.display.set_mode((width, height))

# Function to display text on the screen
def display_text(text, size, position, color=(255, 255, 255)):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)

# Intro page function
def intro_page():
    background = pygame.image.load('bg2-final.jpg')

    intro_running = True
    while intro_running:
        screen.blit(background, (0, 0))
        display_text("Welcome to the Car Game!", 70, (400, 200))
        display_text("Press Enter to Start", 50, (400, 300))
        display_text("Press Esc to Quit", 40, (400, 350))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    intro_running = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

# Instruction page function
def instruction_page():
    background = pygame.image.load('instbg-final.jpg')

    instruction_running = True
    while instruction_running:
        screen.blit(background, (0, 0))
        display_text("Instructions", 70, (400, 100))
        display_text("Use 'f' to start the game.", 40, (400, 250))
        display_text("Use 'SPACE' to avoid the crash.", 40, (400, 300))
        display_text("Avoid crashing, crashing earns 0 points.", 40, (400, 350))
        display_text("Avoid crashing as late as possible to earn max. rewards", 40, (400, 400))
        display_text("Press Enter to Play", 50, (400, 450))
        display_text("Press Esc to Quit", 40, (400, 500))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                instruction_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    instruction_running = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                    
def gameover_page():
    background = pygame.image.load('game-over-final.jpg')
    intro_running = True
    start_time = time.time()  # Record intro start time

    while intro_running:

        # Draw background on each frame
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro_running = False  # Exit loop on QUIT event
            # if event.key == pygame.K_ESCAPE:
            #     pygame.quit()
            #     quit()
        # Update the display (needed for each frame)
        pygame.display.flip()

        # Check elapsed time and exit after 5 seconds
        if time.time() - start_time >= 3:
            intro_running = False
            
# Trail page function
# Trail page function
def trail_page():
    background = pygame.image.load('back (1).jpg')
    font = pygame.font.Font(None, 36)
    for i in range(10):
        acceleration_boosted = False  # Initialize acceleration_boosted
        playerX = 720
        playerY = 450
        enemyX = 20
        enemyY = 450
        enemy_change = 0
        acceleration_probability = 0.0002
        gpressed=False
        beforeg=True
        flag=False
        s_l=0.05
        s_r=0.075
        m_l=0.09
        m_r=0.11
        f_l=0.12
        f_r=0.14
        
        def mean(a,b):
            return (a+b)/2
        def std(a,b):
            return (b-a)/4
        def simulate_speed():
            nonlocal acceleration_boosted
            nonlocal enemyX
            nonlocal enemy_change
            nonlocal s_l
            nonlocal s_r
            nonlocal m_l
            nonlocal m_r
            nonlocal f_l
            nonlocal f_r
            enemyX += enemy_change
            
            if not acceleration_boosted and random.random() < acceleration_probability:
                slow = np.random.normal(mean(s_l,s_r), std(s_l,s_r))
                # medium = random.uniform(0.091, 0.2)
                
                medium = np.random.normal(mean(m_l,m_r), std(m_l,m_r))
                # fast = random.uniform(0.21, 0.35)
                
                fast = np.random.normal(mean(f_l,f_r), std(f_l,f_r))

                acceleration_boost = random.choice([slow,medium,fast])
                
                enemy_change = acceleration_boost
                enemyX += enemy_change
                acceleration_boosted = True
                
        running = True
        while running:
            # Screen setup
            screen.fill((0,125,0))
            screen.blit(background, (0,0))

            # Display score text
            score_text = font.render("Count: " + str(i+1), True, (0, 0, 0))  # Render score text
            screen.blit(score_text, (680, 10))  # Blit score text onto the screen
            text= font.render("Trial",True,(0,0,0))
            screen.blit(text, (400, 10))
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f and beforeg:
                        enemy_change = 0.02
                        gpressed=True
                        beforeg=False
                    if event.key == pygame.K_SPACE and gpressed:
                        speed = enemy_change
                        # enemy_change = 0
                        fid = playerX - (enemyX+64)
                        money = 1000 / fid
                        flag=True
                        # running = False
                        
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

            # Enemy movement
            enemyX += enemy_change
            
            if enemy_change:
                simulate_speed()
                speed = enemy_change
            
            if flag:
                playerX +=0.05
                # enemyX += enemy_change

            if enemyX >=800-64:
                running=False
                enemyX=800-64
                
            # Collision detection
            if playerX-enemyX <= 64:
                enemy_change = 0
                # fid = 0
                money = 0
                crash_count = 1
                print("Crash")
                running = False
                gameover_page()
                
            if playerX>=800:
                running=False    

            # Draw player and enemy
            player(playerX, playerY)
            enemy(enemyX, enemyY)
            pygame.display.update()


# Main game function
def main_game():
    try:
        df = pd.read_csv('results2.csv', dtype={'boost_flag': bool})
    except FileNotFoundError:
        df = pd.DataFrame(columns=['economic_score', 'fail_count', 'fid', 'boost_distance','final distance','before speed', 'after speed', 'threat-type', 'boost_flag'])
    
    background = pygame.image.load('back (1).jpg')
    font = pygame.font.Font(None, 36)
    earn=0
    result_dfs = []
    for i in range(50):
        acceleration_boosted = False  # Initialize acceleration_boosted
        playerX = 720
        playerY = 450
        enemyX = 20
        enemyY = 450
        enemy_change = 0
        acceleration_probability = 0.0002
        money = 0
        fid = 0        
        crash_count = 0    
        speed=0.0
        initial_distance = playerX - (enemyX+64)
        speed_flag=False
        speedb=0
        final_distance=0
        # print(initial_distance)
        gpressed=False
        beforeg=True
        boost_distance=0
        threat=""
        flag=False
        s_l=0.05
        s_r=0.08
        m_l=0.125
        m_r=0.155
        f_l=0.171
        f_r=0.22
        
        def mean(a,b):
            return (a+b)/2
        def std(a,b):
            return (b-a)/4
        def simulate_speed():
            nonlocal acceleration_boosted
            nonlocal enemyX
            nonlocal enemy_change
            nonlocal speed
            nonlocal boost_distance
            nonlocal speed_flag

            enemyX += enemy_change
            nonlocal s_l
            nonlocal s_r
            nonlocal m_l
            nonlocal m_r
            nonlocal f_l
            nonlocal f_r
            if not acceleration_boosted and random.random() < acceleration_probability:
                
                # slow = random.uniform(0.04, 0.09)
                
                
                slow = np.random.normal(mean(s_l,s_r), std(s_l,s_r))
                # medium = random.uniform(0.091, 0.2)
                
                medium = np.random.normal(mean(m_l,m_r), std(m_l,m_r))
                # fast = random.uniform(0.21, 0.35)
                
                fast = np.random.normal(mean(f_l,f_r), std(f_l,f_r))

                acceleration_boost = random.choice([slow,medium,fast])
                # acceleration_boost = slow
                speed_flag=True
                enemy_change = acceleration_boost
                speed=enemy_change
                boost_distance=enemyX+64
                
                enemyX =enemyX + enemy_change
                acceleration_boosted = True
                
        running = True
        while running:
            # Screen setup
            screen.fill((0,125,0))
            screen.blit(background, (0,0))

            # Display score text
            score_text = font.render("Count: " + str(i+1), True, (0, 0, 0))  # Render score text
            screen.blit(score_text, (680, 10))  # Blit score text onto the screen
            text= font.render("Main Game",True,(0,0,0))
            screen.blit(text, (320, 10))
            money_text= font.render("Score: "+str(round(earn,2)),True,(0,0,0))
            screen.blit(money_text, (50, 10))

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f and beforeg:
                        enemy_change = 0.02
                        speed=enemy_change
                        gpressed=True
                        beforeg=False
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()    
                    if event.key == pygame.K_SPACE and gpressed:
                        speedb = enemy_change
                        # enemy_change = 0
                        fid = 720 - (enemyX+64)
                        money = 1000 / fid
                        earn+=money
                        flag=True
                        # running = False
                        # playerX +=0.02
                        

            # Enemy movement
            enemyX += enemy_change
            
            
            if enemy_change and speed_flag==False:
                simulate_speed()
                speed = enemy_change
                if speed >= s_l-0.005 and speed <= s_r+0.005:
                    threat="slow"
                elif speed >= m_l-0.005 and speed <= m_r+0.005:
                    threat="medium"
                elif speed >= f_l-0.005 and speed <= f_r+0.005:
                    threat="fast"
                elif speed==0.02:
                    threat="slow"            
                # boost_distance=playerX-boost_distance
            
            if flag:
                playerX +=0.05
                # enemyX += enemy_change

            if enemyX >=800-64:
                running=False
                enemyX=800-64
                
                
            
            # Collision detection
            if playerX-enemyX <= 64:
                enemy_change = 0
                earn-=money
                # fid = 0
                money = 0
                final_distance=0
                crash_count = 1
                print("Crash")
                running = False
                gameover_page()
                
            if playerX>=800:
                final_distance=800-(enemyX+64)
                running=False    

            # Draw player and enemy
            player(playerX, playerY)
            enemy(enemyX, enemyY)
            pygame.display.update()
            
        result_dict = {
        'economic_score': round(money,4),
        'fail_count': crash_count,
        'fid': round(fid,4),
        'boost_distance': round(boost_distance,4),
        'final distance': round(final_distance,4),
        'before speed': round(speedb,4),
        'after speed': round(speed,4),
        'threat-type': threat,
        'boost_flag': acceleration_boosted
        }
        result_df = pd.DataFrame([result_dict])  # Create a DataFrame for this game
        result_dfs.append(result_df)  # Append the DataFrame to the list
    # Concatenate all DataFrames in the list
    df = pd.concat(result_dfs, ignore_index=True)

    # Save DataFrame to CSV file
    df.to_csv('Naman_Goyal.csv', index=False)
        

# Player and enemy functions
def player(x, y):
    player_img = pygame.image.load('car.png')
    screen.blit(player_img, (x, y))

def enemy(x, y):
    enemy_img = pygame.image.load('enemy-car.png')
    screen.blit(enemy_img, (x, y))

def main():
    intro_page()
    instruction_page()
    trail_page()
    instruction_page()
    main_game()
    

if __name__ == "__main__":
    main()