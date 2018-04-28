#!/usr/bin/env python3

from bisect import bisect_left, bisect_right

class OrderedHashSet:
    """
        Container that has O(1) __contains__ check that is done by __hash__
        method of element.
        Also, inserted elements are orderedy by __lt__ method, so the smallest
        element will be available by @getElem method
    """
    def __init__(self):
        self.table = {}
        self.keys_list = []

    def add(self, elem):
        """
            Adds element @elem into OrderedHashSet, select order by @elem.__lt__
        """
        self.table[elem] = 1
        pos = bisect_left(self.keys_list, elem)
        if pos == len(self.keys_list):
            self.keys_list.append(elem)
        else:
            self.keys_list.insert(pos, elem)

    def getElem(self):
        """
           Returns element with the smallest value over all set
        """
        return self.keys_list[0]

    def __iter__(self):
        """
            Iteration over all elemnts, does not grantied to be ordered
        """
        yield next(iter(self.table))

    def __len__(self):
        """
            Returns number of elements in OrderedHashSet
        """
        return len(self.table)

    def __contains__(self, element):
        """
            Checks if element @key in OrderedHashSet
        """
        try:
            if self.table[element]:
                pass
            return True
        except KeyError:
            return False

    def remove(self, elem):
        """
            Deletes element from OrderedHashSet, actually O(n) complexity
        """
        if elem in self.table:
            self.table.pop(elem)

        pos = self.keys_list.index(elem)
        if pos == len(self.keys_list):
            pos -= 1
            if self.keys_list[pos] != elem:
                raise KeyError("Value " + repr(elem) + " not in OrderedHashSet")
        self.keys_list.pop(pos)

        if elem in self.table:
            raise ValueError("NOT REMOVED ELEM")

