# Tracy Quan
# CS251 Project 3
# view.py

import numpy
import math

class View:

    def __init__(self):
        self.vrp = numpy.matrix([0.5, 0.5, 1])
        self.vpn = numpy.matrix([0, 0, -1])
        self.vup = numpy.matrix([0, 1, 0])
        self.u = numpy.matrix([-1, 0, 0])
        self.extent = numpy.matrix([1, 1, 1])
        self.screen = numpy.matrix([400, 400])
        self.offset = numpy.matrix([20, 20])

    # reset the View object
    def reset(self):
        self.vrp = numpy.matrix([0.5, 0.5, 1])
        self.vpn = numpy.matrix([0, 0, -1])
        self.vup = numpy.matrix([0, 1, 0])
        self.u = numpy.matrix([-1, 0, 0])
        self.extent = numpy.matrix([1, 1, 1])
        self.screen = numpy.matrix([400, 400])
        self.offset = numpy.matrix([20, 20])

    # uses the current viewing parameters to return a view matrix
    def build(self):
        vtm = numpy.identity(4, float)
        # a translation matrix to move the VRP to the origin
        t1 = numpy.matrix( [[1, 0, 0, -self.vrp[0, 0]],
                    [0, 1, 0, -self.vrp[0, 1]],
                    [0, 0, 1, -self.vrp[0, 2]],
                    [0, 0, 0, 1] ] )
        vtm = t1 * vtm
        # tu is the cross product of vup and vpn vectors
        tu = numpy.cross(self.vup, self.vpn)
        # tvup is the cross product of the vpn and tu vectors.
        tvup = numpy.cross(self.vpn, tu)
        # tvpn is a copy of the vpn vector.
        tvpn = numpy.copy(self.vpn)

        # Normalize the view axes tu, tvup, and tvpn to unit length.
        norm = numpy.linalg.norm(tu)
        tu = tu/norm

        norm = numpy.linalg.norm(tvup)
        tvup = tvup/norm

        norm = numpy.linalg.norm(tvpn)
        tvpn = tvpn/norm


        self.u = numpy.copy(tu)
        self.vup = numpy.copy(tvup)
        self.vpn = numpy.copy(tvpn)

        # align the axes
        r1 = numpy.matrix( [[ tu[0, 0], tu[0, 1], tu[0, 2], 0.0 ],
                    [ tvup[0, 0], tvup[0, 1], tvup[0, 2], 0.0 ],
                    [ tvpn[0, 0], tvpn[0, 1], tvpn[0, 2], 0.0 ],
                    [ 0.0, 0.0, 0.0, 1.0 ] ] )
        vtm = r1 * vtm

        # Translate the lower left corner of the view space to the origin.
        # Since the axes are aligned, this is just a translation by half the
        # extent of the view volume in the X and Y view axes.
        t2 = numpy.matrix( [[1, 0, 0, 0.5*self.extent[0,0]],
                    [0, 1, 0, 0.5*self.extent[0,1]],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1] ] )
        vtm = t2 * vtm

        # Use the extent and screen size values to scale to the screen.
        s1 = numpy.matrix([[-self.screen[0,0]/self.extent[0,0], 0, 0, 0],
                    [0, -self.screen[0,1]/self.extent[0,1], 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1] ])
        vtm = s1 * vtm

        # translate the lower left corner to the origin and add the view offset
        t3 = numpy.matrix( [ [1, 0, 0, self.screen[0,0]+self.offset[0,0]] ,
                    [ 0, 1, 0, self.screen[0,1]+self.offset[0,1]],
                    [ 0, 0, 1, 0 ],
                    [ 0.0, 0.0, 0.0, 1.0]] )
        vtm = t3 * vtm
        return vtm

    # makes a duplicate View object and returns it
    def clone(self):
        new_obj = View()
        new_obj.vrp = self.vrp
        new_obj.vpn = self.vpn
        new_obj.vup = self.vup
        new_obj.u = self.u
        new_obj.extent = self.extent
        new_obj.screen = self.screen
        new_obj.offset = self.offset

        return new_obj

    # rotates about vrp
    def rotateVRC(self, angle_vup, angle_u):

        pt = self.vrp + self.vpn * self.extent[0,2] * 0.5
        # Make a translation matrix to move the point ( VRP + VPN * extent[Z] * 0.5 ) to the origin. Put it in t1.
        t1 = numpy.matrix( [[ 1, 0, 0, pt[0,0] ],
                           [ 0, 1, 0, pt[0,1]],
                           [ 0, 0, 1, pt[0,2]],
                           [ 0, 0, 0, 1 ] ] )


        # Make an axis alignment matrix Rxyz using u, vup and vpn.
        Rxyz = numpy.matrix( [[ self.u[0,0], self.u[0,1], self.u[0,2], 0 ],
                             [ self.vup[0,0], self.vup[0,1], self.vup[0,2], 0 ],
                             [ self.vpn[0,0], self.vpn[0,1], self.vpn[0,2], 0 ],
                             [ 0, 0, 0, 1 ] ] )

        # Make a rotation matrix about the Y axis by the VUP angle, put it in r1.
        r1 = numpy.matrix( [[ math.cos(angle_vup), 0, math.sin(angle_vup), 0 ],
                           [ 0, 1, 0, 0 ],
                           [ -math.sin(angle_vup), 0, math.cos(angle_vup), 0 ],
                           [ 0, 0, 0, 1 ] ] )

        # Make a rotation matrix about the X axis by the U angle. Put it in r2.
        r2 = numpy.matrix( [[ 1, 0, 0, 0 ],
                           [ 0, math.cos(angle_u), -math.sin(angle_u), 0 ],
                           [ 0, math.sin(angle_u), math.cos(angle_u), 0 ],
                           [ 0, 0, 0, 1 ] ] )

        # Make a translation matrix that has the opposite translation from step 1.
        t2 = numpy.matrix( [[ 1, 0, 0, -pt[0,0] ],
                           [ 0, 1, 0, -pt[0,1]],
                           [ 0, 0, 1, -pt[0,2]],
                           [ 0, 0, 0, 1 ] ] )

        # Make a numpy matrix where the VRP is on the first row, with a 1 in the homogeneous coordinate, and u, vup, and vpn are the next three rows, with a 0 in the homogeneous coordinate.
        tvrc = numpy.matrix( [[ self.vrp[0,0], self.vrp[0,1], self.vrp[0,2], 1 ],
                              [ self.u[0,0], self.u[0,1], self.u[0,2], 0 ],
                              [ self.vup[0,0], self.vup[0,1], self.vup[0,2], 0 ],
                              [ self.vpn[0,0], self.vpn[0,1], self.vpn[0,2], 0]])

        # Execute the following: tvrc = (t2*Rxyz.T*r2*r1*Rxyz*t1*tvrc.T).T
        tvrc = (t2*Rxyz.T*r2*r1*Rxyz*t1*tvrc.T).T

        # normalize new vrp
        tvrp = numpy.matrix([tvrc[0,0], tvrc[0,1], tvrc[0,2]])
        self.vrp = tvrp

        # normalize new u
        tu = numpy.matrix([tvrc[1,0], tvrc[1,1], tvrc[1,2]])
        self.u = tu

        # normalize new vup
        tvup = numpy.matrix([tvrc[2,0], tvrc[2,1], tvrc[2,2]])
        self.vup = tvup

        # normalize new vpn
        tvpn = numpy.matrix([tvrc[3,0], tvrc[3,1], tvrc[3,2]])
        self.vpn = tvpn



if __name__ == '__main__':
    view = View()
    new_view = view.clone()
    print(view.build())
    print(new_view.clone().build())
    print("Screen size:", view.screen)
    print("Extent:", view.get_extent())
