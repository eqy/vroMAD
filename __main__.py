import GameProcessor
import Player 

gameProcessor = GameProcessor.GameProcessor("../example")
player = Player.Player()
gameProcessor.findFiles()
gameProcessor.processFiles()
