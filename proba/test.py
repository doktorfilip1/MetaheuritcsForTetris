import random
import numpy as np
x = 10
y = 20
table = [[0 for _ in range(x)] for _ in range(y)]

for i in range(y):
    for j in range(x):
        table[i][j] = random.randint(0,1)

ran = random.randint(0,y)

for i in range(x):
    table[ran][i] = 1
    
print(np.array(table), '\n')

for i in range(y):
    lineFull = True
    for j in range(x):
        if table[i][j] == 0:
            lineFull = False
    if lineFull:
        #score
        for m in range(i,0,-1):
            for k in range(x):
                table[m][k] = table[m-1][k]
        for m in range(x):
            table[0][m] = 0
                
print(np.array(table), '\n')

