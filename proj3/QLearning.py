
from __future__ import print_function

from future import standard_library

standard_library.install_aliases()
from builtins import range
from builtins import object
import MalmoPython
import json
import logging
import os
import random
import sys
import time

if sys.version_info[0] == 2:
    import Tkinter as tk
else:
    import tkinter as tk


class TabQAgent(object):
    """Tabular Q-learning agent for discrete state/action spaces."""

    def __init__(self):

        self.epsilon = 0.05  # exploration rate
        self.alpha = 0.2     # learning rate
        self.gamma = 0.8  # reward discount factor

        self.logger = logging.getLogger(__name__)
        if False:  # True if you want to see more information
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        self.logger.handlers = []
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
        


        self.actions = ["movenorth 1", "movesouth 1", "movewest 1", "moveeast 1"]
        self.q_table = {}
        self.canvas = None
        self.root = None

    ### Change q_table to reflect what we have learnt.
    # Inputs: reward - int, current_state - coordinate tuple, prev_state - coordinate tuple, prev_a - int
    # Output: updated q_table
    def updateQTable(self, reward, current_state, prev_state, prev_a):
        

        bestOption = max(self.q_table[current_state])

        current_learning = self.alpha * (reward + (self.gamma * bestOption))
        previous_learning = (1-self.alpha) * (self.q_table[prev_state][prev_a])
        self.q_table[prev_state][prev_a] = current_learning + previous_learning

        

                    ### YOUR CODE HERE ###
                    ### YOUR CODE HERE ###
                    ### YOUR CODE HERE ###
        return
    ### Change q_table to reflect what we have learnt upon reaching the terminal state.
    # Input: reward - int, prev_state - coordinate tuple, prev_a - int
    # Output: updated q_table
    def updateQTableFromTerminatingState(self, reward, prev_state, prev_a):
        if reward <= -100:
            self.q_table[prev_state][prev_a] = -100

        if reward > 0:
            self.q_table[prev_state][prev_a] = 100

                    ### YOUR CODE HERE ###
                    ### YOUR CODE HERE ###
                    ### YOUR CODE HERE ###


        return


    def act(self, world_state, agent_host, current_r):
        def moveRight(ah):
            ah.sendCommand("strafe 1")
            time.sleep(0.05)


        def moveLeft(ah):
            ah.sendCommand("strafe -1")
            time.sleep(0.05)


        def moveStraight(ah):
            ah.sendCommand("move 1")
            time.sleep(0.05)


        def moveBack(ah):
            ah.sendCommand("move -1")
            time.sleep(0.05)


        def legalMoves(x, y):
            listOfLegalMoves = []
            if y < 13:
                listOfLegalMoves.append("up")
            if y > 0:
                listOfLegalMoves.append("down")
            if x >0:
                listOfLegalMoves.append("left")
            if x < 5:
                listOfLegalMoves.append("right")
            return listOfLegalMoves

                    ### YOUR CODE HERE ###

        moveCommands = {"up": [moveStraight, 0], "down":[moveBack, 1], "left":[moveLeft, 2], "right":[moveRight, 3]}
        moveCommandsList = [moveStraight, moveBack, moveLeft, moveRight]
        
        obs_text = world_state.observations[-1].text
        obs = json.loads(obs_text)  # most recent observation
        self.logger.debug(obs)
        if not u'XPos' in obs or not u'ZPos' in obs:
            self.logger.error("Incomplete observation received: %s" % obs_text)
            return 0
        current_s = "%d:%d" % (int(obs[u'XPos']), int(obs[u'ZPos']))
        self.logger.debug("State: %s (x = %.2f, z = %.2f)" % (current_s, float(obs[u'XPos']), float(obs[u'ZPos'])))
        if current_s not in self.q_table:
            self.q_table[current_s] = ([0] * len(self.actions))

        # update Q values
        if self.prev_s is not None and self.prev_a is not None:
            self.updateQTable(current_r, current_s, self.prev_s, self.prev_a)

        self.drawQ(curr_x=int(obs[u'XPos']), curr_y=int(obs[u'ZPos']))


        coords = current_s.split(":")
        xcoord = int(coords[0])
        ycoord = int(coords[1])
        
        legalList = legalMoves(xcoord, ycoord)

        
        
        
        #if self.prev_a==
        # select the next action (find a s.t. self.actions[a] == next action)

                    ### YOUR CODE HERE ###
                    ### YOUR CODE HERE ###

       
        


        if random.random() <= 0.05:
            randomMove = legalList[random.randint(0, len(legalList)-1)]
            self.prev_a = moveCommands[randomMove][1]
            self.prev_s = current_s 

            moveCommands[randomMove][0](agent_host)

        else:
            #slight optimization:
            #remove the opposite of the previous action from the list of legal moves so that the agent doesn't
            #immediately move back to the previous state.
            #before the agent finds a reward, all state-action pairs that don't lead to death have a q-score of 0. 
            #the agent chooses randomly among all maximal q scores, so before a reward is found, at every state, 
            #one of the maximal state-action pairs includes going back to the old square. we removed that as a legal option
            #to speed up the rate of exploration. 
            if(self.prev_a == 0 and "down" in legalList):
                legalList.remove("down")
            if(self.prev_a == 1 and "up" in legalList):
                legalList.remove("up")
            if(self.prev_a == 2 and "right" in legalList):
                legalList.remove("right")
            if(self.prev_a == 3 and "left" in legalList):
                legalList.remove("left")
            



            #populates 'indices' with indices of all max q scores
            value = max(self.q_table[current_s])
            indices = []
            for i in range(len(self.q_table[current_s])):
                if(self.q_table[current_s][i]==value):
                    indices.append(i)

            randomBest = random.choice(indices)
            self.prev_a = randomBest
            self.prev_s = current_s 


            moveCommandsList[randomBest](agent_host)
        

        """
        if(current_s=="4:1"):
            moveRight(agent_host)
        if("up" in legalList):
            moveStraight(agent_host)


        print("printing current_s")
        print(current_s)
        """
        # try to send the selected action to agent, only update prev_s if this succeeds

                    ### YOUR CODE HERE ###
                    ### YOUR CODE HERE ###
                    ### YOUR CODE HERE ###



        return current_r

    # do not change this function
    def run(self, agent_host):
        """run the agent on the world"""

        total_reward = 0

        self.prev_s = None
        self.prev_a = None

        is_first_action = True

        # TODO complete the main loop:
        world_state = agent_host.getWorldState()
        while world_state.is_mission_running:
            current_r = 0

            if is_first_action:
                # wait until have received a valid observation
                while True:
                    time.sleep(0.1)
                    world_state = agent_host.getWorldState()
                    for error in world_state.errors:
                        self.logger.error("Error: %s" % error.text)
                    for reward in world_state.rewards:
                        current_r += reward.getValue()
                    if world_state.is_mission_running and len(world_state.observations) > 0 and not \
                    world_state.observations[-1].text == "{}":
                        total_reward += self.act(world_state, agent_host, current_r)
                        break
                    if not world_state.is_mission_running:
                        break
                is_first_action = False
            else:
                # wait for non-zero reward
                while world_state.is_mission_running and current_r == 0:
                    time.sleep(0.1)
                    world_state = agent_host.getWorldState()
                    for error in world_state.errors:
                        self.logger.error("Error: %s" % error.text)
                    for reward in world_state.rewards:
                        current_r += reward.getValue()
                # allow time to stabilise after action
                while True:
                    time.sleep(0.1)
                    world_state = agent_host.getWorldState()
                    for error in world_state.errors:
                        self.logger.error("Error: %s" % error.text)
                    for reward in world_state.rewards:
                        current_r += reward.getValue()
                    if world_state.is_mission_running and len(world_state.observations) > 0 and not \
                    world_state.observations[-1].text == "{}":
                        total_reward += self.act(world_state, agent_host, current_r)
                        break
                    if not world_state.is_mission_running:
                        break


        # process final reward
        total_reward += current_r

        # update Q values
        if self.prev_s is not None and self.prev_a is not None:
            self.updateQTableFromTerminatingState(current_r, self.prev_s, self.prev_a)

        # used to dynamically draw the QTable in a separate window
        print("self.q_table", self.q_table)
        self.drawQ()

        return total_reward

    # do not change this function
    def drawQ(self, curr_x=None, curr_y=None):
        scale = 50
        world_x = 6
        world_y = 14
        if self.canvas is None or self.root is None:
            self.root = tk.Tk()
            self.root.wm_title("Q-table")
            self.canvas = tk.Canvas(self.root, width=world_x * scale, height=world_y * scale, borderwidth=0,
                                    highlightthickness=0, bg="black")
            self.canvas.grid()
            self.root.update()
        self.canvas.delete("all")
        action_inset = 0.1
        action_radius = 0.1
        curr_radius = 0.2
        action_positions = [(0.5, action_inset), (0.5, 1 - action_inset), (action_inset, 0.5), (1 - action_inset, 0.5)]
        # (NSWE to match action order)
        min_value = -20
        max_value = 20
        for x in range(world_x):
            for y in range(world_y):
                s = "%d:%d" % (x, y)
                self.canvas.create_rectangle(x * scale, y * scale, (x + 1) * scale, (y + 1) * scale, outline="#fff",
                                             fill="#002")
                for action in range(4):
                    if not s in self.q_table:
                        continue
                    value = self.q_table[s][action]
                    
                    color = int(255 * (value - min_value) / (max_value - min_value))  # map value to 0-255
                    color = max(min(color, 255), 0)  # ensure within [0,255]
                    color_string = '#%02x%02x%02x' % (255 - color, color, 0)
                    self.canvas.create_oval((x + action_positions[action][0] - action_radius) * scale,
                                            (y + action_positions[action][1] - action_radius) * scale,
                                            (x + action_positions[action][0] + action_radius) * scale,
                                            (y + action_positions[action][1] + action_radius) * scale,
                                            outline=color_string, fill=color_string)
        if curr_x is not None and curr_y is not None:
            self.canvas.create_oval((curr_x + 0.5 - curr_radius) * scale,
                                    (curr_y + 0.5 - curr_radius) * scale,
                                    (curr_x + 0.5 + curr_radius) * scale,
                                    (curr_y + 0.5 + curr_radius) * scale,
                                    outline="#fff", fill="#fff")
        self.root.update()


