import math


class Point:
    def __init__(self, x=0, y=0, name=""):
        self.x = x
        self.y = y
        self.name = name

    def get_x(self):
        self._result = self.x
        return self

    def get_y(self):
        self._result = self.y
        return self

    def get_name(self):
        self._result = self.name
        return self

    def getInfo(self):
        try:
            return self._result
        except:
            return "No result"

    def asGeoJson(self):
        return {
            "type": "Point",
            "coordinates": [self.x, self.y]
        }


class Polyline:
    def __init__(self, agrs):
        self.points = agrs
        print(self.points[0].x, self.points[0].y)

    def get_points(self):
        self._result = self.points
        return self

    def get_length(self):
        # √((x2 – x1)² + (y2 – y1)²)
        length = 0
        for i in range(len(self.points) - 1):
            x1, y1 = self.points[i].x, self.points[i].y
            x2, y2 = self.points[i+1].x, self.points[i+1].y
            length += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        self._result = length
        return self

    def getInfo(self):
        try:
            return self._result
        except:
            return "No result"
