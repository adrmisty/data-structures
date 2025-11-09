import math

class CuckooTable:
    """Hash table with Cuckoo hashing.

    We have two hash functions, which map 32-bit keys to buckets of a common
    hash table. Unused buckets contain None.
    """

    def __init__(self, num_buckets, hashes):
        """Initialize the table with the given number of buckets.
        The number of buckets is expected to stay constant."""

        # The array of buckets
        self.num_buckets = num_buckets
        self.table = [None] * num_buckets
        self.hashes = hashes

    def get_table(self):
        return self.table

    def lookup(self, key):
        """Check if the table contains the given key. Returns True or False."""

        b0 = self.hashes[0].hash(key)
        b1 = self.hashes[1].hash(key)
        # print("## Lookup key={} b0={} b1={}".format(key, b0, b1))
        return self.table[b0] == key or self.table[b1] == key

    def insert(self, key):
        """"Insert a new key to the table. Assumes that the key is not present yet.

        Theory notes about CUCKOO HASHING:
        ----------------------------------
        *  uses two hash functions (f and g) and places each key in one of two possible locations, then:
        
        1. insert looks inside both buckets (hash from f or g)
        2. if one is empty,insert there
        3. otherwise
        --> cuckoo kick out item from one of the buckets,
        hashing with the other function, and replace with new item
        --> this can lead to subsequent kicks and replacements
        
        4. insertion timeout: after LOG N attempts, give up
        and rehash everything with new choice of f and g
        --> m (2+ε)n, is set to 6logn 

        Args:
            key (int): 32-bit key to insert in the table
        
        """
        # https://ktiml.mff.cuni.cz/~fink/teaching/data_structures_I/tutorial_02.pdf sl. 4/12
        TIMEOUT = math.ceil(6 * math.log(self.num_buckets))
        
        # pos <- h1(x)
        pos = self.hashes[0].hash(key)

        for _ in range(TIMEOUT):
            # if T[pos] is empty then
            # T[pos] ← x; # return
            if self.table[pos] is None:
                self.table[pos] = key
                return
            
            # swap(x, T[pos])
            self.table[pos], key = key, self.table[pos]
            
            # if pos == h1(x)
            # then pos ← h2(x)
            # else pos ← h1(x)
            if pos == self.hashes[0].hash(key):
                pos = self.hashes[1].hash(key)
            else:
                pos = self.hashes[0].hash(key)

        # timeout reached
        self.rehash(key)

    def rehash(self, key):
        """ Relocate all items using new hash functions and insert a given key. """
        # (!!) 0. save keys before regeneration
        keys = [k for k in self.table if k is not None]
        keys.append(key)

        # 1. obtain new hash functions
        for h in self.hashes:
            h.regenerate()

        # 2. reinsert with new hash functions
        self.table = [None] * self.num_buckets
        for k in keys:
            self.insert(k)


    # -----------------------------------------------------------------------------------
    # https://ktiml.mff.cuni.cz/~fink/teaching/data_structures_I/tutorial_02.pdf sl. 6/16

    def insert_incorrect(self, key):
        """INCORRECT IMPLEMENTATION OF INSERT."""
        # this only passes small, fixed
        # doesnt even execute middle, let alone big or multiple test
        
        # 0. set insertion timeout to 6logn
        n = self.num_buckets
        m = (2+4) * n
        TIMEOUT = 6 * int(math.log2(m))
        
        k = key
        
        for _ in range(TIMEOUT):
            
            # 1. check both buckets hashed with f or g
            hash_f = self.hashes[0]
            bucket = hash_f.hash(k)
            
            # 2. if empty, insert there
            if self.table[bucket] is None:
                self.table[bucket] = k
                return

            # ------- 3. otherwise, cuckoo kick and swap
            k, self.table[bucket] = self.table[bucket], k

            # 1.x2
            hash_f = self.hashes[1]
            bucket = hash_f.hash(k)

            # 2.x2
            if self.table[bucket] is None:
                self.table[bucket] = k
                return
            
            # 3.x2
            k, self.table[bucket] = self.table[bucket], k 

        # 4. timeout reached, rehash
        self.rehash(k)
