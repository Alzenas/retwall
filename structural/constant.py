import numpy as np

# define a single beam element stiffness matrix coefficients
LOCAL_ELEMENT_STIFFNESS = np.array([[12, 6, -12, 6], [6, 4, -6, 2], [-12, -6, 12, -6], [6, 2, -6, 4]], dtype=float)
# define multiplication matrix, to include L into stiffness matrix
LOCAL_ELEMENT_L = np.array([[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]])
# define multiplication matrix, to include L^2 into stiffness matrix
LOCAL_ELEMENT_L2 = np.array([[0, 0, 0, 0], [0, 1, 0, 1], [0, 0, 0, 0], [0, 1, 0, 1]])
