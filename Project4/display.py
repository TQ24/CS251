################
# CS 251
# Spring 2018
# Tracy Quan
# Project 4

import tkinter as tk
import math
import random
import numpy as np
import view
from tkinter import messagebox
from tkinter import filedialog
import data
import sys
import analysis



# create a class to build and manage the display
class DisplayApp:

    def __init__(self, width, height):

        # create a tk object, which is the root window
        self.root = tk.Tk()

        # width and height of the window
        self.initDx = width
        self.initDy = height
        self.texture_selection = None
        self.hasHistogram = False
        self.datamatrix = None

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

        self.data_obj = None

        # EXTENSIONS
        self.panning = 5

        self.plot_cols = None

        self.data_obj = None

        self.x_label = None 

        self.y_label = None

        self.z_label = None

        self.color_label = None 

        self.size_label = None


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
    # build data points on info canvas
    def buildDataPoints2(self):
        if self.hasHistogram == True:
            return
        vobj_clone = self.vobj.clone()
        vobj_clone.screen = np.matrix([250, 250])
        vobj_clone.offset = np.matrix([10, 90])
        vtm = vobj_clone.build()
        pts = vtm * self.datamatrix.T
        pts = pts.T
        print(pts)
        #print(self.infocanvas.winfo_width(), self.infocanvas.winfo_height())
        #print(pts.shape[0])
        self.infopts = []
        for i in range(pts.shape[0]):
            x = pts[i, 0]
            y = pts[i, 1]
            dx = 2
            infopt = self.infocanvas.create_oval( x+10-dx, y-70-dx, x+10+dx, y-70+dx, fill = "dark blue", outline="")
            self.infopts.append(infopt)
            #self.objects.append(pt)


    # update the color of datapoints on info canvas
    def update_infocanvas(self):
        if self.hasHistogram == True:
            return 
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
        self.infocanvas = tk.Canvas(self.cntlframe, background = "grey90", height = '10c')
        self.infocanvas.pack(side=tk.BOTTOM)

        infocanvaslabel = tk.Label(self.cntlframe, text = "Mini Window :D")
        infocanvaslabel.pack(side = tk.BOTTOM)

        sep = tk.Frame( self.root, height=self.initDy, width=2, bd=1, relief=tk.SUNKEN )
        sep.pack( side=tk.RIGHT, padx = 2, pady = 2, fill=tk.Y)

        # make a cmd 1 button in the frame
        self.buttons = []
        self.button1 = tk.Button( self.cntlframe, text="Reset", command=self.handleResetButton, width=5 )
        self.buttons.append( self.button1)
        self.button1.pack(side=tk.TOP, pady = 10)

        self.button2 = tk.Button( self.cntlframe, text="Plot Data", command=self.handlePlotData, width=8 )
        self.button2.pack(side = tk.TOP, pady = 10)
        #self.buttons[-1][1].pack(side=tk.TOP)  # default side is top

        #bt1 = tk.Button(self.cntlframe, text="Panning Factor", command=self.set_panning, width = 5)
        #bt1.pack(side = tk.TOP)

        self.s1 = tk.Scale(self.cntlframe, label = "Panning", width = 5, orient = tk.HORIZONTAL, to = 10)
        self.s1.set(5)
        self.s1.pack(side=tk.TOP, pady = 10)

        self.s2 = tk.Scale(self.cntlframe, label = "Rotation", width = 5, orient = tk.HORIZONTAL, to = 10)
        self.s2.set(5)
        self.s2.pack(side=tk.TOP, pady = 10)

        #############
        # EXTENSION #
        #############
        self.texture_selection = tk.StringVar(self.root)
        self.texture_selection.set("Texture")
        texture_box = tk.OptionMenu(self.cntlframe, self.texture_selection, "Solid", "Outline")
        texture_box.pack(side=tk.TOP, pady = 10)
        #print("self.texture", self.texture_selection.get())
        # update texture
        self.button3 = tk.Button( self.cntlframe, text="Update Texture", command=self.updatePoints, width=15 )
        self.button3.pack( side = tk.TOP )
        # user instruction
        self.button4 = tk.Button( self.cntlframe, text="User Instruction", command = self.showInstruction)
        self.button4.pack(side= tk.BOTTOM, pady = 10)

        return


    def buildPoints(self, plot_cols):
        # Delete any existing canvas objects used for plotting data.
        self.clearData()

        # If you are selecting only 2 columns to plot, add a column of 0's (z-value) 
        # and a column of 1's (homogeneous coordinate) to the data.
        self.datamatrix = analysis.normalize_columns_separately(plot_cols, self.data_obj)
        if self.selected_size == 1:
            self.size_list = 1
        else:
            self.size_list = analysis.normalize_columns_separately([self.selected_size], self.data_obj)

        if self.selected_color == "blue":
            self.color_list = "blue"
        else:
            self.color_list = analysis.normalize_columns_separately([self.selected_color], self.data_obj)
        # print("color list:", self.color_list)
        n,m = self.datamatrix.shape
        ones = np.ones((n, 1))
        if len(plot_cols)==1:
            self.hasHistogram = True
            zeros = ones * 0
            self.datamatrix = np.hstack((self.datamatrix, zeros, zeros, ones))
            self.buildHistogram()
            return
        if len(plot_cols)==2:
            self.hasHistogram = False
            zeros = ones * 0
            # zeros = np.matrix(zeros)
            self.datamatrix = np.hstack((self.datamatrix, zeros, ones))
        if len(plot_cols)==3:
            self.hasHistogram = False
            self.datamatrix = np.hstack((self.datamatrix, ones))
        self.build_miniwin()
        vtm = self.vobj.build()
        pts = vtm * self.datamatrix.T
        pts = pts.T
        for i in range(pts.shape[0]):
            x = pts[i, 0]
            y = pts[i, 1]
            if isinstance(self.size_list, int):
                dx = 1
            else:
                dx = float(self.size_list[i])*2+1
            #print("dx", dx)
            # print(rgb)
            if isinstance(self.color_list, str):
                color = "blue"
            else:
                rgb = (0, int((1-float(self.color_list[i]))*255), int(float(self.color_list[i])*255))
                color = f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
            print(color)
            if self.texture_selection.get() == "Solid":
                pt = self.canvas.create_oval( x-dx, y-dx, x+dx, y+dx, fill = color, outline="")
            elif self.texture_selection.get() == "Outline":
                pt = self.canvas.create_oval( x-dx, y-dx, x+dx, y+dx, fill="", outline=color)
            else:
                pt = self.canvas.create_oval( x-dx, y-dx, x+dx, y+dx, fill = color, outline="")
            self.objects.append(pt)


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
        self.current_y = pts.item(1,0)
        #self.buildDataPoints()


    def build_miniwin(self):
        self.buildDataPoints2()


    # modify the endpoints of the axes to their new location
    def updateAxes(self):
        vtm = self.vobj.build()
        pts = (vtm * self.axes.T).T
        #for line in self.lineobjs:
        #i = self.lineobjs.index(line)
        #self.canvas.coords(line, pts.item(2*i,0),pts.item(2*i,1), pts.item(2*i+1,0),pts.item(2*i+1,1))
        self.canvas.coords(self.lineobjs[0], pts.item(0,0),pts.item(0,1), pts.item(1,0),pts.item(1,1))
        self.canvas.coords(self.lineobjs[1], pts.item(2,0),pts.item(2,1), pts.item(3,0),pts.item(3,1))            
        self.canvas.coords(self.lineobjs[2], pts.item(4,0),pts.item(4,1), pts.item(5,0),pts.item(5,1))

        if self.x_label != None:
            self.canvas.delete(self.lineobjs[3])
            self.lineobjs[3] = self.canvas.create_text(pts[1,0]+5, pts[1,1]+5, 
                                                        text = self.x_label, fill="blue", font="Arial")
        else:
            self.canvas.coords(self.lineobjs[3], pts[1,0]+5, pts[1,1]+5)

        if self.y_label != None:
            self.canvas.delete(self.lineobjs[4])
            self.lineobjs[4] = self.canvas.create_text(pts[3,0]+8, pts[3,1]+5, 
                                                        text = self.y_label, fill="red", font="Arial")
        else:
            self.canvas.coords(self.lineobjs[4], pts[3,0]+8, pts[3,1]+5)

        if self.z_label != None:
            self.canvas.delete(self.lineobjs[5])
            self.lineobjs[5] = self.canvas.create_text(pts[5,0]+8, pts[5,1]+5, 
                                                        text = self.z_label, fill="dark green", font="Arial")
        else:
            self.canvas.coords(self.lineobjs[5], pts[5,0]+8, pts[5,1]+5)
        #self.current_y = pts.item(0,1)
        #print("self.current y",self.current_y)

        if self.color_label != None:
            if len(self.lineobjs)>6:
                self.canvas.delete(self.lineobjs[6])
                s = "Color dimension: " + self.color_label
                self.lineobjs[6] = self.canvas.create_text(500, 50, 
                                                            text = s, fill="dark blue", font="Arial")
            else:
                s = "Color dimension: " + self.color_label
                self.lineobjs.append(self.canvas.create_text(500, 50, 
                                                            text = s, fill="dark blue", font="Arial"))
        else:
            self.lineobjs.append(self.canvas.create_text(500, 50, 
                                                            text = " ", fill="dark blue", font="Arial"))

        if self.size_label != None:
            if len(self.lineobjs)>7:
                self.canvas.delete(self.lineobjs[7])
                s = "Size dimension: " + self.size_label
                self.lineobjs[7] = self.canvas.create_text(500, 70, 
                                                            text = s, fill="dark blue", font="Arial")
            else:
                s = "Size dimension: " + self.size_label
                self.lineobjs.append(self.canvas.create_text(500, 70, 
                                                            text = s, fill="dark blue", font="Arial"))
        else:
            self.lineobjs.append(self.canvas.create_text(500, 70, 
                                                            text = " ", fill="dark blue", font="Arial"))
        self.update_infocanvas()

    # update points
    def updatePoints(self):
        if len(self.objects)==0:
            return 
        vtm = self.vobj.build()
        dapts = vtm * self.datamatrix.T 
        dapts = dapts.T 
        for i in range(len(self.objects)):
            x = dapts[i,0]
            y = dapts[i,1]
            if isinstance(self.size_list, int):
                dx = 1
            else:
                dx = float(self.size_list[i])*2+1
            self.canvas.coords(self.objects[i], x-dx, y-dx, x+dx, y+dx)
            if isinstance(self.color_list, str):
                color = "blue"
            else:
                rgb = (0, int((1-float(self.color_list[i]))*255), int(float(self.color_list[i])*255))
                color = f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
            
            if self.texture_selection.get() == "Solid" and isinstance(self.color_list, str)==False:
                self.canvas.itemconfig( self.objects[i], fill=color, outline="")
            elif self.texture_selection.get() == "Outline" and isinstance(self.color_list, str)==False:
                self.canvas.itemconfig( self.objects[i], fill="", outline=color)


    # set bindings
    def setBindings(self):
        self.root.bind( '<Button-1>', self.handleButton1 )
        self.root.bind( '<Button-2>', self.handleButton2 )
        self.canvas.bind( '<Button-3>', self.handleButton3 )
        self.canvas.bind( '<B1-Motion>', self.handleButton1Motion )
        self.canvas.bind( '<B2-Motion>', self.handleButton2Motion )
        self.canvas.bind( '<B3-Motion>', self.handleButton3Motion )
        self.root.bind( '<Control-Button-1>', self.handleButton2 )
        self.canvas.bind( '<Control-B1-Motion>', self.handleButton2Motion )
        self.root.bind( '<Control-q>', self.handleQuit )
        self.root.bind( '<Control-o>', self.handleModO )
        self.root.bind( '<Command-O>', self.handleOpen)
        self.root.bind( '<Control-y>', self.yzaxes)
        # self.root.bind( '<Control-z>', self.zxaxes)
        self.canvas.bind( '<Configure>', self.handleResize )
        self.root.bind( '<Left>', self.leftrotate)
        self.root.bind( '<Right>', self.rightrotate)
        self.root.bind( '<Up>', self.uprotate)
        self.root.bind( '<Down>', self.downrotate)
        # self.canvas.bind( '<Motion>', self.handleMouseMotion )
        return

    
    def handlePlotData(self, event=None):
        # Check if any file is loaded
        if self.data_obj == None:
            tk.messagebox.showinfo("Alert!","Please Open a file first ( Cmd-O )")
            return
        # pop up options dialog
        self.plotdata_dialog = MyDialog(self.root, self.data_obj)
        if self.plotdata_dialog.userCancelled() == True:
            return
        self.plot_cols = self.handleChooseAxes()
        if self.plot_cols != None:
            self.buildPoints(self.plot_cols)
            self.updateAxes()


    def handleChooseAxes(self, event=None):
        # self.colorlist = ["blue", "sky blue", "red", "green", "orange"]
        if self.plotdata_dialog.x_selection==() and self.plotdata_dialog.y_selection==() and self.plotdata_dialog.z_selection==():
            tk.messagebox.showinfo("Instruction", "Please select at lease one column")
            return
        self.selected_x = self.data_obj.numeric[self.plotdata_dialog.x_selection[0]]
        self.x_label = self.selected_x
        #############
        # EXTENSION #
        #############
        if self.plotdata_dialog.y_selection != ():
            self.selected_y = self.data_obj.numeric[self.plotdata_dialog.y_selection[0]]
            self.y_label = self.selected_y
        else:
            self.selected_y = None

        if self.plotdata_dialog.z_selection != ():
            self.selected_z = self.data_obj.numeric[self.plotdata_dialog.z_selection[0]]
            self.z_label = self.selected_z
        else:
            self.selected_z = None
        
        if self.plotdata_dialog.color_selection != ():
            self.selected_color = self.data_obj.numeric[self.plotdata_dialog.color_selection[0]]
            self.color_label = self.selected_color
        else:
            self.selected_color = "blue"
            self.color_label = "blue"
        
        if self.plotdata_dialog.size_selection != ():
            self.selected_size = self.data_obj.numeric[self.plotdata_dialog.size_selection[0]]
            self.size_label = self.selected_size
        else:
            self.selected_size = 1
            self.size_label = "1"

        if self.selected_y == None and self.selected_z == None:
            selected_cols = [self.selected_x]
        elif self.selected_z == None:
            selected_cols = [self.selected_x, self.selected_y]
        else:
            selected_cols = [self.selected_x, self.selected_y, self.selected_z]
        print(selected_cols)


        return selected_cols


    #############
    # EXTENSION #
    #############
    def buildHistogram(self):
        self.clearData()
        self.vobj.reset()
        self.updateAxes()
        vtm = self.vobj.build()
        pts = vtm*self.datamatrix.T
        #pts = self.datamatrix / np.linalg.norm(self.datamatrix)
        pts = pts.T
        print(pts)

        #print(pts)
        #print("first item",pts[0, 0])
        #print(pts.shape[0])
        #print(pts.shape[1])
        for i in range(pts.shape[0]):
            len_x = self.canvas.coords(self.lineobjs[0])
            #print("len:",len_x[2]-len_x[0])
            len_y = self.canvas.coords(self.lineobjs[1])
            y_extent = len_y[3]-len_y[1]
            unit = -y_extent/(pts.shape[0]*1.0)
            print(unit)
            y1 = len_x[1]
            y2 = pts[i, 0]
            x1 = len_x[0] + unit*i
            x2 = len_x[0]+unit*(i+1)
            #print(x1, x2)
            rec = self.canvas.create_rectangle(x1, y1, x2, y2, fill = "sky blue", outline="")
            self.objects.append(rec)
            print("should draw rec")


    def updateHistogram(self):       
        if len(self.objects)==0:
            return 
        if self.widget_under_mouse(self.cntlframe)!= self.s1 and self.widget_under_mouse(self.cntlframe)!= self.s2 and self.widget_under_mouse(self.cntlframe)!= self.cntlframe:
            #self.clearData()
            vtm = self.vobj.build()
            pts = vtm*self.datamatrix.T
            #pts = self.datamatrix / np.linalg.norm(self.datamatrix)
            pts = pts.T

            for i in range(len(self.objects)):
                len_x = self.canvas.coords(self.lineobjs[0])
                #print(len_x)
                #print("len:",len_x[2]-len_x[0])
                len_y = self.canvas.coords(self.lineobjs[1])
                y_extent = len_y[3]-len_y[1]
                unit = -y_extent/(pts.shape[0]*1.0)
                y1 = self.current_y
                print("y1",y1)
                y2 = pts[i, 0]
                x1 = len_x[0] + unit*i
                x2 = len_x[0]+unit*(i+1)
                #print(x1, x2)
                self.canvas.coords(self.objects[i], x1, y1, x2, y2)
                # rec = self.canvas.create_rectangle(x1, y1, x2, y2, fill = "sky blue", outline="")
            #self.objects.append(rec)
            #print("should draw rec")


    def showInstruction(self):
        str = "- Use Command + O(capital) to open a file or go to File menu bar\n\n" +\
              "- Use Mouse Button 1 (left) to pan\n\n" +\
              "- Use Mouse Button 2 (right) to rotate\n\n" +\
              "- Use Arrow Keys to rotate faster\n\n" +\
              "- Use Mouse Button 3 (scroll) to zoom in or zoom out\n\n" +\
              "- Use the Scale bar on the right control frame to adjust mouse sensitivity\n\n"
        tk.messagebox.showinfo("Instruction", str)

    #############
    # EXTENSION #
    #############
    def handleResize(self, event=None):
        # You can handle resize events here
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        short = min(w,h)
        self.vobj.screen = np.matrix([short-250, short - 250])
        self.updateAxes()
        self.updatePoints()


    def handleOpen(self, event=None):
        print('handleOpen')
        fn = filedialog.askopenfilename( parent=self.root,
                                           title='Choose a data file', initialdir='.' )
        self.data_obj = data.Data(fn)
        

    def handleModO(self, event):
        self.handleOpen()


    def handleQuit(self, event=None):
        print('Terminating')
        self.root.destroy()


    def handleResetButton(self):
        print('handling reset button')
        self.vobj.reset()
        self.clearData()
        self.clearData_info()
        self.status_scale = tk.Label(self.canvas, text = "Scaling: 1.00x").grid(row=0, padx =self.initDx/2, pady = self.initDy-100)
        self.status_rotation = tk.Label(self.root, text = "Rotation-- Angle1:  0.00, Angle2: 0.00").grid(row=1, padx =self.initDx/4, pady = self.initDy-100)
        self.updateAxes()
        self.updatePoints()
        self.hasHistogram = False



    def widget_under_mouse(self, root):
        x,y = root.winfo_pointerxy()
        widget = root.winfo_containing(x,y)
        return widget


    def handleButton1(self, event):
        print('handle button 1: %d %d' % (event.x, event.y))
        self.baseClick1 = (event.x, event.y)
        if self.texture_selection!=None:
            print(self.texture_selection.get())


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
        if self.hasHistogram == True:
            print("Can't pan a histogram")
            return
        print('handle button 1 motion: %d %d' % (event.x - self.baseClick1[0], event.y -self.baseClick1[1]) )
        self.panning = self.s1.get()
        delta0 = (self.panning*3+5)/20*(event.x - self.baseClick1[0])/self.vobj.screen[0,0]*self.vobj.extent[0,0]
        delta1 = (self.panning*3+5)/20*(event.y - self.baseClick1[1])/self.vobj.screen[0,1]*self.vobj.extent[0,1]

        self.vobj.vrp = self.vobj.vrp + delta0 * self.vobj.u + delta1 * self.vobj.vup
        self.updateAxes()
        self.updatePoints()
        self.baseClick1=(event.x, event.y)
    

    # rotation
    def handleButton2Motion( self, event ):
        if self.hasHistogram == True:
            print("Can't rotate a histogram")
            return
        print('handle button 2 motion: %d %d' % (event.x, event.y) )
        ro_fac = 2000 * ((10-self.s2.get()) * 3 + 5) / 20
        delta0 = -(event.x - self.baseClick2[0])/ro_fac*math.pi
        print(delta0)
        delta1 = (event.y - self.baseClick2[1])/ro_fac*math.pi
        self.vobj = self.vobj_clone.clone()
        self.vobj.rotateVRC(delta0, delta1)
        self.updateAxes()
        self.updatePoints()
        print("should update")

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
        if self.hasHistogram == True:
            print("Can't scale a histogram")
            return
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
        self.updatePoints()

        factor = self.begin_ext[0,0]/self.vobj.extent[0,0]
        factor = "%.2f" % factor
        s = "Scaling: " + str(factor) + "x"
        self.status_scale = tk.Label(self.canvas, text = s).grid(row=0, padx =self.initDx/2, pady = self.initDy-100)


    def clearData(self, event=None):
        for obj in self.objects:
            self.canvas.delete(obj)
        self.objects = []

    def clearData_info(self, event=None):
        for obj in self.infopts:
            self.infocanvas.delete(obj)
        self.infopts = []


    def yzaxes(self, event):
        self.vobj.vpn = np.matrix([1,0,0])
        self.u = np.matrix([0,1,0])
        self.updateAxes()
        self.updatePoints()

    #############
    # EXTENSION #
    #############
    def leftrotate(self, event):
        self.vobj.rotateVRC(0.1, 0)
        self.updateAxes()
        self.updatePoints()


    def rightrotate(self, event):
        self.vobj.rotateVRC(-0.1, 0)
        self.updateAxes()
        self.updatePoints()


    def uprotate(self, event):
        self.vobj.rotateVRC(0, -0.1)
        self.updateAxes()
        self.updatePoints()


    def downrotate(self, event):
        self.vobj.rotateVRC(0, 0.1)
        self.updateAxes()
        self.updatePoints()


    def main(self):
        print('Entering main loop')
        self.root.mainloop()


