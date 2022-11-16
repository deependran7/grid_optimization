import numpy as np
from numpy.random import randint, rand

class Binary_Genetic_Algorithm():


    def __init__(self, objective=None,n_bits=None,n_iter=100,n_pop=10,r_cross=0.8,r_mut=0.3):
        self.objective = objective
        self.n_bits = n_bits
        self.n_pop = n_pop
        self.r_cross = r_cross
        self.r_mut = r_mut
        self.pop = np.array([randint(0,2,n_bits).tolist() for _ in range(n_pop)])
        self.scores = np.array([])
        self.n_iter = n_iter
        self.best_bits = np.zeros(n_bits)
        self.best_eval = np.inf
        

    #selection of the population
    def selection(self,pop,scores, k = 3):
        #first random selection
        selection_ix = randint(len(pop))
        for ix in randint(0,len(pop),k-1):
            if scores[ix]<scores[selection_ix]:
                selection_ix = ix
        return pop[selection_ix]

    def crossover(self,p1,p2, r_cross):
        c1,c2 = p1.copy(), p2.copy()
        if rand() < r_cross:
            pt = randint(1,len(p1)-2)
            #perform crossover
            c1 = np.concatenate([p1[:pt], p2[pt:]])
            c2 = np.concatenate([p2[:pt] , p1[pt:]])

        return np.array([c1,c2])


    def mutation(self,bitstring, r_mut):
        for i in range(len(bitstring)):
            #check for a mutation
            if rand()< r_mut:
                #flip the bit
                bitstring[i] = 1 - bitstring[i]


    def optimize(self):
        for gen in range(self.n_iter):
            self.scores = np.array([self.objective(c) for c in self.pop])
            for i in range(self.n_pop):
                if self.scores[i] < self.best_eval:
                    self.best_bits, self.best_eval = self.pop[i], self.scores[i]
                    #print(self.best_eval)
            
            #select parents
            selected = np.array([self.selection(self.pop,self.scores) for _ in range(self.n_pop)])
            childern = list()
            for i in range(0,self.n_pop,2):
                p1,p2 = selected[i], selected[i+1]
                #crossover and mututaion
                for c in self.crossover(p1,p2, self.r_cross):
                    self.mutation(c,self.r_mut)
                    childern.append(c)
            self.pop = childern
            print("Generation ", gen)
            print("Best Bits", self.best_bits)
            print("Best Cost", self.best_eval)
        
        return self.best_bits,self.best_eval