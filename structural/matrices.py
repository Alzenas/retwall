import numpy as np
from structural.constant import LOCAL_ELEMENT_STIFFNESS, LOCAL_ELEMENT_L2, LOCAL_ELEMENT_L


def assemble_local_matrix(_L, _EI):
    """Adjusts local element stiffness matrix, to include L and L2 terms."""
    # _L = length of local element
    # _EI = Product of Young's modulus and Moment of Inertia of the local element
    # _local_matrix = Local element stiffness matrix

    # include L terms
    _matrixL = LOCAL_ELEMENT_L * _L
    _matrixL[_matrixL == 0] = 1  # replace 0's with 1's

    # include L2 terms
    _matrixL2 = LOCAL_ELEMENT_L2 * _L ** 2
    _matrixL2[_matrixL2 == 0] = 1  # replace 0's with 1's

    # define a coefficient
    _EIL3 = _EI / _L ** 3

    # adjust local element stiffness matrix
    _local_matrix = LOCAL_ELEMENT_STIFFNESS * _matrixL * _matrixL2 * _EIL3

    return _local_matrix


# def assemble_global_matrix(_lengths, _EI):
#     """Assembles a global stiffness matrix."""
#
#     # determine number of nodes from the length matrix
#     _num_nodes = len(_lengths) + 1
#
#     # create an empty matrix first
#     _global = np.zeros((_num_nodes * 2, _num_nodes * 2))
#
#     # fill global matrix with local element stiffness matrices
#     _num_elements = num_nodes - 1
#
#     # assemble local element matrices into a single array
#     _local_matrices = []
#     for i in range(0, _num_elements):
#         _local_matrices.append(assemble_local_matrix(_lengths[i], _EI))
#
#     for i in range(0, _num_elements):
#         _node = i + 1
#         _i = (_node - 1) * 2  # overlap
#         _j = _i + 4  # four is added since local matrix has 4 rows
#         _global[_i:_j, _i:_j] += _local_matrices[i]  # add local element matrix to a global matrix
#
#     return _global

def assemble_global_matrix(_beam_elements):
    """Assembles a global stiffness matrix."""

    # determine number of nodes from the length matrix
    _num_nodes = len(_beam_elements) + 1

    # create an empty matrix first
    _global = np.zeros((_num_nodes * 2, _num_nodes * 2))

    # fill global matrix with local element stiffness matrices
    _num_elements = _num_nodes - 1

    # assemble global matrix from local stiffness matrices
    for i in range(0, _num_elements):
        _node = i + 1
        _i = (_node - 1) * 2  # overlap
        _j = _i + 4  # four is added since local matrix has 4 rows
        _global[_i:_j, _i:_j] += _beam_elements[i].get_stiffness_matrix()  # add local element matrix to a global matrix

    return _global


