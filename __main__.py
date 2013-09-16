import VroMAD

vromad = VroMAD.VroMAD("../example", "../test/Dayshi vs Lucifron TvT Akilon Wastes Game 3.SC2Replay") 
vromad.extractPlayers()
vromad.calcSimGauss()

#gameProcessor = GameProcessor.GameProcessor("../example")
#player = Player.Player()
#gameProcessor.findFiles()
#gameProcessor.processFiles()