if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools

    print = functools.partial(print, flush=True)

agent = TabQAgent()
agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse(sys.argv)
except RuntimeError as e:
    print('ERROR:', e)
    print(agent_host.getUsage())
    exit(1)

# -- set up the mission -- #
mission_file = './qlearning.xml'
with open(mission_file, 'r') as f:
    print("Loading mission from %s" % mission_file)
    mission_xml = f.read()
    my_mission = MalmoPython.MissionSpec(mission_xml, True)

# add some random holes in the ground to spice things up
for x in range(1, 3):
    for z in range(1, 13):
        if random.random() < 0.1:
            my_mission.drawBlock(x, 45, z, "water")

max_retries = 3

num_repeats = 150

cumulative_rewards = []
for i in range(num_repeats):

    print()
    print('Repeat %d of %d' % (i + 1, num_repeats))

    my_mission_record = MalmoPython.MissionRecordSpec()

    for retry in range(max_retries):
        try:
            agent_host.startMission(my_mission, my_mission_record)
            break
        except RuntimeError as e:
            if retry == max_retries - 1:
                print("Error starting mission:", e)
                exit(1)
            else:
                time.sleep(2.5)

    print("Waiting for the mission to start", end=' ')
    world_state = agent_host.getWorldState()
    while not world_state.has_mission_begun:
        print(".", end="")
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            print("Error:", error.text)
    print()

    # -- run the agent in the world -- #
    cumulative_reward = agent.run(agent_host)
    print('Cumulative reward: %d' % cumulative_reward)
    cumulative_rewards += [cumulative_reward]

    # -- clean up -- #
    time.sleep(0.5)  # (let the Mod reset)

print("Done.")

print()
print("Cumulative rewards for all %d runs:" % num_repeats)
print(cumulative_rewards)


