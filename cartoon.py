import cv2
import numpy as np

cap = cv2.VideoCapture(0)
_, img = cap.read()

if not type(img) is np.ndarray:
    raise Exception('"img" must be image data from opencv')

numDownSamples = 2 # number of downscaling steps
numBilateralFilters = 7  # number of bilateral filtering steps

# -- STEP 1 --
# downsample image using Gaussian pyramid
img_color = img
for _ in range(numDownSamples):
    img_color = cv2.pyrDown(img_color)

# repeatedly apply small bilateral filter instead of applying
# one large filter
for _ in range(numBilateralFilters):
    img_color = cv2.bilateralFilter(img_color, 9, 9, 7)

# upsample image to original size
for _ in range(numDownSamples):
    img_color = cv2.pyrUp(img_color)

# -- STEPS 2 and 3 --
# convert to grayscale and apply median blur
img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
img_blur = cv2.medianBlur(img_gray, 7)

# -- STEP 4 --
# detect and enhance edges
img_edge = cv2.adaptiveThreshold(img_blur, 255,
    cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 7)

# -- STEP 5 --
# convert back to color so that it can be bit-ANDed
# with color image
img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
cart_img = cv2.bitwise_and(img_color, img_edge)

cv2.imwrite('image.jpg', cart_img)