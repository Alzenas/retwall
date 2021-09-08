import numpy as np
from scipy import sparse

# define a single beam element stiffness matrix coefficients
local_element_stiffness = np.array([[12, 6, -12, 6], [6, 4, -6, 2], [-12, -6, 12, -6], [6, 2, -6, 4]], dtype=float)
# define multiplication matrix, to include L into stiffness matrix
local_element_L = np.array([[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]])
# define multiplication matrix, to include L^2 into stiffness matrix
local_element_L2 = np.array([[0, 0, 0, 0], [0, 1, 0, 1], [0, 0, 0, 0], [0, 1, 0, 1]])


def assemble_local_matrix(_local_matrix, _L, _EI):
    """Adjusts local element stiffness matrix, to include L and L2 terms."""
    # _L = length of local element
    # _EI = Product of Young's modulus and Moment of Inertia of the local element
    # _local_matrix = Local element stiffness matrix

    # include L terms
    _matrixL = local_element_L * _L
    _matrixL[_matrixL == 0] = 1  # replace 0's with 1's

    # include L2 terms
    _matrixL2 = local_element_L2 * (_L ** 2)
    _matrixL2[_matrixL2 == 0] = 1  # replace 0's with 1's

    # define a coefficient
    _EIL3 = _EI / _L ** 3

    # adjust local element stiffness matrix
    _local_matrix = _local_matrix * _matrixL * _matrixL2 * _EIL3

    return _local_matrix


def assemble_global_matrix(_local_matrix, _num_nodes):
    """Assembles a global stiffness matrix."""

    # create an empty matrix first
    _global = np.zeros((_num_nodes * 2, _num_nodes * 2))

    # fill global matrix with local element stiffness matrices
    _num_elements = num_nodes - 1
    for i in range(0, _num_elements):
        _node = i + 1
        _i = (_node - 1) * 2  # overlap
        _j = _i + 4  # four is added since local matrix has 4 rows
        _global[_i:_j, _i:_j] += _local_matrix  # add local element matrix to a global matrix

    return _global


def get_element_results(_results, _L, _EI):
    """Assembles element results into a single matrix"""
    # Results of the linear solver are comprised of a single matric which
    # contains calculated displacements and rotations:
    # x(1), theta(1) x(2), theta(2), .... x(n), theta(n)

    # first separate displacements from rotations
    _y = _results[0::2]  # takes every other value, starting from index 0
    # _y = lambda x: round(x, 1): _y
    _theta = _results[1::2]  # takes every other value, starting from index 1

    # from derivations from first principles the formula for the moment
    #
    # M1 = -EI(-6d1/L2 - 4t1/L + 6d2/L2 - 2t2/L)        // moment at node 1
    # M2 = -EI(+6d1/L2 + 2t1/L - 6d2/L2 + 4t2/L)        // moment at node 2
    # Q  = -EI/L2 (12d1/L + 6t1 - 12d2/L + 6t2          // shear force
    #
    # where d1 = displacement at node 1, d2 = displacement at node 2
    #       t1 = rotation at node 1, t2 = rotation at node 2
    #       L = length of element
    #       L2 = length of element squared
    #       EI = product of Young's modulus and moment of inertia for the element

    _element_m = []  # element moments (node 1 and node 2)
    _nodal_m = []  # nodal moments
    _element_q = []  # element shear force (average shear, across the element)
    _nodal_q = []  # nodal shear
    _L2 = _L ** 2
    _EIL2 = _EI / _L2
    _x = [0]
    for i in range(0, len(_y) - 1):
        # derive nodal x values
        _x.append(_x[-1] + _L)

        # define parameters used in the equation
        _d1 = _y[i]
        _d2 = _y[i + 1]
        _t1 = _theta[i]
        _t2 = _theta[i + 1]
        _m1 = -_EI * (- 6 * _d1 / _L2 - 4 * _t1 / _L + 6 * _d2 / _L2 - 2 * _t2 / _L) / 1000  # in kNm
        _m2 = -_EI * (+ 6 * _d1 / _L2 + 2 * _t1 / _L - 6 * _d2 / _L2 + 4 * _t2 / _L) / 1000  # in kNm
        _qe = -_EIL2 * (12 * _d1 / _L + 6 * _t1 - 12 * _d2 / _L + 6 * _t2) / 1000  # in kN
        _nodal_m.append(round(_m1, 3))  # moments at node 1
        _element_m.append([round(_m1, 3), round(_m2, 3)])
        _element_q.append(_qe)

    # add last moment (node 2) to nodal moments array
    _nodal_m.append(_element_m[-1][1])

    # derive nodal shears from average (element) shears
    for i in range(0, len(_element_q) - 1):
        _qn = 2 * _element_q[i] - 0.5 * (_element_q[i] + _element_q[i + 1])
        _nodal_q.append(round(_qn, 3))
    # now derive shear for last two nodes
    # penultimate node
    _qn = 0.5 * (_element_q[-2] + _element_q[-1])  # average of the last and penultimate element
    _nodal_q.append(round(_qn, 3))
    # ultimate (last) node
    _qn = 2 * _element_q[-1] - _nodal_q[-1]
    _nodal_q.append(round(_qn, 3))

    return _x, _y, _theta, _element_m, _nodal_m, _nodal_q


