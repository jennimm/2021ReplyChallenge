import numpy
from copy import deepcopy

filename = 'data_scenarios_a_example.in'
data = open(filename,'r')
W,H = (int(x) for x in data.readline().split())
N,M,R = (int(x) for x in data.readline().split())
buildings = []
for i in range(N):
    buildings.append([int(x) for x in data.readline().split()])
for i in range (len(buildings)):
    id_build='id'+str(i)
    buildings[i].append(id_build)
antennas = []
for i in range(M):
    antennas.append([int(x) for x in data.readline().split()])
print(buildings)
print(antennas)

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

def findAdjBuildings(buildings):
    buildings_adj=[]
    for j in range (len(buildings)):
        x=buildings[j][0]
        y=buildings[j][1]
        building=[]
        building.append(buildings[j][4])
        for k in buildings:
            if (x-2) <= k[0] <= (x+2) or (y-2) <= k[1] <= (y+2):
                if k[4] != building[0]:
                    building.append(k[4])
        buildings_adj.append(building)
    return buildings_adj

def distanceBetween(x, y):
    return numpy.abs(x-y).sum()

def buildingAntennaScore(building, antenna):
    #check the index is correct
    buildingPos = numpy.array(building[1], building[2])
    antennaPos = numpy.array(antenna[2], antenna[3])
    score = ( building[-1] * antenna[-1] ) - (building[3] * distanceBetween(buildingPos, antennaPos))
    return score

def generateSolution(position, rankOfAntennas, rankOfBuildings, adjacentBuildings, buildings):
    buildingsPlaced = deepcopy(rankOfBuildings)
    noAllocatedAntenna = []
    solution = []
    idsPlaced = []
    x = 0
    while x < len(rankOfAntennas):
        if x == 0: 
            buildingId = int(buildingsPlaced[0][0][2:])
        else:
            print(noAllocatedAntenna[0][0][2:])
            buildingId = int(noAllocatedAntenna[0][0][2:])
        if len(buildingsPlaced) == 0:
            for j in range(len(noAllocatedAntenna)):
                if j not in idsPlaced:
                    buildingsPlaced.append(noAllocatedAntenna[j])
        
        xPos = buildingsPlaced[0][0]
        rankOfAntennas[x].append(xPos)
        y = 0
        while y < len(buildingsPlaced):
            if buildingsPlaced[y][0] in adjacentBuildings[buildingId]:
                if y != buildingId:
                    noAllocatedAntenna.append(buildingsPlaced[y])
                else:
                    idsPlaced.append(buildingId)
                del buildingsPlaced[y]
                y -= 1
            y += 1
        positionArray = []
        positionArray.append(rankOfAntennas[x][0])
        positionArray.append(buildings[int(rankOfAntennas[x][-1][2:])][0])
        positionArray.append(buildings[int(rankOfAntennas[x][-1][2:])][1])
        x += 1
        solution.append(positionArray)
    return solution



def getNeighbours(solution,W,H):
    # where solution is just a pair of coordinates
    x = solution[0]
    y = solution[1]
    neighbours = []
    if (x<W):
        neighbours = neighbours+[x+1,y]
    if (x > 0):
        neighbours = neighbours+[x-1,y]
    if (y < H):
        neighbours = neighbours+[x,y+1]
    if y > 0:
        neighbours = neighbours+[x,y-1]
    return neighbours

def getBestNeighbour(building,antenna,neighbours):
    score = buildingAntennaScore(building,antenna)
    bestNeighbour = neighbours[0]
    for n in neighbours:
        pass

def hillclimbing(building, antenna):
    # for optimization
    currentsolution = generateSolution()
    currentscore = buildingAntennaScore(building,antenna)
    neighbours = getNeighbours(currentsolution)
    bestNeighbour, bestNeighbourscore = getBestNeighbour(building,antenna, neighbours)
    while bestNeighbourscore < currentscore:
        currentsolution= bestNeighbour
        currentscore = bestNeighbourLength
        neighbours = getNeighbours(currentsolution)
        bestNeighbour,bestNeighbourscore = getBestNeighbour(building,antenna,neighbours)
    return currentscore,currentsolution

def output(antenna):
    # antennas = [id,x,y]
    outname = filename[0]+'out.txt'
    f = open(outname,'w')
    f.writelines(str(len(antenna)))
    for i in antenna:
        line = ' '.join(str(e) for e in i)
        line = line + "\n"
        f.writelines(line)
    f.close()

rankOfAntennas = antennasRanking(antennas)
rankOfBuildings = buildingRanking(buildings)
adjacentBuildings = findAdjBuildings(buildings)
print(antennas)
print(buildings)
print(rankOfBuildings)
print(adjacentBuildings)
print(generateSolution(0, rankOfAntennas, rankOfBuildings, adjacentBuildings, buildings))

    