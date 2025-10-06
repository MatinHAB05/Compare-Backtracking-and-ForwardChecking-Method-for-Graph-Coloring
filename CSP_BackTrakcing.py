import math
import time
import sys
import gen_text
import os
import re
import shutil
import datetime

class Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for s in self.streams:
            s.write(data)
            s.flush()

    def flush(self):
        for s in self.streams:
            s.flush()

import networkx as nx
import matplotlib.pyplot as plt
 

# Defining a Class
import networkx as nx
import matplotlib.pyplot as plt

class GraphVisualization:
    def __init__(self):
        self.visual = []

    def addEdge(self, a, b):
        self.visual.append([a, b])

    def visualize(self, filename=None, dpi=300):
        plt.figure(figsize=(10,10))
        G = nx.Graph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G)

        if filename:
            # ذخیره با رزولوشن دلخواه
            plt.savefig(filename, dpi=dpi, bbox_inches='tight')
            plt.close()  # بستن شکل تا در حافظه نمونه‌ها نماند
        else:
            plt.show()

    @staticmethod
    def DrawGraph(consG, filename=None, dpi=300):
        G = GraphVisualization()
        L = set()
        for x in consG:
            for y in consG[x].neighbors.keys():
                if (y, x) in L:
                    continue
                L.add((x, y))
                G.addEdge(x, y)
        G.visualize(filename, dpi)



MAX_TIME_LENGTH_GLOBAL = 30

