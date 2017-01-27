from enum import Enum
from Block import *
from Constants import *
import numpy as np
import math


class Snake:
    def __init__(self, game_map, head, gen):
        self.game_map = game_map
        self.direction = gen[0]
        self.body = head
        self.gen = gen
        self.fitness = 0
        self.count_move = 0
        self.reached = False

    def calcualte_fitness(self):
        self.fitness = self.body.position.x + self.body.position.y - self.count_move
        self.body.type = BlockType.Normal

    def check_direction(self, step):
        if self.direction == UP:
            if step == DOWN:
                return False
        elif self.direction == DOWN:
            if step == UP:
                return False

        elif self.direction == LEFT:
            if step == RIGHT:
                return False
        elif self.direction == RIGHT:
            if step == LEFT:
                return False
        return True

    def move(self, step):
        if self.check_direction(self.gen[step]) :
            self.direction = self.gen[step]
        else:
            if self.reached is False:
                self.count_move += 2
            return
        head = self.body
        to_pos = [
            int(head.position.x / BLOCK_SIZE),
            int(head.position.y / BLOCK_SIZE)
        ]
        to_pos[0] = to_pos[0] + self.direction[0]
        if to_pos[0] >= MAP_HEIGHT:
            to_pos[0] = to_pos[0] - MAP_HEIGHT
        if to_pos[0] < 0:
            to_pos[0] = to_pos[0] + MAP_HEIGHT
        to_pos[1] = to_pos[1] + self.direction[1]
        if to_pos[1] >= MAP_WIDTH:
            to_pos[1] = to_pos[1] - MAP_WIDTH
        if to_pos[1] < 0:
            to_pos[1] = to_pos[1] + MAP_WIDTH
        to = self.game_map[to_pos[0]][to_pos[1]]
        if to.type == BlockType.Wall:
            if self.reached is False:
                self.count_move += 2
            pass
        else:
            to.type = BlockType.Snake
            self.body.type = BlockType.Normal
            self.body = to
            if self.reached is False:
                self.count_move += 1
            if self.body.position.x == GOAL[
                    0] and self.body.position.y == GOAL[1]:
                self.reached = True
