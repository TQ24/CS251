# Tracy Quan
# CS251 Project2
# Extension1&2 test file

import numpy
import sys
import data

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
    print('Number of columns: ', dobj.get_num_dimensions() )

    # print out the headers
    print("\nHeaders:")
    headers = dobj.get_headers()
    s = headers[0]
    for header in headers[1:]:
        s += ", " + header
    print( s )

    # print out the types
    print("Types:")
    types = dobj.get_types()
    s = types[0]
    for type in types[1:]:
        s += ", " + type
    print( s )

    print("------------------------------")

if __name__ == "__main__":
    main()