# ------------ Dialog class ---------------
# Dialog class
class Dialog(tk.Toplevel):
    def __init__(self, parent, dobj, title = None):

        tk.Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = tk.Frame(self)

        self.initial_focus = self.body(body, dobj)

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
    

    # command hooks
    def validate(self):

        return 1 # override


    def apply(self):
        pass # override


class MyDialog(Dialog):
    def __init__(self, master, dobj):
        Dialog.__init__(self, master, dobj)
        self.cancel = False

    def body(self, master, dobj):
        x_label = tk.Label(master, text="x-axis:")
        x_label.pack(side=tk.LEFT)

        self.x_listbox = tk.Listbox(master, height = len(dobj.numeric),  exportselection = 0)
        for header in dobj.numeric:
            self.x_listbox.insert(tk.END, header)
        self.x_listbox.pack(side = tk.LEFT)

        y_label = tk.Label(master, text="y-axis:")
        y_label.pack(side=tk.LEFT)

        self.y_listbox = tk.Listbox(master, height = len(dobj.numeric),  exportselection = 0)
        for header in dobj.numeric:
            self.y_listbox.insert(tk.END, header)
        self.y_listbox.pack(side = tk.LEFT)

        z_label = tk.Label(master, text="z-axis:")
        z_label.pack(side=tk.LEFT)

        self.z_listbox = tk.Listbox(master, height = len(dobj.numeric),  exportselection = 0)
        for header in dobj.numeric:
            self.z_listbox.insert(tk.END, header)
        self.z_listbox.pack(side = tk.LEFT)

        color_label = tk.Label(master, text="Color:")
        color_label.pack(side=tk.LEFT)

        self.color_listbox = tk.Listbox(master, height = len(dobj.numeric),  exportselection = 0)
        for header in dobj.numeric:
            self.color_listbox.insert(tk.END, header)
        self.color_listbox.pack(side = tk.LEFT)

        size_label = tk.Label(master, text="Size:")
        size_label.pack(side=tk.LEFT)

        self.size_listbox = tk.Listbox(master, height = len(dobj.numeric),  exportselection = 0)
        for header in dobj.numeric:
            self.size_listbox.insert(tk.END, header)
        self.size_listbox.pack(side = tk.LEFT)




    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()
        self.cancel = True


    def apply(self):
        self.x_selection = self.x_listbox.curselection()
        self.y_selection = self.y_listbox.curselection()
        self.z_selection = self.z_listbox.curselection()
        self.color_selection = self.color_listbox.curselection()
        self.size_selection = self.size_listbox.curselection()
        self.ok = True


    def numPoints_accessor(self):
        return self.numPoints


    def userCancelled(self):
        if self.ok == True:
            return False
        return True
        


if __name__ == "__main__":
    dapp = DisplayApp(1024, 768)
    dapp.main()


