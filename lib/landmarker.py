from math import gcd
import numpy
from typing import Tuple
from typing_extensions import Self
from mediapipe.python.solutions import pose
from lib.utils import Rect, bzo


class BodyRector(pose.Pose):
    def detect(self: Self,
               image: numpy.ndarray,
               margin: Tuple[int, int],
               paper: Tuple[int, int]) -> Rect:

        left, top, right, bottom = 1, 1, 0, 0
        height, width = image.shape[0:2]

        for landmark in self.process(image).pose_landmarks.landmark:
            left = bzo(landmark.x) if bzo(landmark.x) < left else left
            top = bzo(landmark.y) if bzo(landmark.y) < top else top
            right = bzo(landmark.x) if bzo(landmark.x) > right else right
            bottom = bzo(landmark.y) if bzo(landmark.y) > bottom else bottom

        top = top * height - margin[0]
        bottom = bottom * height + margin[1]
        left *= width
        right *= width

        left -= (horizontal_margin :=
                 ((bottom - top) * (paper[0] / paper[1]) - (right - left)) * 0.5)
        right += horizontal_margin

        return ((left, top), (right, bottom))
