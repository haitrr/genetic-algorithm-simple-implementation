"""UI of the game"""

from tkinter import *
from Constants import *
from Block import *
from Point import Point
from random import randint, shuffle, uniform
from Walker import *
import time
from Gen import Gen


def create_blocks():
    blocks = []
    for i in range(map_height.get()):
        temp = []
        for j in range(map_width.get()):
            block = Block(Point(j * block_size.get(), i * block_size.get()))

            # Randomly create wall block base WALL_RATE
            if uniform(0, 1000) < wall_rate.get():
                block.type = BlockType.Wall

            #  Store the rectangle id to the block to update it later
            block.rectangle = game_canvas.create_rectangle(
                (block.position.x, block.position.y),
                (block.position.x + block_size.get(),
                 block.position.y + block_size.get()),
                fill='black',
                outline='black')
            temp.append(block)
        blocks.append(temp)
    return blocks


def update(step):

    # Let all walkers move
    for walker in walkers:
        walker.move(step)

    # Redraw the game
    root.update()


def calculate_fitness():

    for walker in walkers:
        walker.calcualte_fitness()


def evolution():

    # Calculate all walker fitness
    calculate_fitness()

    # Update max fitness on interface
    update_max_fitness()

    # Create new generation
    breed()


def update_max_fitness():
    global max_fitness

    # Sort walkers by fitness decreasing
    walkers.sort(key=lambda x: x.fitness, reverse=True)

    # Update max fitness
    max_fitness = walkers[0].fitness
    max_fitness_label.config(text="Max: " + str(int(max_fitness)))


def select():

    selected_gens = []

    # Calculate total fitness of population
    total_fitness = sum(x.fitness for x in walkers)

    # Always select the best walker
    selected_gens.append(walkers[0].gen)

    # Select a half of population
    # The higher finess they are the higher chance they are selected
    while len(selected_gens) < int(population_size.get() / 2):
        rd = uniform(0, total_fitness - 1)
        sum_fitness = 0
        for walker in walkers:
            sum_fitness += walker.fitness
            if sum_fitness > rd:
                if walker.gen not in selected_gens:
                    selected_gens.append(walker.gen)
                    break
    return selected_gens


def breed():

    # Select parent from the this generation
    selected_parents = select()

    # Add them to new generation
    new_generation = selected_parents[:]

    # Shuffle it to keep the variety of population
    shuffle(selected_parents)

    # Let them cross over to create 1 child each couple
    # The 1/4 population remain will be generate randomly
    children = []
    for i in range(0, len(selected_parents), 2):
        children += selected_parents[i].cross_over(selected_parents[i + 1])
        new_generation.append(Gen(life_time.get()))

    # Let the children mutate
    mutation(children)

    # Add children to new generation
    new_generation += children

    # Clear out the population
    walkers.clear()

    # Create new population from the selected gens
    for i in range(len(new_generation)):
        walkers.append(
            Walker(map_blocks, map_blocks[start_point[0]][start_point[1]],
                   new_generation[i], game_canvas))

    # Track the best walker
    walkers[0].best = True


def mutation(gens):

    # Let the walkers mutate with the rate of MUTATION_RATE
    for gen in gens:
        rd = uniform(0, 1000)
        if rd <= mutation_rate.get():
            gen.mutate()


def init_population():

    # Randomly create the initial population
    # Size of POPULATION_SIZE
    Walker.block_size = block_size.get()
    Walker.life_time = life_time.get()
    Walker.goal_point=goal_point
    population = []
    for i in range(population_size.get()):
        population.append(
            Walker(map_blocks, map_blocks[start_point[0]][start_point[1]],
                   Gen(life_time.get()), game_canvas))
    return population


def start_game():
    global started, walkers
    if started:
        evolution()
        started = False
        start_game_button.config(text="Start")
    else:
        walkers = init_population()
        started = True
        start_game_button.config(text="Stop")
        step = 0
        generation = 1
        i = life_time.get()
        while i > 0 and started:

            # Update the game until life time is over
            update(step)
            step += 1
            i -= 1
            if i == 0:

                # Do the evolution
                evolution()
                i = life_time.get()
                step = 0

                # Increase and update the generation on UI
                generation += 1
                generation_label.config(text="Gen: " + str(generation))


def bound_wall():

    # Create the wall in each edge of the map
    for i in map_blocks[0]:
        i.type = BlockType.Wall
    for i in map_blocks[map_height.get() - 1]:
        i.type = BlockType.Wall
    for i in range(map_height.get()):
        map_blocks[i][0].type = BlockType.Wall
        map_blocks[i][map_width.get() - 1].type = BlockType.Wall


