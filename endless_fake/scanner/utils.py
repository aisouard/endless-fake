import cv2
import math
import numpy as np


def draw_line_with_direction(image, coords, angle, color, length=200, thickness=5, offset=0):
    coords = (int(coords[0]), int(coords[1]))
    if offset > 0:
        a = int(round(coords[1] + offset * math.cos(angle * math.pi / 180.0)))
        b = int(round(coords[0] + offset * math.sin(angle * math.pi / 180.0)))
        coords = (int(round(b)), int(round(a)))

    a = int(coords[1] + length * math.cos(angle * math.pi / 180.0))
    b = int(coords[0] + length * math.sin(angle * math.pi / 180.0))
    cv2.line(image, coords, (b, a), color, thickness=thickness)


def cleanup_mask(mask, morph_size=5, blur_size=5):
    morph_kernel = np.ones((morph_size, morph_size), np.uint8)
    morph_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, morph_kernel)
    return cv2.medianBlur(morph_mask, blur_size)


def find_edge_from_overlap(edge_mask, overlap):
    cnts, _ = cv2.findContours(edge_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i, cnt in enumerate(cnts):
        sample = np.zeros(edge_mask.shape, dtype=np.uint8)
        cv2.drawContours(sample, cnts, i, 255, thickness=-1)
        result = cv2.bitwise_and(sample, overlap)
        count = cv2.countNonZero(result)
        if count < 1:
            continue
        return cv2.countNonZero(sample)
    return 0
