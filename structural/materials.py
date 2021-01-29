# structural materials
from math import sqrt
from enum import Enum


class CodeType(Enum):
    """Enumeration of Structural Design Codes."""
    ACI318_14 = "ACI318-14"
    ACI318_10 = "ACI318-10"


class MaterialType(Enum):
    Concrete = "Structural Concrete"
    Steel = "Structural Steel"
    Reinforcement = "Concrete Reinforcement Bars"


class Code(object):
    """Structural Code for use in calculations. Pass through class."""
    pass


class Aci31810(Code):
    """ACI 318-10 Code Definitions."""
    # Defined for later use
    cType = CodeType.ACI318_10  # define type by CodeType(Enum)
    CodeName = cType.value


class Aci31814(Code):
    """ACI 318-14 Code Definitions."""
    # Defined for later use
    cType = CodeType.ACI318_14  # define type by CodeType(Enum)
    CodeName = cType.value


class Concrete:
    """Structural concrete class."""
    MaterialType = MaterialType.Concrete.value

    def __init__(self, code, name, fc, weight):
        self.code = code
        self.Name = name
        self.CompressionStrength = fc
        self.UnitWeight = weight
        self.Modulus = self.get_modulus()
        self.LightweightFactor = 1.0

    def get_modulus(self):
        """Calculates Young's Modulus of concrete in accordance with design code specified."""
        _ct = CodeType  # temp definition, for easier typing in code

        # define a condition for ACI codes
        _aci_code = bool(self.code.cType == _ct.ACI318_10 or self.code.cType == _ct.ACI318_14)

        _Ec = 0
        if _aci_code:
            # calculate Young's Modulus of concrete based on ACI318 codes
            _Ec = 4700 * sqrt(self.CompressionStrength)
        else:
            pass

        return round(_Ec, 0)


if __name__ == '__main__':
    pass
