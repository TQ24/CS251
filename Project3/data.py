# CS251 Project3
# Data Management
# Tracy Quan
# Data.py

import sys
import csv
import numpy
import time
import pandas as pd


class Data:

    # constructor
    def __init__(self, filename=None):
        # create and initialize fields for the class
        self.filename = filename
        self.headers = []
        self.types = []
        self.NumPy = []
        self.cols = 0
        if filename!=None:
            self.read(filename)

    # read the file and put data into matrix
    def read(self, filename):
        fp = open(self.filename, 'rU')
        if '.csv' in filename:
            file_reader = csv.reader(fp)
        elif '.xls' in filename:
            file_reader = pd.read_excel(fp)
        line = next(file_reader)
        for header in line:
            self.headers.append(header.strip())
        line = next(file_reader)
        for typer in line:
            self.types.append(typer.strip())

        # a list of list
        for line in file_reader:
            sublist = []
            for data in line:
                dict = {'Colby': 1, 'Bowdoin': 2, 'Bates': 3}
                # Store a non-numeric column separately, possibly as the string that was read.
                index = line.index(data)
                if self.types[index]=='numeric':
                    sublist.append(float(data))
                # extension 1
                elif self.types[index]=='enum':
                    if data in dict:
                        sublist.append(dict[data])
                elif self.types[index]=='date':
                    #print(data)
                    # extension2
                    try:
                        struct_time = time.strptime(data, "%m/%d/%y")
                    except:
                        pass
                    try:
                        struct_time = time.strptime(data, "%d %b %y")
                    except:
                        pass
                    try:
                        struct_time = time.strptime(data, "%d %B %Y")
                    except:
                        pass
                    try:
                        struct_time = time.strptime(data, "%d-%b-%y")
                    except:
                        pass
                    string = str(struct_time[0])+str(struct_time[1])+str(struct_time[2])
                    sublist.append(float(string))
            self.NumPy.append(sublist)

        self.NumPyMatrix = numpy.matrix(self.NumPy)
        self.dimensions = self.NumPyMatrix.shape # return a tuple (rows,cols)

        # header2col dictionary
        self.header2col = {}
        self.col = len(self.headers)
        for i in range(self.col):
            h = self.headers[i]
            t = self.types[i]
            h.strip()
            t.strip()
            self.header2col[h]=t

        self.numeric = []
        for header in self.headers:
            if self.get_type(header)=='numeric':
                self.numeric.append(header)

    # return filename
    def get_filename(self):
        return self.filename

    # return a list of header
    def get_headers(self):
        return self.headers

    # return a list of type
    def get_types(self):
        return self.types

    # return # of columns
    def get_num_dimensions(self):
        return self.dimensions[1]

    # return # of rows
    def get_num_points(self):
        return self.dimensions[0]

    # return a specific row
    def get_row(self, rowIndex):
        return self.NumPyMatrix[rowIndex]

    # return the value of given header and rowIndex
    def get_value(self, header, rowIndex):
        col_index = 0
        keylist = list(self.header2col.keys())
        for i in range(len(self.header2col)):
            if keylist[i] == header:
                col_index = i
        return self.NumPyMatrix[rowIndex, col_index]

    # return the corresponding type of the given header
    def get_type(self, header):
        return self.header2col[header]

    # takes in a list of columns headers and return a Numpy matrix
    # with the data for all rows but just the specified columns.
    def get_matrix(self, h):
        column_list = []
        for header in self.headers:
            if header in h:
                for i in range(self.dimensions[1]):
                    if self.headers[i] == header:
                        column_list.append(self.NumPyMatrix[:, i])
        return numpy.hstack(column_list)

    # return the list of header with numeric datatype
    def get_numericheaders(self):
        return self.numeric

    # return the entire matrix
    def get_whole_matrix(self):
        return self.NumPyMatrix

    # take header, type, data (a list)
    def add_colummn(self, header, typer, data):
        # add the new header and type into the field
        if len(data)!= self.dimensions[0]:
            return
        self.headers.append(header)
        self.types.append(typer)
        if typer == 'numeric':
            self.numeric.append(typer)
        new_cols = []
        cols = self.dimensions[1]
        m = self.NumPyMatrix
        for i in range(cols):
            ls = m[:,i]
            sublist = []
            for num in ls:
                sublist.append(float(num))
            new_cols.append(sublist)
        new_cols.append(data)
        new_matrix = numpy.column_stack(new_cols)
        self.dimensions = new_matrix.shape
        self.NumPyMatrix = new_matrix


