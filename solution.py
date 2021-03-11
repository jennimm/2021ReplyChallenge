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
print(W,H,N,M,R,buildings,antennas)

antennasRank = []
for x in range(len(antennas)):
    score = (antennas[x][0] + antennas[x][1]) // 2
    antennasRank.append([x, score])
antennasRank.sort(key = lambda x:x[1], reverse=True)

print(antennasRank)

    