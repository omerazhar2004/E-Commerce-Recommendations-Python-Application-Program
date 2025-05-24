import numpy as np
import math

def arrForm():
    with open("history.txt", "r") as f:
        num_customers, num_items, num_transactions = map(int, f.readline().strip().split())   #reading the first line of the file
        purchase_history = [[0] * num_items for _ in range(num_customers)]   #initialising the array
        
        for _ in range(num_transactions):
            customer_id, item_id = map(int, f.readline().strip().split())
            purchase_history[customer_id - 1][item_id - 1] = 1    #makes it so that when a customer buys an item, the corresponding entry in the matrix is set to 1
    
    print(f"Positive entries: {sum(sum(row) for row in purchase_history)}")
    return np.array(purchase_history), num_items


def calc_angle(itemA, itemB):
    norm_a = np.linalg.norm(itemA)
    norm_b = np.linalg.norm(itemB)
    if norm_a == 0 or norm_b == 0:  # Edge case prevention
        return 90.0
    cos_theta = np.dot(itemA, itemB) / (norm_a * norm_b)
    return round(math.degrees(np.arccos(cos_theta)), 2)



def makeVector(num_items, purchase_history_array):
    return purchase_history_array.T  # Transposing gives column vectors directly



def makeVectorAngle(colVect_arr, num_items):
    map_arr = np.full((num_items, num_items), 90.0)  # Initialize with default 90.0 degrees values which will be replaced by float angle values
    angles = []
    for i in range(num_items):
        for j in range(i + 1, num_items):
            angle = calc_angle(colVect_arr[i], colVect_arr[j])
            map_arr[i, j] = map_arr[j, i] = angle  # Symmetric assignment
            angles.append(angle)    

    avg_angle = np.mean(angles)         #for calculating the average of the angles in angles list
    print(f"Average angle: {avg_angle:.2f}")
    return avg_angle, map_arr



def querForm():
    with open("queries.txt", "r") as f:
        for line in f:
            shp_cart = list(map(int, line.strip().split()))     #creating a list that stores all queries, i.e. all items in a shopping cart
            yield shp_cart  # Yield each shopping cart for processing



def mapIter(map_arr, queries):
    for shp_cart in queries:
        print(f"Shopping cart: {' '.join(map(str, shp_cart))}")

        recommendation_list = []  # Store tuples for sorting
        
        for item in shp_cart:
            min_angle = 90.00
            best_match = None
            
            for match_item in range(len(map_arr)):
                if (match_item + 1) not in shp_cart and map_arr[item - 1, match_item] < min_angle:      #makes sure that the matching item is not present in the current shopping cart, and that the corresponding angle in angles list i.e map_arr is less than 90 degrees
                    best_match, min_angle = match_item + 1, map_arr[item - 1, match_item]     #changes the values of best_match and min_angle and replaces them with the values that met the conditions of the if statement

            if best_match is not None:
                print(f"Item: {item} ; match: {best_match} ; angle: {min_angle:.2f}")
                recommendation_list.append((best_match, min_angle))  # Store tuples for sorting
            else:
                print(f"Item: {item} no match")

        # Sorting recommendations by angle and enforcing uniqueness
        unique_recommendations = {item[0]: item[1] for item in sorted(recommendation_list, key=lambda x: x[1])}  # Dict removes duplicates
        final_recommendations = [str(item) for item in unique_recommendations.keys()]
        print(f"Recommend: {' '.join(final_recommendations)}")

# Running the entire pipeline
purchase_history_array, num_items = arrForm()
colVect_arr = makeVector(num_items, purchase_history_array)
average_ang, map_arr = makeVectorAngle(colVect_arr, num_items)
queries = list(querForm())  # Convert generator to list for reuse
mapIter(map_arr, queries)