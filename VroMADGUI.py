import traceback
import multiprocessing as mp
import queue
import tkinter as tk
import tkinter.filedialog
import tkinter.ttk
import VroMAD


#Very ugly hackjob for GUI, I have no idea what I'm doing
class VroMADGUI():
    CONST_GAUSS_SIM = 0
    CONST_EUCLID_DIST = 1    
    CONST_CELL_W = 32
    CONST_99 = '#039331'
    CONST_98 = '#3A9B20'
    CONST_95 = '#92C00E'
    CONST_94 = '#C5D300'
    CONST_93 = '#E6E209'
    CONST_90 = '#ED9E0A'
    CONST_L  = '#CA2136'

    def __init__(self):
        self.started = False
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

        ##Create labels
        self.playerLabel = tk.Label(self.tableFrame, text="Player",width=self.CONST_CELL_W,bg='white')
        self.playerLabel.grid(row=0,column=0)
        self.simLabel    = tk.Label(self.tableFrame, text="Similarity",width=self.CONST_CELL_W,bg='white')
        self.simLabel.grid(row=0,column=1)
        self.raceLabel = tk.Label(self.tableFrame, text="Race",width=self.CONST_CELL_W,bg='white')
        self.raceLabel.grid(row=0,column=2)
        self.mapLabel = tk.Label(self.tableFrame,text="Map",width=self.CONST_CELL_W,bg='white')
        self.mapLabel.grid(row=0,column=3)
         
        #Radio buttons for player selection
        self.radioButtonVar = tk.IntVar()
        self.radioButtonP1 = tk.Radiobutton(self.frame,text="Player 0", variable=self.radioButtonVar, value=0, command=self.drawTable)
        self.radioButtonP1.grid(row=2,column=4,columnspan=3, sticky=tk.W)
        
        self.radioButtonP2 = tk.Radiobutton(self.frame,text="Player 1", variable=self.radioButtonVar, value=1, command=self.drawTable)
        self.radioButtonP2.grid(row=3,column=4,columnspan=3, sticky=tk.W)

        #Popup with exception information
        self.popup = None 

        #Progressbar
        self.progressBar = tk.ttk.Progressbar(self.frame,length=1000)
        self.progressBar.grid(row=5,column=0,columnspan=10)

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
        self.startStatus = tk.StringVar()
        self.startStatusLabel['textvariable']=self.startStatus
        if self.testPath != "" and self.referencePath != "":
            self.startStatus.set("OK.")
            self.vromad.samplePath = self.referencePath
            self.vromad.testPath = self.testPath
            outqueue = mp.Queue()
            objqueue = mp.Queue()
            progqueue = mp.Queue()
            errqueue = mp.Queue()
            process = mp.Process(target=self.vromad.extractPlayers_mp,args=[outqueue, objqueue, progqueue, errqueue])
            process.daemon = True
            process.start()
            print("started process")
            self.frame.after(10, self.checkStatus,[outqueue, objqueue, progqueue, errqueue])
            print("bar should have started")
        else:
            self.startStatus.set("Please select valid paths.")
           
    def drawTable(self):
        if self.start:
            results = self.vromad.calcSimGauss()
            self.resultLabels = list()
            i=1
            choice = self.radioButtonVar.get()
            for player in results[choice]:
                currentRow = list()
                currentRow.append(tk.Label(self.tableFrame,text=player.name,width=self.CONST_CELL_W, bg='white'))
                currentRow[-1].grid(row=i,column=0)
                currentRow.append(tk.Label(self.tableFrame,text=str(player.simToTest[choice]),width=self.CONST_CELL_W, bg='white'))
                if player.simToTest[choice] >= 0.99:
                    currentRow[-1].configure(bg=self.CONST_99)
                elif player.simToTest[choice] >= 0.98:
                    currentRow[-1].configure(bg=self.CONST_98)
                elif player.simToTest[choice] >= 0.95:
                    currentRow[-1].configure(bg=self.CONST_95)
                elif player.simToTest[choice] >= 0.94:
                    currentRow[-1].configure(bg=self.CONST_94)
                elif player.simToTest[choice] >= 0.93:
                    currentRow[-1].configure(bg=self.CONST_93)
                elif player.simToTest[choice] >= 0.90:
                    currentRow[-1].configure(bg=self.CONST_90)
                else:
                    currentRow[-1].configure(bg=self.CONST_L) 
                currentRow[-1].grid(row=i,column=1)
                currentRow.append(tk.Label(self.tableFrame,text=player.race,width=self.CONST_CELL_W, bg='white'))
                currentRow[-1].grid(row=i,column=2)
                currentRow.append(tk.Label(self.tableFrame,text=player.mapName,width=self.CONST_CELL_W, bg='white'))
                currentRow[-1].grid(row=i,column=3)
                self.resultLabels.append(currentRow)
                i=i+1
    
    def exceptionPopUp(self,msg):
        self.popup = tk.Toplevel()
        self.errMessage = tk.Message(self.popup, text=msg)
        self.errMessage.pack()
        self.popup.title("EXCEPTION")

    def checkStatus(self,queues):
        print("updateplz")
        try:
            queuestuff = queues[2].get_nowait()
        except queue.Empty:
            print("empty")
            self.root.update()
            queuestuff = "WAIT"
        if queuestuff == "FATAL":
            self.exceptionPopUp(queues[3].get())
            return 
        elif queuestuff != "ALLDONEHERE":
            if queuestuff != "WAIT":
                self.progressBar.step(float(queuestuff))
            self.frame.after(10, self.checkStatus, queues)
        else:
            #Handle done
            extractStatus = queues[0].get()
            self.vromad =   queues[1].get()
            if extractStatus <= 0:
                self.startStatus.set("Please try a different path")
            else:
                self.startStatus.set("Found " + str(extractStatus) + " players in reference folder.")   
                self.drawTable()
                self.radioButtonP1.configure(text="Player 0 (" + self.vromad.testPlayers[0].name + ")")
                self.radioButtonP2.configure(text="Player 1 (" + self.vromad.testPlayers[1].name + ")")
        

def wtf():
    print("WTF")
