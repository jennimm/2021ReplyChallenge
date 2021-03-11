import numpy

filename = 'data_scenarios_a_example.in'
data = open(filename,'r')
W,H = (int(x) for x in data.readline().split())
N,M,R = (int(x) for x in data.readline().split())
buildings = []
for i in range(N):
    buildings.append([int(x) for x in data.readline().split()])
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
        buidlingRank.append([x, score])
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

def generateSolution():
    pass


def getNeighbours(solution):
    pass

def hillclimbing(building,antenna):
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
    for i in antenna:
        line = ' '.join(str(e) for e in i)
        line = line + "\n"
        f.writelines(line)
    f.close()

rankOfAntennas = antennasRanking(antennas)
rankOfBuildings = buildingRanking(buildings)
adjacentBuildings = findAdjBuildings(buildings)


    