class DFS_BACKtracking_Coloring : 
    JJJ=0
    VERTEX_LIST = dict()
    DomainVertex = dict()
    DefaultColor=-97
    ColorDomain =[1,2,3,4]
    ConstraingGraph = dict()
    MAX_TIME_LENGTH = -1
    stratTime=0
    EndTime = 0
    failFlag = -1
    NoneAssignVar = []
    @staticmethod
    def initClassObj(ColorDom,VERTEX__LIST,constraint) :
        global MAX_TIME_LENGTH_GLOBAL
        DFS_BACKtracking_Coloring.VERTEX_LIST = VERTEX__LIST
        DFS_BACKtracking_Coloring.DefaultColor=-97
        DFS_BACKtracking_Coloring.ColorDomain = ColorDom[:]
        DFS_BACKtracking_Coloring.DomainVertex = { x:ColorDomain[:] for x in VERTEX__LIST.keys() }
        DFS_BACKtracking_Coloring.ConstraingGraph = constraint
        DFS_BACKtracking_Coloring.MAX_TIME_LENGTH = MAX_TIME_LENGTH_GLOBAL
        DFS_BACKtracking_Coloring.stratTime = time.time()
        DFS_BACKtracking_Coloring.EndTime = DFS_BACKtracking_Coloring.stratTime + DFS_BACKtracking_Coloring.MAX_TIME_LENGTH
        DFS_BACKtracking_Coloring.failFlag=-1
        DFS_BACKtracking_Coloring.NoneAssignVar=[xx for xx in VERTEX__LIST.keys() ]
    
    @staticmethod
    def DFS_BACK_Coloring(const_graph,meth,ColorDom,VerTex_list) :
        DFS_BACKtracking_Coloring.initClassObj(ColorDom,VerTex_list,const_graph)
        
        if meth=="BACK" : 
            return DFS_BACKtracking_Coloring.REC_BACK_DFS_Coloring(DFS_BACKtracking_Coloring.VERTEX_LIST,const_graph)
        elif meth=="FORWARDING" : 
            DFS_BACKtracking_Coloring.DomainVertex = { x:DFS_BACKtracking_Coloring.ColorDomain[:] for x in DFS_BACKtracking_Coloring.ConstraingGraph.keys() }
            return DFS_BACKtracking_Coloring.REC_BACK_Forward_Coloring(VerTex_list,const_graph)
    
    @staticmethod
    def REC_BACK_Forward_Coloring(AssignStatus,const_graph) :
        if DFS_BACKtracking_Coloring.EndTime < time.time() :
            DFS_BACKtracking_Coloring.failFlag=1
            return False

        if not DFS_BACKtracking_Coloring.NoneAssignVar :
            return True
        CurrentVarName = min(DFS_BACKtracking_Coloring.NoneAssignVar,key=lambda x : len(DFS_BACKtracking_Coloring.DomainVertex[x]))
        # CurrentVarName = min(AssignStatus,key=AssignStatus.get)
        # print(CurrentVarName)
        CurrentVar = {"key" :CurrentVarName , "value" :AssignStatus[CurrentVarName] }

        if not DFS_BACKtracking_Coloring.DomainVertex[CurrentVarName] : 
            return False

        for d in DFS_BACKtracking_Coloring.DomainVertex[CurrentVarName] : 
            AssignStatus[CurrentVar["key"]] = d
            DFS_BACKtracking_Coloring.NoneAssignVar.remove(CurrentVarName)
            # print(AssignStatus)
            # Forwarding....
            ll = DFS_BACKtracking_Coloring.ForwardingDeleteConstraint(CurrentVarName,d,DFS_BACKtracking_Coloring.DomainVertex,const_graph)

            status = DFS_BACKtracking_Coloring.REC_BACK_Forward_Coloring(AssignStatus,const_graph)
            if  status==False : 
                AssignStatus[CurrentVar["key"]] = DFS_BACKtracking_Coloring.DefaultColor
                DFS_BACKtracking_Coloring.NoneAssignVar.append(CurrentVarName)

                for Var,D in ll :
                    DFS_BACKtracking_Coloring.DomainVertex[Var].append(D)
                continue
            return True
        return False
        
    @staticmethod 
    def ForwardingDeleteConstraint(VertexCurrent,d,domVertex,const_g) :
        neighbor = const_g[VertexCurrent].neighbors
        ll = []
        for Var , obj in neighbor.items() : 
            if d in domVertex[Var] : 
                domVertex[Var].remove(d)
                ll.append((Var,d))
        return ll

    @staticmethod
    def REC_BACK_DFS_Coloring(AssignStatus,const_graph) :

        if DFS_BACKtracking_Coloring.EndTime < time.time() :
            DFS_BACKtracking_Coloring.failFlag=1
            return False
         
        flag=DFS_BACKtracking_Coloring.ValiditionAssignment(AssignStatus,const_graph)
        # print(flag)
        if flag==True:
            return True
        elif flag is not None and flag == False :
            return False
        
        CurrentVarName = DFS_BACKtracking_Coloring.NoneAssignVar[0]
        # print(CurrentVarName)
        CurrentVar = {"key" :CurrentVarName , "value" :AssignStatus[CurrentVarName] }
        
        for d in DFS_BACKtracking_Coloring.ColorDomain : 
            AssignStatus[CurrentVar["key"]] = d
            # print(AssignStatus)
            DFS_BACKtracking_Coloring.NoneAssignVar.remove(CurrentVarName)
            status = DFS_BACKtracking_Coloring.REC_BACK_DFS_Coloring(AssignStatus,const_graph)
            if  status==False : 
                AssignStatus[CurrentVar["key"]] = DFS_BACKtracking_Coloring.DefaultColor
                DFS_BACKtracking_Coloring.NoneAssignVar.append(CurrentVarName)
                continue
            return True
        return False

    @staticmethod
    def ValiditionAssignment(ass_status,const_graph) : 

        flag = True
        for L_name , L_obj in const_graph.items() :
            for R_name , R_obj  in L_obj.neighbors.items() :
                color_L = ass_status[L_name]
                color_R = ass_status[R_name]
                if color_L==DFS_BACKtracking_Coloring.DefaultColor or color_R==DFS_BACKtracking_Coloring.DefaultColor :
                    flag=None
                if color_L==color_R  and not ( color_L==DFS_BACKtracking_Coloring.DefaultColor or color_R==DFS_BACKtracking_Coloring.DefaultColor):
                    # print("****",L_name,color_L,color_R,R_name)
                    return False
        if flag==None :
            return None
        
        return True
    
class NodeStar : 
    def __init__(self,name,the_neighbors=None,the_color=DFS_BACKtracking_Coloring.DefaultColor):
        self.color = the_color
        self.neighbors = the_neighbors if the_neighbors is not None else dict()
        self.name=name 

#
DefaultColor = DFS_BACKtracking_Coloring.DefaultColor
ColorDomain = [1,2,3,4,5]
VERTEX_LIST = dict()
Constraing_Graph = dict()

def Exe_CSP(method) : 
        
        print("start Exe:",method,"~~~~~~~~~")
        start = time.time()
        status=DFS_BACKtracking_Coloring.DFS_BACK_Coloring(Constraing_Graph,method,ColorDomain,VERTEX_LIST)
        end = time.time()
        if DFS_BACKtracking_Coloring.failFlag==-1 :
            print(status)
        else :
            print("Out of Time!!!    MAX_TIME =",DFS_BACKtracking_Coloring.MAX_TIME_LENGTH)
        print((end-start)*1000," ms")
        print(VERTEX_LIST)    
        return end - start
