import random
import math
import MyMath

class Agent:

    ####### constructor #######
    def __init__(self, type, dap, trait_coordinates, tolerance, initial_strategy = [-1,-1]):

        # agent's type and agent's disagreement point (dap)
        self.type = type
        self.dap = dap
        self.tolerance = tolerance
        self.trait_coordinates = trait_coordinates


        # conditional strategy what to do when receive signal 1 or signal 2
        self.strategy = initial_strategy
        if initial_strategy == [-1,-1]:
            self.strategy = [random.randint(0,2), random.randint(0,2)]

        # the agent's last choice (L:0, M:1, H:2) and last plays's utility
        self.current_utility = 0.0
        self.current_choice = -1

        # an agent's accumulated utility for a number of plays
        self.accumulated_utility = 0.0

        # how many agents of type 1 and 2 are ingroup or not
        self.ingroup_members0 = 0
        self.ingroup_members1 = 0


    ### interaction ###
    def interact(self, opponent, game):

        # check the distance between agents
        distance = MyMath.euc_distance(self.trait_coordinates,opponent.trait_coordinates)

        # play in-group of out-group strategy dependent on tolerance
        if distance <= self.tolerance:
            self.current_choice = self.strategy[0]

            if opponent.type == 0:
                self.ingroup_members0 += 1
            else:
                self.ingroup_members1 += 1
        else:
            self.current_choice = self.strategy[1]

        if distance <= opponent.tolerance:
            opponent.current_choice = opponent.strategy[0]
        else:
            opponent.current_choice = opponent.strategy[1]

        # compute current utility
        self.current_utility = max(game.utility[self.current_choice][opponent.current_choice],self.dap)

        # update accumulated reward values
        self.accumulated_utility += self.current_utility



    ### imitation ###
    def imitate(selfself, opponent):

        x = 0


    ### reset round values ###
    def reset(self):

        # reset accumulated reward values
        self.accumulated_utility = 0.0
        self.ingroup_members0 = 0
        self.ingroup_members1 = 0

