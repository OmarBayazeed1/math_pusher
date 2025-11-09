from game_object import GameObject
class Wall(GameObject):
    def __init__(self,x,y):
        super().__init__(x,y)
    def __str__(self):
        return f'I am a wall at position ({self.position})'