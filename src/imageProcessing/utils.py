import cv2 as cv
import numpy as np
from math import atan


#Signal detection function: Sigma
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

    img1_bg1 = cv.bitwise_and(img, img, mask=mask1)
    img2_bg2 = cv.bitwise_and(img, img, mask=mask2)
    edges = cv.Canny(img, 100, 200)
    lines = cv.HoughLines(edges, 1, np.pi / 180, 50)

    right_wall = 0
    left_wall = 0
    front_wall = 0
    line_slopes = []
    fx1, fx2, fy1, fy2, rx1, rx2, ry1, ry2, lx1, lx2, ly1, ly2 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    if lines is not None:
        for line in lines:
            try:
                x1, x2, y1, y2 = find_lines(line)
                angle = 180 / np.pi * atan(1 / ((y2 - y1) / (x2 - x1)))
                if round(angle) not in line_slopes:
                    cv.line(img, (x1, y1), (x2, y2), (0, 255, 255), 2)
                    line_slopes.append(round(angle))
                    if angle > 45 or angle < -45:
                        fx1, fx2, fy1, fy2 = x1, x2, y1, y2
                        front_wall = angle
                    elif angle > 0:
                        rx1, rx2, ry1, ry2 = x1, x2, y1, y2
                        right_wall = angle
                    else:
                        lx1, lx2, ly1, ly2 = x1, x2, y1, y2
                        left_wall = angle
            except:
                pass

    if left_wall != 0 - threshold and left_wall != 0:
        llx1, lly1, llx2, lly2 = get_real_coords(lx1, lx2, ly1, ly2, l, b)
        P1_disy = 20 * (1 - (lly1 / b)) + 20
        P2_disy = 20 * (1 - (lly2 / b)) + 20
        P1_disx = 20 * (llx1 / l)
        P2_disx = 20 * (llx2 / l)
        m = (P1_disy - P2_disy) / (P1_disx - P2_disx)
        line_dis = (m * P2_disx - P2_disy + 0) / m
        if abs(line_dis) < 10:
            return img, "R", abs(left_wall)

    if right_wall != threshold and right_wall != 0:
        llx1, lly1, llx2, lly2 = get_real_coords(rx1, rx2, ry1, ry2, l, b)
        P1_disy = 20 * (1 - (lly1 / b)) + 20
        P2_disy = 20 * (1 - (lly2 / b)) + 20
        P1_disx = 20 * (llx1 / l)
        P2_disx = 20 * (llx2 / l)
        m = (P1_disy - P2_disy) / (P1_disx - P2_disx)
        line_dis = ((m * P1_disx - P1_disy + 0) / m) - 15
        if abs(line_dis) < 10:
            return img, "L", abs(right_wall)

    if front_wall != 0:
        llx1, lly1, llx2, lly2 = get_real_coords(fx1, fx2, fy1, fy2, l, b)

        P1_dis = 20 * (1 - (lly1 / l)) + 20
        P2_dis = 20 * (1 - (lly2 / l)) + 20
        if (P1_dis + P2_dis) / 2 < 35:
            return img, "F", abs(front_wall)

    return img, "N", 0
