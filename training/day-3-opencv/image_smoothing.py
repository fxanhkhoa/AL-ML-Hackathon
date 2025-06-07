# Python code to read image
import cv2
import numpy as np

# To read image from disk, we use
# cv2.imread function, in below method,
img = cv2.imread("images/lane_line_1.jpg", cv2.IMREAD_COLOR)

# Creating GUI window to display an image on screen
# first Parameter is windows title (should be in string format)
# Second Parameter is image array
cv2.imshow("image", img)

 # Gaussian blur
blurred_image_g = cv2.GaussianBlur(img, (15, 15), 0)

# Median blur
noise = cv2.imread("images/noise.png", cv2.IMREAD_COLOR)
blurred_image_m = cv2.medianBlur(noise, 3)

# Average blur
blurred_image_a = cv2.blur(img, (15, 15))
 
cv2.imshow('Blurred Image g', blurred_image_g)
cv2.imshow('Blurred Image m', blurred_image_m)
cv2.imshow('Blurred Image a', blurred_image_a)

# 1.Erosion
img = cv2.imread('images/j.png', cv2.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"
kernel = np.ones((5,5),np.uint8)
erosion = cv2.erode(img,kernel,iterations = 1)
dilation = cv2.dilate(img,kernel,iterations = 1)

cv2.imshow('erosion', erosion)
cv2.imshow('dilation', dilation)


# To hold the window on screen, we use cv2.waitKey method
# Once it detected the close input, it will release the control
# To the next line
# First Parameter is for holding screen for specified milliseconds
# It should be positive integer. If 0 pass an parameter, then it will
# hold the screen until user close it.
cv2.waitKey(0)

# It is for removing/deleting created GUI window from screen
# and memory
cv2.destroyAllWindows()