def set_nodal_boundary_conditions(_node, _global_matrix, _loads, _condition="fixed"):
    """Sets boundary conditions to a global stiffness matrix"""
    # condition: fixed, pinned, free

    # first, get the shape of global stiffness matrix
    _rows, _cols = np.shape(_global_matrix)

    if _node >= 0 and _node < (_rows / 2):
        _boundary_row = np.zeros(_cols)  # create a row of zeros
        _boundary_row = np.vstack((_boundary_row, _boundary_row))  # and stack another row of zeros on top of it
        # for a fixed condition, restrain both displacements and rotations
        if _condition == "fixed":
            _boundary_row[0, _node * 2] = 1  # displacements row
            _boundary_row[1, _node * 2 + 1] = 1  # rotations row
            _loads[_node * 2] = 0
            _loads[_node * 2 + 1] = 0
        # for a pinned condition, restrain only displacements
        elif _condition == "pinned":
            _boundary_row[0, _node * 2] = 1  # displacements row
            _boundary_row[1] = _global_matrix[_node * 2 + 1]  # rotations row copied from global stiffness matrix
            _loads[_node * 2] = 0
        else:
            _boundary_row[0] = _global_matrix[_node * 2]  # copy displacements row from global matrix
            _boundary_row[1] = _global_matrix[_node * 2 + 1]  # copy rotations row from global matrix

        # replace rows in global matrix
        for i in range(0, 2):
            _global_matrix[_node * 2 + i] = _boundary_row[i]
    else:
        print("*** WARNING ***\tFailed to assign boundary conditions at Node {}.\n".format(_node))

    return _global_matrix, _loads


if __name__ == '__main__':
    # *****************    TEST AREA HERE   **************************************
    from structural.materials import Concrete, Aci31814
    import matplotlib.pyplot as plt

    num_nodes = 21  # number of nodes to use for analysis
    num_elements = num_nodes - 1  # inferred number of elements
    L = 5  # overall length of beam in m
    Le = L / num_elements  # length of local element

    # define concrete
    c35 = Concrete(Aci31814, "C35/45", 35, 24.5)
    Ec = 1000000 * c35.Modulus  # Young's Modulus in N/m2

    # define beam section properties
    width = 250  # in mm
    depth = 400  # in mm

    # second moment of area
    Iz = (width / 1000) * (depth / 1000) ** 3 / 12  # Test section 400 x 600 mm

    # stiffness parameter EI
    EI = Ec * Iz

    # applied Uniformly Distributed Load:
    q = -10  # applied UDL in kN/m
    q0 = 1000 * q * Le  # force derived from UDL for application to each nodes
    # define a test load matrix [V1, M1, V2, M2... Vn, Mn]
    load = []
    for i in range(0, num_nodes):
        load.append(q0)  # applied force
        load.append(0)  # applied moment
    load[0] = 0.5 * load[0]  # load on first node is only a half
    load[-2] = 0.5 * load[-2]  # load on the last node is only a half

    # prepare local matrix (include element length and EI into it)
    local_matrix = assemble_local_matrix(local_element_stiffness, Le, EI)
    # assemble global matrix
    global_matrix = assemble_global_matrix(local_matrix, num_nodes)

    # Assign boundary conditions to global stiffness matrix and load matrix END 1
    global_matrix, load = set_nodal_boundary_conditions(0, global_matrix, load, _condition='pinned')
    # Assign boundary conditions to global stiffness matrix and load matrix END 2
    global_matrix, load = set_nodal_boundary_conditions(num_nodes - 1, global_matrix, load, _condition='pinned')

    # solve matrix
    result = np.linalg.solve(global_matrix, load)

    # extract element results and separate them
    x, y, theta, element_moments, nodal_moments, shears = get_element_results(result, Le, EI)
    # convert displacements to mm (*1000) and round to 3 decimals
    y = list(map(lambda _k: round(1000 * _k, 3), y))

    # output to screen
    print("************** RESULTS SUMMARY ***************")
    print("Moment maxima: \t{} kNm and {} kNm".format(max(nodal_moments), min(nodal_moments)))
    print("Shear maxima: \t{} kN and {} kN".format(max(shears), min(shears)))
    print("Deflection maxima: \t{} mm and {} mm".format(max(y), min(y)))
    print("**********************************************")

    # plot results
    plt.figure(figsize=(10, 8))
    plt.grid(True, which="both")
    # plt.plot(x, 1000 * y)  # y multiplied by 1000 to convert m to mm
    plt.plot(x, nodal_moments)  # y multiplied by 1000 to convert m to mm
    plt.xlabel('distance')
    # plt.ylabel('displacement')
    plt.ylabel('moment')
    plt.show()
