from copy import deepcopy

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
        adj = findNext(x,y,plan)
        if adj == []:
            array = [building]
        else:
            adj = "".join(adj)
            array = [building, adj]
        buildings_adj.append(array)
    return buildings_adj

def findCoords(ids):
    num = int(ids[2:])
    x = buildings[num][0]
    y = buildings[num][1]
    return [x,y]

def generateSolution(position, rankOfAntennas, rankOfBuildings):
    buildingsPlaced = deepcopy(rankOfBuildings)
    solution = []
    for x in range(len(rankOfAntennas)):
        buildingId = buildingsPlaced[x][0]
        rankOfAntennas[x].append(buildingId)
        coord = findCoords(buildingId)
        positionArray = [rankOfAntennas[x][0],coord[0],coord[1]]
        solution.append(positionArray)
    return solution

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

sol = (generateSolution(0, rankOfAntennas, rankOfBuildings))
output(sol)