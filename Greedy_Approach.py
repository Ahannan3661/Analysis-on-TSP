import math
import numpy as np
import matplotlib.pyplot as plt
import time

def get_length(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1.0 / 2.0)


def build_graph(data):
    graph = {}
    for this in range(len(data)):
        for another_point in range(len(data)):
            if this != another_point:
                if this not in graph:
                    graph[this] = {}

                graph[this][another_point] = get_length(data[this][0], data[this][1], data[another_point][0],
                                                        data[another_point][1])

    return graph


# this returns distanceMatrix, an
# array of arrays of the distances from
# each city to each other city.
def getDistanceMatrix(cities):
    distanceMatrix = []
    for currentNode in cities:
        subArray = []
        for comparisonNode in cities:
            subArray.append(getDistanceBetweenTwoCities(currentNode, comparisonNode))
        distanceMatrix.append(subArray)
    print("dis_matrix is: ", distanceMatrix)
    return distanceMatrix


# city1 and city2 are both arrays like, [id, X-coordinate, Y-coordinate]
def getDistanceBetweenTwoCities(city1, city2):
    global global_count
    x1 = city1[1]
    y1 = city1[2]
    x2 = city2[1]
    y2 = city2[2]
    numToGetSquareRootOf = ((pow((x1 - x2), 2)) + (pow((y1 - y2), 2)))
    global_count += 6
    if numToGetSquareRootOf < 0:
        numToGetSquareRootOf *= -1
        global_count += 1
    return int(round(math.sqrt(numToGetSquareRootOf)))


############### getNearestCity #################
# Returns the closest city to city with id cityID
def getNearestCity(distanceMatrix, cityId):
    global global_count
    i = 0
    for distanceList in distanceMatrix:
        if i == cityId:
            smallestDistance = min(idx for idx in distanceList if idx > 0)
            global_count += len(distanceList)
            if smallestDistance > 9999 * 3:
                return -1, -1
            else:
                return smallestDistance, distanceList.index(smallestDistance)
        i += 1


############### getNeighborCities ##############
# Returns the closest two cities in distanceMatrix
def getNeighborCities(distanceMatrix):
    closeCity_1 = 0
    closeCity_2 = -1
    smallestDistance = 99999
    for distanceList in distanceMatrix:
        temp = min(i for i in distanceList if i > 0)
        if temp < smallestDistance:
            smallestDistance = temp
            closeCity_1 = distanceList.index(smallestDistance)
            closeCity_2 = distanceMatrix.index(distanceList)
    return closeCity_1, closeCity_2


############### bestBetweenCities ##############
# Finds the best city between two cities, given
# arrays of each of their distances to other cities.
# This is the only one I don't actually use in this
# program, but leaving here for future reference in
# case someone would want to uses this for a different
# algorithm.
def bestBetweenCities(distArray_1, distArray_2):
    minDist = 99999 * 2
    minIndex = -1
    for i in range(0, len(distArray_1)):
        fromBoth = distArray_1[i] + distArray_2[i]
        if fromBoth < minDist:
            minDist = fromBoth
            minIndex = i
    return minDist, minIndex


########## getDistanceForTripHome ##############
# Return the distane between the first and last
# cities in the path

def getDistanceForTripHome(thePath, cities):
    global global_count
    for city in cities:
        # print("City is: ", city)
        if city[0] == thePath[0]:  # If first city in path
            firstCity = city
        if city[0] == thePath[len(thePath) - 1]:  # If last city in path
            lastCity = city
        global_count += 2
    return getDistanceBetweenTwoCities(firstCity, lastCity)


################## addCity ##################
# Adds city to pathArray and removes it from citiesToVisit.
# Modifies: pathArray, citiesToVisit, distanceList

def addCity(pathArray, citiesToVisit, distanceMatrix, city_id):
    global global_count
    pathArray.append(city_id)
    prev_city_id = pathArray[len(pathArray) - 2]
    for city in citiesToVisit:
        if city[0] == prev_city_id:
            global_count += 1
            citiesToVisit.remove(city)
    global_count += len(distanceMatrix)
    for distanceList in distanceMatrix:
        distanceList[prev_city_id] = 99999


################## chooseCity ##################
# Return success flag, id of the city with the best distance between
# the middle 2 cities in citiesToVisit, and midIndex_2

def chooseCity(pathArray, citiesToVisit, distanceMatrix):
    global global_count
    if len(pathArray) == 0:  # If path empty, return starting node
        return 0, 0, 0

    bestDistance, idOfBestCity = getNearestCity(distanceMatrix, pathArray[(len(pathArray) - 1)])

    if idOfBestCity == -1:
        return -1, -1, -1  # Indicates we are done visiting cities
    return 0, idOfBestCity, bestDistance


############### findBestPath ###################
# Returns the best path

def findBestPath(distanceMatrix, cities_to_add):
    # startingCity, endingCity = getNeighborCities(distanceMatrix)
    global global_count
    pathArray = []  # array to hold the paths that we will use
    flag = 0  # Holds flag as to weather we are done adding cities
    totalDistance = 0  # Holds the total distance (in theory)

    # Add cities until we have added them all.
    while flag != -1:
        flag, city_id, distance = chooseCity(pathArray, cities, distanceMatrix)
        if flag == 0:
            addCity(pathArray, cities_to_add, distanceMatrix, city_id)
            totalDistance += distance
            global_count += 1

    return totalDistance, pathArray  # Return the final path to main


# main
if __name__ == "__main__":

    coordinates = []
    vertex_no = []
    with open("test-input-6.csv", 'r') as csv_file:
        for line in csv_file:
            line = list(map(int, line.split(',')))
            vertex_no.append(line[0])
            coordinates.append(line)
    global global_count
    global_count = 0
    start = time.time()

    # Grab Current Time After Running the Code

    cities = list(coordinates)  # we will use this as our cities_to_add above
    distance_matrix = getDistanceMatrix(coordinates)  # returns a matrix of city distances

    # Retrieve the total distance travelled and the path
    totalDistance, thePath = findBestPath(distance_matrix, cities)

    # Get distance for drive home from the last city to starting city.
    totalDistance += getDistanceForTripHome(thePath, coordinates)

    thePath.append(thePath[0])

    end = time.time()

    # Subtract Start Time from The End Time
    total_time = end - start
    print("Time is\n" + str(total_time))
    print("Number of operations: ", global_count)
    print("Path is: ", thePath)
    print("Length of the path is: ", totalDistance)
    print("Number of operations: ", global_count)
    x_coordinate = []
    y_coordinate = []
    for i in range(0, len(thePath), 1):
        for j in range(0, len(vertex_no), 1):
            if vertex_no[j] == thePath[i]:
                x_coordinate.append(coordinates[j][1])
                y_coordinate.append(coordinates[j][2])

                # print("x_coordinates are: ", x_coordinate)
    # print("y_coordinates are: ", y_coordinate)

    # draw_tour(thePath, x_coordinate,y_coordinate)
    # plt.show()
