####################################################################################################

import argparse
import cv2
import numpy as np

from collections import namedtuple

TEMPLATE_FILENAME = "digits.png"
TEMPLATE_BLUR_SIZE = 7
TEMPLATE_DIGITS_NUM = 10

# crop region
CROP_RECT = (586, 206, 938, 306)

# number of digits to read
DIGITS_NUM = 6

# min correlation coefficient to accept a digit
MIN_CCOEFF = 0.5

# adaptive threshold params
THRESHOLD_KERNEL = 77
THRESHOLD_CONST = 10

# denoise params
ERODE_KERNEL_SIZE = 7
DILATE_KERNEL_SIZE = 4

####################################################################################################

def genTemplate(template, index, maxIndex):
    "Generate digit image template for matching"

    b = TEMPLATE_BLUR_SIZE / 2
    width = template.shape[1] / maxIndex

    # Preprocess digit image
    digit = template[:, index * width : (index + 1) * width]
    digit = cv2.copyMakeBorder(digit, b, b, b, b, cv2.BORDER_CONSTANT, digit, 0)
    digit = cv2.GaussianBlur(digit, (TEMPLATE_BLUR_SIZE, TEMPLATE_BLUR_SIZE), 0)

    return digit


def loadDigits():
    "Load digits templates"

    template = cv2.imread(TEMPLATE_FILENAME, cv2.IMREAD_GRAYSCALE)
    digits = [ genTemplate(template, i, TEMPLATE_DIGITS_NUM) for i in range(TEMPLATE_DIGITS_NUM) ]

    return digits

####################################################################################################

def loadImage(file):
    "Load and preprocess input image"

    # Load image
    data = np.asarray(bytearray(file.read()), dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if image is None: raise RuntimeError("Failed to load image")

    # Crop and convert to gray
    cropped = image[CROP_RECT[1]:CROP_RECT[3], CROP_RECT[0]:CROP_RECT[2]]
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

    # Binarize
    blured = cv2.GaussianBlur(gray, (3, 3), 0)
    binary = cv2.adaptiveThreshold(blured, 255,
                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
                                   THRESHOLD_KERNEL, THRESHOLD_CONST)

    # Denoise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ERODE_KERNEL_SIZE, ERODE_KERNEL_SIZE))
    display = cv2.erode(binary, kernel)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (DILATE_KERNEL_SIZE, DILATE_KERNEL_SIZE))
    display = cv2.dilate(display, kernel)

    return display

####################################################################################################

DigitMatch = namedtuple("DigitMatch", "digit pos")


def matchDigits(display, digits):
    "Match digits within LCD display image"

    # Match digits templates
    match = [ cv2.matchTemplate(display, digit, cv2.TM_CCOEFF_NORMED) for digit in digits ]
    match = np.vstack(tuple(match))

    result = [ ]
    templateHeight = match.shape[0] / TEMPLATE_DIGITS_NUM

    for i in range(DIGITS_NUM):
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(match)
        digit = maxLoc[1] / templateHeight
        result.append(DigitMatch(digit, (maxLoc[0], maxLoc[1] % templateHeight)))

        if maxVal < MIN_CCOEFF: raise RuntimeError("Failed to recognize digit")

        # Remove local maximum neighborhood
        width = (digits[0].shape[1] - TEMPLATE_BLUR_SIZE) * 4 / 5
        xa, xb = max(0, maxLoc[0] - width), min(match.shape[1], maxLoc[0] + width)
        match[:, xa:xb] = 0

    # Prepare result
    result.sort(key = lambda foo: foo.pos[0])
    output = "".join([str(foo.digit) for foo in result])

    return output

####################################################################################################

def readDigits(file):
    "Read digits from LCD display image"

    display = loadImage(file)
    digits = loadDigits()

    return matchDigits(display, digits)

####################################################################################################

if __name__ == "__main__":
    args = argparse.ArgumentParser(description="OCR number from LCD display")
    args.add_argument("image", nargs=1, help="path to input image")
    params = vars(args.parse_args())

    image = params["image"][0]

    print readDigits(open(image))

####################################################################################################