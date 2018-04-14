################
# CS 251
# Spring 2018
# Tracy Quan
# Project 6

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
import subprocess
import csv





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

        self.linregress_lines = []

        self.multiregress_lines = []

        self.axesticks = []

        self.endpoints = None 

        self.endpoints2 = None

        self.x_label = None 

        self.y_label = None

        self.z_label = None

        # set up the geometry for the window
        self.root.geometry( "%dx%d+50+30" % (self.initDx, self.initDy) )

        # set the title of the window
        self.root.title("Data Insider")

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

        self.infopts = None

        # EXTENSIONS
        self.panning = 5

        self.plot_cols = None

        self.data_obj = None

        self.color_label = None 

        self.size_label = None

        self.eqlabel = None

        self.xmin = None

        self.xmanx = None

        self.ymin = None 

        self.ymax = None

        self.zmin = None

        self.zmax = None

        self.pcanamelst = []

        self.pcadobjlst = []

        self.plotpca_dobj = None
    

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
        menutext = [ [ 'Open...  \xE2\x8C\x98-O', '-', 'Quit  \xE2\x8C\x98-Q' , 'Linear Regression', 'PCA File Open'] ]

        # menu callback functions
        menucmd = [ [self.handleOpen, None, self.handleQuit, self.handleLinearRegression, self.handleOpenPCA]  ]
        
        # build the menu elements and callbacks
        for i in range( len( self.menulist ) ):
            for j in range( len( menutext[i]) ):
                if menutext[i][j] != '-':
                    self.menulist[i].add_command( label = menutext[i][j], command=menucmd[i][j] )
                else:
                    self.menulist[i].add_separator()


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
        self.cntlframe2 = tk.Frame(self.root)
        self.cntlframe2.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)
        
        self.cntlframe = tk.Frame(self.root)
        self.cntlframe.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)


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
        self.button1.pack(side=tk.TOP, pady = 2)

        self.button2 = tk.Button( self.cntlframe, text="Plot Data", command=self.handlePlotData, width=8 )
        self.button2.pack(side = tk.TOP, pady = 2)
        
        self.button3 = tk.Button( self.cntlframe, text="Single Linear Regression", command=self.handleLinearRegression)
        self.button3.pack(side = tk.TOP, pady = 2)

        self.button4 = tk.Button( self.cntlframe, text = "Multi Linear Regression", command=self.handleMulti)
        self.button4.pack(side = tk.TOP, pady = 2)

        self.s1 = tk.Scale(self.cntlframe, label = "Panning", width = 5, orient = tk.HORIZONTAL, to = 10)
        self.s1.set(5)
        self.s1.pack(side=tk.TOP, pady = 2)

        self.s2 = tk.Scale(self.cntlframe, label = "Rotation", width = 5, orient = tk.HORIZONTAL, to = 10)
        self.s2.set(5)
        self.s2.pack(side=tk.TOP, pady = 2)

        self.texture_selection = tk.StringVar(self.root)
        self.texture_selection.set("Texture")
        texture_box = tk.OptionMenu(self.cntlframe, self.texture_selection, "Solid", "Outline")
        texture_box.pack(side=tk.TOP, pady = 2)
        #print("self.texture", self.texture_selection.get())
        # update texture
        self.button3 = tk.Button( self.cntlframe, text="Update Texture", command=self.updatePoints, width=15 )
        self.button3.pack( side = tk.TOP, pady = 1 )
        # user instruction
        self.button4 = tk.Button( self.cntlframe, text="User Instruction", command = self.showInstruction)
        self.button4.pack(side= tk.BOTTOM)

        # show stats
        self.button5 = tk.Button( self.cntlframe, text="Show Stats", command = self.showStats)
        self.button5.pack(side= tk.BOTTOM, pady = 1)
        
        self.button6 = tk.Button( self.cntlframe, text = "Capture", command = self.capture)
        self.button6.pack(side = tk.BOTTOM, pady = 1)
        
        ##############
        ## Project6 ##

        PCAlabel = tk.Label(self.cntlframe2, text = "PCA Analysis")
        PCAlabel.pack(side = tk.TOP)
        
        self.pcalistbox = tk.Listbox(self.cntlframe2, height = 5,  exportselection = 0)
        self.pcalistbox.pack(side=tk.TOP, pady = 1)

        self.button7 = tk.Button( self.cntlframe2, text = "PCA Plot", command = self.handleplotPCA)
        self.button7.pack(side=tk.TOP)

        self.button8 = tk.Button( self.cntlframe2, text = "Delete PCA", command = self.deletepca)
        self.button8.pack( side = tk.TOP )

        self.button9 = tk.Button( self.cntlframe2, text = "PCA Stats", command = self.showpcastats)
        self.button9.pack( side = tk.TOP )

        self.button10 = tk.Button( self.cntlframe2, text = "Write to cvs", command = self.writePCAtoCSV)
        self.button10.pack( side = tk.TOP )


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
        self.buildTicks()

                      
    def buildLinearRegression(self):
        self.ind_header = self.data_obj.numeric[self.linregress_dialog.ind_selection[0]]
        self.dep_header = self.data_obj.numeric[self.linregress_dialog.dep_selection[0]]
        lin_header = [self.ind_header, self.dep_header]
        m_nor = analysis.normalize_columns_separately( lin_header, self.data_obj )
        n,m = m_nor.shape
        ones = np.ones((n,1))
        self.datamatrix = np.hstack( (m_nor, ones*0, ones) )

        self.x_label = self.ind_header
        self.y_label = self.dep_header
        self.z_label = None

        vtm = self.vobj.build()
        pts = vtm * self.datamatrix.T
        pts = pts.T

        if self.linregress_dialog.size_selection == ():
            self.size_list = 1
        else:
            size_header = self.data_obj.numeric[self.linregress_dialog.size_selection[0]]
            self.size_label = size_header
            self.size_list = analysis.normalize_columns_separately([size_header], self.data_obj)

        if self.linregress_dialog.color_selection == ():
            self.color_list = "blue"
        else:
            color_header = self.data_obj.numeric[self.linregress_dialog.color_selection[0]]
            self.color_label = color_header
            self.color_list = analysis.normalize_columns_separately([color_header], self.data_obj)

        for i in range(pts.shape[0]):
            x = pts[i,0]
            y = pts[i,1]

            if isinstance(self.size_list, int):
                dx = 1
            else:
                dx = float(self.size_list[i])*2+1
            
            if isinstance(self.color_list, str):
                color = "blue"
            else:
                rgb = (0, int((1-float(self.color_list[i]))*255), int(float(self.color_list[i])*255))
                color = f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

            pt = self.canvas.create_oval( x-dx, y-dx, x+dx, y+dx, fill = color, outline="")
            self.objects.append(pt)

        lin_result = analysis.single_linear_regression( self.data_obj, self.ind_header, self.dep_header )
        m = lin_result[0]
        b = lin_result[1]
        rrs = lin_result[2]
        xmin = lin_result[5]
        xmax = lin_result[6]
        ymin = lin_result[7]
        ymax = lin_result[8]
        self.xmin = xmin 
        self.xmax = xmax
        self.ymin = ymin 
        self.ymax = ymax
        self.endpoints = np.matrix([[ 0, (( xmin * m + b ) - ymin)/(ymax - ymin), 0, 1 ],
                          [ 1, (( xmax * m + b ) - ymin)/(ymax - ymin), 0, 1 ]])
        ep = vtm * self.endpoints.T
        ep = ep.T

        l = self.canvas.create_line( ep[0,0], ep[0,1], ep[1,0], ep[1,1], fill = "red", width = 2)
        self.linregress_lines.append(l)
        print(lin_result)
        if b > 0:
            t = "y = " + str(m) + "* x + " + str("%.3f" % b) + "\n" + "RRS: " + str("%.3f" % rrs)
        else:
            t = "y = " + str(m) + "* x " + str("%.3f" % b) + "\n" + "RRS: " + str("%.3f" % rrs)
        t = t + "\nDependent Var: " + self.dep_header + "\n" + "Independent Var: " + self.ind_header
        self.eqlabel = tk.Label(self.canvas, text=t, background = "gray95", font = ("Courier", 13))
        self.eqlabel.pack(side = tk.TOP, padx = 10)
        

    def buildTicks(self):
        if self.x_label != None and self.xmin != None and self.xmax!= None:
            x_coords = self.canvas.coords(self.lineobjs[0])
            x0 = x_coords[0]
            y0 = x_coords[1]
            t1 = self.canvas.create_text(x0, y0+15, text = self.xmin, fill = "gray50")
            x1 = x_coords[2]
            y1 = x_coords[3]
            t2 = self.canvas.create_text(x1, y1+15, text = self.xmax, fill = "gray50")

            half = (self.xmin+self.xmax)/2
            x2 = (x0 + x1)/2
            y2 = y1 
            t = str("%.2f" % half)
            t3 = self.canvas.create_text(x2, y2+15, text = t, fill = "gray50")

            self.axesticks.append(t1)
            self.axesticks.append(t2)
            self.axesticks.append(t3)

            l1 = self.canvas.create_line(x1, y1, x1, y1-10, fill = "gray50", width = 2)
            l2 = self.canvas.create_line(x2, y2, x2, y2-10, fill = "gray50", width = 2)
            self.axesticks.append(l1)
            self.axesticks.append(l2)

        if self.y_label != None and self.ymin != None and self.ymax!= None:
            y_coords = self.canvas.coords(self.lineobjs[1])
            x0 = y_coords[0]
            y0 = y_coords[1]
            t1 = self.canvas.create_text(x0-20, y0, text = self.ymin, fill = "gray50")
            x1 = y_coords[2]
            y1 = y_coords[3]
            t2 = self.canvas.create_text(x1-20, y1, text = self.ymax, fill = "gray50")

            half = (self.ymin+self.ymax)/2
            y2 = (y0 + y1)/2
            x2 = x1 
            t = str("%.2f" % half)
            t3 = self.canvas.create_text(x2-20, y2, text = t, fill = "gray50")

            self.axesticks.append(t1)
            self.axesticks.append(t2)
            self.axesticks.append(t3)

            l1 = self.canvas.create_line(x1, y1, x1+10, y1, fill = "gray50", width = 2)
            l2 = self.canvas.create_line(x2, y2, x2+10, y2, fill = "gray50", width = 2)
            self.axesticks.append(l1)
            self.axesticks.append(l2)


    def updateTicks(self):
        if len(self.axesticks)>0:
            x_coords = self.canvas.coords(self.lineobjs[0])
            x0 = x_coords[0]
            y0 = x_coords[1]
            self.canvas.coords(self.axesticks[0], x0, y0+15 )
    
            x1 = x_coords[2]
            y1 = x_coords[3]
            self.canvas.coords(self.axesticks[1], x1, y1+15 )

            x2 = (x0 + x1)/2
            y2 = y1 
            self.canvas.coords(self.axesticks[2], x2, y2+15 )

            self.canvas.coords(self.axesticks[3], x1, y1, x1, y1-10 )

            self.canvas.coords(self.axesticks[4], x2, y2, x2, y2-10 )

        if len(self.axesticks)>5:
            y_coords = self.canvas.coords(self.lineobjs[1])
            x0 = y_coords[0]
            y0 = y_coords[1]
            self.canvas.coords(self.axesticks[5], x0-20, y0 )
            x1 = y_coords[2]
            y1 = y_coords[3]
            self.canvas.coords(self.axesticks[6], x1-20, y1 )
            half = (self.ymin+self.ymax)/2
            y2 = (y0 + y1)/2
            x2 = x1 
            self.canvas.coords(self.axesticks[7], x2-20, y2 )

            self.canvas.coords(self.axesticks[8], x1, y1, x1+10, y1 )

            self.canvas.coords(self.axesticks[9], x2, y2, x2+10, y2 )

                      
    def updateRegress(self):
        vtm = self.vobj.build()
        ep = (vtm * self.endpoints.T).T
        self.canvas.coords(self.linregress_lines[0], ep[0,0], ep[0,1], ep[1,0], ep[1,1])


    def buildMultiRegression(self):
        h1 = self.multi_dialog.ind_selection[0]
        h2 = self.multi_dialog.ind_selection[1]
        header1 = self.data_obj.numeric[h1]
        header2 = self.data_obj.numeric[h2]
        dep_h = self.data_obj.numeric[self.multi_dialog.dep_selection[0]]
        lin_header = [header1, dep_h, header2] #alert
        m_nor = analysis.normalize_columns_separately( lin_header, self.data_obj )
        n,m = m_nor.shape
        ones = np.ones((n,1))
        self.datamatrix = np.hstack( (m_nor, ones) )
        self.x_label = header1
        self.y_label = dep_h
        self.z_label = header2

        vtm = self.vobj.build()
        pts = vtm * self.datamatrix.T
        pts = pts.T

        if self.multi_dialog.size_selection == ():
            self.size_list = 1
        else:
            size_header = self.data_obj.numeric[self.multi_dialog.size_selection[0]]
            self.size_label = size_header
            self.size_list = analysis.normalize_columns_separately([size_header], self.data_obj)

        if self.multi_dialog.color_selection == ():
            self.color_list = "blue"
        else:
            color_header = self.data_obj.numeric[self.multi_dialog.color_selection[0]]
            self.color_label = color_header 
            self.color_list = analysis.normalize_columns_separately([color_header], self.data_obj)

        for i in range(pts.shape[0]):
            x = pts[i,0]
            y = pts[i,1]

            if isinstance(self.size_list, int):
                dx = 1
            else:
                dx = float(self.size_list[i])*2+1
            
            if isinstance(self.color_list, str):
                color = "blue"
            else:
                rgb = (0, int((1-float(self.color_list[i]))*255), int(float(self.color_list[i])*255))
                color = f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

            pt = self.canvas.create_oval( x-dx, y-dx, x+dx, y+dx, fill = color, outline="")
            self.objects.append(pt)

        result = analysis.linear_regression( self.data_obj, [header1, header2], dep_h )
        
        e = result[0]
        m0 = float(e[0])
        m1 = float(e[1])
        b = float(e[2])
        r2 = result[2]
        x0 = result[5][0]
        print("x0",x0)
        x0min = x0[0]
        x0max = x0[1]
        x1 = result[6][0]
        x1min = x1[0]
        x1max = x1[1]
        y = result[7][0]
        ymin = y[0]
        ymax = y[1]

        self.xmin = x0min
        self.xmax = x0max
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = x1min
        self.zmax = x1max


        self.endpoints2 = np.matrix([[ 0, (( x0min * m0 + x1min * m1 + b ) - ymin)/(ymax - ymin), 0, 1 ],
                                    [ 0, (( x0min * m0 + x1max * m1 + b ) - ymin)/(ymax - ymin), 1, 1 ],
                                    [ 1, (( x0max * m0 + x1min * m1 + b ) - ymin)/(ymax - ymin), 0, 1 ],
                                    [ 1, (( x0max * m0 + x1max * m1 + b ) - ymin)/(ymax - ymin), 1, 1 ]])
        ep = vtm * self.endpoints2.T
        ep = ep.T

        l1 = self.canvas.create_line( ep[0,0], ep[0,1], ep[1,0], ep[1,1], fill = "orange", width = 2)
        l2 = self.canvas.create_line( ep[1,0], ep[1,1], ep[3,0], ep[3,1], fill = "orange", width = 2)
        l3 = self.canvas.create_line( ep[0,0], ep[0,1], ep[2,0], ep[2,1], fill = "orange", width = 2)
        l4 = self.canvas.create_line( ep[2,0], ep[2,1], ep[3,0], ep[3,1], fill = "orange", width = 2)

        self.multiregress_lines.append(l1)
        self.multiregress_lines.append(l2)
        self.multiregress_lines.append(l3)
        self.multiregress_lines.append(l4)

        #print(result)
        if b > 0:
            t = "y = " + str("%.3f" % m0) + "* x0 + " + str("%.3f" % m1) + "* x1 + " + str("%.3f" % b) + "\n" + "R2: " + str("%.3f" % r2)
        else:
            t = "y = " + str("%.3f" % m0) + "* x0 + " + str("%.3f" % m1) + "* x1" + str("%.3f" % b) + "\n" + "R2: " + str("%.3f" % r2)
        t = t + "\n---------------------------------------------------------------"
        t = t + "\nDependent Var: " + dep_h + "\n" + "Independent Var: " + header1 + ", " + header2
        self.eqlabel = tk.Label(self.canvas, text=t, background = "gray95", font = ("Courier", 13))
        self.eqlabel.pack(side = tk.TOP, padx = 10)


    def updateMultiRegress(self):
        vtm = self.vobj.build()
        ep = (vtm * self.endpoints2.T).T
        self.canvas.coords( self.multiregress_lines[0], ep[0,0], ep[0,1], ep[1,0], ep[1,1] )
        self.canvas.coords( self.multiregress_lines[1], ep[1,0], ep[1,1], ep[3,0], ep[3,1] )
        self.canvas.coords( self.multiregress_lines[2], ep[0,0], ep[0,1], ep[2,0], ep[2,1] )
        self.canvas.coords( self.multiregress_lines[3], ep[2,0], ep[2,1], ep[3,0], ep[3,1] )
        

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
            self.canvas.delete(self.lineobjs[3])
            self.lineobjs[3] = self.canvas.create_text(pts[1,0]+5, pts[1,1]+5, 
                                                        text = "x", fill="blue", font="Arial")
        if self.y_label != None:
            self.canvas.delete(self.lineobjs[4])
            self.lineobjs[4] = self.canvas.create_text(pts[3,0]+8, pts[3,1]+5, 
                                                        text = self.y_label, fill="red", font="Arial")
        else:
            self.canvas.delete(self.lineobjs[4])
            self.lineobjs[4] = self.canvas.create_text(pts[3,0]+8, pts[3,1]+5, 
                                                        text = "y", fill="red", font="Arial")

        if self.z_label != None:
            self.canvas.delete(self.lineobjs[5])
            self.lineobjs[5] = self.canvas.create_text(pts[5,0]+8, pts[5,1]+5, 
                                                        text = self.z_label, fill="dark green", font="Arial")
        else:
            self.canvas.delete(self.lineobjs[5])
            self.lineobjs[5] = self.canvas.create_text(pts[5,0]+8, pts[5,1]+5, 
                                                        text = "z", fill="dark green", font="Arial")
        #self.current_y = pts.item(0,1)
        #print("self.current y",self.current_y)

        if self.color_label != None:
            if len(self.lineobjs)>6:
                self.canvas.delete(self.lineobjs[6])
                s = "Color dimension: " + self.color_label
                self.lineobjs[6] = self.canvas.create_text(300, 70, 
                                                            text = s, fill="dark blue", font="Arial")
            else:
                s = "Color dimension: " + self.color_label
                self.lineobjs.append(self.canvas.create_text(300, 70, 
                                                            text = s, fill="dark blue", font="Arial"))
        else:
            self.lineobjs.append(self.canvas.create_text(300, 70, 
                                                            text = " ", fill="dark blue", font="Arial"))

        if self.size_label != None:
            if len(self.lineobjs)>7:
                self.canvas.delete(self.lineobjs[7])
                s = "Size dimension: " + self.size_label
                self.lineobjs[7] = self.canvas.create_text(300, 90, 
                                                            text = s, fill="dark blue", font="Arial")
            else:
                s = "Size dimension: " + self.size_label
                self.lineobjs.append(self.canvas.create_text(300, 90, 
                                                            text = s, fill="dark blue", font="Arial"))
        else:
            self.lineobjs.append(self.canvas.create_text(300, 90, 
                                                            text = " ", fill="dark blue", font="Arial"))
        if self.infopts != None:
            self.update_infocanvas()

        if len(self.linregress_lines)!=0:
            self.updateRegress()

        if len(self.multiregress_lines)!=0:
            self.updateMultiRegress()
        if len(self.axesticks)==0:
            self.buildTicks()
        self.updateTicks()


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


    # let the user select the variables to fit and then display them on the main screen
    def handleLinearRegression(self):
        # Check if any file is loaded
        if self.data_obj == None:
            tk.messagebox.showinfo("Alert!","Please Open a file first ( Cmd-O )")
            return
        self.linregress_dialog = LinearRegressionDialog(self.root, self.data_obj)
        if self.linregress_dialog.userCancelled() == True:
            return
        self.clearData()
        if self.infopts != None:
            self.clearData_info()
        #self.clearData_info()
        self.linregress_lines = []
        self.vobj.reset()
        self.updateAxes()
        self.buildLinearRegression()
        self.buildDataPoints2()
        self.updateAxes()


    def handleMulti(self):
        # Check if any file is loaded
        if self.data_obj == None:
            tk.messagebox.showinfo("Alert!","Please Open a file first ( Cmd-O )")
            return
        self.multi_dialog = MultiRegressionDialog(self.root, self.data_obj)
        if self.multi_dialog.userCancelled() == True:
            return
        if len(self.multi_dialog.ind_selection)!=2:
            tk.messagebox.showinfo("Alert!","Please select 2 independent variable)")
            return
        self.clearData()
        if self.infopts != None:
            self.clearData_info()
        #self.clearData_info()
        self.multi_lines = []
        self.vobj.reset()
        self.updateAxes()
        self.buildMultiRegression()
        self.buildDataPoints2()
        self.updateAxes()

    
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
            self.clearData()
            self.buildPoints(self.plot_cols)
            self.updateAxes()


    def handleChooseAxes(self, event=None):
        # self.colorlist = ["blue", "sky blue", "red", "green", "orange"]
        if self.plotdata_dialog.x_selection==() and self.plotdata_dialog.y_selection==() and self.plotdata_dialog.z_selection==():
            tk.messagebox.showinfo("Instruction", "Please select at lease one column")
            return
        self.selected_x = self.data_obj.numeric[self.plotdata_dialog.x_selection[0]]
        self.x_label = self.selected_x
        
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


    def showStats(self):
        if self.data_obj == None or self.plot_cols == None:
            tk.messagebox.showinfo("Alert!","Please Open a file ( Cmd-O ) and plot data or run a regression first")
            return
        s = "----- STATS -----\n\n"
        if self.x_label != None:
            s = s + "X-Axis: " + self.x_label + "\n"
            x_range = analysis.data_range([self.x_label], self.data_obj)
            xmin  = str("%.2f" % x_range[0][0])
            xmax = str("%.2f" % x_range[0][1])
            s = s + "X-Axis Data Range: " + xmin + " - " + xmax + "\n"
            x_stdev = analysis.stdev([self.x_label], self.data_obj)
            s = s + "X-Axis Data Stdev: " + str("%.2f" % x_stdev[0]) + "\n\n"
        if self.y_label != None:
            s = s + "Y-Axis: " + self.y_label + "\n"
            y_range = analysis.data_range([self.y_label], self.data_obj)
            ymin  = str("%.2f" % y_range[0][0])
            ymax = str("%.2f" % y_range[0][1])
            s = s + "Y-Axis Data Range: " + ymin + " - " + ymax + "\n"
            y_stdev = analysis.stdev([self.y_label], self.data_obj)
            s = s + "Y-Axis Data Stdev: " + str("%.2f" % y_stdev[0]) + "\n\n"
        if self.z_label != None:
            s = s + "Z-Axis: " + self.z_label + "\n"
            z_range = analysis.data_range([self.z_label], self.data_obj)
            zmin  = str("%.2f" % z_range[0][0])
            zmax = str("%.2f" % z_range[0][1])
            s = s + "Z-Axis Data Range: " + zmin + " - " + zmax + "\n"
            z_stdev = analysis.stdev([self.z_label], self.data_obj)
            s = s + "Z-Axis Data Stdev: " + str("%.2f" % z_stdev[0]) + "\n\n"
        tk.messagebox.showinfo("Stats", s)


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
    
    
    def handleOpenPCA(self, event=None):
        self.handleOpen()

        pcacols_dia = PCADialog(self.root, self.data_obj)

        if pcacols_dia.userCancelled() == True:
            return
            
        col_ind = pcacols_dia.pca_lb_selection
        h_lst = []
        for num in col_ind:
            h_lst.append(self.data_obj.numeric[num])
        self.pcacols = h_lst   # PCA selected headers
        print("PCA cols:", self.pcacols)
        

        name_dia = PCANameDia(self.root, self.data_obj)
        if name_dia.userCancelled() == True:
            return
        name = name_dia.anal_name
        # create pca data object
        print(self.data_obj.get_matrix(self.pcacols))
        print("final",pcacols_dia.var.get())
        if pcacols_dia.var.get()==0:
            dobj = analysis.pca(self.data_obj, self.pcacols, False)
        else:
            dobj = analysis.pca(self.data_obj, self.pcacols, True)

        # list box
        self.pcalistbox.insert(tk.END, name)

        self.pcanamelst.append(name)
        self.pcadobjlst.append(dobj)

        print("analysis name list: ", self.pcanamelst)


    def deletepca(self):
        if self.pcanamelst == []:
            tk.messagebox.showinfo("Alert!","Empty!")
        an_ind = self.pcalistbox.curselection()[0]
        print(an_ind)
        self.pcalistbox.delete(an_ind)
        self.pcanamelst.pop(an_ind)
        self.pcadobjlst.pop(an_ind)


    # Plot PCA Button
    # Choose Axes
    def handleplotPCA(self):
        self.clearData()
        if self.infopts != None:
            self.clearData_info()
        if self.pcanamelst == []:
            tk.messagebox.showinfo("Alert!","Please Create a PCA Analysis First :)")
            return

        if self.pcalistbox.curselection() == ():
            tk.messagebox.showinfo("Alert!","Please Select One Analysis :)")
            return

        an_ind = self.pcalistbox.curselection()[0]

        self.plotpca_dobj = self.pcadobjlst[an_ind]

        self.plotpca_dia = PlotPCADialog(self.root, self.plotpca_dobj)

        if self.plotpca_dia.userCancelled() == True:
            return

        # column selection
        ind = self.plotpca_dia.x_selection[0]
        x = self.plotpca_dobj.numeric[ind]

        ind = self.plotpca_dia.y_selection[0]
        y = self.plotpca_dobj.numeric[ind]

        ind = self.plotpca_dia.z_selection[0]
        z = self.plotpca_dobj.numeric[ind]
        
        if self.plotpca_dia.color_selection == ():
            color = self.plotpca_dobj.numeric[ind]
        else:
            ind = self.plotpca_dia.color_selection[0]
            color = self.plotpca_dobj.numeric[ind]
            self.color_label = color

        if self.plotpca_dia.size_selection == ():
            size = self.plotpca_dobj.numeric[ind]
        else:
            ind = self.plotpca_dia.size_selection[0]
            size = self.plotpca_dobj.numeric[ind]
            self.size_label = size

        plot_cols = [x, y, z, color, size]
        print([x, y, z, color, size])

        self.clearData()
        self.buildPCAPoints( plot_cols )
        self.updateAxes()


    def buildPCAPoints(self, plot_cols):
        # Delete any existing canvas objects used for plotting data.
        self.clearData()

        # If you are selecting only 2 columns to plot, add a column of 0's (z-value) 
        # and a column of 1's (homogeneous coordinate) to the data.
        xyz = [plot_cols[0], plot_cols[1], plot_cols[2]]
        self.datamatrix = analysis.normalize_columns_separately(xyz, self.plotpca_dobj)
        
        self.size_list = analysis.normalize_columns_separately([plot_cols[4]], self.plotpca_dobj)

        self.color_list = analysis.normalize_columns_separately([plot_cols[3]], self.plotpca_dobj)
        
        self.x_label = xyz[0]
        self.y_label = xyz[1]
        self.z_label = xyz[2]

        n,m = self.datamatrix.shape
        ones = np.ones((n, 1))
        self.datamatrix = np.hstack((self.datamatrix, ones))
        self.build_miniwin()

        vtm = self.vobj.build()
        pts = vtm * self.datamatrix.T
        pts = pts.T
        for i in range(pts.shape[0]):
            x = pts[i, 0]
            y = pts[i, 1]
            
            dx = float(self.size_list[i])*2+1
            
            rgb = (0, int((1-float(self.color_list[i]))*255), int(float(self.color_list[i])*255))
            color = f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
            if self.texture_selection.get() == "Solid":
                pt = self.canvas.create_oval( x-dx, y-dx, x+dx, y+dx, fill = color, outline="")
            elif self.texture_selection.get() == "Outline":
                pt = self.canvas.create_oval( x-dx, y-dx, x+dx, y+dx, fill="", outline=color)
            else:
                pt = self.canvas.create_oval( x-dx, y-dx, x+dx, y+dx, fill = color, outline="")
            self.objects.append(pt)    

    #############
    # Extension #
    def writePCAtoCSV(self):
        if self.plotpca_dobj == None:
            tk.messagebox.showinfo("Alert!", "Please plot one PCA first!")
            return

        row1 = ["E-vec"]
        for h in self.plotpca_dobj.get_headers():
            row1.append(h)
        myFile = open('PCAoutput.csv', 'w')
        row1 = [row1]

        row2 = ["E-val"]
        sum = 0
        for v in self.plotpca_dobj.get_eigenvalues():
            row2.append(v)
            sum = sum + v
        row2 = [row2]
        print("eigvec",row2)

        perc = 0
        row3 = ["Cumulative"]
        for v in self.plotpca_dobj.get_eigenvalues():
            perc = perc + v/sum
            row3.append(perc)
        row3 = [row3]

        with myFile:
            writer = csv.writer(myFile)
            writer.writerows(row1)
            writer.writerows(row2)
            writer.writerows(row3)

            i = 0
            eigvec = self.plotpca_dobj.get_eigenvectors()
            print(eigvec)
            for h in self.plotpca_dobj.get_original_headers():
                row = []
                row.append(h)
                for c in range(len(eigvec)):
                    row.append(eigvec.item(i,c))
                    print("c,i:",c,i)
                i = i+1
                
                writer.writerows([row])


        
        


    def showpcastats(self):
        ind = self.pcalistbox.curselection()[0]
        dobj = self.pcadobjlst[ind]
        dia = PCAStatsDia(self.root, dobj)


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
        self.status_scale = tk.Label(self.canvas, text = "Scaling: 1.00x").grid(row=0, padx =self.initDx/4, pady = self.initDy-100)
        self.status_rotation = tk.Label(self.root, text = "Rotation-- Angle1:  0.00, Angle2: 0.00").grid(row=1,  pady = self.initDy-100)
        self.x_label = None
        self.y_label = None
        self.z_label = None
        self.color_label = None
        self.size_label = None
        self.updateAxes()
        self.updatePoints()
        self.hasHistogram = False


    def widget_under_mouse(self, root):
        x,y = root.winfo_pointerxy()
        widget = root.winfo_containing(x,y)
        return widget


    def capture(self):
        if self.data_obj == None:
            tk.messagebox.showinfo("Alert!","Please create a plot first")
            return
        filenamed = FNDialog(self.root, self.data_obj)
        if self.linregress_dialog.userCancelled() == True:
            return
        fn = filenamed.filename
        print(fn)
        capture = self.canvas.postscript(file = fn)
        
        print("Capture generated")


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

        delta0 = -delta0
        delta1 = -delta1
        d0 = "%.2f" % delta0
        d1 = "%.2f" % delta1
        s = "Rotation -- " + "Angle1: " + d0 + ", " + "Angle2: " + d1
        self.status_rotation = tk.Label(self.root, text = s).grid(row=1,  pady = self.initDy-100)
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
        self.status_scale = tk.Label(self.canvas, text = s).grid(row=0, padx =self.initDx/4, pady = self.initDy-100)


    def clearData(self, event=None):
        for obj in self.objects:
            self.canvas.delete(obj)
        for obj in self.linregress_lines:
            self.canvas.delete(obj)
        for obj in self.multiregress_lines:
            self.canvas.delete(obj)
        for obj in self.axesticks:
            self.canvas.delete(obj)
        if len(self.lineobjs)>6:
            self.canvas.delete(self.lineobjs[6])
        if len(self.lineobjs)>7:
            self.canvas.delete(self.lineobjs[7])
        self.objects = []
        self.linregress_lines = []
        self.multiregress_lines = []
        self.axesticks = []
        self.xmin = None
        self.xmax = None
        self.ymin = None 
        self.ymax = None
        self.zmin = None 
        self.zmax = None
        if self.eqlabel != None:
            self.eqlabel.config(text="")


    def clearData_info(self, event=None):
        for obj in self.infopts:
            self.infocanvas.delete(obj)
        self.infopts = []


    def yzaxes(self, event):
        self.vobj.vpn = np.matrix([1,0,0])
        self.u = np.matrix([0,1,0])
        self.updateAxes()
        self.updatePoints()


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


