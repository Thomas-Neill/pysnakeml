import pygame
from pygame.locals import *
import snake

def draw_state(window,state):
    window.fill((100,100,100))
    for i in state.body:
        pygame.draw.rect(window,(0,125,0),(20*i[0],380 - 20*i[1],20,20))
    pygame.draw.rect(window,(0,125,0),(20*state.head[0],380 - 20*state.head[1],20,20))
    pygame.draw.rect(window,(125,0,0),(20*state.food_pos[0],380 - 20*state.food_pos[1],20,20))
    pygame.display.update()

def play_snake(state):
    while True:
        draw_state(window,state)
        for i in pygame.event.get():
            if i.type == QUIT:
                yield snake.STOP
            if i.type == KEYDOWN:
                if i.key == K_UP:
                    yield snake.UP
                elif i.key == K_DOWN:
                    yield snake.DOWN
                elif i.key == K_LEFT:
                    yield snake.LEFT
                elif i.key == K_RIGHT:
                    yield snake.RIGHT
def bot_1(state):
    while True:
        if state.head[0] < state.food_pos[0]:
            yield snake.RIGHT
        elif state.head[0] > state.food_pos[0]:
            yield snake.LEFT
        elif state.head[1] < state.food_pos[1]:
            yield snake.UP
        elif state.head[1] > state.food_pos[1]:
            yield snake.DOWN

def show_bot(window,bot):
    def new_code(state):
        for i in bot(state):
            draw_state(window,state)
            for _nope in range(10):
                pygame.time.wait(16)
                for x in pygame.event.get():
                    if x.type == QUIT:
                        quit()
            yield i
    return new_code
