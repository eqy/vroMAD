import VroMADGUI
import VroMAD
from multiprocessing import freeze_support

if __name__ == "__main__":
    freeze_support() 
    gui = VroMADGUI.VroMADGUI()
    #gui.populate()
    gui.paint()
#vromad = VroMAD.VroMAD("../example", "../test/Dayshi vs Lucifron TvT Akilon Wastes Game 3.SC2Replay") 
#vromad.extractPlayers()
#vromad.calcSimGauss()
#vromad.calcEuclidDist()

#gameProcessor = GameProcessor.GameProcessor("../example")
#player = Player.Player()
#gameProcessor.findFiles()
#gameProcessor.processFiles()