class LinearRegressionDialog(Dialog):
    def __init__(self, master, dobj):
        Dialog.__init__(self, master, dobj)
        self.cancel = False

    def body(self, master, dobj):
        var_dep = tk.Label(master, text="Dependent Variable:")
        var_dep.pack(side=tk.LEFT)

        self.dep_listbox = tk.Listbox(master, height = len(dobj.numeric),  exportselection = 0)
        for header in dobj.numeric:
            self.dep_listbox.insert(tk.END, header)
        self.dep_listbox.pack(side = tk.LEFT)

        var_ind = tk.Label(master, text="Independent Variable:")
        var_ind.pack(side=tk.LEFT)

        self.ind_listbox = tk.Listbox(master, height = len(dobj.numeric),  exportselection = 0)
        for header in dobj.numeric:
            self.ind_listbox.insert(tk.END, header)
        self.ind_listbox.pack(side = tk.LEFT)

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
        self.ind_selection = self.ind_listbox.curselection()
        self.dep_selection = self.dep_listbox.curselection()
        self.color_selection = self.color_listbox.curselection()
        self.size_selection = self.size_listbox.curselection()
        self.ok = True


    def userCancelled(self):
        if self.ok == True:
            return False
        return True


class MultiRegressionDialog(Dialog):
    def __init__(self, master, dobj):
        Dialog.__init__(self, master, dobj)
        self.cancel = False

    def body(self, master, dobj):
        var_dep = tk.Label(master, text="Dependent Variable:")
        var_dep.pack(side=tk.LEFT)

        self.dep_listbox = tk.Listbox(master, height = len(dobj.numeric),  exportselection = 0)
        for header in dobj.numeric:
            self.dep_listbox.insert(tk.END, header)
        self.dep_listbox.pack(side = tk.LEFT)

        var_ind = tk.Label(master, text="Independent Variables:")
        var_ind.pack(side=tk.LEFT)

        self.ind_listbox = tk.Listbox(master, height = len(dobj.numeric),  exportselection = 0, selectmode = "multiple")
        for header in dobj.numeric:
            self.ind_listbox.insert(tk.END, header)
        self.ind_listbox.pack(side = tk.LEFT)

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
        self.ind_selection = self.ind_listbox.curselection()
        self.dep_selection = self.dep_listbox.curselection()
        self.color_selection = self.color_listbox.curselection()
        self.size_selection = self.size_listbox.curselection()
        self.ok = True


    def userCancelled(self):
        if self.ok == True:
            return False
        return True


