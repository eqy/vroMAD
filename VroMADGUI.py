import tkinter as tk
import tkinter.filedialog
import VroMAD

#Very ugly hackjob for GUI, I have no idea what I'm doing
class VroMADGUI():
    CONST_GAUSS_SIM = 0
    CONST_EUCLID_DIST = 1    

    def __init__(self):
        self.referencePath = ""
        self.testPath      = ""  
 
        self.root = tk.Tk()
        self.root.title("vroMAD")
        self.frame = tk.Frame(self.root)
        self.frame.grid(row=0, column=0, padx=5, pady=5)
   
        ##Label and reference path handling
        self.pathLabel = tk.Label(self.frame, text="Path of reference replays")
        self.pathLabel.grid(row=0, column=0, columnspan=4, sticky=tk.W)        
        self.pathFrame = tk.Frame(self.frame)
        self.pathFrame['borderwidth']=2
        self.pathFrame['relief']='sunken'
        self.pathFrame.grid(row=1, column=0, columnspan=4, sticky=tk.W)
        self.pathFrameLabel = tk.Label(self.pathFrame, width=50, text="")
        self.pathFrameLabel.grid(row=0,column=0, sticky=tk.W)
    
        #Label and test path handling
        self.idPathLabel = tk.Label(self.frame, text="Path of replay to analyze")
        self.idPathLabel.grid(row=0, column=5, columnspan=4,sticky=tk.W)
        self.idPathFrame = tk.Frame(self.frame)
        self.idPathFrame['borderwidth']=2
        self.idPathFrame['relief']='sunken'
        self.idPathFrame.grid(row=1, column=5, columnspan=4, sticky=tk.W)
        self.idPathFrameLabel = tk.Label(self.idPathFrame, width=50,text="") 
        self.idPathFrameLabel.grid(row=0, column=0, sticky=tk.W)
     
        #Browse buttons 
        self.button1 = tk.Button(self.frame, text="Browse...", command=self.changePath)
        self.button1.grid(row=1, column=4, padx=2, pady=2, sticky=tk.W)    
        
        self.button2 = tk.Button(self.frame, text="Browse...",command=self.changeFile)
        self.button2.grid(row=1, column=9, padx=2, pady=2, sticky=tk.W)

        #Start button
        self.button3 = tk.Button(self.frame, text="Start", command=self.start)
        self.button3.grid(row=2, column=0, padx=5,pady=5, sticky=tk.W) 
        
        self.startStatusLabel = tk.Label(self.frame, text="")
        self.startStatusLabel.grid(row=2,column=1,columnspan=4, sticky=tk.W)

        #Canvas for table
        self.tableCanvas = tk.Canvas(self.frame, width=1000, height=700)
        self.tableCanvas.grid(row=4, column=0, columnspan=10, sticky=tk.W)

        #Frame for table canvas
        self.tableFrame = tk.Frame(self.tableCanvas, width=1000, height=700,  bg='white')
        self.tableFrame.grid(row=0,column=0)
        
        #Scrollbar for canvas
        self.scrollBar = tk.Scrollbar(self.frame)
        self.scrollBar.grid(row=4,sticky=tk.N+tk.S,column=10) 

    def paint(self):
        self.root.mainloop()
    
    def changePath(self):
        self.referencePath = tk.filedialog.askdirectory()
        newPathContent = tk.StringVar()
        self.pathFrameLabel['textvariable']=newPathContent
        newPathContent.set(self.referencePath)

    def changeFile(self):
        self.testPath = tk.filedialog.askopenfilename()
        newPathContent = tk.StringVar()
        self.idPathFrameLabel['textvariable']=newPathContent
        newPathContent.set(self.testPath)

    def start(self):
        startStatus = tk.StringVar()
        self.startStatusLabel['textvariable']=startStatus
        if self.testPath != "" and self.referencePath != "":
            startStatus.set("OK.")
            self.vromad = VroMAD.VroMAD(self.referencePath, self.testPath)
            extractStatus = self.vromad.extractPlayers()
            if extractStatus < 0:
                startStatus.set("Please try a different path")
            else:
                startStatus.set("Found " + str(extractStatus) + " players in reference folder.")   
                self.drawTable()
        else:
            startStatus.set("Please select valid paths.")
           
    def drawTable(self):
        results = self.vromad.calcSimGauss()
        self.resultLabels = list()
        i=0
        for player in results[0]:
            printableResults = "" 
            printableResults = printableResults + player.name + " "
            printableResults = printableResults + str(player.simToTest_0) + " "
            printableResults = printableResults + player.race + " "
            printableResults = printableResults + player.mapName + " "
            self.resultLabels.append(tk.Label(self.tableFrame,text=printableResults,bg='white'))
            self.resultLabels[-1].grid(row=i,column=0)
            i=i+1
            print(printableResults)
        
