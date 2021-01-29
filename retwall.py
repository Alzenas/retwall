# Analysis and design of cantilevered and propped
# reinforced concrete retaining walls

from structural.elements import *
from structural.materials import *

if __name__ == '__main__':
    structural_code = Aci31814
    c35 = Concrete(structural_code, "C35/45", 35, 25)
    c45 = Concrete(structural_code, "C45/55", 45, 25)

    soil = Soil()
    soil.phi = 30

    print(soil.ka()[0], soil.ka()[1])
    print(soil.kp()[0], soil.kp()[1])
    print(soil.k0()[0], soil.k0()[1])

    print(soil.phi)
    print(soil.wall_friction)


    pass
