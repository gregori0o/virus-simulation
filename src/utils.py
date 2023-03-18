from enum import Enum


class RegionShape(Enum):
    RECTANGLE = "rectangle"
    CIRCLE = "circle"


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

    @classmethod
    def list(cls):
        return list(map(lambda x: x.value, cls))

    @classmethod
    def next(cls, dir):
        match dir:
            case cls.UP.value:
                return cls.RIGHT.value
            case cls.RIGHT.value:
                return cls.DOWN.value
            case cls.DOWN.value:
                return cls.LEFT.value
            case cls.LEFT.value:
                return cls.UP.value
