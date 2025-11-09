from game_object import GameObject
class Player(GameObject):
    def __init__(self,x,y):
        super().__init__(x,y)
    def __str__(self):
        return f'I am the Player and I am at {self.position}'