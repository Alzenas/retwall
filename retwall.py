# Analysis and design of cantilevered and propped
# reinforced concrete retaining walls

from structural.matrices import *
from structural.elements import *
from structural.materials import *

if __name__ == '__main__':
    import matplotlib.pyplot as plt

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

    print("Vertical soil points:", verticalSoilPoints)

    # Enf of Test Soil Layers Definitions ------------------------------------------------

    # Define test materials
    structural_code = Aci31814
    c35 = Concrete(structural_code, "C35/45", 35, 25)
    c45 = Concrete(structural_code, "C45/55", 45, 25)

    # Define test walls ------------------------------------------------------------------
    numberOfSegments = 4  # number of walls
    wallSegment = []
    for i in range(0, numberOfSegments):
        wallSegment.append(Wall(i))
        wallSegment[i].length = 1.0  # unit length of the wall
        wallSegment[i].alignment = Alignment.Left.value
        wallSegment[i].material = c35

    i = 0  # first segment
    wallSegment[i].name = "Parapet"
    wallSegment[i].height = 1.2

    i = 1  # second segment
    wallSegment[i].name = "Top Wall"
    wallSegment[i].height = 2.0

    i = 2  # third segment
    wallSegment[i].name = "Lower Wall"
    wallSegment[i].height = 1.5

    i = 3  # fourth segment (heel)
    wallSegment[i].name = "Heel"
    wallSegment[i].height = 0.95

    verticalWallPoints = [0]
    for i in range(0, numberOfSegments):
        verticalWallPoints.append(wallSegment[i].height + verticalWallPoints[-1])
    print("Vertical wall points:", verticalWallPoints)

    # enf of temporary wall definitions --------------------------------------

    # Collect all vertical points into a single, sorted list (use a set, to remove duplicates)
    verticalPoints = sorted(set(verticalSoilPoints + verticalWallPoints))
    print("Significant vertical points: {}".format(verticalPoints))

    # define cross sections
    section150 = RectangularSection(1000, 150)
    section250 = RectangularSection(1000, 250)
    section350 = RectangularSection(1000, 350)
    # assign cross sections to wall segments
    wallSegment[0].section = section150
    wallSegment[1].section = section150
    wallSegment[2].section = section150
    wallSegment[3].section = section150

    maxElementLength = 0.05
    dlengths = get_cumulative_discrete_lengths(maxElementLength, verticalPoints)


    nodes = []
    for i, point in enumerate(dlengths):
        nodes.append(Node(i, 0, point))
        if point == 4.7:
            print("Node ",i)

    elements = []
    for i, node in enumerate(nodes[:-1]):
        elements.append(BeamFiniteElement(i, node, nodes[i + 1]))

    height = 0
    for wall in wallSegment:
        for element in elements:
            if element.node1.y >= height:
                element.section = wall.section
                element.refresh()
        height += wall.height

    global_matrix = assemble_global_matrix(elements)

    # define a load matrix [V1, M1, V2, M2... Vn, Mn]
    load = get_empty_load_matrix(len(nodes))  # first create an empty load matrix
    load = set_udl_between_nodes(-10, 0, len(nodes) - 1, elements, load)  # then, apply UDL from node 0 to last node
    # load = set_linear_load_between_nodes(10, - 10, 0, len(nodes) - 1, elements, load)
    # load = set_point_force(-2 * 10, int(2 * len(nodes) / 3), load)

    load_bc = load.copy()
    # Assign boundary conditions to global stiffness matrix and load matrix END 1
    global_matrix, load_bc = set_nodal_boundary_conditions(0, global_matrix, load_bc, _condition='pinned')
    # Assign boundary conditions to global stiffness matrix and load matrix END 2
    global_matrix, load_bc = set_nodal_boundary_conditions(len(nodes)-1, global_matrix, load_bc, _condition='pinned')

    # solve matrix
    result = np.linalg.solve(global_matrix, load_bc)

    # extract element results and separate them
    x, y, theta, element_moments, nodal_moments, shears = get_element_results(result, elements)
    # convert displacements to mm (*1000) and round to 3 decimals
    y = list(map(lambda _k: round(1000 * _k, 3), y))

    # output to screen
    print("************** RESULTS SUMMARY ***************")
    print("Moment maxima: \t{} kNm and {} kNm".format(max(nodal_moments), min(nodal_moments)))
    print("Shear maxima: \t{} kN and {} kN".format(max(shears), min(shears)))
    print("Deflection maxima: \t{} mm and {} mm".format(max(y), min(y)))
    print("Sum of applied load: \t{} kN".format(round(sum(load) / 1000, 3)))
    print("**********************************************")

    print(5000 * 10000 * (7.4**4) / (384 * elements[0].get_EI()))

    # plot results
    fig, axis = plt.subplots(4, figsize=(8, 9), sharex=True)
    axis[0].plot(x, nodal_moments, marker='.')
    axis[1].plot(x, shears, marker='.', color='red')
    axis[2].plot(x, y, marker='.', color="orange", linestyle='--')
    axis[3].plot(x, theta, marker='.', color="green", linestyle='--')
    fig.suptitle("Beam Analysis Results")
    plt.xlabel('Distance')
    axis[0].set_ylabel("Bending moment")
    axis[1].set_ylabel("Shear force")
    axis[2].set_ylabel("Deflection")
    axis[3].set_ylabel("Rotations")
    axis[0].grid()
    axis[1].grid()
    axis[2].grid()
    axis[3].grid()
    plt.subplots_adjust(hspace=0.2)
    plt.subplots_adjust(left=0.15)
    plt.show()
