import numpy as np
import copy

def minmax_normalize_two_pos(pos1, pos2):
    pos1 = copy.deepcopy(pos1)
    pos2 = copy.deepcopy(pos2)

    if pos1 and pos2:
        min_x = min_y = min_z = float('inf')
        max_x = max_y = max_z = float('-inf')

        # Iterate through both sets of landmarks simultaneously and update min/max
        for a, b in zip(pos1, pos2):
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

        for pairs in (pos1, pos2):
            for item in pairs:
                item.x = normalize(item.x, min_x, max_x)
                item.y = normalize(item.y, min_y, max_y)
                item.z = normalize(item.z, min_z, max_z)

    return (pos1, pos2)


def compare_pos_by_landmarks_cosine_similarity(pos1, pos2):
    if pos1 and pos2:
        pos1, pos2 = minmax_normalize_two_pos(pos1, pos2)  # normalize both landmark sets in place

        # Gather all coordinates into two vectors
        vector1 = []
        vector2 = []
        for a in pos1:
            vector1.extend([a.x, a.y, a.z])
        for b in pos2:
            vector2.extend([b.x, b.y, b.z])

        # Convert lists to numpy arrays for vector operations
        vector1 = np.array(vector1)
        vector2 = np.array(vector2)

        # Calculate cosine similarity
        dot_product = np.dot(vector1, vector2)
        norm1 = np.linalg.norm(vector1)
        norm2 = np.linalg.norm(vector2)
        if norm1 == 0 or norm2 == 0:
            return 0  # To handle the case where a norm is zero
        cosine_similarity = dot_product / (norm1 * norm2)
        return cosine_similarity



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

def sim_to_positive_score(sim):
    if sim >= 0.95:
        return 5
    elif sim >= 0.90:
        return 4
    elif sim >= 0.80:
        return 3
    elif sim >= 0.75:
        return 3
    elif sim >= 0.70:
        return 2
    elif sim >= 0.65:
        return 1
    else:
        return 0
