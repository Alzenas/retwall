# Analysis and design of cantilevered and propped
# reinforced concrete retaining walls

from structural.elements import *
from structural.materials import *

if __name__ == '__main__':
    structural_code = Aci31814
    c35 = Concrete(structural_code, "C35/45", 35, 25)
    c45 = Concrete(structural_code, "C45/55", 45, 25)

    # Define test soil layers --------------------------------------------
    geology = []
    numberOfSoilLayers = 4

    for i in range(0, numberOfSoilLayers):
        geology.append(Soil())
        geology[i].name = "Soil Layer {}".format(i)
        geology[i].top_offset = 0
        geology[i].isTopLayer = False

    i = 0
    geology[i].isTopLayer = True
    geology[i].top_offset = 1.5
    geology[i].layer_thickness = 1.0
    geology[i].inclination = 20.0

    i = 1
    geology[i].layer_thickness = 2.0

    i = 2
    geology[i].layer_thickness = 0.90

    i = 3
    geology[i].layer_thickness = 2.0

    verticalSoilPoints = [0]
    for i in range(0, numberOfSoilLayers):
        if (geology[i].isTopLayer):
            verticalSoilPoints.append(verticalSoilPoints[-1] + geology[i].top_offset)
        verticalSoilPoints.append(verticalSoilPoints[-1] + geology[i].layer_thickness)

    print(verticalSoilPoints)

    # Enf of Test Soil Layers Definitions ------------------------------------------------

    # Define test walls ------------------------------------------------------------------
    numberOfSegments = 4  # number of walls
    wallSegment = []
    for i in range(0, numberOfSegments):
        wallSegment.append(Wall(i))
        wallSegment[i].length = 1.0  # unit length of the wall

    i = 0  # first segment
    wallSegment[i].name = "Parapet"
    wallSegment[i].thickness = 150
    wallSegment[i].height = 1.2
    wallSegment[i].alignment = Alignment.Left

    i = 1  # second segment
    wallSegment[i].name = "Top Wall"
    wallSegment[i].thickness = 250
    wallSegment[i].height = 2.0
    wallSegment[i].alignment = Alignment.Left

    i = 2  # third segment
    wallSegment[i].name = "Lower Wall"
    wallSegment[i].thickness = 350
    wallSegment[i].height = 1.5
    wallSegment[i].alignment = Alignment.Left

    i = 3  # fourth segment (heel)
    wallSegment[i].name = "Heel"
    wallSegment[i].thickness = 250
    wallSegment[i].height = 0.95
    wallSegment[i].alignment = Alignment.Left

    verticalWallPoints = [0]
    for i in range(0, numberOfSegments):
        verticalWallPoints.append(wallSegment[i].height + verticalWallPoints[-1])

    print(verticalWallPoints)
    # enf of temporary wall definitions --------------------------------------

    # Collect all vertical points into a single, sorted list (use a set, to remove duplicates)
    verticalPoints = sorted(set(verticalSoilPoints + verticalWallPoints))
    print("Significant vertical points: {}".format(verticalPoints))


    pass
