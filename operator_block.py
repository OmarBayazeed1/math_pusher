from game_object import GameObject 
class OperatorBlock(GameObject):
    def __init__(self, x, y, operator):
        super().__init__(x, y)
        if operator not in '+-*/':
            raise ValueError("OperatorBlock value must be between + or - or * or /.")
        self.operator = operator

    def __str__(self):
        # We'll just print its value for now
        return f" -I am an OperatorBlock ({self.operator}) at {self.position}"