################
# CS 251
# Spring 2018
# Tracy Quan
# Project 3

import tkinter as tk
import math
import random
import numpy as np
import view
from tkinter import messagebox
import data
import sys


# create a class to build and manage the display
class DisplayApp:

    def __init__(self, width, height):

        # create a tk object, which is the root window
        self.root = tk.Tk()

        # width and height of the window
        self.initDx = width
        self.initDy = height

        # set up the geometry for the window
        self.root.geometry( "%dx%d+50+30" % (self.initDx, self.initDy) )

        # set the title of the window
        self.root.title("Viewing Axes")

        # set the maximum size of the window for resizing
        self.root.maxsize( 1024, 768 )

        # bring the window to the front
        self.root.lift()

        # setup the menus
        self.buildMenus()

        # build the controls
        self.buildControls()

        # build the objects on the Canvas
        self.buildCanvas()

        # set up the key bindings
        self.setBindings()

        # Create a View object and set up the default parameters
        self.vobj = view.View()

        self.begin_ext = self.vobj.extent

        # Create the axes fields and build the axes
        self.axes = np.matrix([[0, 0, 0, 1], [1, 0, 0, 1], 
                              [0, 0, 0, 1], [0, 1, 0, 1],
                              [0, 0, 0, 1], [0, 0, 1, 1]])

        # set up the application state
        self.objects = []
        self.data = None

        # a field to hold a list that contains the actual graphics line objects
        self.lineobjs = []

        # instantiate them on the screen
        self.buildAxes()

        # EXTENSIONS
        self.panning = 5


    def buildMenus(self):
        
        # create a new menu
        self.menu = tk.Menu(self.root)

        # set the root menu to our new menu
        self.root.config(menu = self.menu)

        # create a variable to hold the individual menus
        self.menulist = []

        # create a file menu
        filemenu = tk.Menu( self.menu )
        self.menu.add_cascade( label = "File", menu = filemenu )
        self.menulist.append(filemenu)


        # menu text for the elements
        menutext = [ [ 'Open...  \xE2\x8C\x98-O', '-', 'Quit  \xE2\x8C\x98-Q' ] ]

        # menu callback functions
        menucmd = [ [self.handleOpen, None, self.handleQuit]  ]
        
        # build the menu elements and callbacks
        for i in range( len( self.menulist ) ):
            for j in range( len( menutext[i]) ):
                if menutext[i][j] != '-':
                    self.menulist[i].add_command( label = menutext[i][j], command=menucmd[i][j] )
                else:
                    self.menulist[i].add_separator()


    #############
    # EXTENSION #
    #############
    def buildDataPoints(self):
        self.dobj = data.Data(sys.argv[1])
        datamatrix = self.dobj.NumPyMatrix
        n,m = datamatrix.shape
        x0 = np.ones((n, 1))
        self.datapts = np.hstack((datamatrix, x0))
        vtm = self.vobj.build()
        pts = vtm * self.datapts.T
        pts = pts.T
        #print(pts.shape[0])
        for i in range(pts.shape[0]):
            x = pts[i, 0]
            y = pts[i, 1]
            dx = 3
            pt = self.canvas.create_oval( x-dx, y-dx, x+dx, y+dx, fill = "dark blue", outline="")
            self.objects.append(pt)

    #############
    # EXTENSION #
    #############
    # build data points on info canvas
    def buildDataPoints2(self):
        vobj_clone = self.vobj.clone()
        vobj_clone.screen = np.matrix([250, 250])
        vtm = vobj_clone.build()
        pts = vtm * self.datapts.T
        pts = pts.T
        print(pts)
        #print(self.infocanvas.winfo_width(), self.infocanvas.winfo_height())
        #print(pts.shape[0])
        self.infopts = []
        for i in range(pts.shape[0]):
            x = pts[i, 0]
            y = pts[i, 1]
            print("x", x)
            print("y", y)
            dx = 2
            infopt = self.infocanvas.create_oval( x+10-dx, y-70-dx, x+10+dx, y-70+dx, fill = "dark blue", outline="")
            self.infopts.append(infopt)
            #self.objects.append(pt)

    # update the color of datapoints on info canvas
    def update_infocanvas(self):
        for i in range(len(self.objects)):
            coords = self.canvas.coords(self.objects[i])
            if coords[0]<0 or coords[1]<0 or coords[0]>self.canvas.winfo_width() or coords[1]>self.canvas.winfo_height():
                self.infocanvas.itemconfig(self.infopts[i], fill = "sky blue")
            else:
                self.infocanvas.itemconfig(self.infopts[i], fill = "dark blue")



    # create the canvas object
    def buildCanvas(self):
        self.canvas = tk.Canvas( self.root, width=self.initDx, height=self.initDy, background = "gray95" )
        self.canvas.pack( expand=tk.YES, fill=tk.BOTH )
        return


    # build a frame and put controls in it
    def buildControls(self):

        # make a control frame
        self.cntlframe = tk.Frame(self.root)
        self.cntlframe.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)

        #############
        # EXTENSION #
        #############
        self.infocanvas = tk.Canvas(self.cntlframe, background = "grey90")
        self.infocanvas.pack(side=tk.BOTTOM)

        infocanvaslabel = tk.Label(self.cntlframe, text = "Mini Window :D")
        infocanvaslabel.pack(side = tk.BOTTOM)

        sep = tk.Frame( self.root, height=self.initDy, width=2, bd=1, relief=tk.SUNKEN )
        sep.pack( side=tk.RIGHT, padx = 2, pady = 2, fill=tk.Y)

        # make a cmd 1 button in the frame
        self.buttons = []
        self.button1 = tk.Button( self.cntlframe, text="Reset", command=self.handleResetButton, width=5 )
        self.buttons.append( self.button1)
        self.button1.pack(side=tk.TOP)
        #self.buttons[-1][1].pack(side=tk.TOP)  # default side is top

        #bt1 = tk.Button(self.cntlframe, text="Panning Factor", command=self.set_panning, width = 5)
        #bt1.pack(side = tk.TOP)

        #############
        # EXTENSION #
        #############
        self.s1 = tk.Scale(self.cntlframe, label = "Panning", width = 5, orient = tk.HORIZONTAL, to = 10)
        self.s1.set(5)
        self.s1.pack(side=tk.TOP)

        self.s2 = tk.Scale(self.cntlframe, label = "Rotation", width = 5, orient = tk.HORIZONTAL, to = 10)
        self.s2.set(5)
        self.s2.pack(side=tk.TOP)
        
        return



    # create the axis line objects in their default location
    def buildAxes(self):
        vtm = self.vobj.build()
        pts = vtm * self.axes.T
        pts = pts.T
        new_x = self.canvas.create_line(pts.item(0,0), pts.item(0,1), pts.item(1,0), pts.item(1,1), 
                                                        fill = "blue", width = 2, arrow = tk.LAST)
        new_y = self.canvas.create_line(pts.item(2,0), pts.item(2,1), pts.item(3,0), pts.item(3,1), 
                                                        fill = "red", width = 2, arrow = tk.LAST)
        new_z = self.canvas.create_line(pts.item(4,0), pts.item(4,1), pts.item(5,0), pts.item(5,1), 
                                                        fill = "dark green", width = 2, arrow = tk.LAST)

        #############
        # EXTENSION #
        #############
        text_x = self.canvas.create_text(pts[1,0]+5, pts[1,1], text="x", fill="blue", font="Arial")
        text_y = self.canvas.create_text(pts[3,0]+8, pts[3,1], text="y", fill="red", font="Arial")
        text_z = self.canvas.create_text(pts[5,0]+8, pts[5,1], text="z", fill="dark green", font="Arial")
        self.lineobjs.append(new_x)
        self.lineobjs.append(new_y)
        self.lineobjs.append(new_z)
        self.lineobjs.append(text_x)
        self.lineobjs.append(text_y)
        self.lineobjs.append(text_z)
        self.buildDataPoints()
        self.build_miniwin()

    def build_miniwin(self):
        self.buildDataPoints2()


    # modify the endpoints of the axes to their new location
    def updateAxes(self):
        if self.widget_under_mouse(self.cntlframe)!= self.s1 and self.widget_under_mouse(self.cntlframe)!= self.s2 and self.widget_under_mouse(self.cntlframe)!= self.cntlframe:
            vtm = self.vobj.build()
            pts = (vtm * self.axes.T).T
            #for line in self.lineobjs:
            #i = self.lineobjs.index(line)
            #self.canvas.coords(line, pts.item(2*i,0),pts.item(2*i,1), pts.item(2*i+1,0),pts.item(2*i+1,1))
            self.canvas.coords(self.lineobjs[0], pts.item(0,0),pts.item(0,1), pts.item(1,0),pts.item(1,1))
            self.canvas.coords(self.lineobjs[1], pts.item(2,0),pts.item(2,1), pts.item(3,0),pts.item(3,1))
            self.canvas.coords(self.lineobjs[2], pts.item(4,0),pts.item(4,1), pts.item(5,0),pts.item(5,1))
            self.canvas.coords(self.lineobjs[3], pts[1,0]+5, pts[1,1])
            self.canvas.coords(self.lineobjs[4], pts[3,0]+8, pts[3,1])
            self.canvas.coords(self.lineobjs[5], pts[5,0]+8, pts[5,1])

            dapts = vtm * self.datapts.T
            dapts = dapts.T
            for i in range(len(self.objects)):
                x = dapts[i, 0]
                y = dapts[i, 1]
                dx = 3
                self.canvas.coords( self.objects[i], x-dx, y-dx, x+dx, y+dx )

            self.update_infocanvas()


    # set bindings
    def setBindings(self):
        self.root.bind( '<Button-1>', self.handleButton1 )
        self.root.bind( '<Button-2>', self.handleButton2 )
        self.root.bind( '<Button-3>', self.handleButton3 )
        self.root.bind( '<B1-Motion>', self.handleButton1Motion )
        self.root.bind( '<B2-Motion>', self.handleButton2Motion )
        self.root.bind( '<B3-Motion>', self.handleButton3Motion )
        self.root.bind( '<Control-Button-1>', self.handleButton2 )
        self.root.bind( '<Control-B1-Motion>', self.handleButton2Motion )
        self.root.bind( '<Control-q>', self.handleQuit )
        self.root.bind( '<Control-o>', self.handleModO )
        self.root.bind( '<Control-y>', self.yzaxes)
        # self.root.bind( '<Control-z>', self.zxaxes)
        self.canvas.bind( '<Configure>', self.handleResize )
        self.root.bind( '<Left>', self.leftrotate)
        self.root.bind( '<Right>', self.rightrotate)
        self.root.bind( '<Up>', self.uprotate)
        self.root.bind( '<Down>', self.downrotate)
        # self.canvas.bind( '<Motion>', self.handleMouseMotion )
        return


    def handleResize(self, event=None):
        # You can handle resize events here
        pass


    def handleOpen(self):
        print('handleOpen')


    def handleModO(self, event):
        self.handleOpen()


    def handleQuit(self, event=None):
        print('Terminating')
        self.root.destroy()


    def handleResetButton(self):
        print('handling reset button')
        self.vobj.reset()
        self.status_scale = tk.Label(self.canvas, text = "Scaling: 1.00x").grid(row=0, padx =self.initDx/2, pady = self.initDy-100)
        self.status_rotation = tk.Label(self.root, text = "Rotation-- Angle1:  0.00, Angle2: 0.00").grid(row=1, padx =self.initDx/4, pady = self.initDy-100)
        self.updateAxes()

    def widget_under_mouse(self, root):
        x,y = root.winfo_pointerxy()
        widget = root.winfo_containing(x,y)
        return widget


    def handleButton1(self, event):
        print('handle button 1: %d %d' % (event.x, event.y))
        self.baseClick1 = (event.x, event.y)


    # rotation
    def handleButton2(self, event):
        print('handle button 2: %d %d' % (event.x, event.y))
        self.baseClick2 = (event.x, event.y)
        self.vobj_clone = self.vobj.clone()


    # scaling
    def handleButton3(self, event):
        print('handle button 3: %d %d' % (event.x, event.y))
        self.baseClick3 = (event.x, event.y)
        v_clone = self.vobj.clone()
        self.origin_ext = v_clone.extent


    # translation
    def handleButton1Motion(self, event):

        print('handle button 1 motion: %d %d' % (event.x - self.baseClick1[0], event.y -self.baseClick1[1]) )
        self.panning = self.s1.get()
        delta0 = (self.panning*3+5)/20*(event.x - self.baseClick1[0])/self.vobj.screen[0,0]*self.vobj.extent[0,0]
        delta1 = (self.panning*3+5)/20*(event.y - self.baseClick1[1])/self.vobj.screen[0,1]*self.vobj.extent[0,1]

        self.vobj.vrp = self.vobj.vrp + delta0 * self.vobj.u + delta1 * self.vobj.vup
        self.updateAxes()
        self.baseClick1=(event.x, event.y)
    

    # rotation
    def handleButton2Motion( self, event ):
        print('handle button 2 motion: %d %d' % (event.x, event.y) )
        ro_fac = 2000 * ((10-self.s2.get()) * 3 + 5) / 20
        delta0 = -(event.x - self.baseClick2[0])/ro_fac*math.pi
        print(delta0)
        delta1 = (event.y - self.baseClick2[1])/ro_fac*math.pi
        self.vobj = self.vobj_clone.clone()
        self.vobj.rotateVRC(delta0, delta1)
        self.updateAxes()

        #############
        # EXTENSION #
        #############
        delta0 = -delta0
        delta1 = -delta1
        d0 = "%.2f" % delta0
        d1 = "%.2f" % delta1
        s = "Rotation -- " + "Angle1: " + d0 + ", " + "Angle2: " + d1
        self.status_rotation = tk.Label(self.root, text = s).grid(row=1, padx =self.initDx/4, pady = self.initDy-100)
        #self.baseClick2 = (event.x, event.y)



    # implement scaling
    def handleButton3Motion( self, event):
        print('handle button 3 motion: %d %d' % (event.x, event.y) )

        # convert the distance between the base click and the current mouse 
        # position into a scale factor
        dist = event.y - self.baseClick3[1]
        print(dist)
        # dist = np.linalg.norm(np.asarray(self.baseClick2)-np.asarray(event.x, event.y))
        factor = 1 + 0.01* dist
        if factor > 3:
            factor = 3
        if factor < 0.1:
            factor = 0.1
        print("factor", factor)
        #print
        self.vobj.extent = self.origin_ext * factor
        self.updateAxes()

        factor = self.begin_ext[0,0]/self.vobj.extent[0,0]
        factor = "%.2f" % factor
        s = "Scaling: " + str(factor) + "x"
        self.status_scale = tk.Label(self.canvas, text = s).grid(row=0, padx =self.initDx/2, pady = self.initDy-100)

    #############
    # EXTENSION #
    #############
    def yzaxes(self, event):
        self.vobj.vpn = np.matrix([1,0,0])
        self.u = np.matrix([0,1,0])
        self.updateAxes()

    #############
    # EXTENSION #
    #############
    def leftrotate(self, event):
        self.vobj.rotateVRC(0.1, 0)
        self.updateAxes()

    def rightrotate(self, event):
        self.vobj.rotateVRC(-0.1, 0)
        self.updateAxes()

    def uprotate(self, event):
        self.vobj.rotateVRC(0, -0.1)
        self.updateAxes()

    def downrotate(self, event):
        self.vobj.rotateVRC(0, 0.1)
        self.updateAxes()


    def main(self):
        print('Entering main loop')
        self.root.mainloop()


