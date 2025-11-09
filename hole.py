from game_object import GameObject
class Hole(GameObject):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.is_passable=False
    def unlock(self):
        self.is_passable=True
        print('\n the hole has been unLocked')
    def __str__(self):
         return '🌀' if self.is_passable else '🕳️'