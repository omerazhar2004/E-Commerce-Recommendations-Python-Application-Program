if best_match is not None:
                print(f"Item: {item} ; match: {best_match} ; angle: {min_angle:.2f}")
                recommendations.append((best_match, min_angle))
            else:
                print(f"Item: {item} no match")
