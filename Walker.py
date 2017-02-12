from enum import Enum
from Block import *
from Constants import *
import numpy as np
import math


class Walker:
    block_size = None
    life_time = None
    goal_point = None

    def __init__(self, game_map, head, gen, game_canvas):
        self.game_map = game_map
        self.direction = DIRECTION[gen.adn[0]]
        self.body = head
        self.gen = gen
        self.fitness = 0
        self.count_move = 0
        self.reached = False
        self.game_canvas = game_canvas
        self.best = False
        self.track = []

    def calcualte_fitness(self):

        # Fitness equal to the distance it has gone
        # minus the wasted move
        #
        self.fitness = (
            self.body.position.x / self.block_size + self.body.position.y /
            self.block_size) * 100 / (self.count_move)

        # Reset the block tyoe
        self.body.type = BlockType.Normal
        self.game_canvas.itemconfig(self.body.rectangle, fill="black")

        # Reset the track of best walker
        if self.best:
            for block in self.track:
                block.track = False
                self.game_canvas.itemconfig(block.rectangle, fill="black")
            self.track.clear()
            self.best = False

    def check_direction(self, step):
        if self.direction[0] + DIRECTION[self.gen.adn[step]][
                0] == 0 and self.direction[1] + DIRECTION[self.gen.adn[step]][
                    1] == 0:
            return False
        return True

    def move(self, step):

        # Stop after the walker reached GOAL
        if self.reached:
            return

        # Check if this move is a reverse move
        if self.check_direction(step) is False:
            self.count_move += 1

        self.direction = DIRECTION[self.gen.adn[step]]
        head = self.body
        # Calculate the destination point
        to_pos = [
            int(head.position.y / self.block_size),
            int(head.position.x / self.block_size)
        ]
        to_pos[0] = to_pos[0] + self.direction[0]

        #ALLOW WALKERS TO GO ACROSS THE BORDER
        #if to_pos[0] >= MAP_HEIGHT:
        #    to_pos[0] = to_pos[0] - MAP_HEIGHT
        #if to_pos[0] < 0:
        #    to_pos[0] = to_pos[0] + MAP_HEIGHT
        to_pos[1] = to_pos[1] + self.direction[1]
        #if to_pos[1] >= MAP_WIDTH:
        #    to_pos[1] = to_pos[1] - MAP_WIDTH
        #if to_pos[1] < 0:
        #    to_pos[1] = to_pos[1] + MAP_WIDTH
        to = self.game_map[to_pos[0]][to_pos[1]]

        # If move to wall -> wasted move
        if to.type == BlockType.Wall:
            self.count_move += 2
        else:
            to.type = BlockType.Walker

            # Do track best walker , and set type blocks
            if self.best:
                self.game_canvas.itemconfig(self.body.rectangle, fill="red")
                self.body.track = True
                self.track.append(self.body)
                self.game_canvas.itemconfig(to.rectangle, fill="red")
            else:
                self.game_canvas.itemconfig(to.rectangle, fill="white")
                if self.body.track:
                    self.game_canvas.itemconfig(
                        self.body.rectangle, fill="red")
                else:
                    self.game_canvas.itemconfig(
                        self.body.rectangle, fill="black")

            # Actualy do move
            self.body.type = BlockType.Normal
            self.body = to

            # Move up and left can be waste
            #if self.direction == UP or self.direction == LEFT:
            #    self.count_move += 1
            self.count_move += 1

            # Check if the walker reach the goal
            if self.body.position.x == self.goal_point[
                    0] * self.block_size and self.body.position.y == self.goal_point[
                        1] * self.block_size:
                self.count_move += len(self.gen.adn) - step
                self.reached = True
