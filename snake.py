import random

UP,RIGHT,DOWN,LEFT,STOP = range(5)

def randpos():
    return [random.randint(0,19),random.randint(0,19)]

def out_of_playzone(pos):
    return pos[0] < 0 or pos[0] > 19 or pos[1] < 0 or pos[1] > 19

def updated_pos(pos,move):
    new = [pos[0],pos[1]]
    if move == UP:
        new[1] += 1
    elif move == DOWN:
        new[1] -= 1
    elif move == LEFT:
        new[0] -= 1
    elif move == RIGHT:
        new[0] += 1
    else:
        print("???")
    return new
class SnakeState:
    def __init__(self):
        self.food_pos = [0,0]
        self.head = [0,0]
        self.body = []
    def place_food(self):
        start = True
        while start or self.head == self.food_pos or self.food_pos in self.body:
            start = False
            self.food_pos = randpos()

def dist(p0,p1):
    return ((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)**.5

def scored_snake(move_generator, limit):
    state = SnakeState()
    state.head = randpos()
    state.place_food()
    score = 0
    for move in move_generator(state):
        score += 0.25
        delta = dist(state.head,state.food_pos)
        new = updated_pos(state.head,move)
        d2 = dist(new,state.food_pos)
        if d2 < delta:
            score += 0.25
        elif d2 > delta:
            score -= 1
        if move == STOP:
            break
        state.body.append(state.head)
        state.head = new
        if state.head == state.food_pos:
            score += 10
            state.place_food()
        else:
            state.body.pop(0)
        if (state.head in state.body or out_of_playzone(state.head)):
            break
        limit -= 1
        if limit == 0:
            break
    return score

def snake(movegen):
    scored_snake(movegen,-1)
