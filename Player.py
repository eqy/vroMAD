class Player:
    def __init__(self, name, freqDist, race, mapName, repName):
        self.name = name
        self.freqDist = freqDist
        self.race = race
        self.simToTest = list()
        self.euclidDist_0  = 0
        self.euclidDist_1  = 0
        self.mapName = mapName
        self.repName = repName
        print("Player created")    
    
