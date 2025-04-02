import numpy as np
import math

def arrForm():
    with open("history.txt", "r") as f:
        num_customers, num_items, num_transactions = map(int, f.readline().strip().split())
        purchase_history = [[0] * num_items for _ in range(num_customers)]
        
        for _ in range(num_transactions):
            customer_id, item_id = map(int, f.readline().strip().split())
            purchase_history[customer_id - 1][item_id - 1] = 1
    
    print(f"Positive entries: {sum(sum(row) for row in purchase_history)}")
    return np.array(purchase_history), num_items

def calc_angle(itemA, itemB):
    norm_a = np.linalg.norm(itemA)
    norm_b = np.linalg.norm(itemB)
    cos_theta = np.dot(itemA, itemB) / (norm_a * norm_b)
    return math.degrees(np.arccos(cos_theta))

def makeVector(num_items, purchase_history_array):
    return purchase_history_array.T  # Transposing gives column vectors directly

def makeVectorAngle(colVect_arr, num_items):
    map_arr = np.full((num_items, num_items), 90)  # Initialize with default 90 degrees

    angles = []
    for i in range(num_items):
        for j in range(i + 1, num_items):
            angle = calc_angle(colVect_arr[i], colVect_arr[j])
            map_arr[i, j] = map_arr[j, i] = angle  # Symmetric assignment
            angles.append(angle)

    avg_angle = np.mean(angles)
    print(f"Average angle: {avg_angle:.2f}")
    return avg_angle, map_arr

def querForm():
    with open("queries.txt", "r") as f:
        for line in f:
            shp_cart = list(map(int, line.strip().split()))
            print(f"Shopping cart: {' '.join(map(str, shp_cart))}")
            yield shp_cart  # Yield each shopping cart for processing


def mapIter(map_arr, shp_cart):
    for cart in shp_cart:
        recommendations = []
        for item in cart:
            min_angle = 90.0
            best_match = None

            for match_item in range(len(map_arr)):
                if (match_item + 1) not in cart and map_arr[item - 1, match_item] < min_angle:
                    best_match, min_angle = match_item + 1, map_arr[item - 1, match_item]  # Convert index to item ID
            if best_match is not None:
                print(f"Item: {item} ; match: {best_match} ; angle: {min_angle:.2f}")
                recommendations.append((best_match, min_angle))
            else:
                print(f"Item: {item} no match")

        recommendations.sort(key=lambda x: x[1])  # Sort by angle
        recommended_items = [str(item[0]) for item in recommendations]
        print(f"Recommend: {' '.join(recommended_items)}")

# Running the entire pipeline
purchase_history_array, num_items = arrForm()
colVect_arr = makeVector(num_items, purchase_history_array)
average_ang, map_arr = makeVectorAngle(colVect_arr, num_items)
queries = list(querForm())  # Convert generator to list for reuse
mapIter(map_arr, queries)