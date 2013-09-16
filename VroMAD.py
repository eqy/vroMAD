import GameProcessor
import Player
import numpy

class VroMAD:
    def __init__(self, samplePathm, testPath):
        self.gameProcessor = GameProcessor.GameProcessor("../example", "")
        self.gameProcessor.findFiles() 
        self.players = list() 
        self.testPath = testPath
        self.dataList = list()   
 
    def extractPlayers(self):
        self.players = self.players + self.gameProcessor.processFiles()
   
        for player in self.players:
            print(player.freqDist) 
            self.dataList.append(player.freqDist)    
             
        self.testPlayers = GameProcessor.processFile(self.testPath)
     
    def calcSimGauss(self):
        data = numpy.array(self.dataList)        
        std     = numpy.std(data, axis=0)
        for i in range(0, std.size):
            #Elminate potential divide-by-zero for unused hotkeys
            if std[i] <= 0:
                std[i] = 1
        print(std)
        for player in self.players:
            player.simToTest_0 = self.playerSimGauss(std, self.testPlayers[0], player)
            player.simToTest_1 = self.playerSimGauss(std, self.testPlayers[1], player)       
 
        ranking_0 = sorted(self.players, key=lambda Player: Player.simToTest_0, reverse=True)
        ranking_1 = sorted(self.players, key=lambda Player: Player.simToTest_1, reverse=True)
        for rank in ranking:
            print(rank.name + " " + str(rank.simToTest))
        

    def playerSimGauss(self, std, player1, player2):
        print("playersimgauss")
        
        data = numpy.subtract(numpy.array(player1.freqDist),numpy.array(player2.freqDist))
        data = numpy.square(data)
        data = numpy.divide(data, 2*std)
        data = numpy.exp(-numpy.sum(data))
        return data;
        #print(data)
        
        