class FNDialog(Dialog):
    def __init__(self, parent, dobj):
        Dialog.__init__(self, parent, dobj)
        # self.cancel = False     # the field indicates if the user hit cancel
        # self.ok = False


    def body(self, master, dobj):
        l = tk.Label(master, text = "File name: ").grid(row = 0)
        self.beginValue = tk.StringVar()
        self.beginValue.set("Capture.ps")
        self.entry = tk.Entry(master, textvariable = self.beginValue)
        self.entry.select_range(0, 7)
        self.entry.grid(row=0, column=1)
        self.entry.focus_set()


    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()
        self.cancel = True

    def apply(self):
        self.filename = self.entry.get()
        self.ok = True

    def numPoints_accessor(self):
        return self.numPoints

    def userCancelled(self):
        if self.ok == True:
            return False
        return True


class PCADialog(Dialog):
    def __init__(self, master, dobj):
        Dialog.__init__(self, master, dobj)
        self.cancel = False
        self.click_norm = False
    
    def body(self, master, dobj):
        pca_cols = tk.Label(master, text="PCA Columns:")
        pca_cols.pack(side=tk.TOP)
        
        self.pca_listbox = tk.Listbox(master, height = len(dobj.numeric),  exportselection = 0, selectmode = "multiple")
        for header in dobj.numeric:
            self.pca_listbox.insert(tk.END, header)
        self.pca_listbox.pack(side = tk.TOP)
        
        self.var = tk.IntVar()
        norm_box = tk.Checkbutton(master, text = "normalize", command = self.check_click, variable = self.var)
        norm_box.pack(side=tk.TOP)



    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()
        self.cancel = True

    def check_click(self):
        if self.var.get() == 1:
            self.click_norm = True
        else:
            self.click_norm = False
        print("check click", self.click_norm)


    def apply(self):
        self.pca_lb_selection = self.pca_listbox.curselection()
        #self.check_click()
        self.ok = True
    
    
    
    def userCancelled(self):
        if self.ok == True:
            return False
        return True


