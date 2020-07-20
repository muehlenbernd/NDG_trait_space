from Game import *
from Agent import *
import random
from MyMath import *
import os

# import Ext_functions as ext

# set the game by defining the L value
small_bit = 0.4
NDG = Game(small_bit)

# set the disagreement point
disagreement = 0.3

# set the maximum runtime
run_time = 2000

# set the number of experiments
num_experiments = 100

# set the population size
size_Blue = 50
size_Red = 50

# set if the round results shall be shown
print_round_results = True
display_factor = 1

# set the number of dimensions of observable traits
dimension = 1

# plasticity of the 1st, 2nd, 3rd, etc dimension - overflow won't be considered
plasticity = [0.1, 0, 0, 0, 0]

# tolerance of the agents, if tol = "ND", tolerance values are
# randomly assigned by normal distribution with med = 0.5 and var = 0.1

tol = "ND"
#tol = 0.45


# make a file name
plasStr = str(int(plasticity[0]*100))
#tolStr = str(int(tol*100))
file_name = "result_"+plasStr+".txt"

# mutation rate
mutation_rate = 0.0001


# some lists for counting things
# this is a list of the strategy pairs from across the experiments
strategy_pair_list_total = []
# this is a count matrix for those strategy pairs
counter_pair_list_total = []
counter_type = [0, 0, 0, 0, 0]




print("EXP_ID \tRT \tSIG \tCD1 \tCONV \tCD2 \tIN&OUT-GROUP RELATIONS \tSTRATEGY SETS")

