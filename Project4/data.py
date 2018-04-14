# CS251 Project2
# Data Management
# Tracy Quan
# Data.py

import sys
import csv
import numpy
import analysis
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
        self.numeric = []
        if filename!=None:
            self.read(filename)

    # read the file and put data into matrix
    def read(self, filename):
        fp = open(self.filename, 'rU')
        file_reader = csv.reader(fp)
        line = next(file_reader)
        for header in line:
            self.headers.append(header.strip())
        line = next(file_reader)
        for typer in line:
            self.types.append(typer.strip())
        print(self.types)
        self.numeric_matrix = []
        # a list of list
        for line in file_reader:
            sublist = []
            numeric_m = []
            print("line", len(line))
            count = 0
            for i in range(len(line)):
                # Store a non-numeric column separately, possibly as the string that was read.
                #index = line.index(data)
                #print(index)
                if self.types[i]=='numeric':
                    sublist.append(float(line[i]))
                    numeric_m.append(float(line[i]))
                    #count = count+1
                else:
                    sublist.append(line[i])
            self.NumPy.append(sublist)
            print("length", len(numeric_m))
            print("sublist length", len(sublist))
            self.numeric_matrix.append(numeric_m)
            #print(sublist)
        self.NumPyMatrix = numpy.matrix(self.NumPy)
        self.dimensions = self.NumPyMatrix.shape # return a tuple (rows,cols)
        self.numeric_matrix = numpy.matrix(self.numeric_matrix)

        print("-----------------------\n--------------------------")
        #print(self.numeric_matrix)
        print("-----------------------\n--------------------------")

        # header2col dictionary
        self.header2col = {}
        self.col = len(self.headers)
        for i in range(self.col):
            h = self.headers[i]
            t = self.types[i]
            h.strip()
            t.strip()
            self.header2col[h]=t
        # numeric header
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
        for header in h:
            if header in self.numeric:
                for i in range(self.numeric_matrix.shape[1]):
                    if header == self.numeric[i]:
                        column_list.append(self.numeric_matrix[:,i])
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



if __name__ == "__main__":
    numpy.set_printoptions(suppress=True)
    print("\n----- Database Info -----")
    if len(sys.argv) < 2:
        print( 'Usage: python %s <csv filename>' % (sys.argv[0]))
        exit(0)

    # create a data object, which reads in the data
    dobj = Data(sys.argv[1])
    print("\nName: ",dobj.get_filename())
    # print out information about the dat
    print('Number of rows:    ', dobj.get_num_points() )
    print('Number of numeric columns: ', dobj.get_num_dimensions() )

    # print out the headers
    print("\nHeaders:")
    headers = dobj.get_headers()
    s = headers[0]
    for header in headers[1:]:
        s += ", " + header
    print( s )

    # print out the headers
    print("\nNumeric Headers:")
    nheaders = dobj.get_numericheaders()
    s = nheaders[0]
    for header in nheaders[1:]:
        s += ", " + header
    print( s )

    print("\nNumeric Matrix:")
    print(dobj.numeric_matrix)

    # print out the types
    print("\nTypes:")
    types = dobj.get_types()
    s = types[0]
    for type in types[1:]:
        s += ", " + type
    print( s )


    r = analysis.data_range(headers, dobj)
    print("Data Range:\n ", r)
    mean = analysis.mean(headers, dobj)
    print("Mean: \n",mean)

    std = analysis.stdev(headers, dobj)
    print("Standard Deviation: \n", std)


    #std = analysis.stdev(headers, dobj)
    #print("Standard Deviation: \n", std)
    
    nor_m1 = analysis.normalize_columns_separately(headers, dobj)
    print("Normalized Columns Separately: \n", nor_m1)

    nor_m2 = analysis.normalize_columns_together(headers, dobj)
    print("Normalized Columns Together: \n", nor_m2)




    #dobj.add_colummn('new col','numeric', [1,2,3,4,5,6,7,8,9,10,11,12,13,14])
    #print("\nAdd new column: 'new col','numeric', [1,2,3,4,5,6,7,8,9,10,11,12,13,14]")
    #print("----- New Matrix: -----")
    #print(dobj.get_whole_matrix())
    print("---------------------------------")
