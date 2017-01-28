"""UI of the game"""

from tkinter import *
from Constants import *
from Block import *
from Point import Point
from random import randint, shuffle, uniform
from Snake import *
import time


def create_blocks():
    """
    create and return blocks of the game
    """
    blocks = []
    for i in range(MAP_HEIGHT):
        temp = []
        for j in range(MAP_WIDTH):
            block = Block(Point(j * BLOCK_SIZE, i * BLOCK_SIZE))
            if uniform(0, 1) < WALL_RATE:
                block.type = BlockType.Wall
            block.rectangle = game_canvas.create_rectangle(
                (block.position.x, block.position.y),
                (block.position.x + BLOCK_SIZE, block.position.y + BLOCK_SIZE),
                fill='black',
                outline='black')
            temp.append(block)
        blocks.append(temp)
    return blocks


def create_snake(code, gen):
    """
    create a snakes at random location in the map
    """
    new_snake = Snake(map_blocks, map_blocks[1][1], gen, game_canvas)
    return new_snake


def update(step):
    """
    Update the game
    """
    global draw
    shuffle(snakes)
    for snake in snakes:
        snake.move(step)
        if (draw):
            root.update()


def calculate_fitness():
    for snake in snakes:
        snake.calcualte_fitness()


def evolution():
    calculate_fitness()
    update_max_fitness()
    breed()


def update_max_fitness():
    global max_fitness, draw
    snakes.sort(key=lambda x: x.fitness, reverse=True)
    if snakes[0].fitness > max_fitness:
        draw = True
        max_fitness = snakes[0].fitness
    else:
        draw = False
    max_fitness_label.config(text="Max: " + str(int(max_fitness)))


def select():
    selected_gens = []
    total_fitness = get_total_fitness()
    selected_gens.append(snakes[0].gen)
    while len(selected_gens) < int(POPULATION_SIZE / 2):
        rd = uniform(0, total_fitness - 1)
        sum_fitness = 0
        for snake in snakes:
            sum_fitness += snake.fitness
            if sum_fitness > rd:
                if snake.gen not in selected_gens:
                    selected_gens.append(snake.gen)
                    break
    return selected_gens


def get_total_fitness():
    total = 0
    for snake in snakes:
        total += snake.fitness
    return total


def breed():
    global best_snake
    selected_parents = select()
    new_generation = selected_parents[:]
    shuffle(selected_parents)
    childrens = []
    couples = [
        selected_parents[x:x + 2] for x in range(0, len(selected_parents), 2)
    ]
    for couple in couples:
        childrens += cross_over(couple)
        new_generation.append(
            [DIRECTION[randint(0, 3)] for i in range(LIFE_TIME)])
    mutation(childrens)
    new_generation += childrens
    snakes.clear()
    for i in range(len(new_generation)):
        snakes.append(create_snake(i, new_generation[i]))
    best_snake.best = False
    best_snake = snakes[0]
    snakes[0].best = True


def cross_over(parents):
    children = [[]]
    for i in range(LIFE_TIME):
        if i % 2 == 0:
            children[0].append(parents[0][i])
        else:
            children[0].append(parents[1][i])
    return children


def mutation(gens):
    for gen in gens:
        rd = uniform(0, 1)
        if rd <= MUTATION_RATE:
            mutate(gen)


def mutate(gen):
    loc = randint(0, LIFE_TIME - 1)
    val = randint(0, 3)
    while val == gen[loc]:
        val = randint(0, 3)
    gen[loc] = DIRECTION[val]


def init_population():
    """
    Create first generation of snakes
    """
    population = []
    for i in range(POPULATION_SIZE):
        gen = [DIRECTION[randint(0, 3)] for i in range(LIFE_TIME)]
        population.append(create_snake(i, gen))
    return population


def start_game():
    """
    Start the game loops
    """
    global draw
    step = 0
    generation = 1
    i = LIFE_TIME
    while i > 0:
        update(step)
        step += 1
        i -= 1
        if i == 0:
            evolution()
            i = LIFE_TIME
            step = 0
            generation += 1
            generation_label.config(text="Gen: " + str(generation))


def bound_wall():
    for i in map_blocks[0]:
        i.type = BlockType.Wall
    for i in map_blocks[MAP_HEIGHT - 1]:
        i.type = BlockType.Wall
    for i in range(MAP_HEIGHT):
        map_blocks[i][0].type = BlockType.Wall
        map_blocks[i][MAP_WIDTH - 1].type = BlockType.Wall


root = Tk()
root.resizable(width=False, height=False)
root.grid()
#start_game_button = Button(root, text="Start Game", command=start_game)
#start_game_button.grid(row=1, column=0)

max_fitness_label = Label(root, text="Max:1")
max_fitness_label.grid(row=1, column=1)
generation_label = Label(root, text="Gen : 1")
generation_label.grid(row=1, column=0)
game_canvas = Canvas(
    root,
    width=MAP_WIDTH * BLOCK_SIZE,
    height=MAP_HEIGHT * BLOCK_SIZE,
    background="black")
game_canvas.grid(row=0, column=0, columnspan=2)

max_fitness = -1000000
draw = False
map_blocks = create_blocks()
bound_wall()
for blocks in map_blocks:
    for block in blocks:
        if block.type == BlockType.Wall:
            game_canvas.itemconfig(block.rectangle, fill="blue")
snakes = init_population()
for blocks in map_blocks:
    for block in blocks:
        if block.type == BlockType.Snake:
            game_canvas.itemconfig(block.rectangle, fill="white")
best_snake = snakes[0]
root.title("Snake evolution")
root.after(500, start_game)
root.mainloop()