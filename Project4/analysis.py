# CS251 Project2
# Data Management
# Tracy Quan
# analysis.py
# All analysis functions will take lists of strings (column headers) to specify what (numeric) data to analyze.

import numpy

# takes a list of column headers and the Data object and returns a list of 2-element lists with
# min and max value for each column.
def data_range(headers, dobj):
    range_list = []
    m = dobj.get_matrix(headers)
    cols = m.shape[1]
    for i in range(cols):
        mini = numpy.amin(m[:,i])
        maxi = numpy.amax(m[:,i])
        sublist = [float(mini), float(maxi)]
        range_list.append(sublist)
    return range_list


# Takes in a list of column headers and the Data object and
# returns a list of the mean values for each column.
def mean(headers, dobj):
    mean_list = []
    m = dobj.get_matrix(headers)
    cols = m.shape[1]
    for i in range(cols):
        #header = dobj.get_headers()[i]
        avg = numpy.mean(m[:, i])
        mean_list.append(avg)
    return mean_list


# Takes in a list of column headers and the Data object and
# returns a list of the standard deviation for each specified column.
def stdev(headers, dobj):
    stdev_list = []
    m = dobj.get_matrix(headers)
    cols = m.shape[1]
    for i in range(cols):
        stdev = numpy.std(m[:,i])
        stdev_list.append(stdev)
    return stdev_list

# Extension7
# Return the sum of the matrix
def sumup(headers, dobj):
    m = dobj.get_matrix(headers)
    a = numpy.asarray(m)
    su = 0
    for ls in a:
        su = su + sum(ls)
    return su

# Extension7
# return the variance of each column
def variance(headers, dobj):
    m = dobj.get_matrix(headers)
    cols = dobj.get_num_dimensions()
    ls = []
    for i in range(cols):
        co = m[:,i]
        va = numpy.var(co)
        ls.append(va)
    return ls

# Takes in a list of column headers and the Data object and returns a matrix with
# each column normalized so its minimum value is mapped to zero and its maximum value is mapped to 1.
def normalize_columns_separately(headers, dobj):
    # Error Check
    for header in headers:
        if dobj.get_type(header) != "numeric":
            print("There are non-numeric columns! ")
            return
    new_matrix = []
    m = dobj.get_matrix(headers)
    cols = m.shape[1]
    rows = m.shape[0]
    column = numpy.ones(rows)
    for i in range(cols):
        mini = numpy.amin(m[:, i])
        extent = numpy.ptp(m[:, i])
        min_col = column * mini 
        min_col = numpy.matrix(min_col)
        #print(m[:,i]-min_col.T)
        col_normed = (m[:,i]-min_col.T)/extent
        new_matrix.append(col_normed)
    return numpy.column_stack(new_matrix)



# Takes in a list of column headers and the Data object and returns a matrix with
# each entry normalized so that the minimum value (of all the data in this set of
# columns) is mapped to zero and its maximum value is mapped to 1.
def normalize_columns_together(headers, dobj):
    for header in headers:
        if dobj.get_type(header) != "numeric":
            print("There are non-numeric columns! ")
            return
    new_matrix = []
    # find the min, max and extent
    m = dobj.get_matrix(headers)
    mini = m.min()
    maxi = m.max()
    extent = maxi-mini
    cols = m.shape[1]
    rows = m.shape[0]
    onescolumn = numpy.ones(rows)
    mini_col = numpy.matrix(onescolumn * mini).T
    for i in range(cols):
        col_normed = (m[:, i]-mini_col)/extent
        new_matrix.append(col_normed)
    return numpy.column_stack(new_matrix)