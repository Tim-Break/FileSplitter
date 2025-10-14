import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkmsg
import tkinter.filedialog as tkfld

from PIL import ImageTk, Image

from splitjoin import split, join


class Interface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.icon = ImageTk.PhotoImage(Image.open(".\\Images\\icon.png"))
        self.loadicon = ImageTk.PhotoImage(Image.open(".\\Images\\icon.png"))
        self.iconphoto(False, self.icon)
        self.title("FileSplitter")
        self.geometry("366x660")

        self.tabs = ttk.Notebook(self)

        self.splitFrame = ttk.Frame(self.tabs)
        self.joinFrame = ttk.Frame(self.tabs)

        self.tabs.add(self.splitFrame, text="Split")
        self.tabs.add(self.joinFrame, text="Join")
        
        self.tabs.grid()

        #split

        self.splitFileLabel = ttk.Label(self.splitFrame, text="File:", width=12)
        self.splitScrFile = ttk.Entry(self.splitFrame, width=35)
        self.splitScrFileChooseBTN = ttk.Button(self.splitFrame, text="Choose", width=10, command=self.SplitChooseScrFile)

        self.splitSizeLabel = ttk.Label(self.splitFrame, text="Split by", width=12)
        vcmd = (self.splitFrame.register(self.SplitSizeEnterValidate), "%S")
        self.splitSize = ttk.Entry(self.splitFrame, validate="key", validatecommand=vcmd, width=35)
        self.splitSize.bind("<FocusOut>", self.SplitSizeValueCheck)
        self.splitSize.insert(0, "1")
        self.splitSizeType = ttk.Combobox(self.splitFrame, width=8, state="readonly", values=["B","KB","MB","GB"])
        self.splitSizeType.current(3)

        self.splitLabelOutPath = ttk.Label(self.splitFrame, text="Output path:", width=12)
        self.splitOutPath = ttk.Entry(self.splitFrame, width=35)
        self.splitChooseOutPathBTN = ttk.Button(self.splitFrame, text="Choose", width=10, command=self.SplitChooseOutDir)
        

        self.splitSIECHKvalue = tk.BooleanVar(value=True)
        self.splitSIECHK = ttk.Checkbutton(self.splitFrame, text="Show in explorer", variable=self.splitSIECHKvalue)


        self.splitRunBTN = ttk.Button(self.splitFrame, text="\nSPLIT\n", width=59, command=self.Split)


        self.splitFileLabel.grid(column=0, row=0)
        self.splitScrFile.grid(column=1, row=0)
        self.splitScrFileChooseBTN.grid(column=2, row=0)


        self.splitSizeLabel.grid(column=0, row=1)
        self.splitSize.grid(column=1, row=1)
        self.splitSizeType.grid(column=2, row=1)


        self.splitLabelOutPath.grid(column=0, row=2)
        self.splitOutPath.grid(column=1, row=2)
        self.splitChooseOutPathBTN.grid(column=2, row=2)

        
        self.splitSIECHK.grid(column=1, row=3, sticky='w')


        self.splitRunBTN.grid(column=0, row=4, columnspan=3, sticky='s')

        #split
        
        #join

        self.joinLabelParts = ttk.Label(self.joinFrame, text="Parts:", width=12)
        self.joinLoadedParts = tk.Listbox(self.joinFrame, width=35, height=32)
        self.joinLoadedPartsScroll = ttk.Scrollbar(self.joinFrame, orient="horizontal", command=self.joinLoadedParts.xview)
        self.joinLoadedParts.config(xscrollcommand=self.joinLoadedPartsScroll.set)

        self.joinLoadedPartsAddBTN = ttk.Button(self.joinFrame, text="Add", width=10, command=self.JoinLoadedPartsADD)
        self.joinLoadedPartsDelBTN = ttk.Button(self.joinFrame, text="Remove", width=10, command=self.JoinLoadedPartsDEL)
        self.joinLoadedPartsCleBTN = ttk.Button(self.joinFrame, text="Clear", width=10, command=self.JoinLoadedPartsCLE)

        
        self.joinLabelOutPath = ttk.Label(self.joinFrame, text="Output path:", width=12)
        self.joinOutPath = ttk.Entry(self.joinFrame, width=35)
        self.joinChooseOutPathBTN = ttk.Button(self.joinFrame, text="Choose", width=10, command=self.JoinChooseOutDir)
        

        self.joinSIECHKvalue = tk.BooleanVar(value=True)
        self.joinSIECHK = ttk.Checkbutton(self.joinFrame, text="Show in explorer", variable=self.joinSIECHKvalue)


        self.joinRunBTN = ttk.Button(self.joinFrame, text="\nJOIN\n", width=59, command=self.Join)


        self.joinLabelParts.grid(column=0, row=0)
        self.joinLoadedParts.grid(column=1, row=0, rowspan=3)
        self.joinLoadedPartsScroll.grid(column=1, row=3, sticky='ew')
        
        self.joinLoadedPartsAddBTN.grid(column=2, row=0)
        self.joinLoadedPartsDelBTN.grid(column=2, row=1)
        self.joinLoadedPartsCleBTN.grid(column=2, row=2, sticky='n')


        self.joinLabelOutPath.grid(column=0, row=4)
        self.joinOutPath.grid(column=1, row=4)
        self.joinChooseOutPathBTN.grid(column=2, row=4)


        self.joinSIECHK.grid(column=1, row=5, sticky='w')


        self.joinRunBTN.grid(column=0, row=6, columnspan=3)


        self.joinFrame.grid_rowconfigure(0, weight=0)
        self.joinFrame.grid_rowconfigure(1, weight=0)
        self.joinFrame.grid_rowconfigure(2, weight=1)
        self.joinFrame.grid_rowconfigure(3, weight=0)
        self.joinFrame.grid_rowconfigure(4, weight=0)
        self.joinFrame.grid_rowconfigure(5, weight=0)
        self.joinFrame.grid_rowconfigure(6, weight=0)

        #join

        self.mainloop()

    
    def SplitChooseScrFile(self):
        self.splitScrFile.delete(0, "end")
        self.splitScrFile.insert("end", tkfld.askopenfilename(title="Select file to be sliced"))
    
    def SplitChooseOutDir(self):
        self.splitOutPath.delete(0, "end")
        self.splitOutPath.insert("end", tkfld.askdirectory(title="Select output directory"))
    
    def SplitSizeValueCheck(self, e):
        value = self.splitSize.get()
        if value == "" or int(value) <= 0:
            self.splitSize.delete(0, "end")
            self.splitSize.insert("end", "1")
        
    def SplitSizeEnterValidate(self, char: str):
        return char.isdecimal()
    
    def Split(self):
        self.iconify()
        self.title("FileSplitter - operating...")
        self.iconphoto(False, self.loadicon)
        try:
            ans = split(self.splitScrFile.get(),
                        self.splitOutPath.get(),
                        [int(self.splitSize.get()), self.splitSizeType.get()],
                        self.splitSIECHKvalue.get())
        except:
            ans = ("Programm error!", 2)
        self.deiconify()
        self.title("FileSplitter")
        self.iconphoto(False, self.icon)
        if ans[1] == 0:
            tkmsg.showinfo(title="Result", message=ans[0])
        elif ans[1] == 1:
            tkmsg.showwarning(title="Result", message=ans[0])
        else:
            tkmsg.showerror(title="Error!", message=ans[0])
    

    def JoinLoadedPartsDEL(self):
        self.joinLoadedParts.delete(self.joinLoadedParts.curselection())
    
    def JoinLoadedPartsCLE(self):
        self.joinLoadedParts.delete(0, "end")
    
    def JoinLoadedPartsADD(self):
        files = tkfld.askopenfilenames(
            title="Select SPLIT files together making up one",
            filetypes=[("SPLIT files", "*.split")]
        )
        for file in files: self.joinLoadedParts.insert("end", file)
    
    def JoinChooseOutDir(self):
        self.joinOutPath.delete(0, "end")
        self.joinOutPath.insert("end", tkfld.askdirectory(title="Select output directory"))
    
    def Join(self):
        self.iconify()
        self.title("FileSplitter - operating...")
        self.iconphoto(False, self.loadicon)
        try:
            ans = join(self.joinLoadedParts.get(0, "end"),
                       self.joinOutPath.get(),
                       self.joinSIECHKvalue.get())
        except:
            ans = ("Programm error!", 2)
        self.deiconify()
        self.title("FileSplitter")
        self.iconphoto(False, self.icon)
        if ans[1] == 0:
            tkmsg.showinfo(title="Result", message=ans[0])
        elif ans[1] == 1:
            tkmsg.showwarning(title="Result", message=ans[0])
        else:
            tkmsg.showerror(title="Error!", message=ans[0])


if __name__ == "__main__":
    gui = Interface()
