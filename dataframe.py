import numpy as np
from random import randint
from warnings import warn


class Dict(object):
    def __init__(self, keys=None, values=None):
        if keys == None:
            keys = []
        if values == None:
            values = []
        if len(keys) != len(values):
            raise (Exception("keys and values must have same length."))
        self._keys = np.array(keys)
        # self._values = np.unique(np.array(values)) # values不需要unique
        self._values = np.array(values)
        if len(self._keys) != len(self._values):
            raise (Exception("keys or values has same items."))

    def __getitem__(self, key):
        return self._values[self._keys == key][0]

    def __len__(self):
        return len(self._keys)

    def __iter__(self):
        return iter(self._keys)

    def __setitem__(self, key, value):
        if key not in self._keys:
            self._keys = np.append(self._keys, key)
            self._values = np.append(self._values, value)
        else:
            self._values[self._keys == key] = value

    def extend(self, other):
        self._keys = np.hstack((self._keys, other._keys))
        self._values = np.hstack((self._values, other._values))

    def __add__(self, other):
        return np.hstack((self._keys, other._keys)), np.hstack((self._values, other._values))

    def __eq__(self, other):
        return (self._keys == other._keys).all() and (self._values == other._values).all()

    def __delitem__(self, key):
        if key in self._keys:
            self._values = np.setdiff1d(self._values, self._values[self._keys == key])
            self._keys = np.setdiff1d(self._keys, np.array([key]))

    def __contains__(self, key):
        return key in self._keys

    def __str__(self):
        print("keys:", self._keys, "values", self._values)
        return ""

    def __repr__(self):
        print("keys:", self._keys, "values", self._values)
        return ""

    def sample(self):
        index = randint(len(self._keys))
        return self._keys[index], self._values[index]

    def pop(self, key):
        temp = self._values[self._keys == key]
        self.__delitem__(key)
        return temp

    def keys(self):
        return self._keys

    def values(self):
        return self._values

    def get(self, key, default=None):
        temp = self._values[self._keys == key]
        if len(temp) > 0:
            return temp[0]
        return default


class List(object):
    def __init__(self, *args):
        self.list = np.array(args)

    def __getitem__(self, index):
        return self.list[index]

    def __len__(self):
        return len(self.list)

    def __iter__(self):
        return iter(self.list)

    def __setitem__(self, index, value):
        self.list[index] = value

    def __delitem__(self, index):
        self.list = np.delete(self.list, index)

    def __iadd__(self, other):
        self.list = np.hstack((self.list, other.list))

    def __add__(self, other):
        return np.hstack((self.list, other.list))

    def index(self, item):
        return np.argwhere(self.list == item)

    def remove(self, item):
        self.__delitem__(self.index(item))

    def append(self, item):
        self.list = np.append(self.list, item)

    def __contains__(self, key):
        return key in self.list

# a = Dict()

# class ndict:
#     def __init__(self, dictkeys=[], values=[]):
#         if len(dictkeys) != len(values):
#             raise (Exception("keys and values must have same length."))
#         self._keys = dictkeys
#         self._values = np.array(values)
#
#     def __getitem__(self, dictkey):
#         for i in range(len(self._keys)):
#             if self._keys[i] == dictkey:
#                 return self._values[i]
#         raise (Exception("match failed."))
#
#     def __len__(self):
#         return len(self._keys)
#
#     def __iter__(self):
#         return iter(self._keys)
#
#     def __setitem__(self, dictkey, value):
#         if dictkey not in self._keys:
#             self._keys += [dictkey]
#             self._values = np.append(self._values, value)
#         else:
#             for i in range(len(self._keys)):
#                 if self._keys[i] == dictkey:
#                     self._values[i] = value
#                     break
#
#     def __iadd__(self, other):
#         self._keys += other._keys
#         self._values = np.hstack((self._values, other._values))
#
#     def __add__(self, other):
#         return self._keys + other._keys, np.hstack((self._values, other._values))
#
#     def __eq__(self, other):
#         return self._keys == other._keys and (self._values == other._values).all()
#
#     def __delitem__(self, dictkey):
#         for i in range(len(self._keys)):
#             if self._keys[i] == dictkey:
#                 self._values = np.delete(self._values, i)
#                 del self._keys[i]
#                 break
#
#     def __contains__(self, dictkey):
#         return dictkey in self._keys
#
#     def pop(self, dictkey):
#         for i in range(len(self._keys)):
#             if self._keys[i] == dictkey:
#                 temp = self._values[i]
#                 self._values = np.delete(self._values, i)
#                 del self._keys[i]
#                 return temp
#
#     def keys(self):
#         return self._keys
#
#     def values(self):
#         return self._values
