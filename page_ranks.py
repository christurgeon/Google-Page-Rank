import random
import queue
import json

# ------------------------------------------------------------------------------

# Build the graph
def buildGraph(n, p):
    # Initialize the graph
    graph = [[0] * n for i in range(n)]
    # Add nodes to the adjacency matrix graph
    for i in range (n):
        for j in range(i, n):
            q = random.random()
            if (q < p and i < j and graph[i][j] == 0):
                graph[i][j] = 1
            elif (q < p and i == j and graph[i][j] == 0):
                graph[i][j] = 1
    return graph


# Print the graph
def printGraph(G):
    for i in G:
        print(i)
    print("")

# ------------------------------------------------------------------------------

# Keeps track of the frequencies
def updateFreq(tracker, number):
    if (number in tracker):
        tracker[number] = tracker[number] + 1
    else:
        tracker[number] = 1


# - The first page rank algorithm
# - Takes a random walk across webpages and for large T values should
#   display similar results to Google's actual PageRank algorithm which
#   is the PageRankTwo function below
def pageRankOne(graph, d, T):
    freqTracker =  dict()
    A = 0
    Q = queue.Queue(maxsize=T)
    for t in range(T):
        next = -1
        p = random.random()

        # p < d so choose a random hyperlink that leaves A
        if (p < d):
            links = []
            for i in range(n):
                if (graph[i][A] == 1):
                    links.append(i)
            next = random.choice(links)
            if (len(links) == 0): # If there are no links leaving A, choose random
                links = [l for l in range(0, n)]
                next = random.choice(links)

        # p > d so choose a random link
        else:
            links = [l for l in range(0, n)]
            next = random.choice(links)

        # 1. Update the frequency of the chosen site
        # 2. Add the clicked link to the Q
        # 3. Set A to the clicked link
        updateFreq(freqTracker, next)
        Q.put(next)
        A = next
    return freqTracker

# ------------------------------------------------------------------------------

# Returns a list with all nodes and the number of links that point to them
def outgoingLinks(graph):
    n = len(graph)
    links = [0] * n
    for i in range(n):
        for j in range(n):
            if (graph[j][i] == 1):
                links[i] += 1
    return links


# Calculates (PR_t(A)/L(A) + PR_t(B)/L(B) + PR_t(C)/L(C) + PR(D)/L(D) +...)
def probabilityDist(graph, page, pageRanks, outgoingLinks):
    sum = 0
    for pr in range(len(pageRanks)):
        if (graph[page][pr] == 1):
            sum += float(pageRanks[pr] / outgoingLinks[pr])
    return sum


# The second page rank algorithm
def pageRankTwo(graph, d, T):
    # Create a list that stores the number of websites
    # that i links to for i = 0...n
    L = outgoingLinks(graph)

    # Initialize the array to all [1/n, ..., 1/n]
    n = len(graph)
    pageRank = [1/n for i in range(n)]
    for i in range(T):
        for r in range(n):
            sum = probabilityDist(graph, r, pageRank, L)
            newVal = (1-d)/n + d*sum
            pageRank[r] = newVal

    # Output the results
    sum = 0
    for pr in range(n):
        sum += pageRank[pr]
        print("Page: ",pr,"   Rank: ",pageRank[pr])

# ------------------------------------------------------------------------------

if __name__ == "__main__":
    graphType = input("Enter \"dat\" for json and anything else for a random graph => ").strip()
    T = int(input("Enter a value for T >= 1:  "))
    d = 0.9
    print("\n=============== PAGE RANK 1 ===============\n")

    if (graphType == "dat"):
        datafile = open("lab5.dat", "r")
        graph = json.load(datafile)
        datafile.close()
        n = len(graph)
        printGraph(graph)
    else:
        n = random.randint(1, 10)
        p = random.random()
        graph = buildGraph(n, p)
        printGraph(graph)

    # Get the frequencies of all webpages in Q.
    ret = pageRankOne(graph, d, T)
    for k,v in ret.items():
        print("Page: ",k,"   Rank: ",float(v/T),"\tFrequency: ",v)
    print("\n=============== PAGE RANK 2 ===============\n")
    pageRankTwo(graph, d, T)
