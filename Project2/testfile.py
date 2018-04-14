# CS251 Project2
# Data Management
# Tracy Quan
# test code

import sys
import data


# test program for the Data class
def main(argv):

    # test command line arguments
    if len(argv) < 2:
        print( 'Usage: python %s <csv filename>' % (argv[0]))
        exit(0)

    # create a data object, which reads in the data
    dobj = data.Data(argv[1])

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
    print("\nTypes")
    types = dobj.get_types()
    s = types[0]
    for type in types[1:]:
        s += ", " + type
    print( s )

    headers = dobj.get_headers()

    #hs = ['headers', 'with']
    hs = ['stringstuff']
    print("Matrix:------")
    matrix = dobj.get_matrix(hs)
    print(matrix)





if __name__ == "__main__":
    main(sys.argv)

