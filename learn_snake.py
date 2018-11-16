import numpy as np
from scipy.special import expit
import pygame
from pygame.locals import *
import snake,play_snake,random
import copy

def safe_len(state,dx,dy):
    len = 0
    test = [state.head[0],state.head[1]]
    while test not in state.body and not snake.out_of_playzone(test):
        test[0] += dx
        test[1] += dy
        len += 1
    return len

@np.vectorize
def relu(x):
    return max(0,x)

def neural_play(data):
    matrices = [np.array(data[0]).reshape(6,4),
        np.array(data[1]).reshape(4,4),
        np.array(data[2]).reshape(4,4)]
    def do_it(state):
        while True:
            dx = state.food_pos[0] - state.head[0]
            dy = state.food_pos[1] - state.head[1]
            p_yclear = safe_len(state,0,1)
            n_yclear = safe_len(state,0,-1)
            p_xclear = safe_len(state,1,0)
            n_xclear = safe_len(state,-1,0)
            activation = np.array([dx,dy,p_yclear,n_yclear,p_xclear,n_xclear])
            for x in matrices:
                activation = activation @ x
                activation = expit(activation)
            max_ind = 0
            for i in range(len(activation)):
                if activation[i] > activation[max_ind]:
                    max_ind = i
            yield max_ind
    return do_it

def random_data():
    return [[random.uniform(-1,1) for i in range(24)],
            [random.uniform(-1,1) for i in range(16)],
            [random.uniform(-1,1) for i in range(16)]]

population = [random_data() for i in range(100)]
fitness = [0 for i in range(100)]

def roulette():
    rand = random.uniform(0,sum(fitness))
    for i in range(100):
        rand -= fitness[i]
        if rand == 0:
            return i
    return 99

def mutate(what):
    mutations = random.randint(1,20)
    for i in range(mutations):
        layer = random.randint(0,2)
        if layer == 0:
            depth = random.randint(0,23)
        else:
            depth = random.randint(0,15)
        what[layer][depth] = random.uniform(-1,1)

pygame.init()
window = pygame.display.set_mode((400,400))

while True:
    for i in range(100):
        fit = 0
        for i in range(5):
            fit += snake.scored_snake(neural_play(population[i]),200)
        fitness[i] = fit
        window.fill((50,50,50))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
    #show off best bot
    max_ind = fitness.index(max(fitness))
    snake.scored_snake(play_snake.show_bot(window,neural_play(population[max_ind])),200)
    #normalize fitnesses
    change = min(fitness) + 1
    for i in range(100):
        fitness[i] += change

    new_population = []
    new_population.append(copy.copy(population[max_ind]))
    for i in range(20):
        new_population.append(random_data())
    while len(new_population) < 100:
        new = copy.copy(population[roulette()])
        mutate(new)
        new_population.append(new)
    population = new_population
