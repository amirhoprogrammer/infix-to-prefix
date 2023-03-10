import tkinter as tk
from converter import Converter
from tree_generator import generate
from structures.Queue import Queue
class GUI:
    def __init__(self):
        #define variables
        self.infix = ""
        self.postfix = ""
        self.prefix = ""
        #set root
        root = tk.Tk()
        self.root = root
        #set title
        root.title("Infix Postfix Prefix Converter")
        #set size
        root.geometry("400x130")
        #add labels
        tk.Label(root, text="Enter Expression:  ").grid(row=0)
        tk.Label(root, text="Infix:  ").grid(row=1, column=0, sticky=tk.W)
        tk.Label(root, text="Postfix:  ").grid(row=2, column=0, sticky=tk.W)
        tk.Label(root, text="Prefix:  ").grid(row=3, column=0, sticky=tk.W)
        self.infix_result = tk.Label(self.root, text=self.infix)
        self.infix_result.grid(row=1, column=1, sticky=tk.W)
        self.postfix_result = tk.Label(self.root, text=self.postfix)
        self.postfix_result.grid(row=2, column=1, sticky=tk.W)
        self.prefix_result = tk.Label(self.root, text=self.prefix)
        self.prefix_result.grid(row=3, column=1, sticky=tk.W)
        #add input box
        self.entry = tk.Entry(root)
        self.entry.grid(row = 0, column=1)
        #add buttons
        tk.Button(root,
            text= "Evaluate",
            command= self.evaluate
            ).grid(row=4, column=1)
        tk.Button(root,
            text= "View Tree",
            command= self.renderTree
            ).grid(row=4, column=2)
        #add drop down menu
        self.mode = tk.StringVar(root)
        self.mode.set("Infix") # default mode
        w = tk.OptionMenu(root, self.mode, "Infix", "Postfix", "Prefix").grid(row=0,column=2)
        root.mainloop()

    def evaluate(self):
        converter = Converter()
        input = self.entry.get().replace(" ","")
        mode = self.mode.get()
        print(mode, input)
        if(mode == "Infix"):
            self.infix = input
            self.postfix = converter.infix_to_postfix(input)
            self.prefix = converter.infix_to_prefix(input)
        elif(mode == "Postfix"):
            self.postfix = input
            self.infix = converter.postfix_to_infix(input)
            self.prefix = converter.postfix_to_prefix(input)
        elif(mode == "Prefix"):
            self.prefix = input
            self.postfix = converter.prefix_to_postfix(input)
            self.infix = converter.prefix_to_infix(input)
        else:
            raise  Exception(f"mode: {mode} is not defined")
        #removing old labels
        if(self.infix_result):
            self.infix_result.destroy()
            self.postfix_result.destroy()
            self.prefix_result.destroy()
        #adding new labels
        self.infix_result = tk.Label(self.root, text=self.infix)
        self.infix_result.grid(row=1, column=1, sticky=tk.W)
        self.postfix_result = tk.Label(self.root, text=self.postfix)
        self.postfix_result.grid(row=2, column=1, sticky=tk.W)
        self.prefix_result = tk.Label(self.root, text=self.prefix)
        self.prefix_result.grid(row=3, column=1, sticky=tk.W)

    def renderTree(self):
        tree = generate(self.postfix)
        depth = tree.depth
        treeWindow = tk.Toplevel(self.root)
        # sets the title of the
        # Toplevel widget
        treeWindow.title("Expression Tree")
    
        # sets the geometry of toplevel
        d1 = 2 ** (depth-1) * 6 # distance between same level nodes
        canvas_width = 4*d1 if 4*d1>250 else 250 
        canvas_height = 60+(30*depth) if 60+(25*depth)>250 else 250
        
        treeWindow.geometry(f"{canvas_width}x{10+canvas_height}")
    
        #adding a custom method to Canvas class
        def _create_circle(self, x1, y1, r = 9, **kwargs):
            return self.create_oval(x1-r, y1-r, x1+r, y1+r, **kwargs)
        tk.Canvas.create_circle = _create_circle

        # setting up canvas and horizental scrollbar
        canvas = tk.Canvas(treeWindow, width=canvas_width, height=canvas_height, borderwidth=0, highlightthickness=0, scrollregion=(0,0,canvas_width,canvas_height)
        )
        canvas.pack(expand=True, fill=tk.BOTH)
        hbar=tk.Scrollbar(treeWindow,orient=tk.HORIZONTAL)
        hbar.pack(side=tk.BOTTOM,fill=tk.X)
        hbar.config(command=canvas.xview)
        canvas.config(xscrollcommand=hbar.set)
        ''' 
        adding entire tree to queue
        list's first element is the tree
        the second element is the width of the node during render
        the "h" variable tracks the height of the node during render
        bfs algorithm is being used to traverse the tree
        '''
        queue = Queue()
        queue.add([tree,canvas_width/2]) 
        h1 = 40
        while not queue.isEmpty():
            next_queue = Queue()
            while not queue.isEmpty():
                [tree, w] = queue.pop()
                canvas.create_circle(w,h1,fill="black")
                canvas.create_text(w,h1,text=tree.data,fill="white")
                if tree.left != None:
                    l = canvas.create_line(w,h1,w-d1,h1+25,fill="black")
                    # making sure the line is not rendered on top of the text
                    canvas.tag_lower(l) 
                    next_queue.add([tree.left,w-d1])
                if tree.right != None:
                    l = canvas.create_line(w,h1,w+d1,h1+25,fill="black")
                    # making sure the line is not rendered on top of the text
                    canvas.tag_lower(l)
                    next_queue.add([tree.right,w+d1])
            d1 /= 2
            h1 += 30
            queue = next_queue