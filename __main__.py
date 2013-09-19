import sys
import VroMADGUI
import VroMAD
from multiprocessing import freeze_support

if __name__ == "__main__":
    #Avoid nasty cx_freeze exception
    try:
        sys.stdout.write("\n")
        sys.stdout.flush()
    except:
        class fakeStream:
            def __init__(self): pass
            def write(self, data): pass
            def read(self, data): pass
            def flush(self): pass
            def close(self): pass
        sys.stdout = fakeStream()
        sys.stderr = fakeStream()
        sys.stdin  = fakeStream()
        sys.__stdout__ = fakeStream()
        sys.__stderr__ = fakeStream()
        sys.__stdin__  = fakeStream()
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
