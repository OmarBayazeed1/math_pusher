from coordinate import Coordinate
class GameObject:
    def __init__(self,starting_x,starting_y):
        self.position=Coordinate(starting_x,starting_y)
    def __str__(self):
        return f'I am the GameObject and I am at {self.position}'