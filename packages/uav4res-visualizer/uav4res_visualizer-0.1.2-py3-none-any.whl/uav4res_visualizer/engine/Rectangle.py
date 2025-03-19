from .Point import Point


class Rectangle:
    def __init__(self, x=0, y=0, width=0, height=0):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self.update()

    def x(self):
        return self._x

    def y(self):
        return self._y

    def w(self):
        return self._width

    def h(self):
        return self._height

    def top(self):
        return self._top

    def bottom(self):
        return self._bottom

    def leftmost(self):
        return self._leftmost

    def rightmost(self):
        return self._rightmost

    def center(self):
        return self._center

    def left_center(self):
        return self._left_center

    def right_center(self):
        return self._right_center

    def top_left(self):
        return self._top_left

    def top_right(self):
        return self._top_right

    def top_center(self):
        return self._top_center

    def bottom_left(self):
        return self._bottom_left

    def bottom_right(self):
        return self._bottom_right

    def bottom_center(self):
        return self._bottom_center

    def add_x(self, dx):
        self._x += dx
        self.update()

    def add_y(self, dy):
        self._y += dy
        self.update()

    def set_x(self, x):
        self._x = x
        self.update()

    def set_y(self, y):
        self._y = y
        self.update()

    def stretch(self, scale_x, scale_y=None):
        if scale_y is None:
            scale_y = scale_x
        self._width = int(self._width * scale_x)
        self._height = int(self._height * scale_y)
        self.update()

    def update(self):
        self._top = self._y
        self._bottom = self._y + self._height
        self._leftmost = self._x
        self._rightmost = self._x + self._width

        self._center = Point(self._x + self._width / 2, self._y + self._height / 2)
        self._left_center = Point(self._x, self._center.y())
        self._right_center = Point(self._rightmost, self._center.y())

        self._top_left = Point(self._x, self._y)
        self._top_right = Point(self._rightmost, self._y)
        self._top_center = Point(self._center.x(), self._y)

        self._bottom_left = Point(self._x, self._bottom)
        self._bottom_right = Point(self._rightmost, self._bottom)
        self._bottom_center = Point(self._center.x(), self._bottom)

    def __repr__(self):
        return f"Rectangle(x={self._x}, y={self._y}, width={self._width}, height={self._height})"
