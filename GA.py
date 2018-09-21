import os 
import sys
import numpy as np
import gym

from GA_Config import Config
from GA_Network import Network
from GA_Helper import *

config = Config()
env = gym.make(Config.env_name)

#fill the population
population = []
for i in range(config.num_policies):
    pop = Network(config)
    population.append(pop)

#every episode evaluates each policy
for episode in range(config.num_generations):
    Reward = np.zeros(config.num_policies)
    for policy in range(config.num_policies):
        curr_pol = population[policy]
        for i in range(config.num_iterations):
            Reward[policy] += curr_pol.playthrough(env)

    Reward /= config.num_iterations
    print(episode, np.mean(Reward), np.max(Reward))

    #sort the policies by score achieved and remove the lowest scoring 
    l1, l2 = zip(*sorted(zip(Reward, population)))
    population = list(l2[int(config.mutate_per*config.num_policies):])
    Reward = list(l1[int(config.mutate_per*config.num_policies):])

    #save and check if solved
    #if (episode % config.checkpoint_freq == 0) and (episode != 0):
    if (episode % config.checkpoint_freq == 0):
        network = population[-1] #take the best network

        summed_reward = 0
        for i in range(config.episodes_to_solve):
            reward = network.playthrough(env)
            #print reward
            summed_reward += reward


        score = summed_reward/config.episodes_to_solve
        print 'Average score over ' + \
            str(config.episodes_to_solve) + ' episodes: ' + str(score) 
        np.savez(config.model_path + str(episode) + '.npz',\
            w_in = network.w_in, w_h = network.w_hidden, w_out = network.w_out)
        if (score > config.score_to_solve):
            print 'The game is solved!'
            break      
        
        print '\n\n\n\n\n'
        print network.w_in
        print '\n'
        print network.w_hidden
        print '\n'
        print network.w_out
        print '\n'
       
        sys.stdout.flush()

    #refill the population      
    mutants = []
    for i in range(int(config.mutate_per*config.num_policies)):
        curr_pol = np.random.choice(population) #p = Reward/sum(Reward))
        new_pol = copy_net(curr_pol)
        mutation(new_pol)
        mutants.append(new_pol)
    population += mutants



s = [0.02159946, -0.00569069, 0.00926815, -0.03274532]
a = network.predict(s)
print s
print a
    
        
