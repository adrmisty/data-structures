#!/usr/bin/env python3

class Node:
    """Node in a binary tree `Tree`"""

    def __init__(self, key, left=None, right=None, parent=None):
        self.key = key
        self.parent = parent
        self.left = left
        self.right = right
        if left is not None: left.parent = self
        if right is not None: right.parent = self

class Tree:
    """A simple binary search tree"""

    def __init__(self, root=None):
        self.root = root

    def rotate(self, node):
        """ Rotate the given `node` up.

        Performs a single rotation of the edge between the given node
        and its parent, choosing left or right rotation appropriately.
        """
        if node.parent is not None:
            if node.parent.left == node:
                if node.right is not None: node.right.parent = node.parent
                node.parent.left = node.right
                node.right = node.parent
            else:
                if node.left is not None: node.left.parent = node.parent
                node.parent.right = node.left
                node.left = node.parent
            if node.parent.parent is not None:
                if node.parent.parent.left == node.parent:
                    node.parent.parent.left = node
                else:
                    node.parent.parent.right = node
            else:
                self.root = node
            node.parent.parent, node.parent = node, node.parent.parent

    # ---------------------------------------------- HW2


    def lookup(self, key):
        """
        Look up the given key in the tree and splay the accessed node.

        [If a node with the requested key has been found,
        said node will be moved all the way to the root of the tree.]

        Parameters
        ----------
        key : int
            value of the key of the node to search for

        Returns
        -------
        node : Node
            node with the requested key if found, or None
        """
        node = self.root
        current = None

        while node is not None:
            current = node
            # found -> splay
            # keep (most-frequently-accessed) nodes closer to the root
            # to optimize further iterations of the same lookup(x)
            if node.key == key:
                self.splay(node)
                return node
            # otherwise -> go on
            node = node.left if key < node.key else node.right

        # last accessed of all
        if current is not None:
            self.splay(current)
        return None

    def insert(self, key):
        """
        Insert key into the tree and splay the inserted node, move it
        all the way to the root.

        Parameters
        ----------
        key : int
            value of the key of the new node to be inserted and splayed
        """
        # empty tree -> inserted node is root
        if self.root is None:
            self.root = Node(key)
            return

        # already in the tree -> do nothing, but splay it
        node = self.root
        parent = None
        while node is not None:
            parent = node
            if key == node.key:
                self.splay(node)
                return
            node = node.left if key < node.key else node.right

        # not in the tree -> insert (left/right) + splay it
        inserted = Node(key, parent=parent)
        if key < parent.key:
            parent.left = inserted
        else:
            parent.right = inserted
        self.splay(inserted)

    def remove(self, key):
        """
        Remove the given key from the tree, splaying the parent of the removed node.

        Parameters
        ----------
        key : int
            value of the key of the node to be removed (if in the tree), whose parent
            (if in the tree) will exist

        """
        node = self.lookup(key)

        # not in the tree
        if node is None:
            return

        if node.left is None or node.right is None:
            substitute = node.left if node.left else node.right
        else:
            # get successor of the node to remove
            successor = self.successor(node)
            node.key = successor.key
            node = successor
            substitute = node.right

        parent = node.parent

        # do effective replacements with left/right sides
        if node.parent is not None:
            if node.parent.left == node:
                node.parent.left = substitute
            else:
                node.parent.right = substitute
        else:
            self.root = substitute
        if substitute is not None:
            substitute.parent = node.parent

        # if not the root of the tree, 
        # after replacements are done,
        # splay it
        if parent is not None:
            self.splay(parent)

    def splay(self, node):
        """Splay the given node.

        If a single rotation needs to be performed, perform it as the last rotation
        (i.e., to move the splayed node to the root of the tree).

        Parameters
        ----------
        node : Node
            node to be splayed in the tree, x -> splay(x)
        """
        # for splay you must take into account
        # the parent node(s) of the node
        while node.parent is not None:
            
            # zig (1 rotation)
            if node.parent.parent is None:
                self.rotate(node)
            
            # zig-zig (2 rotations)
            elif (node.parent.left == node) == (node.parent.parent.left == node.parent):  # Zig-Zig step
                self.rotate(node.parent)
                self.rotate(node)
            
            # zig-zag (2 rotations)
            else:
                self.rotate(node)
                self.rotate(node)

    # ---------------------------------------------- HW1

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