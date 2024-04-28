def minmax_normalize_two_pos(pos1, pos2):
    if pos1 and pos2:
        min_x = min_y = min_z = float('inf')
        max_x = max_y = max_z = float('-inf')

        # Iterate through both sets of landmarks simultaneously and update min/max
        for a, b in zip(pos1.landmark, pos2.landmark):
            # Update min and max for x
            min_x = min(min_x, a.x, b.x)
            max_x = max(max_x, a.x, b.x)
            # Update min and max for y
            min_y = min(min_y, a.y, b.y)
            max_y = max(max_y, a.y, b.y)
            # Update min and max for z
            min_z = min(min_z, a.z, b.z)
            max_z = max(max_z, a.z, b.z)

        def normalize(value, min_val, max_val):
            return (value - min_val) / (max_val - min_val) if max_val != min_val else 0

        for landmarks in (pos1.landmark, pos2.landmark):
            for landmark in landmarks:
                landmark.x = normalize(landmark.x, min_x, max_x)
                landmark.y = normalize(landmark.y, min_y, max_y)
                landmark.z = normalize(landmark.z, min_z, max_z)


# not sure how to type annotate.
# takes landmark like tracked_objects["pose_landmarks"].extra["landmarks"] and gives sse
def compare_pos_by_landmarks(pos1, pos2):
    if pos1 and pos2:
        minmax_normalize_two_pos(pos1, pos2)  # normalize both landmark sets in place

        def euclidean_dist_squared(a, b):
            return (a.x - b.x)**2 + (a.x - b.y)**2 + (a.x - b.y)**2

        sse = 0
        for a, b in zip(pos1.landmark, pos2.landmark):
            sse += euclidean_dist_squared(a, b)

        return sse