# def get_element_results(_results, _lengths, _EI):
#     """Assembles element results into a single matrix"""
#     # Results of the linear solver are comprised of a single matric which
#     # contains calculated displacements and rotations:
#     # x(1), theta(1) x(2), theta(2), .... x(n), theta(n)
#
#     # first separate displacements from rotations
#     _y = _results[0::2]  # takes every other value, starting from index 0
#     # _y = lambda x: round(x, 1): _y
#     _theta = _results[1::2]  # takes every other value, starting from index 1
#
#     # from derivations from first principles the formula for the moment
#     #
#     # M1 = -EI(-6d1/L2 - 4t1/L + 6d2/L2 - 2t2/L)        // moment at node 1
#     # M2 = -EI(+6d1/L2 + 2t1/L - 6d2/L2 + 4t2/L)        // moment at node 2
#     # Q  = -EI/L2 (12d1/L + 6t1 - 12d2/L + 6t2          // shear force
#     #
#     # where d1 = displacement at node 1, d2 = displacement at node 2
#     #       t1 = rotation at node 1, t2 = rotation at node 2
#     #       L = length of element
#     #       L2 = length of element squared
#     #       EI = product of Young's modulus and moment of inertia for the element
#
#     _element_m = []  # element moments (node 1 and node 2)
#     _nodal_m = []  # nodal moments
#     _element_q = []  # element shear force (average shear, across the element)
#     _nodal_q = []  # nodal shear
#     _x = [0]
#     for i in range(0, len(_y) - 1):
#         _L = _lengths[i]
#         # derive nodal x values
#         _x.append(round(_x[-1] + _L, 3))
#
#         # define parameters used in the equation
#         _L2 = _L ** 2
#         _EIL2 = _EI / _L2
#         _d1 = _y[i]
#         _d2 = _y[i + 1]
#         _t1 = _theta[i]
#         _t2 = _theta[i + 1]
#
#         # calculate nodal moments and average lement shears
#         _m1 = -_EI * (- 6 * _d1 / _L2 - 4 * _t1 / _L + 6 * _d2 / _L2 - 2 * _t2 / _L) / 1000  # node 1 moment, in kNm
#         _m2 = -_EI * (+ 6 * _d1 / _L2 + 2 * _t1 / _L - 6 * _d2 / _L2 + 4 * _t2 / _L) / 1000  # node 2 moment, in kNm
#         _qe = -_EIL2 * (12 * _d1 / _L + 6 * _t1 - 12 * _d2 / _L + 6 * _t2) / 1000  # average element shear, in kN
#
#         # hold calculated values into arrays
#         _nodal_m.append(round(_m1, 3))  # moments at node 1
#         _element_m.append([round(_m1, 3), round(_m2, 3)])  # moments at nodes 1 and 2 (as an array)
#         _element_q.append(_qe)  # average element shear
#
#     # add last moment (node 2) to nodal moments array
#     _nodal_m.append(_element_m[-1][1])
#
#     # Derive nodal shears
#     # Determine first nodal shear
#     _qn = 0.5 * (_element_q[0] + _element_q[1])
#     _nodal_q.append(round(_element_q[0] + (_element_q[0] - _qn), 3))
#     # Determine the remaining nodal shears
#     for i in range(0, len(_element_q) - 1):
#         _qn = 0.5 * (_element_q[i] + _element_q[i + 1])
#         _nodal_q.append(round(_qn, 3))
#     # Now, derive shear for the last node:
#     _qn = 0.5 * (_element_q[-2] + _element_q[-1])  # average of the last and penultimate element
#     _nodal_q.append(round(_element_q[-1] + (_element_q[-1] - _qn), 3))
#
#     return _x, _y, _theta, _element_m, _nodal_m, _nodal_q
def get_element_results(_results, _elements):
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
    _x = [0]
    for i in range(0, len(_y) - 1):
        _L = _elements[i].length
        _EI = _elements[i].get_EI()
        # derive nodal x values
        _x.append(round(_x[-1] + _L, 3))

        # define parameters used in the equation
        _L2 = _L ** 2
        _EIL2 = _EI / _L2
        _d1 = _y[i]
        _d2 = _y[i + 1]
        _t1 = _theta[i]
        _t2 = _theta[i + 1]

        # calculate nodal moments and average element shears
        _m1 = -_EI * (- 6 * _d1 / _L2 - 4 * _t1 / _L + 6 * _d2 / _L2 - 2 * _t2 / _L) / 1000  # node 1 moment, in kNm
        _m2 = -_EI * (+ 6 * _d1 / _L2 + 2 * _t1 / _L - 6 * _d2 / _L2 + 4 * _t2 / _L) / 1000  # node 2 moment, in kNm
        _qe = -_EIL2 * (12 * _d1 / _L + 6 * _t1 - 12 * _d2 / _L + 6 * _t2) / 1000  # average element shear, in kN

        # hold calculated values into arrays
        _nodal_m.append(round(_m1, 3))  # moments at node 1
        _element_m.append([round(_m1, 3), round(_m2, 3)])  # moments at nodes 1 and 2 (as an array)
        _element_q.append(_qe)  # average element shear

    # add last moment (node 2) to nodal moments array
    _nodal_m.append(_element_m[-1][1])

    # Derive nodal shears
    # Determine first nodal shear
    _qn = 0.5 * (_element_q[0] + _element_q[1])
    _nodal_q.append(round(_element_q[0] + (_element_q[0] - _qn), 3))
    # Determine the remaining nodal shears
    for i in range(0, len(_element_q) - 1):
        _qn = 0.5 * (_element_q[i] + _element_q[i + 1])
        _nodal_q.append(round(_qn, 3))
    # Now, derive shear for the last node:
    _qn = 0.5 * (_element_q[-2] + _element_q[-1])  # average of the last and penultimate element
    _nodal_q.append(round(_element_q[-1] + (_element_q[-1] - _qn), 3))

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