class PCANameDia(Dialog):
    def __init__(self, parent, dobj):
        Dialog.__init__(self, parent, dobj)
    
    def body(self, master, dobj):
        l = tk.Label(master, text = "PCA analysis name: ").grid(row = 0)
        self.beginValue = tk.StringVar()
        self.beginValue.set("Analysis")
        self.entry = tk.Entry(master, textvariable = self.beginValue)
        self.entry.select_range(0, tk.END)
        self.entry.grid(row=0, column=1)
        self.entry.focus_set()
    
    
    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()
        self.cancel = True
    
    def apply(self):
        self.anal_name = self.entry.get()
        self.ok = True
    
    def numPoints_accessor(self):
        return self.numPoints
    
    def userCancelled(self):
        if self.ok == True:
            return False
        return True


class PlotPCADialog(Dialog):
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
        if self.x_selection == () or self.y_selection == () or self.z_selection==():
            tk.messagebox.showinfo("Alert!", "Please Select X-Y-Z Dimensions")
            return
        #if self.x_selection == () or self.y_selection == () or self.z_selection==() or self.color_selection==() or self.size_selection==():
            #tk.messagebox.showinfo("Alert!", "Please Select ALL Five Dimensions")
            #return
        self.ok = True


    def userCancelled(self):
        if self.ok == True:
            return False
        return True


