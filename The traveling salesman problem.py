
import numpy as np 
import matplotlib.pyplot as plt
import random
from distance_matrix import distance_matrix, park_names #we import from other script the distance matrix of the cities
import time
start_time = time.time()

def generate_parks(number_cities,poblation): #we generate the random population of parks 
    generator=[]
    for i in range(poblation):
        middle=(np.random.choice(range(1, number_cities+1), number_cities, replace=False))#random combination of cities 
        vector=[0]+middle.tolist()+[number_cities+1] #fixed the first and the last city 
        generator.append(vector)
    return generator

def distance(city1,city2): #give the distance between cities
    return distance_matrix[city1,city2] 

def total_distance(route):
    return sum(distance(route[i], route[i+1]) for i in range(len(route)-1)) #the computation of the route's total distance

def tournament(population,size=3):
    a=sorted(random.sample(population,size),key=lambda route: total_distance(route)) #we select the routes with smallest distance
    return a[0]
def crossover(parent1,parent2):
    size=len(parent1)
    start,end=sorted(random.sample(range(1,size),2)) #the crossover between the best population to create a "child"
    child=[-1]*size
    child[0]=parent1[0]
    child[-1]=parent1[-1]
    child[start:end]=parent1[start:end]
    parent2_values=[parks for parks in parent2 if parks not in child]
    fill_idx=0
    for i in range(size):
        if child[i] == -1:
            child[i] = parent2_values[fill_idx]
            fill_idx += 1
    return child 

def mutation(cld,mr): #the mutation process
    if random.random() < mr:
        i,j = sorted(random.sample(range(1,len(cld)-1), 2)) # we exchange indices in the child vector    
        cld[i],cld[j]=cld[j],cld[i]
    return cld
    
number_cities=len(distance_matrix[0,:])-2
poblation=1000
generation=300
population=generate_parks(number_cities, poblation) #generate the first population 
initial_population=population 

best_route=[]
best_distance=best_distance = float('inf')
mutation_rate=0.2 #the mutation probability
for generation in range(generation): #the genetic algorithm 
    new_population=[]
    population = sorted(population, key=lambda route: total_distance(route)) 
    if total_distance(population[0]) < best_distance:
        best_distance = total_distance(population[0])
        best_route = population[0]
        
    new_population = [population[0]] # Keep the best route (elitism)
    while len(new_population)< len(population):
        parent1=tournament(population)
        parent2=tournament(population)        
        child=crossover(parent1, parent2)
        child=mutation(child,mutation_rate)
        new_population.append(child)
    population=new_population
    if generation % 20 == 0: #print the generation and the best distance
        print(f"Generation {generation}: Best Distance = {best_distance:.2f}")     
        
        
route=[park_names[i] for i in best_route] 
print("--- %s seconds ---" % (time.time() - start_time))