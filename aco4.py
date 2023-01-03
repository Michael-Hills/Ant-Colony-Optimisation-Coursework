import sys
import numpy as np
import random
from numpy.random import choice
np.set_printoptions(threshold=sys.maxsize)


class ant:
    """
    class to contain all important information for an ant and its path
    path - the path taken
    cost - the cost of the path
    visited - locations currently visited by an ant
    availabe - locations still available to visit
    """
    def __init__(self):
        self.path = [None] * num_facilities
        self.cost = 0
        self.visited = []
        self.available = list(range(0,num_facilities))


def cost(distance, flow, path):
    """
    function to calculate the cost of a path
    distance - the distance matrix
    flow - the flow matrix
    path - the path to calculat cost
    returns the cost calculated
    """

    cost = 0
    #iterate through all links between locations
    for i in range(num_facilities):
        for j in range(num_facilities):
            cost += distance[i][j] * flow[path[i]][path[j]]

    return cost
    

def evaporate_pheromone(pheromone, e):
    """
    function to calculate new matrix after evaporatiom
    pheremone - current phereomone matrix
    e - the evaporation rate
    returns upated matrix
    """
    
    return np.multiply(pheromone,(1-e))

def deposit_pheromone(pheromone, ant):
    """
    function to calculate new matrix after depositing
    pheremone - current phereomone matrix
    ant - which ant is depositing
    returns upated matrix
    """

    for i in range(num_facilities - 1):
        #change values for both directions in the matrix
        pheromone[ants[ant].path[i]][ants[ant].path[i+1]] +=  1/ants[ant].cost
        pheromone[ants[ant].path[i+1]][ants[ant].path[i]] +=  1/ants[ant].cost 
     

    return pheromone
    
def generate_path(ant):
    """
    function to generate a path for an ant
    ant - the ant whos path it is
    """

    
    ants[ant].path = [None] * num_facilities              #reset ants path to none
    ants[ant].visited = []                      #reset visisted to none
    ants[ant].available = list(range(0,num_facilities))     #reset available to all

    #set start node randomly
    current = random.randint(0,num_facilities-1)
    for i in range(num_facilities):
        
        ants[ant].visited.append(current)       #add current node to visited
        ants[ant].path[int(current)] = i        #add current to path
        ants[ant].available.remove(current)     #remove current from availale
    
        #calculate the cumulative pheremone value for all available locations
        cumulative = 0
        if (len(ants[ant].available) > 0):
            for j in range(len(ants[ant].available)):
                cumulative += pheromone[current][ants[ant].available[j]]
        
        #calculate probability for all available locations (pheromone value/cumulative)
        probabilitites = []
        if (len(ants[ant].available) > 0):
            for j in range(len(ants[ant].available)):
                probabilitites.append((pheromone[current][ants[ant].available[j]])/cumulative)

        #select next node based on probabilities
        if (len(ants[ant].available) > 0):
            current = int(choice(ants[ant].available, 1, p=probabilitites))

if __name__ == "__main__":

    new_min = 999999999999999999
    e = 0.9     #evaporation rate
    m = 10      #number of ants
    np.random.seed(1264)    #random number seed

    #read number of facilities
    file = open('Uni50a.dat', 'r')
    num_facilities = int(file.readline())

    #create ant objects
    ants = []
    while len(ants) < m:
        ants.append(ant())
    
    #create distance and flow matrices from file
    distance = np.loadtxt('Uni50a.dat', usecols=range(num_facilities), skiprows= 2, max_rows = num_facilities, dtype=int)
    flow = np.loadtxt('Uni50a.dat', usecols=range(num_facilities), skiprows= 53, max_rows = num_facilities, dtype=int)

    #create random marix for number of facilities
    pheromone = np.random.rand(num_facilities, num_facilities)
    #make diagonal zeros
    np.fill_diagonal(pheromone, 0)  
    #make matrix symmetrical over diagonal
    low = np.tril_indices(num_facilities, 0) 
    pheromone[low] = pheromone.T[low]
   
    #compute 10000 fitness evaluations
    evalutaion = 0
    for i in range (int(10000/m)):
        for j in range(m):

            #generate m paths
            generate_path(j)
            ants[j].cost = cost(distance,flow,ants[j].path)     #calculate costs
            evalutaion += 1
            #if new best, save as new best
            if(ants[j].cost <= new_min):
                new_min = ants[j].cost
                print('New best found: ', new_min, 'at evaluation', evalutaion)
           
        #evaporate pheromone
        pheromone = evaporate_pheromone(pheromone,e)

        #deposit pheromone for each ant
        for j in range(m):
            pheromone = deposit_pheromone(pheromone,j)

            
    print("End: ", new_min)
    print(evalutaion)

            






