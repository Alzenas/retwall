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
