import tkinter as tk
import tkinter.filedialog

class VroMADGUI():
    def __init__(self):
        self.referencePath = ""
        self.testPath      = ""  
 
        self.root = tk.Tk()
        self.root.title("vroMAD")
        self.frame = tk.Frame(self.root)
        self.frame.grid(row=0, column=0, padx=5, pady=5)
   
        ##Label and reference path handling
        self.pathLabel = tk.Label(self.frame, text="Path to reference replays")
        self.pathLabel.grid(row=0,column=0)        
        self.pathFrame = tk.Frame(self.frame)
        self.pathFrame['borderwidth']=2
        self.pathFrame['relief']='sunken'
        self.pathFrame.grid(row=1, column=0)
        self.pathFrameLabel = tk.Label(self.pathFrame, width=50, text="")
        self.pathFrameLabel.grid(row=0,column=0)
    
        #Label and test path handling
        self.idPathLabel = tk.Label(self.frame, text="Path to replay to ID")
        self.idPathLabel.grid(row=0,column=2)
        self.idPathFrame = tk.Frame(self.frame)
        self.idPathFrame['borderwidth']=2
        self.idPathFrame['relief']='sunken'
        self.idPathFrame.grid(row=1,column=2)
        self.idPathFrameLabel = tk.Label(self.idPathFrame, width=50,text="") 
        self.idPathFrameLabel.grid(row=0,column=1)
     
        #Browse buttons 
        self.button1 = tk.Button(self.frame, text="Browse...", command=self.changePath)
        self.button1.grid(row=1, column=1, padx=2, pady=2)    
        
        self.button2 = tk.Button(self.frame, text="Browse...",command=self.changeFile)
        self.button2.grid(row=1, column=3, padx=2, pady=2)

        #Start button
        self.button3 = tk.Button(self.frame, text="Start", command=self.start)
        self.button3.grid(row=2,padx=5,pady=5) 

        self.path = ""
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
        print("start")
