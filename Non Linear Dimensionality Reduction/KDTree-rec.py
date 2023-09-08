from collections import namedtuple
from pprint import pformat
import numpy as np

class Node(namedtuple("Node", "location left_child right_child")):
    def __repr__(self):
        return pformat(self._asdict())

def kdtree(points, axis = 0):
    """ Given
     - a 2D numpy array points, where each column denotes a dimension and each
       row a datapoint
     - an integer axis indicating the dimension to split at the top level
    this recursive function creates and returns a KDTree as it was discussed
    in the lecture.
    """
    if points.shape[0] == 0:
        return None

    k = points.shape[1]  # assumes all points have the same dimension

    # Sort point list by axis and choose median as pivot element
    points = points[points[:, axis].argsort()] 
    median = points.shape[0] // 2

    # Create node and construct subtrees
    return Node(
        location=points[median],
        left_child=kdtree(points[:median], (axis+1)%k),
        right_child=kdtree(points[median + 1 :], (axis+1)%k)
    )


def one_NN_rec(tree, axis, query, neighbor):
    """
    This recursive function accepts
     - a KDTree tree
     - the axis along which the root node of tree splits
     - a query point query
     - the current nearest neighbor

    The function should return a tuple, which contains the distance
    to the query point and the location of the neighbor. For example the
    data points np.array([(1, 3), (1, 8), (2, 2), (2, 10), (3, 6), (4, 1), (5,
    4), (6, 8), (7, 4), (7, 7), (8, 2), (8, 5), (9, 9)]) should return for a
    query point [4,8] the result (2.0, array([6, 8])). 
    """

    return


def kNN_rec(tree, axis, query, neighbors, n_neighbors):
    """
    This recursive function accepts
     - a KDTree tree
     - the axis along which the root node of tree splits
     - a query point query
     - a current list of neighbors, sorted with ascending distance
       (list of pairs each containing the distance and the point itself)
     - the desired number of neighbors n_neighbors
    and modifies the neighbors list so that
     - points from the tree are added while we have fewer than n_neighbors
     - all closer points from the tree replace existing neighbors once we
       reached n_neighbors
    It returns the number of nodes that were visited during traversal and modifies
    the neighbors-object in-place.
    """

    return
