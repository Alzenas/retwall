from math import sin, radians


class ProjectUnits:
    """Project units class."""
    title = "International (SI)"

    def set_imperial(self):
        """Sets project units to Imperial System of Units."""
        pass

    def set_international(self):
        """Sets project units to International System of Units."""
        pass

    def get_imperial(self):
        """Returns conversion into Imperial units."""
        pass

    def get_international(self):
        """Returns conversion into S.I. units."""
        pass


class Force:
    """Force class. Defines basic properties of force."""

    def __init__(self):
        self.fx = []  # Magnitude in x direction
        self.fy = []  # Force magnitude in y direction
        self.x = []  # Location of application or occurrence of the force (x coordinate)
        self.y = []  # Location of application or occurrence of the force (y coordinate)


class BendingMoment:
    """Bending moment class. Defines basic properties of a bending moment."""

    def __init__(self):
        self.mz = []  # Magnitude of the bending moment
        self.x = []  # Point of application or occurrence (x-direction)
        self.y = []  # Point of application or occurrence (y-direction)


class Displacement:
    def __init__(self):
        self.x = []  # In x direction
        self.y = []  # In y direction
        self.rz = []  # Rotation


class Soil:
    def __init__(self,
                 title='Default Soil',
                 weight=18,
                 phi=30):
        self.title = title
        self.weight = weight
        self.phi = phi
        self.wall_friction = self.phi * 2 / 3

    def ka(self):
        """Calculates active soil pressure coefficient"""
        _angle = radians(self.phi)
        _msg = '"{}": Active pressure coefficient was calculated as {}.'
        _ret = round((1 - sin(_angle)) / (1 + sin(_angle)), 3)
        _msg = _msg.format(self.title, _ret)
        # return ka and a message
        return [_ret, _msg]

    def kp(self):
        """Calculates passive soil pressure coefficient"""
        _angle = radians(self.phi)
        _msg = '"{}": Passive pressure coefficient was calculated as {}.'
        if self.phi < 90:
            _ret = round((1 + sin(_angle)) / (1 - sin(_angle)), 3)
            _msg = _msg.format(self.title, _ret)
        else:
            _msg = "Specified angle: {}, but should not be be >= 90".format(self.phi)
            _ret = 999

        # return ka and a message
        return [_ret, _msg]

    def k0(self):
        """Calculates 'at rest' soil pressure coefficient"""
        _msg = '"{}": "At rest" pressure coefficient was calculated as {}.'
        _angle = radians(self.phi)
        _ret = round(1 - sin(_angle), 3)
        _msg = _msg.format(self.title, _ret)
        # return ka and a message
        return [_ret, _msg]


if __name__ == '__main--':
    soil = Soil
    pass
