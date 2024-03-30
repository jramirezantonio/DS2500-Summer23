"""
@author Josue Antonio
@date June 5, 2023
@file vector.py
@description A simple vector class
"""

class Vector:
    """ A simple vector class """
    def __init__(self, *components):
        """ The vector constructor/initializer """
        self._components = list(components) # name it _components to raise a flag that this variable is supposed to
                                            # to be internal only. " _ " is the flag

    def mag(self):
        """ The magnitude of vector """
        return round(sum([i ** 2 for i in self._components]) ** 0.5, 3)

    def dim(self):
        """  Dimensions of this vector """
        return len(self._components)

    def __getitem__(self, idx):
        """ Use indexing (subscripting) to fetch the ith vector component"""
        return self._components[idx]

    def __add__(self, other):
        """ addition '+' operator overloading
            other must have the same dimensions.
            Class notes have a generalization. """
        copy = self._components[:]
        for i in range(len(copy)):
            copy[i] = copy[i] + other[i]
        return Vector(*copy)  # convert the copy list into a list of params which is what Vector() takes

    def __mul__(self, other):
        """ vector dot product or vector * scalar """
        if type(other) == Vector:
            return sum([self[i] * other[i] for i in range(self.dim())])
        elif type(other) == int or type(other) == float:
            scaled = [other * c for c in self]
            return Vector(*scaled) # convert list of scaled components into params

    def __neg__(self):
        """ Negative of a vector """
        return self * -1

    def __sub__(self, other):
        """ Subtracting two vectors """
        return self + (-other)

    def cosine(self, other):
        """ Cosine of the angle between two vectors
         A dot B = |A| * |B| cos(theta) """
        return self * other / (self.mag() * other.mag())

    def angle(self, other):
        import math
        return f"{math.acos(self.cosine(other)) * 180 / math.pi} degrees"

    def __repr__(self):
        # if self.dim() == 2:
        #     result = str(self._components[0]) + "i + " + str(self._components[1]) + "j"
        # elif self.dim() == 3:
        #     result = str(self._components[0]) + "i + " + str(self._components[1]) + "j + " \
        #              + str(self._components[2]) + "k"
        # else:
        result = "<"
        for i in range(len(self._components)):
            if i != len(self._components) - 1:
                result += str(self[i]) + ", "
            else:
                result += str(self[i]) + ">"
        return result

def main():
    """ Test methods on the vector class """
    v = Vector(3, 4, 2)
    u = Vector(4, 5, 6, 7, 8, 9, 10)
    w = Vector(10, 2, -1)

    print(w.mag())
    print(u)
    z = w + v # w.__add__(v)
    print("z: ", z)

    y = Vector(-2, -4, 0)
    x = v + w + y
    print("x: ", x)
    print("slicing? : ", x[:2])

    dp = v * w
    print("dp: ", dp)

    scaled = u * 3
    print("scaled: ", scaled)

    print(-w)

    print("v - w: ", v-w)

    i = Vector(1, 0, 0)
    j = Vector(0, 1, 0)
    print(i.angle(j))

    # my_object = Classname(initial parameters to construct that instance)

if __name__ == "__main__": # only call main() if you are running this file as the main application
    main()