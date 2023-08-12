import csv
import math
import sys
from random import random, randrange

if len(sys.argv) < 3:
    print("density and target Size must be provided !")
    quit()

density = int(sys.argv[1])
targetSize = int(sys.argv[2])
width = 800
height = 1024
minDistance = targetSize
maxTries = 30
cell_size = minDistance / math.sqrt(2)
column_count = width // cell_size
row_count = height // cell_size

samples_background = [[-1 for x in range(int(width // cell_size))] for y in range(int(height // cell_size))]
initial_sample = (random() * (height - 1), random() * (width - 1))
active_list = [initial_sample]
samples_background[int(initial_sample[0] // cell_size)][int(initial_sample[1] // cell_size)] = initial_sample
result = []

# check that the candidate point is doesn't have too close neighbors
def is_valid(point):
    py, px = int(point[0] // cell_size), int(point[1] // cell_size)

    # check if point is within the grid
    if py < 0 or py >= row_count or px < 0 or px >= column_count:
        return False

    # check if there is already a point in cell
    if samples_background[py][px] != -1:
        return False

    for y in range(py - 2, py + 2):
        for x in range(px - 2, px + 2):
            if 0 <= y < row_count and 0 <= x < column_count:
                if samples_background[y][x] != -1 and math.dist(samples_background[y][x], point) < r:
                    return False

    return True


# Generate a new random candidate from a point
def generate_random_point(point):
    theta = random() * math.pi * 2
    length = minDistance + random() * minDistance

    return point[0] + math.sin(theta) * length, point[1] + math.cos(theta) * length


while active_list:
    # random sample from active list
    sample = active_list[randrange(0, len(active_list))]

    for i in range(maxTries):
        # generate a new candidate
        candidate = generate_random_point(sample)

        if is_valid(candidate):
            active_list.append(candidate)
            samples_background[int(candidate[0] // cell_size)][int(candidate[1] // cell_size)] = candidate
            result.append(candidate)
            break

        # no candidate were valid, remove the sample from the active list
        if i == maxTries - 1:
            active_list.remove(sample)

# choice randomly density number of points
choicePoints = []
for point in range(density):
    choicePoints.append(result[randrange(0, len(result))])

with open('assets/bubble' + str(density) + 'x' + str(targetSize) + '.csv', 'w') as out:
    for row in choicePoints:
        out.write(str(int(row[0])) + "," + str(int(row[1])) + "," + str(minDistance) + "\n")
    out.close()

# choice randomly points to selected
selectedPoints = []
for i in range(5):
    selectedPoints.append(randrange(0, len(choicePoints)))

with open('assets/selected' + str(density) + 'x' + str(targetSize) + '.csv', 'w') as out:
    for row in selectedPoints:
        out.write(str(row) + "\n")
    out.close()
