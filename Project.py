from PIL import Image
import numpy as np

# Function to get neighboring pixels
def get_neighbors(x, y, width, height):
    neighbors = []
    if x > 0:
        neighbors.append((x - 1, y))  # Left
    if x < width - 1:
        neighbors.append((x + 1, y))  # Right
    if y > 0:
        neighbors.append((x, y - 1))  # Top
    if y < height - 1:
        neighbors.append((x, y + 1))  # Bottom
    return neighbors

# Function to check pixel similarity based on Manhattan distance
def is_similar(pixel1, pixel2, threshold=35):
    manhattan_distance = abs(pixel1[0] - pixel2[0]) + abs(pixel1[1] - pixel2[1]) + abs(pixel1[2] - pixel2[2])
    return manhattan_distance < threshold

# Function for region growing algorithm with multiple seed points
def region_grow_multi_seed(image, initial_seed_points, threshold=35):
    width, height = image.size
    img_array = np.array(image)  # Convert the image to a NumPy array of pixels (R, G, B)

    segmented = np.zeros((height, width), dtype=bool)  # Boolean array to mark segmented regions
    region = np.zeros((height, width, 3), dtype=np.uint8)  # Array for output segmented image
    segment_color = 255  # Color intensity for the segmented regions (can adjust to a different color or randomize)

    # Process each seed point to segment multiple regions
    for seed_point in initial_seed_points:
        if segmented[seed_point[1], seed_point[0]]:
            continue  # Skip if the seed point is already segmented

        # Stack for seed points in the current region
        stack = [seed_point]
        seed_value = img_array[seed_point[1], seed_point[0]]  # RGB value of the seed pixel

        while stack:
            x, y = stack.pop()

            if segmented[y, x]:  # Skip if already segmented
                continue

            # Mark this pixel as part of the region
            segmented[y, x] = True
            region[y, x] = seed_value  # Assign the seed color to the region

            # Check the neighbors
            neighbors = get_neighbors(x, y, width, height)
            for nx, ny in neighbors:
                if not segmented[ny, nx] and is_similar(img_array[ny, nx], seed_value, threshold):
                    stack.append((nx, ny))  # Add similar neighbors to the stack

        # Find the next unsegmented pixel as a new seed point, if any
        new_seed_found = False
        for y in range(height):
            for x in range(width):
                if not segmented[y, x]:  # Find the first unsegmented pixel
                    initial_seed_points.append((x, y))  # Add it to seed points
                    new_seed_found = True
                    break
            if new_seed_found:
                break

    return Image.fromarray(region)  # Convert NumPy array back to an image

# Main code to run region growing on the uploaded image
input_image = Image.open("D:\\Neccessary\\Project 7th SEM\\Input Images\\knee.jpg")  # Open the input image
initial_seeds = [(10, 10)]  # Choose initial seed points (you can add more manually if desired)
output_image = region_grow_multi_seed(input_image, initial_seeds, threshold=35)

output_image.show()  # Show the output segmented image