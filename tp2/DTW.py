import math

def DTWDistance(s:list, t:list):
    n = len(s)
    m = len(t)
    DTW = [[math.inf for j in range(m+1)] for i in range(n+1)]
    DTW[0][0] = 0
    
    for i in range(1, n+1):
        for j in range(1, m+1):
            cost = math.dist(s[i-1], t[j-1])
            DTW[i][j] = cost + min(DTW[i-1][j], DTW[i][j-1], DTW[i-1][j-1])
            
    return DTW[n][m]