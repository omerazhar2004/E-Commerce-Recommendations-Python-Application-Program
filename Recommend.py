import numpy as np
import math
from itertools import combinations

def arrForm():
    f = open("history.txt", "r")
    line1 = f.readline().strip().split()
    num_customers = int(line1[0])
    num_items = int(line1[1])
    num_transactions = int(line1[2])
    purchase_history = [[0] * num_items for x in range(num_customers)]
    for x in range(num_transactions):
        line2 = f.readline().strip().split()
        customer_id = int(line2[0])
        num_id = int(line2[1])
        purchase_history[customer_id - 1][num_id - 1] = 1
    print(f"positive entries: {sum(sum(row) for row in purchase_history)}")
    purchase_history_array = np.array(purchase_history)
    print(purchase_history_array)    #remove later
    return purchase_history_array, num_items


def calc_angle(itemA, itemB):
    norm_a = np.linalg.norm(itemA)
    norm_b = np.linalg.norm(itemB)
    cos_theta = np.dot(itemA, itemB) / (norm_a * norm_b)
    angle_theta = math.degrees(np.arccos(cos_theta))
    return angle_theta


def makeVector(num_items, purchase_history_array):
    colVect = []
    for i in range(num_items):
        colVect.append(purchase_history_array[: , i])
    colVect_arr = np.array(colVect)
    print(colVect_arr)
    return colVect_arr


def makeVectorAngle(colVect_arr, num_items): 
    row_angs = []  
    # num_rows = colVect_arr.shape[0]
    # num_rows = len(colVect_arr)
    map = [[90] * num_items] * num_items
    map_arr = np.array(map)
    # print(map_arr)  

    for i in range(num_items):
        for j in range(i + 1, num_items):
            # VectAngs = calc_angle(colVect_arr[i], colVect_arr[j])
            # row_angs.append(VectAngs)
            map_arr[i][j] = calc_angle(colVect_arr[i], colVect_arr[j])
            VectAngs = map_arr[i][j]
            row_angs.append(VectAngs)
    rowAngs_arr = np.array(row_angs)        
    print(rowAngs_arr)
      # remove later
    print(map_arr)    
    print(map_arr[0][1])
    average_ang = np.mean(row_angs)
    print(f"average angle : {average_ang}")
    return average_ang, map_arr


def querForm(purchase_history_array):
    f = open("queries.txt", "r")
    for line in f:
        shpCrt = f.readline()
        shpCrt_arr = np.array(shpCrt)
        print(f"Shopping Cart: {shpCrt_arr}")


def mapIter(map_arr):
    rows, cols = map_arr.shape  # Get array dimensions
    for i in range(rows):
        for j in range(cols):
            if map_arr[i, j] < 90:
                print(f"Item: ({i}, {j}); Match: Yes; Angle: {map_arr[i, j]}")
            else:
                print(f"Item: ({i}, {j})")




purchase_history_array, num_items = arrForm()  
colVect_arr = makeVector(num_items, purchase_history_array)  
average_ang, map_arr = makeVectorAngle(colVect_arr, num_items)
# querForm()
mapIter(map_arr)
