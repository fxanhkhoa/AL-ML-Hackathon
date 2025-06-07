import cv2
import numpy as np
# Load the image
image = cv2.imread('images/lane_line_2.jpg', cv2.IMREAD_COLOR)
# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Apply thresholding
ret, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
# Find contours
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# Draw contours
cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
# Analyze contours
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > 100: # Filter by area
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

# Create a mask
mask = np.zeros_like(gray)
cv2.drawContours(mask, contours, -1, 255, cv2.FILLED)
# Apply the mask
segmented_image = cv2.bitwise_and(image, image, mask=mask)

# Display images
cv2.imshow('Original Image', image)
cv2.imshow('Binary Image', thresh)
cv2.imshow('Image with Contours', image)
cv2.imshow('Segmented Image', segmented_image)
cv2.waitKey(0)
cv2.destroyAllWindows()