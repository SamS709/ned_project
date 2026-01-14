import numpy as np
from Connect4 import Connect4

table_0 = np.array([[0 for j in range(7)] for i in range(6)])
table = np.array([[0 for j in range(7)] for i in range(6)])


table_0 = np.array([[0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 1, 2, 0, 0, 0]                 
])

table[table_0 != 0] = table_0[table_0 != 0]
table[5,1] = 1
# table[1,3] = 1
def compare_tables(table_0, table):
    L_avaible_pos = Connect4().avaible_pos_graphics(Connect4().table_to_grid(table_0))
    count_different_pieces = 0
    p, q = 0, 0
    for i in range((table.shape[0])):
        for j in range(table.shape[1]):
            if table_0[i,j] != table[i,j]:
                count_different_pieces +=1
                p, q = i, j
    print(count_different_pieces)
    print(p,q)
    if count_different_pieces != 1:
        return False
    elif [p,q] in L_avaible_pos:
        return True
    return False

print(compare_tables(table_0, table))








