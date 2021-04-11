import numpy
from copy import deepcopy

filename = 'data_scenarios_f_tokyo.in'
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

def findAdjBuilding(buildings):
    buildings_adj=[]
    for j in range(len(buildings)):
        #random = iter(buildings)
        x=buildings[j][0]
        y=buildings[j][1]
        building=[buildings[j][4]]
        for k in range(j+1, len(buildings)):
            if (x-2) >= 0 and (x+2) <= W and (y-2) >= 0 and (y+2) <= H :
                if (x-2) <= buildings[k][0] <= (x+2) or (y-2) <= buildings[k][1] <= (y+2):
                    if buildings[k][4] != building[0]:
                        building.append(buildings[k][4])
                buildings_adj.append(building)
    return buildings_adj

def findNext(y,x, plan):
    nextTo = []
    
    for i in range(3):
        if 0 < x < H-1:
            if plan[y-i][x] != '*':
                nextTo.append(plan[x-i][y])
        if 0 < y < W-1:
            if plan[y-1][x-i] != '*':
                nextTo.append(plan[x][y-i])
    return nextTo

def findAdjBuildings(buildings, W, H, plan):
    buildings_adj=[]
    for j in range(len(buildings)):
        x=buildings[j][0]
        y=buildings[j][1]
        building=buildings[j][4]
        #for k in range(len(buildings)):
        adj = findNext(x,y,plan)
        if adj == []:
            array = [building]
        else:
            adj = "".join(adj)
            array = [building, adj]
        #buildings_adj.append(building)
        buildings_adj.append(array)
    return buildings_adj

def distanceBetween(x, y):
    return numpy.abs(x-y).sum()

def buildingAntennaScore(building, antenna):
    #check the index is correct
    buildingPos = numpy.array(building[1], building[2])
    antennaPos = numpy.array(antenna[2], antenna[3])
    score = ( building[-1] * antenna[-1] ) - (building[3] * distanceBetween(buildingPos, antennaPos))
    return score

def basicGenerateSolution(position, rankOfAntennas, rankOfBuildings, adjacentBuildings, buildings):
    buildingsPlaced = deepcopy(rankOfBuildings)
    noAllocatedAntenna = []
    solution = []
    idsPlaced = []
    x = 0
    while x < len(rankOfAntennas):
        #if x == 0:
        buildingId = int(buildingsPlaced[0][0][2:])
        #else:
            #buildingId = int(noAllocatedAntenna[0][0][2:])
        # if len(buildingsPlaced) == 0:
        #     for j in range(len(noAllocatedAntenna)):
        #         if j not in idsPlaced:
        #             buildingsPlaced.append(noAllocatedAntenna[j])
        
        xPos = buildingsPlaced[0][0]
        rankOfAntennas[x].append(xPos)
        y = 0
        while y < len(buildingsPlaced):
            if buildingsPlaced[y][0] in adjacentBuildings[buildingId]:
                if int(buildingsPlaced[y][0][2:]) != buildingId:
                   # noAllocatedAntenna.append(buildingsPlaced[y])
                   pass
                else:
                    idsPlaced.append(buildingId)
                #del buildingsPlaced[y]
                y -= 1
            y += 1
        positionArray = []
        positionArray.append(rankOfAntennas[x][0])
        positionArray.append(buildings[int(rankOfAntennas[x][-1][2:])][0])
        positionArray.append(buildings[int(rankOfAntennas[x][-1][2:])][1])
        x += 1
        solution.append(positionArray)
        if x > 10:
            x = len(rankOfAntennas)
    return solution

def findCoords(ids, W, H, plan):
    for x in range(W):
        for y in range(H):
            if plan[x][y] == ids:
                return [x,y]
    else:
        return []

def generateSolution(position, rankOfAntennas, rankOfBuildings, adjacentBuildings, buildings, W, H, plan):
    buildingsPlaced = deepcopy(rankOfBuildings)
    noAllocatedAntenna = []
    solution = []
    ignore = []
    idsPlaced = []
    for x in range(len(rankOfAntennas)):
        #if x == 0:
        idFound = False
        p = 0
        while idFound == False:
            if p not in idsPlaced and ("id"+str(p)) not in ignore:
                buildingId = p
                idFound = True
            else:
                p += 1
                if p == len(buildingsPlaced):
                    ignore = []
                    p = 0

        rankOfAntennas[x].append(buildingId)
        #ignore = adjacentBuildings[buildingId]
        coord = findCoords("id"+str(buildingId), W, H, plan)
        if coord != []:
            ignore = plan[coord[0]][coord[1]]
        else:
            ignore = []
        if p > 2500:
            x = len(rankOfAntennas)
            break
        #del ignore[0]
        idsPlaced.append(buildingId)
        positionArray = []
        positionArray.append(rankOfAntennas[x][0])
        positionArray.append(buildings[rankOfAntennas[x][-1]][0])
        positionArray.append(buildings[rankOfAntennas[x][-1]][1])
        
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
    rankOfAntennas = antennasRanking(antennas)
    rankOfBuildings = buildingRanking(buildings)
    adjacentBuildings = findAdjBuildings(buildings)
    currentsolution = generateSolution(position, rankOfAntennas, rankOfBuildings, adjacentBuildings, buildings)
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
    pos =  filename.find('.')
    outname = filename[:pos]+'.out'
    f = open(outname,'w')
    f.writelines(str(len(antenna))+"\n")
    for i in antenna:
        line = ' '.join(str(e) for e in i)
        line = line + "\n"
        f.writelines(line)
    f.close()

rankOfAntennas = antennasRanking(antennas)
rankOfBuildings = buildingRanking(buildings)
adjacentBuildings = findAdjBuildings(buildings,W, H, plan)

sol = (generateSolution(0, rankOfAntennas, rankOfBuildings, adjacentBuildings, buildings, W, H, plan))
output(sol)
    
