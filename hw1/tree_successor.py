#!/usr/bin/env python3

class Node:
    """Node in a binary tree `Tree`"""

    def __init__(self, key, left=None, right=None, parent=None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = parent

class Tree:
    """A simple binary search tree"""

    def __init__(self, root=None):
        self.root = root

    def insert(self, key, node=None):
        """Insert key into the tree.

        If the key is already present, do nothing.
        If the node is given, start searching a new position from that node.
        """
        if self.root is None:
            self.root = Node(key)
            return self.root

        if not node:
            node = self.root

        while node.key != key:
            if key < node.key:
                if node.left is None:
                    node.left = Node(key, parent=node)
                node = node.left
            else:
                if node.right is None:
                    node.right = Node(key, parent=node)
                node = node.right

        return node


    def left(self, node):
        """
        Auxiliary function: retrieves the smallest node
        (that is, the most leftwards), of a subtree.
        """
        l = node
        while l.left:
            l = l.left
        return l
    
    def right_of(self, node):
        """
        Auxiliary function: retrieves the biggest node
        for which a given node is on the left of.
        """
        while node.parent and node.parent.right == node:
            node = node.parent
        return node.parent


    def successor(self, node=None):
        """
        Return successor of the given node.

        Parameters
        ----------
        self : Tree
            binary search tree (BST) instance
        node : Node
            node of the BST for which we'd like to find the successor
            for a None argument, we 
            
        
        Return
        ------
        node : Node
            - the successor, being the smallest element of the set which has a greater key than 'node', 
                if it exists. if not, None is returned
            - if no node is specified for successor search, return the node with the smallest key

        """
        succ_root = None
        if node is None:
            succ_root = self.root # 1. get the node with the smallest key
        elif node.right:
            succ_root = node.right # 2. get the successor node on the right subtree
        
        if succ_root:
            return self.left(succ_root) # -> traverse leftwards from the root until minimum is reached

        else:
            return self.right_of(node) # 3. node should be in the left subtree of the successor