# start experiments
for exp in range(num_experiments):

    f = open(os.path.join("results", file_name), mode='a')

    break_condition= False

    line_string = str(exp)+"\t"


    print exp, "\t",

    # create a population of agents with random strategies
    agents = []

    # build all the blue agents first
    for dummy in range(size_Blue):

        # in-group and out-group strategy
        s0 = random.randint(0, 2)
        s1 = random.randint(0, 2)

        # set coordinates and tolerance
        coordinates = []
        for dummy in range(dimension):
            coordinates.append(random.random()*0.5)

        if tol == "ND":
            tolerance = MyMath.normal_distribution(0.5,0.1)
        else:
            tolerance = tol

        # blue agent is agent type 0, disagreement point, coordinates, tolerance radius, list of strategies
        agents.append(Agent(0, disagreement, coordinates, tolerance, [s0, s1]))


    # now build all the red agents
    for dummy in range(size_Red):

        # in-group and out-group strategy
        s0 = random.randint(0, 2)
        s1 = random.randint(0, 2)

        # set coordinates and tolerance
        coordinates = []
        for dummy in range(dimension):
            coordinates.append(random.random() * 0.5 + 0.5)

        if tol == "ND":
            tolerance = MyMath.normal_distribution(0.5, 0.1)
        else:
            tolerance = tol

        # blue agent is agent type 1, disagreement point, coordinates, tolerance radius, list of strategies
        agents.append(Agent(1, 0.0, coordinates, tolerance, [s0, s1]))


    # normalizer that includes the numbe of interactions and the maximum utility of the game
    normalizer = (1.0-small_bit)*(len(agents)-1)


    # run the algorithm
    # for each round from 1000
    for current_round in range(run_time):

        # some more lists for counting things
        # list and counts of strategies of blue agents
        strategy0_list = []
        counter0_list = []
        # list and counts of strategies of red agents
        strategy1_list = []
        counter1_list = []

        ingroup_Blues = [0.0, 0.0]
        ingroup_Reds = [0.0, 0.0]




        # resetting and mutation
        for agent in agents:

            # reset each agent
            agent.reset()

            # apply mutation
            if random.random() < mutation_rate:
                agent.strategy[0] = random.randint(0, 2)
                agent.strategy[1] = random.randint(0, 2)
                agent.coor1 = random.random()
                agent.coor2 = random.random()



        # interaction
        # looks like all pairs of agents are run against each other in some way
        for agent1 in agents:
            for agent2 in agents:
                if agent1 != agent2:
                    agent1.interact(agent2, NDG)

        # imitation
        for index in range(len(agents)):

            # pick current indexed agent and opponent of same type
            agent = agents[index]
            if index < size_Blue:
                op_agent = random.choice(agents[0:size_Blue-1])
            else:
                op_agent = random.choice(agents[size_Blue:])


            # imitate the other agent if scored better with probability of score difference
            if op_agent.accumulated_utility > agent.accumulated_utility:

                # normaliser is 60% of the number of agents, not sure why
                diff = (op_agent.accumulated_utility-agent.accumulated_utility)/normalizer

                # with some chance that increases the larger the difference is in accumulated resources
                prob = random.random()
                if prob < diff:

                    # copy the strategy and signal of the other agent
                    agent.strategy[0] = op_agent.strategy[0]
                    agent.strategy[1] = op_agent.strategy[1]

                    # approximate the coordinates of the other agent
                    my_coor = agent.trait_coordinates
                    op_coor = op_agent.trait_coordinates
                    new_coordinates = approximation_step(my_coor, op_coor, plasticity)

                    agent.trait_coordinates = new_coordinates


            # if it a a blue agent
            if index < size_Blue:

                ingroup_Blues[0] += (agent.ingroup_members0*1.0 / (size_Blue-1))
                ingroup_Blues[1] += (agent.ingroup_members1*1.0 / size_Red)

                # print(agent.strategy)
                # if the strategy is new
                if agent.strategy not in strategy0_list:
                    # add it to the list
                    strategy0_list.append(agent.strategy)
                    # add one instance of this strategy to your count
                    counter0_list.append(1)
                else:
                    # increment the count for the duplicate strategy
                    this_index = strategy0_list.index(agent.strategy)
                    # increment its count by one
                    counter0_list[this_index] += 1

            # if it's a red agent
            else:

                ingroup_Reds[0] += (agent.ingroup_members0*1.0 / size_Blue)
                ingroup_Reds[1] += (agent.ingroup_members1*1.0 / (size_Red-1))

                if agent.strategy not in strategy1_list:
                    strategy1_list.append(agent.strategy)
                    counter1_list.append(1)
                else:
                    this_index = strategy1_list.index(agent.strategy)
                    counter1_list[this_index] += 1



        if counter0_list[0]*1.0/size_Blue > 0.9 and counter1_list[0]*1.0/size_Red > 0.9:
            break_condition = True


        # after a round: print the round results
        if (print_round_results and current_round%(run_time/display_factor) == (run_time/display_factor)-1) or break_condition:

            line_string += (str(current_round)+"\t")

            print current_round, "\t",

            if (ingroup_Blues[1]/ingroup_Blues[0] < 0.5) and (ingroup_Reds[0]/ingroup_Reds[1] < 0.5):
                print "DisS", "\t", 0, "\t",
                line_string += ("DisS"+"\t"+"0"+"\t")

            elif (ingroup_Blues[1] / ingroup_Blues[0] > 0.5) and (ingroup_Reds[0] / ingroup_Reds[1] > 0.5):
                print "SimS", "\t", 1, "\t",
                line_string += ("SimS" + "\t"+"1"+"\t")
            else:
                print "MixS", "\t", 10, "\t",
                line_string += ("MixS" + "\t"+"10"+"\t")


            # compute the number of proBlue players in both populations
            sumProBinB = 0
            for index in range(len(strategy0_list)):
                if strategy0_list[index][1] == 2:
                    sumProBinB += counter0_list[index]

            sumProBinR = 0
            for index in range(len(strategy1_list)):
                if strategy1_list[index][1] == 0:
                    sumProBinR += counter1_list[index]





            if counter0_list[0]*1.0/size_Blue >= 0.8 and strategy0_list[0] == [1,1] and counter1_list[0]*1.0/size_Red >= 0.8 and strategy1_list[0] == [1,1]:
                print "Fair", "\t", 2, "\t",
                line_string += ("Fair" + "\t"+"2"+"\t")
            elif counter0_list[0]*1.0/size_Blue >= 0.8 and strategy0_list[0][1] == 2 and counter1_list[0]*1.0/size_Red >= 0.8 and strategy1_list[0][1] == 0:
                print "proB", "\t", 4, "\t",
                line_string += ("proB" + "\t"+"4"+"\t")
            elif sumProBinB*1.0/size_Blue >= 0.8 and sumProBinR*1.0/size_Red >= 0.8:
                print "proB", "\t", 4, "\t",
                line_string += ("proB" + "\t"+"4"+"\t")
            else:
                line_string += ("Else" + "\t"+"10"+"\t")
                print "Else", "\t", 10, "\t",



            print round(ingroup_Blues[0],0), round(ingroup_Blues[1],0), "-", round(ingroup_Reds[0],0), round(ingroup_Reds[1],0), "\t",

            line_string += (str(round(ingroup_Blues[0],0))+" "+str(round(ingroup_Blues[1],0))+"-"+str(round(ingroup_Reds[0],0))+" "+str(round(ingroup_Reds[1],0))+"\t")

            # strategy0_list is the set of conditional strategies [2 item list]

            for index in range(len(strategy0_list)):
                print counter0_list[index], strategy0_list[index], "\t",
                line_string += (str(counter0_list[index])+" "+str(strategy0_list[index][0])+str(strategy0_list[index][1])+"\t")

            print "-", "\t",

            for index in range(len(strategy1_list)):
                print counter1_list[index], strategy1_list[index], "\t",
                line_string += (str(counter1_list[index]) + " "+str(strategy1_list[index][0])+str(strategy1_list[index][1])+"\t")


            print


        if break_condition:
            break

    f.write(line_string + '\n')

    f.close()
