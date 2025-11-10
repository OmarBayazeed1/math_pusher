from game_object import GameObject
class Hole(GameObject):
    def __init__(self,x,y):
        super().__init__(x,y)
    def __str__(self):
         return '🕳️'