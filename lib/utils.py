from typing import Tuple, Union
import numpy

Point = Tuple[float, float]
Number = Union[int, float]
Rect = Tuple[Point, Point]


def cut(image: numpy.ndarray, rect: Rect) -> numpy.ndarray:

    pt1, pt2 = rect

    return image[int(pt1[1]):int(pt2[1])+1, int(pt1[0]):int(pt2[0])+1]


# def fa4w(width: Number) -> Number:

#     return w if width > (w := 210/297) else 0 if width < 0 else width


# def fa4h(height: Number) -> Number:

#     return h if height > (h := 1) else 0 if height < 0 else height


def bzo(value: Number):
    """
    Return the value between 0 and 1.
    """

    return 1 if value > 1 else 0 if value < 0 else value
