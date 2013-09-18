import GameProcessor
import Player
import numpy

class VroMAD:
    def __init__(self, samplePath="", testPath=""):
        self.samplePath = samplePath
        self.gameProcessor = None 
        self.players = list() 
        self.testPath = testPath
        self.dataList = list()   
 
    def extractPlayers(self):
        if self.gameProcessor is None:
            self.gameProcessor = GameProcessor.GameProcessor(self.samplePath, self.testPath)
        self.gameProcessor.path = self.samplePath
        self.gameProcessor.exclude = self.testPath
        self.gameProcessor.findFiles()
        self.players = self.players + self.gameProcessor.processFiles()
        if len(self.players) <= 0:
            return -1; 
        self.dataList = list()
        for player in self.players:
            print(player.freqDist) 
            self.dataList.append(player.freqDist)    
             
        self.testPlayers = GameProcessor.processFile(self.testPath)
        return len(self.players);
     
    def calcSimGauss(self):
        data = numpy.array(self.dataList)        
        std     = numpy.std(data, axis=0)
        for i in range(0, std.size):
            #Elminate potential divide-by-zero for unused hotkeys
            if std[i] <= 0:
                std[i] = 1
        print(std)
        for player in self.players:
            player.simToTest_0 = playerSimGauss(std, self.testPlayers[0], player)
            player.simToTest_1 = playerSimGauss(std, self.testPlayers[1], player)       
 
        ranking_0 = sorted(self.players, key=lambda Player: Player.simToTest_0, reverse=True)
        ranking_1 = sorted(self.players, key=lambda Player: Player.simToTest_1, reverse=True)
        return [ranking_0, ranking_1]
             
        
    def calcEuclidDist(self):
        for player in self.players:
            player.euclidDist_0 = playerEuclidDist(self.testPlayers[0], player)
            player.euclidDist_1 = playerEuclidDist(self.testPlayers[1], player)
        ranking_0 = sorted(self.players, key=lambda Player: Player.euclidDist_0)
        ranking_1 = sorted(self.players, key=lambda Player: Player.euclidDist_1)
    
        for rank in ranking_0:
            print(rank.name + " " + str(rank.euclidDist_0) + " " + rank.race) 

def playerSimGauss(std, player1, player2):
    print("playersimgauss")
    
    data = numpy.subtract(numpy.array(player1.freqDist),numpy.array(player2.freqDist))
    data = numpy.square(data)
    data = numpy.divide(data, 2*std)
    data = numpy.exp(-numpy.sum(data))
    return data;
    #print(data)

def playerEuclidDist(player1, player2):
    data = numpy.subtract(numpy.array(player1.freqDist),numpy.array(player2.freqDist))
    data = numpy.square(data)
    data = numpy.sum(data)
    data = numpy.sqrt(data)
    return data;

        
        
