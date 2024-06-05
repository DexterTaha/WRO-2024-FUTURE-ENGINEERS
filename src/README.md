## Signal Detection Function: Sigma

The following Python code demonstrates a signal detection function using OpenCV. The function processes an image to detect green and red signals and calculates distances and angles for navigation purposes.

```python
import cv2 as cv
import numpy as np
from math import atan

# Signal detection function: Sigma
def signal_detection(image, signal_size, weight, object_size, focal_distance, px, l):
    img = image
    blurred = cv.medianBlur(img, 15)
    hsv = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)
    height, width = img.shape[:2]

    # Setting up the first mask
    lower_limit = np.array([25, 150, 40])
    upper_limit = np.array([85, 230, 255])
    mask1 = cv.inRange(hsv, lower_limit, upper_limit)
    kernel = np.ones((11, 11), np.uint8)
    mask1 = cv.dilate(mask1, kernel, iterations=2)
    mask1 = cv.erode(mask1, kernel, iterations=2)

    # Setting up the second mask
    lower_limit = np.array([97, 170, 70])
    upper_limit = np.array([180, 255, 255])
    mask2 = cv.inRange(hsv, lower_limit, upper_limit)
    kernel = np.ones((11, 11), np.uint8)
    mask2 = cv.dilate(mask2, kernel, iterations=2)
    mask2 = cv.erode(mask2, kernel, iterations=2)

    # Finding the contours and marking them
    contours1, _ = cv.findContours(mask1, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[-2:]
    for cnt in contours1:
        if cv.contourArea(cnt) > height * width * 0.012:
            (cx, cy), radius = cv.minEnclosingCircle(cnt)
            x, y, w, h = cv.boundingRect(cnt)
            cv.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
            font = cv.FONT_HERSHEY_SIMPLEX
            cv.putText(img, "Green", (x, y), font, 0.5, (255, 255, 255), 2, cv.LINE_AA)
            dis, latx = d_l(x+w//2, h, signal_size, focal_distance, l)
            print("Green Object lateral distance :", latx, "cm")
            print("Green Object distance :", dis, "cm")
            try:
                angle = 100 - (180/np.pi*(atan(dis/abs(latx))))
                print("Degrees to turn :", angle)

            except ZeroDivisionError:
                angle = 30
                print("Degrees to turn :", 30)
            if angle < 40:
                angle = 40
            if dis < 60:
                if cx < (width // 2 - object_size // 2):
                    return img, [1, 1, angle, dis, latx]
                else:
                    return img, [1, 0, angle, dis, latx]

    contours2, _ = cv.findContours(mask2, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[-2:]
    for cnt in contours2:
        if cv.contourArea(cnt) > height * width * 0.012:
            (cx, cy), radius = cv.minEnclosingCircle(cnt)
            x, y, w, h = cv.boundingRect(cnt)
            cv.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
            font = cv.FONT_HERSHEY_SIMPLEX
            cv.putText(img, "Red", (x, y), font, 0.5, (255, 255, 255), 2, cv.LINE_AA)
            dis, latx = d_l(x+w//2, h, signal_size, focal_distance, l)
            print("Red Object lateral distance :", latx, "cm")
            print("Red Object distance :", dis, "cm")
            try:
                angle = 100 - (180/np.pi*(atan(dis/abs(latx))))
                print("Degrees to turn :", angle)
            except ZeroDivisionError:
                angle = 30
                print("Degrees to turn :", 30)
            if angle < 40:
                angle = 40
            if dis < 60:
                if cx > (width // 2 + object_size // 2):
                    return img, [0, 1, angle, dis, latx]
                else:
                    return img, [0, 0, angle, dis, latx]  # The first argument refers to the colour of the signal and the second one refers
                    # to whether the object is on the right side
    return img, [2, 0, 0]

def d_l(sx, sy, object_size, f, window_size):
    y = sy * 0.0264583333  # Converting to cm
    distance_from_object = int((f * object_size) / y)
    x = ((window_size // 2) - sx) * 0.0264583333  # Converting to cm
    rx = int(((x * distance_from_object) / f))
    return distance_from_object, rx

def get_real_coords(x1, x2, y1, y2, l, b):
    m = (y2 - y1) / (x2 - x1)
    coords = []
    coords.append(int((m*x1 - y1 + 0) / m))
    coords.append(int(y1 - m*(x1 - 0)))
    coords.append(int((m*x1 - y1 + b) / m))
    coords.append(int(y1 - m*(x1 - l)))
    for i in range(len(coords)):
        if i % 2 == 0:
            if coords[i] < 0:
                coords[i] = 0
            if coords[i] > l:
                coords[i] = 0
        else:
            if coords[i] < 0:
                coords[i] = 0
            if coords[i] > b:
                coords[i] = 0
    rx1 = 0
    ry1 = 0
    rx2 = 0
    ry2 = 0
    for i in range(len(coords)):
        if i == 0:
            if coords[i] != 0:
                rx1 = coords[i]
                ry1 = 1
        if i == 1:
             if coords[i] != 0:
                if ry1 == 0:
                    rx1 = 1
                    ry1 = coords[i]
                else:
                    rx2 = 1
                    ry2 = coords[i]
        if i == 2:
            if coords[i] != 0:
                if rx1 == 0:
                    rx1 = coords[i]
                    ry1 = b
                else:
                    rx2 = coords[i]
                    ry2 = b
        if i == 3:
            if coords[i] != 0:
                if ry1 == 0:
                    rx1 = l
                    ry1 = coords[i]
                else:
                    rx2 = l
                    ry2 = coords[i]
    return rx1, ry1, rx2, ry2

def find_lines(line_details):
    rho, theta = line_details[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    px1 = int(x0 + 1000 * -b)
    py1 = int(y0 + 1000 * a)
    px2 = int(x0 - 1000 * -b)
    py2 = int(y0 - 1000 * a)
    return px1, px2, py1, py2

def warpImg(img, points, w, h, inv=False):
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    if inv:
        matrix = cv.getPerspectiveTransform(pts2, pts1)
    else:
        matrix = cv.getPerspectiveTransform(pts1, pts2)
    imgWarp = cv.warpPerspective(img, matrix, (w, h))
    return imgWarp

def wall_detection(image, l, b, threshold):
    points = np.float32([(13, 73), (l - 13, 73),
                         (0, 118), (l - 0, 118)])

    img = warpImg(image, points, l, b)
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # Mask to subtract the blue and orange lines
    lower_limit = np.array([25, 150, 40])
    upper_limit = np.array([85, 230, 255])
    mask1 = cv.inRange(hsv, lower_limit, upper_limit)
    kernel = np.ones((11, 11), np.uint8)
    mask1 = cv.dilate(mask1, kernel, iterations=2)
    mask1 = cv.erode(mask1, kernel, iterations=2)

    lower_limit = np.array([97, 170, 70])
    upper_limit = np.array([180, 255, 255])
    mask2 = cv.inRange(hsv, lower_limit, upper_limit)
    kernel = np.ones((11, 11), np.uint8)
    mask2 = cv.dilate(mask2, kernel, iterations=2)
    mask2 = cv.erode(mask2, kernel, iterations=2)
    mask = mask1 + mask2
    kernel = np.ones((5, 5), np.uint8)
    mask = cv.dilate(mask, kernel, iterations=1)
    mask = cv.erode(mask, kernel, iterations=1)
    lower_limit = np.array([0, 0, 50])
    upper_limit = np.array([180, 100, 255])
    mask_walls = cv.inRange(hsv, lower_limit, upper_limit)
    mask_walls = mask_walls - mask
    edges = cv.Canny(mask_walls, 150, 300, apertureSize=3)
    lines = cv.HoughLines(edges, 1, np.pi / 180, threshold)
    if lines is not None:
        rho, theta = lines[0][0]
        for i in range(0, 1):
            x1, x2, y1, y2 = find_lines(lines[i])
            rx1, ry1, rx2, ry2 = get_real_coords(x1, x2, y1, y2, l, b)
            cv.line(img, (rx1, ry1), (rx2, ry2), (0, 255, 0), 3)
            m = (ry2 - ry1) / (rx2 - rx1)
            if m < 0:
                if x1 < l / 2:
                    return img, -1
                else:
                    return img, -2
            else:
                if x1 < l / 2:
                    return img, 1
                else:
                    return img, 2
    return img, 0

def find_lane(image):
    height, width = image.shape[:2]
    img, signal_details = signal_detection(image, 7, 2, 7, 27, 640, width)
    img, lane_details = wall_detection(img, width, height, 60)
    return img, signal_details, lane_details