class PCAStatsDia(Dialog):

    def __init__(self, parent, data):
        self.data = data
        Dialog.__init__(self, parent, data)

    def body(self, parent, data):
        
        frame = tk.Frame(self)
        frame.pack(side=tk.TOP)

        tk.Label(frame, text="E-vec", borderwidth=3).grid(row = 0, column = 0)
        rh = 1
        for h in self.data.get_headers():
            tk.Label(frame, text=h, borderwidth=3).grid(row=rh, column=0)
            rh += 1

        tk.Label(frame, text = "E-val", borderwidth=3).grid(row = 0, column = 1)
        rv = 1
        sum = 0
        for v in self.data.get_eigenvalues():
            sum += v
            tk.Label(frame, text=str('%.4f' % v), borderwidth=3).grid(row=rv, column=1)
            rv += 1

        rc = 1
        percentSum = 0
        tk.Label(frame, text="Cumulative", borderwidth=3).grid(row=0, column=2)
        for v in self.data.get_eigenvalues():
            percentSum += v/sum
            tk.Label(frame, text=str('%.4f' % percentSum), borderwidth=2).grid(row=rc, column=2)
            rc += 1

        ch = 3
        for h in self.data.get_original_headers():
            tk.Label(frame, text=h, borderwidth=3).grid(row=0, column=ch)
            ch += 1
        eigvec = self.data.get_eigenvectors()
        for r in range(0, len(eigvec)):
            for c in range(len(self.data.get_eigenvectors())):
                tk.Label(frame, text=str('%.4f' % eigvec.item(r,c)), borderwidth=2).grid(row=r+1, column=c+3)


if __name__ == "__main__":
    dapp = DisplayApp(1024, 768)
    dapp.main()


