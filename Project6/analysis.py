# CS251 Project6
# Data Management
# Tracy Quan
# analysis.py

import numpy
import scipy.stats as stats
import sys
import data


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


# Return the sum of the matrix
def sumup(headers, dobj):
    m = dobj.get_matrix(headers)
    a = numpy.asarray(m)
    su = 0
    for ls in a:
        su = su + sum(ls)
    return su


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


def single_linear_regression( dobj, ind_var, dep_var):
    var_m = dobj.get_matrix([ind_var, dep_var])
    x = numpy.array(var_m[ :,0 ].T)[0]
    y = numpy.array(var_m[ :,1 ].T)[0]
    slope, intercept, r_value, p_value, std_err = stats.linregress( x, y )
    range_ind = data_range( [ind_var], dobj)
    range_dep = data_range( [dep_var], dobj)
    #print(slope, intercept, r_value, p_value, std_err, range_ind[0][0], range_dep[0][0])
    return (slope, intercept, r_value, p_value, std_err, range_ind[0][0], 
            range_ind[0][1], range_dep[0][0], range_dep[0][1])


# takes in the data set, a list of headers for the independent variables, 
# and a single header (not in a list) for the dependent variable
def linear_regression(dobj, ind, dep):
    y = dobj.get_matrix([dep])
    A = dobj.get_matrix(ind)
    n,m = A.shape 
    ones = numpy.ones((n, 1))
    A = numpy.hstack((A, ones))

    AAinv = numpy.linalg.inv( numpy.dot(A.T, A) )
    x = numpy.linalg.lstsq( A, y, rcond=None )
    b = x[0]

    N, M = y.shape
    C, D = b.shape 
    df_e = N-C
    df_r = C-1

    error = y - numpy.dot(A, b)
    sse = numpy.dot(error.T, error) / df_e
    stderr = numpy.sqrt( numpy.diagonal( sse[0,0] * AAinv ) )
    t = b.T / stderr
    p = 2*(1 - stats.t.cdf(abs(t), df_e))
    r2 = 1 - error.var() / y.var()

    x0_range = data_range([ind[0]], dobj)
    x1_range = data_range([ind[1]], dobj)
    y_range = data_range([dep], dobj)
    return (b, float(sse), float(r2), t, p, x0_range, x1_range, y_range)


# This version uses SVD
def pca(dobj, headers, normalize=True):
    
    if normalize == True:
        A = normalize_columns_separately( headers, dobj )
        print(A)
    else:
        A = dobj.get_matrix( headers )

    list = []
    matrix = A.transpose()
    for n in range(0, len(matrix)):
        list.append(numpy.mean(matrix[n].tolist()))
    m = list

    D = A-m

    U,S,V = numpy.linalg.svd(D, full_matrices = False)


    eigenvalues = S*S/(D.shape[0]-1)

    eigenvectors = V
    pdata = (V * D.T).T

    return data.PCAData( pdata, eigenvectors, eigenvalues, m, headers )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print( 'Usage: python %s <csv filename>' % (sys.argv[0]))
        exit(0)
    dobj = data.Data(sys.argv[1])
    ind = ["FG%","3P%"]
    dep = "Win%"
    result = linear_regression(dobj, ind, dep)
    print("---- Regression ----:")
    e = result[0]
    m0 = float(e[0])
    m1 = float(e[1])
    b = float(e[2])
    sse = result[1]
    r2 = result[2]
    t = numpy.asarray(result[3])
    p = numpy.asarray(result[4])
    print("Filename: ", sys.argv[1])
    print("Dependent Var: ", dep)
    print("Independent Var: ", ind)
    print("m0:", "%.3f" % m0, " m1:", "%.3f" % m1, " b:", "%.3f" % b, " sse:", "%.3f" % sse)
    print("R2:", "%.3f" % r2, " t:", t[0], " p:", p[0])