#
Constraing_Graph = dict()
VERTEX_LIST = dict()
def CreateTestCase(Probility_Edge) : 
    global Constraing_Graph
    global VERTEX_LIST
    Constraing_Graph=dict()
    VERTEX_LIST = dict()
    gen_text.main(Probility_Edge)
    with open("testCase2.txt",'r') as f : 
        Lines =  f.readlines()

        for line in Lines:
            L,R = line.strip().split(",")

            if L==R :
                continue

            if L not in Constraing_Graph.keys() :
                Constraing_Graph[L]=NodeStar(name=L)


            if R not in Constraing_Graph.keys() :
                Constraing_Graph[R]=NodeStar(name=R)


            if R not in Constraing_Graph[L].neighbors.keys() :
                Constraing_Graph[L].neighbors[R]=Constraing_Graph[R]
                # print("L:",L,"R:",R)

            if L not in Constraing_Graph[R].neighbors.keys() :
                Constraing_Graph[R].neighbors[L] = Constraing_Graph[L]  
                # print("R:",R,"L:",L)
            # print("###",Constraing_Graph[R].neighbors.keys())

            VERTEX_LIST[L] = DefaultColor
            VERTEX_LIST[R] = DefaultColor

# meth = "FORWARDING"
(lambda pattern :  ( [    (  os.remove(os.path.join(".", objF))  if re.match(pattern,objF) else None,None)[1]  for objF in os.listdir(".") ], None)[1])(r"^testCase_\d+\.png$")

with open("resault.txt",'w') as res :
    sys.stdout = Tee(sys.__stdout__, res)
    print("ColorDomian : ",ColorDomain)
    TIME_avg_FOREWARDING = 0
    TIME_avg_BACK = 0
    iter = 0
    fail_FORWARD = 0
    fail_BACK = 0
    for I in range(1,25) : 
        if (I-1)%5 ==0 :
            iter+=0.05 
            print("\n=====Probility_Edge : ",iter,"========\n")


        print("\n*********",I,"************")
        print("\ntest Case Building...")
        CreateTestCase(iter)
        time.sleep(1)
        print("test Case Build Finished!")
        print("\nBuild Visual : ")
        GraphVisualization.DrawGraph(Constraing_Graph,"testCase_"+str(I))
        print("\nBuild Visual Finished...")

        print("\n")

        Len_Forw = Exe_CSP("FORWARDING")
        if DFS_BACKtracking_Coloring.failFlag==1 : 
            fail_FORWARD+=1
            TIME_avg_FOREWARDING = TIME_avg_FOREWARDING*(I-1) + TIME_avg_FOREWARDING            
        else :
            TIME_avg_FOREWARDING = TIME_avg_FOREWARDING*(I-1) +( (Len_Forw)*1000)

        TIME_avg_FOREWARDING = TIME_avg_FOREWARDING / I

        Len_Back = Exe_CSP("BACK")
        if DFS_BACKtracking_Coloring.failFlag==1 : 
            fail_BACK+=1
            TIME_avg_BACK = TIME_avg_BACK*(I-1) + TIME_avg_BACK            

        else :
            TIME_avg_BACK = TIME_avg_BACK*(I-1) +( (Len_Back)*1000)

        TIME_avg_BACK = TIME_avg_BACK / I

        print("############",I,"###########\n")
    print("\n\n@@@@@@@@@ FORWRDING : " ,TIME_avg_FOREWARDING,"ms @@@@@@@@@@@\n\n")
    print("\n\n@@@@@@@@@ Fail FORWRDING : " ,fail_FORWARD," @@@@@@@@@@@\n\n")
    print("\n\n@@@@@@@@@ BACK : " ,TIME_avg_BACK,"ms @@@@@@@@@@@\n\n")
    print("\n\n@@@@@@@@@ Fail BACK : " ,fail_BACK," @@@@@@@@@@@\n\n")


    
    sys.stdout = sys.__stdout__

# path where original file is located
sourcePath = "resault.txt"

# path were a copy of file is needed
destinationPath = f"Outputs__resault/resault__{datetime.datetime.fromtimestamp(int(time.time()))}.txt".replace(":","%")

# call copyfile() method
shutil.copyfile(sourcePath, destinationPath)

