import cv2
import numpy as np

def is_circular(contour, tolerance=0.2):
    """
    Checks if a contour is approximately a circle.

    Args:
        contour: A contour point array (e.g., from cv2.findContours).
        tolerance: A small float to account for imperfections.

    Returns:
        True if the contour is approximately a circle, False otherwise.
    """
    # Calculate the area and perimeter of the contour
    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)

    # If the perimeter is zero, it's not a valid shape
    if perimeter == 0:
        return False

    # Calculate the circularity using the formula: 4 * pi * area / (perimeter * perimeter)
    circularity = 4 * np.pi * area / (perimeter * perimeter)
    print(area, perimeter, circularity)

    # A perfect circle has a circularity of 1. Check if it's within the tolerance.
    return 1 - tolerance <= circularity <= 1 + tolerance

def is_square(contour, tolerance=0.05):
    """
    Checks if a contour is approximately a square.

    Args:
        contour: A contour point array (e.g., from cv2.findContours).
        tolerance: A small float to account for imperfections.

    Returns:
        True if the contour is approximately a square, False otherwise.
    """
    # Approximate the contour to get a simpler polygon
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
    print(perimeter, approx)

    # A square has 4 vertices
    if len(approx) != 4:
        return False

    # Get the bounding box and calculate its aspect ratio
    x, y, w, h = cv2.boundingRect(approx)
    aspect_ratio = float(w) / h

    # Check if the aspect ratio is close to 1
    if not (1 - tolerance <= aspect_ratio <= 1 + tolerance):
        return False

    # Further check the area of the approximated polygon against the bounding box area
    contour_area = cv2.contourArea(contour)
    bbox_area = w * h
    if bbox_area == 0:
        return False
    extent = float(contour_area) / bbox_area
    if extent < 0.8:  # Squares tend to have a high extent
        return False

    # Consider angles (optional but can improve accuracy)
    # Sort the vertices to easily access adjacent points
    rect = np.reshape(approx, (4, 2))
    (tl, tr, br, bl) = rect

    def dist_sq(p1, p2):
        return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

    side1 = np.sqrt(dist_sq(tl, tr))
    side2 = np.sqrt(dist_sq(tr, br))
    side3 = np.sqrt(dist_sq(br, bl))
    side4 = np.sqrt(dist_sq(bl, tl))

    sides = sorted([side1, side2, side3, side4])
    if not (sides[0] * (1 + tolerance) >= sides[3]): # Check if sides are roughly equal
        return False

    # You could also check if diagonals are roughly equal if needed for more robustness

    return True

# Load the image
image = cv2.imread('images/no-turn-right-1.jpg')  # Replace 'shapes.png' with your image path
if image is None:
    print("Error: Could not load image.")
    exit()

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
cv2.imshow('blurred', blurred)

# Perform edge detection
edges = cv2.Canny(blurred, 10, 150)

cv2.imshow('edges', edges)

# Find contours
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Iterate through the contours and check for squares
square_contours = []
for contour in contours:
    if is_circular(contour):
        square_contours.append(contour)

# Draw the detected squares on the original image
cv2.drawContours(image, square_contours, -1, (0, 255, 0), 2)

# Display the result
cv2.imshow('Detected Circle', image)
cv2.waitKey(0)
cv2.destroyAllWindows()