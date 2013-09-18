import traceback
import tkinter as tk
import tkinter.filedialog
import VroMAD

#Very ugly hackjob for GUI, I have no idea what I'm doing
class VroMADGUI():
    CONST_GAUSS_SIM = 0
    CONST_EUCLID_DIST = 1    

    def __init__(self):
        self.vromad = VroMAD.VroMAD()
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
        self.startStatusLabel.grid(row=2,column=1,columnspan=3, sticky=tk.W)
      
         
        #Hideous hack below, I have no idea how this really works 
        #We need this to be able to use pack nevermind we don't
        #self.canvasContainerFrame = tk.Frame(self.frame)
        #self.canvasContainerFrame.grid(row=3,column=0,columnspan=10)

        #Still, I don't really know how this works
        #Canvas for table, we need 
        self.tableCanvas = tk.Canvas(self.frame,width=1000,height=700,bg='white')

        #Scrollbar for canvas
        self.scrollBar = tk.Scrollbar(self.frame,command=self.tableCanvas.yview)
        self.scrollBar.grid(row=4, column=10, sticky=tk.N+tk.S) 

        self.tableCanvas.configure(yscrollcommand=self.scrollBar.set)

        #Frame for table canvas
        self.tableFrame = tk.Frame(self.tableCanvas, bg='white')
        self.tableFrame.grid()      
 
        self.tableLabels = list()
        self.tableCanvas.grid(row=4, column=0,columnspan=10)
        self.tableCanvas.create_window((0,0),window=self.tableFrame, anchor='nw')
        #The <Configure> here is our salvation
        self.tableFrame.bind("<Configure>", self.OnFrameConfigure)
        
        self.tableCanvas.configure(scrollregion=self.tableCanvas.bbox('all'))       
         
        #Radio buttons for player selection
        self.radioButtonVar = tk.IntVar()
        self.radioButtonP1 = tk.Radiobutton(self.frame,text="Player 0", variable=self.radioButtonVar, value=0)
        self.radioButtonP1.grid(row=2,column=4)
        
        self.radioButtonP2Var = tk.IntVar()
        self.radioButtonP2 = tk.Radiobutton(self.frame,text="Player 1", variable=self.radioButtonVar, value=1)
        self.radioButtonP2.grid(row=3,column=4)
        
        #Popup with exception information
        self.popup = None 

    def OnFrameConfigure(self, event):
        self.tableCanvas.configure(scrollregion=self.tableCanvas.bbox('all'))       
 
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
            self.vromad.samplePath = self.referencePath
            self.vromad.testPath = self.testPath
            try:
                 extractStatus = self.vromad.extractPlayers()
            except:
                 self.exceptionPopUp(traceback.format_exc())
                 extractStatus = -1
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
            currentRow = list()
            currentRow.append(tk.Label(self.tableFrame,text=player.name,width=30))
            currentRow[-1].grid(row=i,column=0)
            currentRow.append(tk.Label(self.tableFrame,text=str(player.simToTest_0),width=30))
            currentRow[-1].grid(row=i,column=1)
            currentRow.append(tk.Label(self.tableFrame,text=player.race,width=30))
            currentRow[-1].grid(row=i,column=2)
            currentRow.append(tk.Label(self.tableFrame,text=player.mapName,width=30))
            currentRow[-1].grid(row=i,column=3)
            self.resultLabels.append(currentRow)
            i=i+1
    
    def exceptionPopUp(self,msg):
        self.popup = tk.Toplevel()
        self.errMessage = tk.Message(self.popup, text=msg)
        self.errMessage.pack()
        self.popup.title("EXCEPTION")
        

