# Simranjit Bhatia (sk8wt)
# Created by Minbiao Han and Roman Sharykin
# AI fall 2018

from __future__ import print_function
from __future__ import division

from builtins import range
from past.utils import old_div
import copy
import MalmoPython
import json
import logging
import math
import os
import random
import sys
import time
import re
import uuid
from collections import namedtuple
from operator import add
from random import *
import numpy as np

### You should define your evaluation function here
# Inputs: pos - tuple (position of player), enemy_pos - tuple, food - array
# Output: your evaluation score


def evalfuncReflex(pos, enemy_pos, dest_blocks):
    ### YOUR CODE HERE ###

    pos = (pos[0] - 0.5, pos[1] - 0.5)
    enemy_pos = (enemy_pos[0] - 0.5, enemy_pos[1] - 0.5)
    enemy_distance = manhattan_distance(pos, enemy_pos)

    smallk = 100
    c = 25
    largek = 225

    closest_block = manhattan_distance(pos, dest_blocks[0])


    if enemy_distance <= 2:
        return -10000000

    
    if pos in dest_blocks:
        return 99990

    
    for food in dest_blocks:
        current_block = manhattan_distance(pos, food)
        if (current_block < closest_block):
            closest_block = current_block

    new_list = copy.deepcopy(dest_blocks)


    
    if pos in new_list:
        new_list.remove(pos)
    
    return (-(smallk * closest_block) - (c/enemy_distance) - (largek*len(new_list)))
    

### Implement a way for the agent to decide which way to move
# Inputs: pos - tuple (position of player), world_state, enemy_pos - tuple, food - array
# Output: direction in which to move (can be a string, int, or whatever way you want to implement it)

def chooseAction(pos, wstate, dest_blocks, enemy_pos):
    ### YOUR CODE HERE ###

    illegal_moves = illegalMoves(wstate)

    eval_result = []
    if ("left" not in illegal_moves):
        left_pos = (pos[0] + 1, pos[1])
        eval_result.append((evalfuncReflex(left_pos, enemy_pos, dest_blocks), "left"))
    if ("right" not in illegal_moves):
        right_pos = (pos[0] - 1, pos[1])
        eval_result.append((evalfuncReflex(right_pos, enemy_pos, dest_blocks), "right"))
    if("forward" not in illegal_moves):
        up_pos = (pos[0], pos[1] + 1)
        eval_result.append((evalfuncReflex(up_pos, enemy_pos, dest_blocks), "forward"))
    if ("back" not in illegal_moves):
        down_pos = (pos[0], pos[1] - 1)
        eval_result.append((evalfuncReflex(down_pos, enemy_pos, dest_blocks), "back"))

    best_move = max(eval_result, key=lambda item:item[0] )

    return best_move


### Move the agent here
# Output: void (should just call the correct movement function)

def reflexAgentMove(agent, pos, wstate, dest_blocks, enemy_pos):
    movement = chooseAction(pos, wstate, dest_blocks, enemy_pos)
    move = movement[1]
    if  move == "left":
        moveLeft(agent)
    if  move == "right":
        moveRight(agent)
    if  move == "back":
        moveBack(agent)
    if  move == "forward":
        moveStraight(agent)

    return
# Simple movement functions
# Hint: if you want your execution to run faster you can decrease time.sleep
def moveRight(ah):
    ah.sendCommand("strafe 1")
    time.sleep(0.1)


def moveLeft(ah):
    ah.sendCommand("strafe -1")
    time.sleep(0.1)


def moveStraight(ah):
    ah.sendCommand("move 1")
    time.sleep(0.1)


def moveBack(ah):
    ah.sendCommand("move -1")
    time.sleep(0.1)

# Used to find which movements will result in the player walking into a wall
### Input: current world state
### Output: An array directional strings
def illegalMoves(world_state):
    blocks = []
    if world_state.number_of_observations_since_last_state > 0:
        msg = world_state.observations[-1].text
        observations = json.loads(msg)
        grid = observations.get(u'floor3x3W', 0)
        if grid[3] == u'diamond_block':
            blocks.append("right")
        if grid[1] == u'diamond_block':
            blocks.append("back")
        if grid[5] == u'diamond_block':
            blocks.append("left")
        if grid[7] == u'diamond_block':
            blocks.append("forward")

        return blocks

# Used to find the Manhattan distance between two tuples
def manhattan_distance(start, end):
    sx, sy = start
    ex, ey = end
    return abs(ex - sx) + abs(ey - sy)

# Do not modify!
###
###
# This functions moves the enemy agent randomly #
def enemyAgentMoveRand(agent, ws):
    time.sleep(0.1)
    illegalgrid = illegalMoves(ws)
    legalLST = ["right", "left", "forward", "back"]
    for x in illegalgrid:
        if x in legalLST:
            legalLST.remove(x)
    y = randint(0,len(legalLST)-1)
    togo = legalLST[y]
    if togo == "right":
        moveRight(agent)

    elif togo == "left":
        moveLeft(agent)

    elif togo == "forward":
        moveStraight(agent)

    elif togo == "back":
        moveBack(agent)
