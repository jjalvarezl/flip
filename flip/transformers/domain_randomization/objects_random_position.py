import numpy as np

from flip.transformers.element import Element
from flip.transformers.constants import Position
from flip.transformers.transformer import Transformer


# Only for element with objects
class ObjectsRandomPosition(Transformer):
    def __init__(
        self,
        mode: Position = Position.random,
        x_min=None,
        x_max=None,
        y_min=None,
        y_max=None,
    ):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.mode = mode

    def map(self, element: Element) -> Element:
        assert element, "Element cannot be None"

        el_h: int = element.image.shape[0]
        el_w: int = element.image.shape[1]

        if self.mode == Position.percentage:
            x_min = (
                (self.x_min if self.x_min <= 1 else (self.x_min % 100) / 100) * el_w
                if self.x_min is not None
                else 0
            )
            x_max = (
                (self.x_max if self.x_max <= 1 else (self.x_max % 100) / 100) * el_w
                if self.x_max is not None
                else el_w
            )
            y_min = (
                (self.y_min if self.y_min <= 1 else (self.y_min % 100) / 100) * el_h
                if self.y_min is not None
                else 0
            )
            y_max = (
                (self.y_max if self.y_max <= 1 else (self.y_max % 100) / 100) * el_h
                if self.y_max is not None
                else el_h
            )
        else:
            x_min = self.x_min if self.x_min is not None else 0
            x_max = self.x_max if self.x_max is not None else el_w
            y_min = self.y_min if self.y_min is not None else 0
            y_max = self.y_max if self.y_max is not None else el_h

        last_x, last_y = 0, 0
        for obj in element.objects:
            obj_h: int = int(obj.image.shape[0])
            obj_w: int = int(obj.image.shape[1])

            while True:
                obj.x = np.random.randint(
                    low=max(0, x_min - obj_w / 2), high=min(x_max, el_w),
                )

                if obj.x > last_x + obj_w / 2 or obj.x < last_x - obj_w / 2:
                    break

            while True:
                obj.y = np.random.randint(
                    low=max(0, y_min - obj_h / 2), high=min(y_max, el_h),
                )

                if obj.y > last_y + obj_h / 2 or obj.y < last_y - obj_h / 2:
                    break

            last_x, last_y = obj.x, obj.y

        return element
