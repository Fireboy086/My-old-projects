from pygame import *
from random import randint
import sounddevice as sd
import numpy as np
import sys
#pip install numpy 

init()
window_size = 1200, 800
window = display.set_mode(window_size)
clock = time.Clock()

player_rect = Rect(150, window_size[1]//2-100, 100, 100)

def generate_pipes(count, pipe_width=140, gap=280, min_height=50, max_height=440, distance=650):
    pipes = []
    start_x = window_size[0]
    for i in range(count):
        height = randint(min_height, max_height)
        top_pipe = Rect(start_x, 0, pipe_width, height)
        bottom_pipe = Rect(start_x, height + gap, pipe_width, window_size[1] - (height + gap))
        pipes.extend([top_pipe, bottom_pipe])
        start_x += distance
    return pipes

pies = generate_pipes(150)
main_font = font.Font(None, 100)
score = 0
lose = False
lose_timer = -1

y_vel = 2.0 
player_y = float(player_rect.y) 

scream = False
scream_threshold = 0.1

def audio_callback(indata, frames, time, status):
    global scream
    if status:
        print(f"Audio status: {status}")
    
    # Calculate volume (RMS)
    volume = np.sqrt(np.mean(indata**2)) *10
    scream = volume

while True:
    # Start audio stream if not already running
    if 'audio_stream' not in locals():
        audio_stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=44100)
        audio_stream.start()
    
    for e in event.get():
        if e.type == QUIT:
            quit()

    window.fill('sky blue')
    # Calculate green component based on scream and threshold
    # Green is 255 if not screaming, 0 if scream > threshold+0.4, linearly between
    if scream <= scream_threshold:
        green_component = 255
    elif scream >= scream_threshold + 0.4:
        green_component = 0
    else:
        # Linear interpolation between 255 and 0
        ratio = (scream - scream_threshold) / 0.4
        green_component = int(255 * (1 - ratio))
    Pcolor = (255, green_component, 0)
    draw.rect(window, Pcolor, player_rect)

    for pie in pies[:]:
        if not lose:
            pie.x -= 10
        draw.rect(window, 'green', pie)
        if pie.x <= -100:
            pies.remove(pie)
            score += 0.5
        if player_rect.colliderect(pie):
            lose = True
            lose_timer = 100

    if len(pies) < 8:
        pies += generate_pipes(150)

    score_text = main_font.render(f'{int(score)}', 1, 'black')
    center_text = window_size[0]//2 - score_text.get_rect().w
    window.blit(score_text, (center_text, 40))

    keys = key.get_pressed()
    if not lose:
        if scream > scream_threshold:
            player_y -= 5 + 1*(scream-scream_threshold)*10
        else:
            player_y += 5
    if keys[K_r] and lose:
        lose = False
        lose_timer = -1
        lose_alpha = 0
        score = 0
        pies = generate_pipes(150)
        player_y = window_size[1]//2-100
        y_vel = 2.0

    #cap the player y
    if not lose:
        player_y = max(0, min(window_size[1] - player_rect.h, player_y))

    if lose:
        player_y += y_vel
        y_vel *= 1.1

    if lose_timer > 0 and lose:
        lose_timer -= 1
        lose_alpha = round(255-lose_timer/100*255)
        #make a full black screen with the opacity decreasing while losing animation
        overlay = Surface(window_size, SRCALPHA)
        overlay.fill((0, 0, 0, lose_alpha))
        window.blit(overlay, (0, 0))
        if lose_timer == 0:
            quit()
            sys.exit()

    player_rect.y = int(player_y)
    
    display.update()
    clock.tick(60)