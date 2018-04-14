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
    cols = dobj.get_num_dimensions()
    for i in range(cols):
        sublist = []
        ls = m[:,i];
        mini = min(ls)
        maxi = max(ls)
        sublist = [float(mini),float(maxi)]
        range_list.append(sublist)
    return range_list

# Takes in a list of column headers and the Data object and
# returns a list of the mean values for each column.
def mean(headers, dobj):
    mean_list = []
    matrix = dobj.get_matrix(headers)
    cols = dobj.get_num_dimensions()
    for i in range(cols):
        header = dobj.get_headers()[i]
        avg = numpy.mean(matrix[:, i])
        mean_list.append(avg)
    return mean_list


# Takes in a list of column headers and the Data object and
# returns a list of the standard deviation for each specified column.
def stdev(headers, dobj):
    stdev_list = []
    matrix = dobj.get_matrix(headers)
    cols = dobj.get_num_dimensions()
    for i in range(cols):
        header = dobj.get_headers()[i]
        stdev = numpy.std(matrix[:,i])
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
    new_matrix = []
    r = data_range(headers, dobj)
    for header in headers:
        min = r[0][0]
        extent = r[0][1]-r[0][0]
        m = dobj.get_matrix(header)
        sublist = []
        for data in m:
            temp = float((data-min)/extent)
            sublist.append(temp)
            #print(sublist)
        new_matrix.append(sublist)
    return numpy.column_stack(new_matrix)

# Takes in a list of column headers and the Data object and returns a matrix with
# each column normalized so its minimum value is mapped to zero and its maximum value is mapped to 1.
def normalize_columns_separately2(headers, dobj):
    new_matrix = []
    for header in headers:
        if dobj.get_type(header) == 'numeric':
            r = data_range(header, dobj)
            print('range',r)
            min = r[0][0]
            extent = r[0][1]-r[0][0]
            m = dobj.get_matrix(header)
            sublist = []
            for data in m:
                temp = float((data-min)/extent)
                sublist.append(temp)
                #print(sublist)
            new_matrix.append(sublist)
    return numpy.column_stack(new_matrix)


# Takes in a list of column headers and the Data object and returns a matrix with
# each entry normalized so that the minimum value (of all the data in this set of
# columns) is mapped to zero and its maximum value is mapped to 1.
def normalize_columns_together(headers, dobj):
    new_matrix = []
    # find the min, max and extent
    range = data_range(headers,dobj)[0]
    min = range[0]
    max = range[1]
    #max = min
    for r in data_range(headers, dobj):
        # min
        if r[0] < min:
            min = r[0]
        elif r[1] > max:
            max = r[1]
    extent = max - min
    for header in headers:
        sublist = []
        m = dobj.get_matrix(header)
        for data in m:
            temp = float((data-min)/extent)
            sublist.append(temp)
        new_matrix.append(sublist)
    return numpy.column_stack(new_matrix)
