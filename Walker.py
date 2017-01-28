from enum import Enum
from Block import *
from Constants import *
import numpy as np
import math


class walker:
    def __init__(self, game_map, head, gen, game_canvas):
        self.game_map = game_map
        self.direction = gen[0]
        self.body = head
        self.gen = gen
        self.fitness = 0
        self.count_move = 0
        self.reached = False
        self.game_canvas = game_canvas
        self.best = False
        self.track = []

    def calcualte_fitness(self):
        self.fitness = self.body.position.x + self.body.position.y - self.count_move
        self.body.type = BlockType.Normal
        self.game_canvas.itemconfig(self.body.rectangle, fill="black")
        if self.best:
            for block in self.track:
                block.track = False
                self.game_canvas.itemconfig(block.rectangle, fill="black")
            self.track.clear()

    def check_direction(self, step):
        if self.direction[0] + step[0] == 0 and self.direction[1] + step[
                1] == 0:
            return False
        return True

    def move(self, step):
        if self.check_direction(self.gen[step]):
            self.direction = self.gen[step]
        else:
            if self.reached is False:
                self.count_move += 10
            return
        head = self.body
        to_pos = [
            int(head.position.y / BLOCK_SIZE),
            int(head.position.x / BLOCK_SIZE)
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
                self.count_move += 10
            pass
        else:
            to.type = BlockType.Walker
            if self.best:
                self.game_canvas.itemconfig(self.body.rectangle, fill="red")
                self.body.track = True
                self.track.append(self.body)
            else:
                if self.body.track:
                    self.game_canvas.itemconfig(
                        self.body.rectangle, fill="red")
                else:
                    self.game_canvas.itemconfig(
                        self.body.rectangle, fill="black")
            if self.best is False:
                self.game_canvas.itemconfig(to.rectangle, fill="white")
            else:
                self.game_canvas.itemconfig(to.rectangle, fill="red")
            self.body.type = BlockType.Normal
            self.body = to
            if self.reached is False:
                if self.direction == UP or self.direction == LEFT:
                    self.count_move += 5
                else:
                    self.count_move += 1
            if self.body.position.x == GOAL[
                    0] and self.body.position.y == GOAL[1]:
                self.reached = True
