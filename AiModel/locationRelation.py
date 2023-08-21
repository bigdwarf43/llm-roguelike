import networkx as nx
import random


class locationRelation:
    def __init__(self, locations) -> None:
        self.locations = locations
        self.affinityGraph = nx.Graph()


    def createAffinityGraph(self):
        self.affinityGraph.add_nodes_from(self.locations)

        # Generate random affinity matrix with positive and negative values
        affinity_matrix = []
        for i in range(len(self.locations)):
            row = []
            for j in range(len(self.locations)):
                if i == j:
                    row.append(0)  # No affinity with itself
                else:
                    affinity = random.randint(-10, 10)  # Random affinity value between -10 and 10
                    row.append(affinity)
            affinity_matrix.append(row)
        
        for i in range(len(self.locations)):
            for j in range(i + 1, len(self.locations)):
                affinity = affinity_matrix[i][j]
                if affinity != 0:
                    self.affinityGraph.add_edge(self.locations[i], self.locations[j], affinity=affinity)


    def getCorrespondingLocations(self, location):
        max_affinity = float('-inf')
        min_affinity = float('inf')

        friend = ""
        enemy = ""

        for neighbour in self.affinityGraph.neighbors(location):
            affinity = self.affinityGraph.get_edge_data(location, neighbour)['affinity']

            if affinity > max_affinity:
                max_affinity = affinity
                friend = neighbour
            elif affinity < min_affinity:
                min_affinity = affinity
                enemy = neighbour

        # print(friend, enemy)
        return friend, enemy
        
        # Print the graph's edges and affinity values
        # print("Edges and affinity values of the graph:")
        # for edge in self.affinityGraph.edges(data=True):
        #     print(edge)

# obj = locationRelation(["A", "b", "C", "D", "E", "F"])
# obj.createAffinityGraph()
# obj.getCorrespondingLocations("A")