def get_points_distance(_points):
    """Determins a distance between two adjacent points in a matrix."""
    _dist = []  # distances between points
    # dtermine distances between adjacent points
    for i in range(0, len(_points) - 1):
        _dist.append(round(abs(_points[i] - _points[i + 1]), 3))
    return _dist


def get_cumulative_discrete_lengths(_minLength, _points):
    """Determine a matrix of element lengths."""

    # get distances between adjacent points in a points matrix
    _dist = get_points_distance(_points)
    _div = []
    _elem = []
    # Determine divisors
    for i in range(0, len(_dist)):
        # calculate whole number divisions between points, so that the element lengths are close to required
        _tmp = round(_dist[i] / _minLength, 0)
        if _tmp > 0:
            # round the divisions to a closest whole number
            _div.append((round(_dist[i] / _minLength, 0)))
        else:
            # in case the rounding resulted in 0
            _div.append(1)

        # further divide into chunks
        for j in range(0, int(_div[-1])):
            _tmp = round(_points[i] + j * (_dist[i] / _div[-1]), 3)
            _elem.append(_tmp)

    # add the last point from the points marix
    _elem.append(_points[-1])

    return _elem


def get_empty_load_matrix(_nodes):
    _load_matrix = np.zeros(_nodes * 2)  # multiply by two to account for forces AND moments
    return _load_matrix


def set_point_force(_f, _node, _load_matrix):
    """Applies a nadal force to a specified node."""
    # for force passed in kN
    _load_matrix[_node * 2] = _f * 1000
    return _load_matrix


def set_point_moment(_m, _node, _load_matrix):
    """Applies a nadal moment to a specified node."""
    # for moment passed in kNm
    _load_matrix[_node * 2 + 1] = _m * 1000
    return _load_matrix


# def set_udl_between_nodes(_udl, _node_from, _node_to, _element_lengths, _load_matrix):
#     """Applies a Uniformly Distributed Load, between specified nodes, to a load matrix."""
#     _current_node = _node_from * 2  # *2 since each node has two values, one for force, one for moments
#     _last_node = _node_to * 2  # *2 since each node has two values, one for force, one for moments
#
#     # in case node entries are reversed, order them
#     if _current_node > _last_node:
#         _tmp = _last_node
#         _last_node = _current_node
#         _current_node = _tmp
#
#     if _current_node == _last_node:
#         _load_matrix = set_point_force(_udl, _node_from, _load_matrix)
#     else:
#         for _length in _element_lengths[_node_from:_node_to]:
#             # split force into two, since UDL is applied as a half of total load upon each node
#             _udl2 = 1000 * _udl * _length / 2  # convert to Newtons by * 1000
#             _load_matrix[_current_node] += _udl2  # load to node 1
#             _load_matrix[_current_node + 2] += _udl2  # load to node 2
#             _current_node += 2  # next node for force application
#
#     return _load_matrix
def set_udl_between_nodes(_udl, _node_from, _node_to, _elements, _load_matrix):
    """Applies a Uniformly Distributed Load, between specified nodes, to a load matrix."""
    _current_node = _node_from * 2  # *2 since each node has two values, one for force, one for moments
    _last_node = _node_to * 2  # *2 since each node has two values, one for force, one for moments

    # in case node entries are reversed, order them
    if _current_node > _last_node:
        _tmp = _last_node
        _last_node = _current_node
        _current_node = _tmp

    if _current_node == _last_node:
        _load_matrix = set_point_force(_udl, _node_from, _load_matrix)
    else:
        for _element in _elements[_node_from:_node_to]:
            _length = _element.length
            # split force into two, since UDL is applied as a half of total load upon each node
            _udl2 = 1000 * _udl * _length / 2  # convert to Newtons by * 1000
            _load_matrix[_current_node] += _udl2  # load to node 1
            _load_matrix[_current_node + 2] += _udl2  # load to node 2
            _current_node += 2  # next node for force application

    return _load_matrix


