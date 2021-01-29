# Analysis and design of cantilevered and propped
# reinforced concrete retaining walls

from structural.elements import *

if __name__ == '__main__':
    soil = Soil()
    soil.phi = 180
    print(soil.ka()[0], soil.ka()[1])
    print(soil.kp()[0], soil.kp()[1])
    print(soil.k0()[0], soil.k0()[1])
    pass
