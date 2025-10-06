import random
import numpy

def main(P_Edge=0.1) : 
    Graph = [[0 for _ in range(51)] for _ in range(51)]
    with open("testCase2.txt",'w') as f :
        for x in range(51) :
            for y in range(x+1,51) :
                Graph[x][y]=Graph[y][x]=numpy.random.choice(2,size=1, p=[1-P_Edge,P_Edge])
                if Graph[x][y] ==1 : 
                    f.write(f"{x},{y}\n")

