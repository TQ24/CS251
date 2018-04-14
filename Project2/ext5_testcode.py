# Tracy Quan
# CS251 Project2
# Extension5 test file
# Command line: python ext5_testcode.py testdata1.csv

import numpy
import sys
import data
import analysis
import csv

def main():
    numpy.set_printoptions(suppress=True)
    print("\n----- Database Info -----")
    if len(sys.argv) < 2:
        print( 'Usage: python %s <csv filename>' % (sys.argv[0]))
        exit(0)

    # create a data object, which reads in the data
    dobj = data.Data(sys.argv[1])
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
    if headers == nheaders:
        nor_m1 = analysis.normalize_columns_separately(headers, dobj)
        print("Normalized Columns Separately: \n", nor_m1)
    if headers == nheaders:
        nor_m2 = analysis.normalize_columns_together(headers, dobj)
        print("Normalized Columns Together: \n", nor_m2)

    s = analysis.sumup(headers, dobj)
    print("Sum:\n", s)

    print("Variance:\n", analysis.variance(headers, dobj))

    # EXTENSION5 ADD COLUMN
    dobj.add_colummn('new col','numeric', [1,2,3,4,5,6,7,8,9,10,11,12,13,14])
    print("\nAdd new column: 'new col','numeric', [1,2,3,4,5,6,7,8,9,10,11,12,13,14]")
    print("----- New Matrix: -----")
    m = dobj.get_whole_matrix()
    print(m)
    print('Number of rows:    ', dobj.get_num_points() )
    print('Number of numeric columns: ', dobj.get_num_dimensions() )
    print("---------------------------------")

    # EXTENSION6 WRITE TO A CSV file
    a = numpy.asarray(m)
    with open('foo.csv', 'w') as outputfile:
        wr = csv.writer(outputfile,delimiter=',')
        wr.writerow(dobj.get_headers())
        wr.writerow(dobj.get_types())
        for ls in a:
            wr.writerow(ls)

if __name__ == "__main__":
    main()