def exit_program():
    root.destroy()
    exit()


def apply_map():
    if started:
        return
    global map_blocks, walkers, goal_point
    setup_game_canvas()
    map_blocks.clear()
    map_blocks = create_blocks()
    bound_wall()
    fill_wall()
    goal_point = (map_width.get() - 2, map_height.get() - 2)


def setup_game_canvas():
    game_canvas.delete("all")
    game_canvas.config(
        width=map_width.get() * block_size.get(),
        height=map_height.get() * block_size.get(),
        background="black")


def fill_wall():
    for blocks in map_blocks:
        for block in blocks:
            if block.type == BlockType.Wall:
                game_canvas.itemconfig(block.rectangle, fill="blue")


def game_canvas_mouse_click(event):
    if started:
        return
    else:
        row = int(event.y / block_size.get())
        column = int(event.x / block_size.get())
        map_blocks[row][column].type = BlockType.Wall
        game_canvas.itemconfig(map_blocks[row][column].rectangle, fill="blue")


# Setup UI
root = Tk()
root.resizable(width=False, height=False)
root.grid()

# Max fitness label
max_fitness_label = Label(root, text="Max:1")
max_fitness_label.grid(row=5, column=1)

# Generation label
generation_label = Label(root, text="Gen : 1")
generation_label.grid(row=5, column=0)

# Start game ButtonBox
start_game_button = Button(root, text="Start", command=start_game)
start_game_button.grid(row=2, column=4, rowspan=2)

# Population size
population_size_label = Label(root, text="Population Size")
population_size_label.grid(row=2, column=0)

population_size = IntVar()
population_size.set(POPULATION_SIZE_DEFAULT)
population_size_entry = Entry(root, width=5, textvariable=population_size)
population_size_entry.grid(row=2, column=1)

# Mutation rate
mutation_rate_label = Label(root, text="Mutation Rate")
mutation_rate_label.grid(row=2, column=2)

mutation_rate = IntVar()
mutation_rate.set(MUTATION_RATE_DEFAULT)
mutation_rate_entry = Entry(root, width=5, textvariable=mutation_rate)
mutation_rate_entry.grid(row=2, column=3)

# Map size
map_size_label = Label(root, text="Map Size")
map_size_label.grid(row=0, column=0)

map_width = IntVar()
map_width.set(MAP_WIDTH_DEFAULT)
map_width_entry = Entry(root, width=5, textvariable=map_width)
map_width_entry.grid(row=0, column=1)

map_size_X_label = Label(root, text="X")
map_size_X_label.grid(row=0, column=2)

map_height = IntVar()
map_height.set(MAP_HEIGHT_DEFAULT)
map_height_entry = Entry(root, width=5, textvariable=map_height)
map_height_entry.grid(row=0, column=3)

apply_map_button = Button(root, text="Apply", command=apply_map)
apply_map_button.grid(row=0, column=4, rowspan=2)

# Block size
block_size_label = Label(root, text="Block size")
block_size_label.grid(row=1, column=0)

block_size = IntVar()
block_size.set(BLOCK_SIZE_DEFAULT)
block_size_entry = Entry(root, width=5, textvariable=block_size)
block_size_entry.grid(row=1, column=1)

# Wall rate
wall_rate_label = Label(root, text="Wall Rate")
wall_rate_label.grid(row=1, column=2)

wall_rate = IntVar()
wall_rate.set(WALL_RATE_DEFAULT)
wall_rate_entry = Entry(root, width=5, textvariable=wall_rate)
wall_rate_entry.grid(row=1, column=3)

# Life time
life_time_label = Label(root, text="Life Time")
life_time_label.grid(row=3, column=0)

life_time = IntVar()
life_time.set(LIFE_TIME_DEFAULT)
life_time_entry = Entry(root, width=5, textvariable=life_time)
life_time_entry.grid(row=3, column=1, columnspan=3)

# Game canvas
game_canvas = Canvas(root)
setup_game_canvas()
game_canvas.bind("<Button-1>", game_canvas_mouse_click)
game_canvas.grid(row=4, column=0, columnspan=5)

# Setup blocks and wall
max_fitness = -1000000
map_blocks = create_blocks()
bound_wall()
fill_wall()

# Start and goal points
start_point = START_POINT_DEFAULT
goal_point = GOAL_POINT_DEFAULT

# Setup population
walkers = init_population()

# Mainloop
started = False
root.title("Walker Evolution")
root.protocol("WM_DELETE_WINDOW", exit_program)
root.mainloop()
