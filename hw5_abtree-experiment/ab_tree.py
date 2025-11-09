#!/usr/bin/env python3

class ABNode:
    """Single node in an ABTree.

    Each node contains keys and children
    (with one more children than there are keys).
    We also store a pointer to node's parent (None for root).
    """
    def __init__(self, keys = None, children = None, parent = None):
        self.keys = keys if keys is not None else []
        self.children = children if children is not None else []
        self.parent = parent

    def find_branch(self, key):
        """ Try finding given key in this node.

        If this node contains the given key, returns (True, key_position).
        If not, returns (False, first_position_with_key_greater_than_the_given).
        """
        i = 0
        while (i < len(self.keys) and self.keys[i] < key):
            i += 1

        return (i < len(self.keys) and self.keys[i] == key, i)

    def insert_branch(self, i, key, child):
        """ Insert a new key and a given child between keys i and i+1."""
        self.keys.insert(i, key)
        self.children.insert(i + 1, child)


class ABTree:
    """A class representing the whole ABTree."""
    def __init__(self, a, b):
        assert a >= 2 and b >= 2 * a - 1, "Invalid values of a, b: {}, {}".format(a, b)
        self.a = a
        self.b = b
        self.root = ABNode(children=[None])

    def find(self, key):
        """Find a key in the tree.

        Returns True if the key is present, False otherwise.
        """
        node = self.root
        while node:
            found, i = node.find_branch(key)
            if found: return True
            node = node.children[i]
        return False

    def delete_min(self):
        """ Delete the smallest element. """
        node = self.root
        while node.children[0]:
            node = node.children[0]

        node.children.pop(0)
        node.keys.pop(0)

        while len(node.children) < self.a and node.parent:
            node = node.parent
            first = node.children[0]
            second = node.children[1]

            # Merge the second to the first
            if len(second.children) == self.a:
                if second.children[0]:
                    for c in second.children:
                        c.parent = first
                first.children.extend(second.children)
                first.keys.append(node.keys.pop(0))
                first.keys.extend(second.keys)
                node.children.pop(1)

            # Move the leftest child of the second to the first
            else:
                second.children[0].parent = first
                first.children.append(second.children.pop(0))
                first.keys.append(node.keys[0])
                node.keys[0] = second.keys.pop(0)

        if len(node.children) == 1:
            assert node == self.root
            node.parent = None
            self.root = node.children[0]

    # ----------------------------------------------------------------------------------
    # HW4: ab_tree insert + split

    def split_node(self, node, size):
        """Helper function for insert

        Split node into two nodes such that original node contains first _size_ children.
        Return new node and the key separating nodes.

        Parameters
        ----------
        node : ABNode
            original node in the tree, to be split
        size : int
            number of the first {size} children the original node should contain after the split

        Returns
        -------
        new_node : ABNode
            new node resulting after splitting the original
        median_key : int
            integer value of the key separating the new and the original nodes,
            being the median (or equivalently now the half of the size)
        """
        # if a node {v} is oversized, i.e. with b keys
        # split {v} into [L, m, R]
        # where m is the median between L and R (as given by the size)
        m = size // 2
        median_key = node.keys[m]
        
        # when we split a node we modify an existing one, and we create a new one
        new_node = ABNode(keys=node.keys[m + 1:], parent=node.parent)

        # split.1) re-assign children to the new node
        new_node.children = node.children[m + 1:]
        for child in new_node.children:
            if child: # could be [None]
                child.parent = new_node  

        # split.2) remove respective children from the existing one
        node.keys = node.keys[:m]
        node.children = node.children[:m + 1]

        return new_node, median_key

    def insert(self, key):
        """Add a given key to the tree, unless already present."""

        # 1. if the key to add is not found, 
        # it means we arrived at a external node (leaf)
        # iteratively re-assign {v} till it is the parent of the leaf
        v = self.root
        while v.children[0]:
            in_tree, leaf_i = v.find_branch(key)
            if in_tree: return
            v = v.children[leaf_i]
        in_tree, leaf_i = v.find_branch(key)
        if in_tree: return
        
        # 2. insert: make sure len(v.keys)+1 == num. children
        # None --> +1
        v.keys.insert(leaf_i, key); v.children.insert(leaf_i + 1, None)

        # 2. splits are necessary because we cannot directly add a new child to a leaf
        # all leaves must be at the same height
        # split oversized nodes: 
        while len(v.keys) >= self.b:
            # split.0) split/create new root
            if v.parent is None:
                new_root = ABNode(children=[v])
                v.parent = new_root
                self.root = new_root
            
            # split.1) split an existing node based on a median
            # apply upwards
            new_node, median_key = self.split_node(v, len(v.keys))
            # insert new node based on separating median key @ leaf index
            v.parent.insert_branch(*v.parent.find_branch(median_key)[1:], median_key, new_node)
            v = v.parent

