__author__ = 'joachimdenil'

from math import ceil
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
import numpy as np
import threading

try:
    import Tkinter as Tk
except ImportError:
    import tkinter as Tk

class ScopeWindow():
    def __init__(self, theOutportRefs, names):
        """
        Plot results in a Tk window using matlplotlib
        @param theOutportRefs: array of values to plot: [[x1,x2,xn], ... ,[y1,y2, , yn]]
        @param names: the labels for each of the plots: list [name1, name2, ...,  namen]
        @return:
        """
        self.root = Tk.Tk()
        self.f = Figure()
        n = len(theOutportRefs)
        n = int(ceil(n*1.00/2))
        index = 1
        self.ax = []
        for outport in theOutportRefs:
            self.ax.append(self.f.add_subplot(n, 2, index))
            # add values:
            self.ax[index-1].plot(outport, 'ro')
            self.ax[index-1].set_xlabel('t')
            self.ax[index-1].set_ylabel(names[index-1])
            index+=1

        self.canvas = FigureCanvasTkAgg(self.f, master=self.root)
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.canvas.show()

        self.toolbar = NavigationToolbar2TkAgg( self.canvas, self.root )
        self.toolbar.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.toolbar.update()

        self.button = Tk.Button(master=self.root, text='Quit', command=self.root.destroy)
        self.button.pack(side=Tk.BOTTOM)
        self.root.mainloop()