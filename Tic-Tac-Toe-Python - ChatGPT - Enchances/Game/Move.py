from .Player import Player
class Move:
    def __init__(self, x, y, player: Player):
        self.x = x
        self.y = y
        self.player = player
        pass

    def getMove(self):
        return (self.x, self.y, self.player.getSymbol())
    
    def getPlayer(self):
        return self.player
