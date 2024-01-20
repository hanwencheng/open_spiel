import enum


class RangeType(enum.IntEnum):
    POINT: 0
    DIRECTIONAL: 1
    SQUARE: 2
    DIAMOND: 3


class Range:
    def __init__(self, range_type: RangeType, range_value: int, length=None, width=None):
        self.range_type = range_type
        self.length = length
        self.width = width
        self.range = range_value

def create_directional_range(range_value: int, length: int, width: int) -> Range:
    return Range(RangeType.DIRECTIONAL, 0, length, width)


def create_point_range() -> Range:
    return Range(RangeType.POINT, 0)


def create_diamond_range(range_value: int) -> Range:
    return Range(RangeType.DIAMOND, range_value)


def create_square_range(range_value: int) -> Range:
    return Range(RangeType.SQUARE, range_value)

# class DirectionalRange(Range):
#     def __int__(self, is_directional: True, length, width, start, end):
#         self.range_type = RangeType.DIRECTIONAL
#         self.start = 0
#         self.end = 0
#         self.length = length
#         self.width = width
#
#
# class SelfRange(Range):
#     def __int__(self, is_directional: False, length, width, start, end):
#         self.range_type = RangeType.SELF
#         self.length = 0
#         self.width = 0
#         self.start = start
#         self.end = end
