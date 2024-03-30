

import math

class Shape:
    """ The BASE class of our shape hierarchy"""
    def __init__(self, name):
        self.name = name
        self.xpos = 0
        self.ypos = 0

    def get_position(self):
        return self.xpos, self.ypos

    def move(self, x, y):
        """ Move the location of the shape to (x,y) """
        self.xpos = x
        self.ypos = y

    def __repr__(self):
        return self.name + " (Shape) @ " +str(self.get_position())



class Circle(Shape):
    """ A circle is a type of shape """
    def __init__(self, name, radius):

        # Instantiate (construct) the parent class
        super().__init__(name)

        # Locally set the radius
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def __repr__(self):
        return self.name + " (Circle) @ " + str(self.get_position()) + ' with radius='+str(self.radius)






class Square(Shape):
    """ A square is a type of shape"""
    pass

def main():
    blob = Shape('blob')
    blob.move(2, 3)
    blob.move(0, -1)
    print(blob)

    c = Circle('Circle of life', 4)
    c.move(5, 5)
    print(c, c.area())



if __name__ == '__main__':
    main()