# def set_linear_load_between_nodes(_f1, _f2, _node_from, _node_to, _element_lengths, _load_matrix):
#     """Apply linearly varying load between two nodes."""
#     _current_node = _node_from * 2  # *2 since each node has two values, one for force, one for moments
#     _last_node = _node_to * 2  # *2 since each node has two values, one for force, one for moments
#
#     # in case node entries are reversed, order them
#     if _current_node > _last_node:
#         _tmp = _last_node
#         _last_node = _current_node
#         _current_node = _tmp
#         # also assume then that the loads are reversed (as in specified in different order)
#         # so, swap values
#         _tmp = _f2
#         _f2 = _f1
#         _f1 = _tmp
#
#     if _current_node == _last_node:
#         # if the nodes are the same, then apply the average value at the node
#         _load_matrix = set_point_force(0.5 * (_f1 + _f2), _node_from, _load_matrix)
#     else:
#         _f1 *= 1000
#         _f2 *= 1000
#         # first establish a linearly varying force
#         _considered_length = sum(_element_lengths[_node_from:_node_to])  # length of segment considered
#         _var_udl = (_f2 - _f1) / _considered_length
#         _node_force = _f1
#         for _length in _element_lengths[_node_from:_node_to]:
#             # apply load to left (first) node of the element
#             _load_matrix[_current_node] += _node_force * (0.5 * _length)  # load to node 1
#             _load_matrix[_current_node + 2] += (_node_force + (_length * _var_udl)) * (0.5 * _length)  # load to node 2
#             _current_node += 2  # next node for force application
#             _node_force += _var_udl * _length
#
#         # and finally set the force upon the last (right) node
#         _load_matrix[_last_node] = _f2 * (0.5 * _element_lengths[_node_from:_node_to][-1])
#
#         return _load_matrix
def set_linear_load_between_nodes(_f1, _f2, _node_from, _node_to, _elements, _load_matrix):
    """Apply linearly varying load between two nodes."""
    _current_node = _node_from * 2  # *2 since each node has two values, one for force, one for moments
    _last_node = _node_to * 2  # *2 since each node has two values, one for force, one for moments

    # in case node entries are reversed, order them
    if _current_node > _last_node:
        _tmp = _last_node
        _last_node = _current_node
        _current_node = _tmp
        # also assume then that the loads are reversed (as in specified in different order)
        # so, swap values
        _tmp = _f2
        _f2 = _f1
        _f1 = _tmp

    if _current_node == _last_node:
        # if the nodes are the same, then apply the average value at the node
        _load_matrix = set_point_force(0.5 * (_f1 + _f2), _node_from, _load_matrix)
    else:
        _f1 *= 1000
        _f2 *= 1000
        # length under consideration
        _considered_length = sum(list(map(lambda _k: _k.length, _elements[_node_from:_node_to])))
        # gradient of linearly varying force
        _var_udl = (_f2 - _f1) / _considered_length
        # force at left-most node
        _node_force = _f1
        print("Considered length:", _considered_length)
        for _element in _elements[_node_from:_node_to]:
            _length = _element.length
            # apply load to left (first) node of the element
            _load_matrix[_current_node] += _node_force * (0.5 * _length)  # load to node 1
            _load_matrix[_current_node + 2] += (_node_force + (_length * _var_udl)) * (0.5 * _length)  # load to node 2
            _current_node += 2  # next node for force application
            _node_force += _var_udl * _length

        # and finally set the force upon the last (right) node
        _load_matrix[_last_node] = _f2 * (0.5 * _elements[_node_from:_node_to][-1].length)

        return _load_matrix


if __name__ == '__main__':
    pass
