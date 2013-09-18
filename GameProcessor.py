import os
import sc2reader
import Player

class GameProcessor:
    CONST_FPS = 16.0
    CONST_EXT = '.SC2Replay'

    def __init__(self):
        self.path = ""
        self.files = list()
        self.exclude = ""
        self.processed = dict()
        print("GameProcessor created")
        
    def __init__(self, path, exclude):
        self.path = path
        self.files = list()
        self.exlude = exclude
        self.processed = dict()
        self.processed[exclude] = 1
        print("GameProcessor created with path: " + path)

    def findFiles(self):
        #each dirpath has subfolders and files
        #each subfolder will get its own "dirpath"
        #this will find each file
        for dirpath, dirnames, filenames in os.walk(self.path):
            for filename in filenames:
                (root, ext) = os.path.splitext(filename)
                #We only care about files ending in .SC2Replay
                if ext == GameProcessor.CONST_EXT:
                    self.files.append(os.path.join(dirpath,filename))
                    print(self.files[-1])

    def processFiles(self):
        players = list()
        for filepath in self.files:
                if filepath not in self.processed:
                    self.processed[filepath] = 1
                    curReplay = sc2reader.load_replay(filepath)
                    total_time = curReplay.frames/GameProcessor.CONST_FPS
                    freqDists = dict()
                    print(curReplay.filename)
                    for player in curReplay.players:
                        freqDists[player.uid] = [0]*10
                        print(player.uid)
                    #This for loop takes on the order of 10^4 iterations per
                    #replay, but it is not a performance bottleneck
                    for event in curReplay.events:
                        #Notice we check that the event was spawned by an actual
                        #player
                        if event.name == 'GetFromHotkeyEvent' and event.control_group < 10 and event.pid in freqDists.keys():
                            (freqDists[event.pid])[event.control_group] = (freqDists[event.pid])[event.control_group]+1        
                    for key in freqDists.keys():
                        freqDists[key]  = [freq/total_time for freq in freqDists[key]]
                        player = Player.Player(lookupName(key, curReplay), freqDists[key], lookupRace(key, curReplay), curReplay.map_name, curReplay.filename)
                        players.append(player)
        return players;


def processFile(singlefile):
    curReplay = sc2reader.load_replay(singlefile)
    freqDists = dict()
    total_time = curReplay.frames/GameProcessor.CONST_FPS
    players = list()
    for player in curReplay.players:
        freqDists[player.uid] = [0]*10
    for event in curReplay.events:
        if event.name == 'GetFromHotkeyEvent' and event.control_group < 10 and event.pid in freqDists.keys():
            #print(event.pid)
            (freqDists[event.pid])[event.control_group] = (freqDists[event.pid])[event.control_group]+1        
            #print(  event._str_prefix() +  " selection event found " + str(event.control_group) + ' ' +  str(i))  
    for key in freqDists.keys():
        freqDists[key]  = [freq/total_time for freq in freqDists[key]]
        player = Player.Player(lookupName(key, curReplay), freqDists[key], lookupRace(key, curReplay), curReplay.map_name, curReplay.filename)
        players.append(player)
    return players

             
#We implement these functions because looking up player names by uid may be
#janky in a future version of sc2reader        
def lookupName(uid, replay):
    for player in replay.players:
        if player.uid == uid:
            return player.name

def lookupRace(uid, replay):
    for player in replay.players:
        if player.uid == uid:
            return player.pick_race
        
        
