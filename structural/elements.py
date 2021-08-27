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


class Shape:
    Rectangular = 0
    Contiguous = 1
    Secant = 2
    Sheet = 3


class Alignment:
    Left = "Left"
    Right = "Right"
    Centre = "Centre"


class WallSection:
    """Cross section class."""

    def __init__(self, _shape):
        self.shape = _shape


class Wall:
    """Concrete Wall Class. Defines basic properties of a concrete wall."""

    def __init__(self, _id):
        self.ID = _id  # Unique identifier
        self.name = []  # Descriptive name of wall layer
        self.thickness = []  # thickness of wall segment
        self.height = []  # height of wall segment
        self.length = 1.0  # unit length of wall segment
        self.alignment = Alignment.Left  # wall alignment in relation to the topmost wall segment


class UniformLoad:
    """Uniformly distributed Load Class."""

    def __init__(self):
        self.x = []  # horiontal location of the start of the UDL, as measured from the wall
        self.y = []  # vertical location of the load, as measured from a given datum
        self.magnitude = []  # magnitude of the UDL in
        self.length = []  # length of the UDL, measured away from the wall


class PointForce:
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
                 name='Default Soil',
                 weight=18.0,
                 phi=30.0):
        self.name = name
        self.weight = weight
        self.phi = phi
        self.wall_friction = round(self.phi * 2 / 3, 1)
        self.cohesion = 0.0
        self.layer_thickness = 1.0
        self.isTopLayer = False
        self.top_offset = 0.0
        self.inclination = 0

    def ka(self):
        """Calculates active soil pressure coefficient"""
        _angle = radians(self.phi)
        _msg = '"{}": Active pressure coefficient was calculated as {}.'
        _ret = round((1 - sin(_angle)) / (1 + sin(_angle)), 3)
        _msg = _msg.format(self.name, _ret)
        # return ka and a message
        return [_ret, _msg]

    def kp(self):
        """Calculates passive soil pressure coefficient"""
        _angle = radians(self.phi)
        _msg = '"{}": Passive pressure coefficient was calculated as {}.'
        if self.phi < 90:
            _ret = round((1 + sin(_angle)) / (1 - sin(_angle)), 3)
            _msg = _msg.format(self.name, _ret)
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
        _msg = _msg.format(self.name, _ret)
        # return ka and a message
        return [_ret, _msg]


if __name__ == '__main--':
    soil = Soil
    pass
