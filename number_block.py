
from game_object import GameObject 
class NumberBlock(GameObject):
    def __init__(self, x, y, value):
        super().__init__(x, y)
        if not 1 <= value <= 9:
            raise ValueError("NumberBlock value must be between 1 and 9.")
        self.value = value

    def __str__(self):
        # We'll just print its value for now
        return f" -I am a NumberBlock({self.value}) at {self.position}"