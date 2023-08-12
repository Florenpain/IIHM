import math

def interpolate(a:tuple, b:tuple, d:int):
    ax, ay = a
    bx, by = b
    ab = math.sqrt((bx - ax) ** 2 + (by - ay) ** 2)
    x = ax + (bx - ax) * d / ab
    y = ay + (by - ay) * d / ab
    return int(x), int(y)

def resample(stroke: list, d: int) -> list:
    total_distance = sum(math.dist(stroke[i-1], stroke[i]) for i in range(1, len(stroke)))
    resampled = [stroke[0]]
    curr = 0
    dist = d
    while curr < len(stroke) - 1:
        a = stroke[curr]
        b = stroke[curr+1]
        ab = math.dist(a, b)
        if ab < dist:
            curr += 1
            dist -= ab
        else:
            new_point = interpolate(a, b, dist)
            resampled.append(new_point)
            # stroke.insert(curr+1, new_point)
            total_distance += math.dist(a, new_point) + math.dist(new_point, b) - ab
            dist = d
        if total_distance >= (len(stroke)-1)*d:
            break
    if resampled[-1] != stroke[-1]:
        resampled.append(stroke[-1])
    return resampled