# ------------ Dialog class ---------------
# Dialog class
class Dialog(tk.Toplevel):
    def __init__(self, parent, num=0, title = None):

        tk.Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = tk.Frame(self)
        self.initial_focus = self.body(body, num)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)


    #
    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics
    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()
    #
    # command hooks

    def validate(self):

        return 1 # override

    def apply(self):

        pass # override

class PanningDialog(Dialog):
    def __init__(self, parent, num):
        Dialog.__init__(self, parent, num)


    def body(self, master, num):
        l = tk.Label(master, text = "Panning Sensitivity: ").grid(row = 0)
        self.beginValue = tk.StringVar()
        if num == 0:
            self.beginValue.set("0-10")
        else:
            self.beginValue.set(num)
        self.entry = tk.Entry(master, textvariable = self.beginValue)
        self.entry.select_range(0, tk.END)
        self.entry.grid(row=0, column=1)
        self.entry.focus_set()


    def is_int(self, s):
        try:
            int(s)
            return True
        except ValueError:
            pass
        return False


    def validate(self):
        if self.is_int(self.entry.get())==False:
            tk.messagebox.showinfo("Alert!","Please type an integer between 0 and 10")
        else:
            if int(self.entry.get()) >=0 and int(self.entry.get()) <= 500:
                return True
            else:
                tk.messagebox.showinfo("Alert!","Please type an integer between 0 and 10")


    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()
        self.cancel = True


    def apply(self):
        self.numPoints = int(self.entry.get())
        self.ok = True


    def numPoints_accessor(self):
        return self.numPoints


    def userCancelled(self):
        if self.ok == True:
            return False
        return True
        if self.ok == True:
            return False
        return True


if __name__ == "__main__":
    dapp = DisplayApp(1024, 768)
    dapp.main()


