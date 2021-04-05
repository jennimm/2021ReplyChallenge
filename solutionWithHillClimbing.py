# import numpy
import random

filename = 'data_scenarios_b_mumbai.in'
data = open(filename,'r')
W,H = (int(x) for x in data.readline().split())
N,M,R = (int(x) for x in data.readline().split())
buildings = []
plan = []
for x in range(W):
    width = []
    for y in range(H):
        width.append("*")
    plan.append(width)

for i in range(N):
    buildings.append([int(x) for x in data.readline().split()])
for i in range (len(buildings)):
    id_build='id'+str(i)
    buildings[i].append(id_build)
    plan[buildings[i][0]][buildings[i][1]] = id_build
    
antennas = []
for i in range(M):
    antennas.append([int(x) for x in data.readline().split()])

def antennasRanking(antennas):
    antennasRank = []
    for x in range(len(antennas)):
        score = (antennas[x][0] + antennas[x][1]) // 2
        antennasRank.append([x, score])
    antennasRank.sort(key = lambda x:x[1], reverse=True)
    return antennasRank

def buildingRanking(buildings):
    buidlingRank = []
    for x in range(len(buildings)):
        score = buildings[x][2]
        buidlingRank.append([buildings[x][-1], score])
    buidlingRank.sort(key = lambda x:x[1], reverse=True)
    return buidlingRank

def distanceBetween(x, y):
    return abs(x[0]-y[0])+abs(x[1]-y[1])

def buildingAntennaScore(building, antenna,antenna_range):
    #check the index is correct
    buildingPos = [building[1], building[2]]
    antennaPos = [antenna[1], antenna[2]]
    distance = distanceBetween(buildingPos, antennaPos)
    antennaconnection = antennas[antenna[0]][-1]
    if antenna_range <= distance:
        return (building[-2] * antennaconnection ) - (building[3] * distance)
    return 0

# def getantennascore(antenna):
#     score = 0
#     for i in buildings:
#         score = score + buildingAntennaScore(i,antenna)
#     return score

def getScore(solution,antennas):
    score = 0
    for i in range(len(solution)):
        antenna_range = antennas[i][0]
        x =solution[i]
        for j in buildings:
            print(j)
            score = score + buildingAntennaScore(j,x,antenna_range)
    return score

def hillclimbing(buildings, antennas):
    # for optimization
    bestsolution = []
    placed = []
    for i in range(len(antennas)):
        x = random.randint(0,W)
        y = random.randint(0,H)
        if [x,y] not in placed:
            bestsolution.append([i,x,y])
            placed.append([x,y])
    bestscore = getScore(bestsolution,antennas)
    for j in range(15):
        print(bestscore)
        placed = []
        newsolution = []
        for i in range(len(antennas)):
            print(i)
            x = random.randint(0,W)
            y = random.randint(0,H)
            if [x,y] not in placed:
                newsolution.append([i,x,y])
                placed.append([x,y])
        newscore = getScore(newsolution,antennas)
        if newscore > bestscore:
            bestscore = newscore
            bestsolution = newsolution
    return bestsolution


def output(antenna):
    # antennas = [id,x,y]
    pos =  filename.find('.')
    outname = filename[:pos]+'hillclimbing.out'
    f = open(outname,'w')
    f.writelines(str(len(antenna))+"\n")
    for i in antenna:
        line = ' '.join(str(e) for e in i)
        line = line + "\n"
        f.writelines(line)
    f.close()

def run():
    sol = hillclimbing(buildings,antennas)
    output(sol)
    
run()