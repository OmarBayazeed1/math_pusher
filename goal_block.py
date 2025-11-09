from game_object import GameObject
class GoalBlock(GameObject):
    def __init__(self,x,y,target_value):
        super().__init__(x,y)
        self.target_value=target_value
    def __str__(self):
        return f'Goal(={self.target_value}) at {self.position}'
