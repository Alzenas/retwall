from math import sin, radians, pi
from enum import Enum
from structural.matrices import assemble_local_matrix
from structural.materials import Concrete, Aci31814


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


class Shape(Enum):
    Rectangular = 0
    Contiguous = 1
    Secant = 2
    Sheet = 3


class RectangularSection:
    def __init__(self, _width, _depth):
        self.name = 'REC_{}x{}'.format(_width, _depth)
        self.width = _width
        self.depth = _depth
        self.area = self.get_section_area()
        self.Izz = self.get_moment_of_inertia()

    def get_moment_of_inertia(self):
        return self.width * self.depth ** 3 / 12

    def get_section_area(self):
        return self.width * self.depth


class CircularSection:
    def __init__(self, _diameter):
        self.diameter = _diameter
        self.area = self.get_section_area()
        self.Izz = self.get_moment_of_inertia()

    def get_moment_of_inertia(self):
        return pi * self.diameter ** 4 / 64

    def get_section_area(self):
        return 0.25 * pi * self.diameter ** 2


class Alignment(Enum):
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
        self.section = []  # thickness of wall segment
        self.height = []  # height of wall segment
        self.length = 1.0  # unit length of wall segment
        self.alignment = Alignment.Left.value  # wall alignment in relation to the topmost wall segment
        self.material = []  # wall segment material


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


class Position:
    def __init__(self):
        self.x = []  # x position
        self.y = []  # y position


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


class Node:
    def __init__(self, _id, _x, _y):
        self.id = _id
        self.x = _x
        self.y = _y


class BeamFiniteElement:
    def __init__(self, _id, _node1, _node2):
        self.id = _id
        self.material = Concrete(Aci31814, "Concrete C35", 35, 25)  # material assigned to the element
        self.node1 = _node1
        self.node2 = _node2
        self.length = self.get_length()
        self.section = RectangularSection(_width=1000, _depth=500)
        self.EI = self.get_EI()
        self.stiffness_matrix = self.get_stiffness_matrix()

    def get_length(self):
        # calculate length of element from node geometry
        return ((self.node2.y - self.node1.y) ** 2 + (self.node2.x - self.node1.x) ** 2) ** 0.5

    def get_EI(self):
        _E = self.material.get_modulus() * 1000000  # convert to N/m2
        _I = self.section.get_moment_of_inertia() / (1000 ** 4)  # convert to m4
        return _E * _I

    def get_stiffness_matrix(self):
        # assemble local matrix
        return assemble_local_matrix(self.get_length(), self.get_EI())

    def refresh(self):
        self.length = self.get_length()
        self.section.Izz = self.section.get_moment_of_inertia()
        self.section.area = self.section.get_section_area()
        self.EI = self.get_EI()
        self.stiffness_matrix = self.get_stiffness_matrix()


if __name__ == '__main__':
    soil = Soil

    node1 = Node(0, 0, 0)
    node2 = Node(1, 1, 1)
    fe = BeamFiniteElement(0, node1, node2)
    fe.get_stiffness_matrix()
    print(fe.stiffness_matrix)

    pass
