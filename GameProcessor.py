import os
#import sys
#sys.path.insert(0, "/home/ketsol/projects/sc2readerfork/sc2reader/")
import sc2reader

class GameProcessor:
    CONST_FPS = 16.0
    
    def __init__(self, path, exclude):
        self.path = path
        self.files = list()
        self.exlude = exclude
        self.processed = dict()
        print("GameProcessor created with path: " + path)

    def findFiles(self):
        #each dirpath has subfolders and files
        #each subfolder will get its own "dirpath"
        #this will find each file
        for dirpath, dirnames, filenames in os.walk(self.path):
            for filename in filenames:
                self.files.append(os.path.join(dirpath,filename))
                print(self.files[-1])
    
    def processFiles(self):
        for filepath in self.files:
                processed[filepath] = 1
                curReplay = sc2reader.load_replay(filepath)
                total_time = curReplay.frames/self.CONST_FPS
                #print(str(total_time))
                i=0
                freqDists = dict()
                for player in curReplay.players:
                    freqDists[player.uid] = [0]*10
                    print(player.uid)
                for event in curReplay.events:
                    if event.name == 'GetFromHotkeyEvent' and event.control_group != 10:
                        i=i+1
                        #print(event.pid)
                        (freqDists[event.pid])[event.control_group] = (freqDists[event.pid])[event.control_group]+1        
                        #print(  event._str_prefix() +  " selection event found " + str(event.control_group) + ' ' +  str(i))  
                for key in freqDists.keys():
                    freqDists[key]  = [freq/total_time for freq in freqDists[key]]
                    print(lookupName(key, curReplay))
                    print(freqDists[key])
             
#We implement this function because looking up player names by uid may be
#janky in a future version of sc2reader        
def lookupName(uid, replay):
    for player in replay.players:
        if player.uid == uid:
            return player.name
        
        
