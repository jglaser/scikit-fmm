from __future__ import division
import numpy as np
import pylab as plt
from sys import float_info
from scipy.optimize import fsolve,root
from .tricubic_interpolation import TriCubicInterp,wrap
from .tricubic_arithmetic_expressions import *

# redefining here to avoid cylic import
FAR, NARROW, FROZEN, MASK = 0, 1, 2, 3
DISTANCE, TRAVEL_TIME, EXTENSION_VELOCITY = 0, 1, 2

class cross_term(object):
    def __init__(self, interp, b0, b1, b2, h):
        self.b0, self.b1, self.b2 = b0, b1, b2
        self.h = h
        self.interp = interp

class cross0(cross_term):
    def __call__(self,p):
        a,cell,d = self.interp.get_coeff_point(p)
        lower0, lower1, lower2 = cell*self.h
        h0, h1, h2 = self.h
        b0, b1, b2 = self.b0, self.b1, self.b2
        c0, c1, c2 = d

        return tricubic_cr0(a,b0,b1,b2,h0,h1,h2,c0,c1,c2,lower0,lower1,lower2)

class cross1(cross_term):
    def __call__(self,p):
        a,cell,d = self.interp.get_coeff_point(p)
        lower0, lower1, lower2 = cell*self.h
        h0, h1, h2 = self.h
        b0, b1, b2 = self.b0, self.b1, self.b2
        c0, c1, c2 = d

        return tricubic_cr1(a,b0,b1,b2,h0,h1,h2,c0,c1,c2,lower0,lower1,lower2)

class cross2(cross_term):
    def __call__(self,p):
        a,cell,d = self.interp.get_coeff_point(p)
        lower0, lower1, lower2 = cell*self.h
        h0, h1, h2 = self.h
        b0, b1, b2 = self.b0, self.b1, self.b2
        c0, c1, c2 = d

        return tricubic_cr2(a,b0,b1,b2,h0,h1,h2,c0,c1,c2,lower0,lower1,lower2)

class jacobian(object):
    def __init__(self, interp, b0, b1, b2, h):
        self.interp = interp
        self.b0, self.b1, self.b2 = b0, b1, b2
        self.h = h

    def __call__(self,p):
        a,cell,d = self.interp.get_coeff_point(p)
        lower0, lower1, lower2 = cell*self.h
        h0, h1, h2 = self.h
        b0, b1, b2 = self.b0, self.b1, self.b2
        c0, c1, c2 = d

        df0dx = tricubic_df0dx(a,b0,b1,b2,h0,h1,h2,c0,c1,c2,lower0,lower1,lower2)
        df0dy = tricubic_df0dy(a,b0,b1,b2,h0,h1,h2,c0,c1,c2,lower0,lower1,lower2)
        df0dz = tricubic_df0dz(a,b0,b1,b2,h0,h1,h2,c0,c1,c2,lower0,lower1,lower2)
        df1dx = tricubic_df1dx(a,b0,b1,b2,h0,h1,h2,c0,c1,c2,lower0,lower1,lower2)
        df1dy = tricubic_df1dy(a,b0,b1,b2,h0,h1,h2,c0,c1,c2,lower0,lower1,lower2)
        df1dz = tricubic_df1dz(a,b0,b1,b2,h0,h1,h2,c0,c1,c2,lower0,lower1,lower2)
        df2dx = tricubic_df2dx(a,b0,b1,b2,h0,h1,h2,c0,c1,c2,lower0,lower1,lower2)
        df2dy = tricubic_df2dy(a,b0,b1,b2,h0,h1,h2,c0,c1,c2,lower0,lower1,lower2)
        df2dz = tricubic_df2dz(a,b0,b1,b2,h0,h1,h2,c0,c1,c2,lower0,lower1,lower2)
        return ((df0dx,df0dy,df0dz),(df1dx,df1dy,df1dz),(df2dx,df2dy,df2dz))


class TriCubicInit(object):
    def __init__(self, phi, flag, speed=None, ext_mask=None, h=(1,1,1), periodic=(False,False,False), seed=123, mode=DISTANCE):
        self.phi = phi
        self.flag = flag
        self.interp = TriCubicInterp(phi,h,periodic)
        self.d = np.ones_like(phi)*float_info.max
        self.pdict = {}
        self.h=h
        self.periodic = periodic
        self.mode = mode
        self.find_frozen()

        if seed is not None:
            np.random.seed(int(seed))

        self.process_points()

        if mode == EXTENSION_VELOCITY:
            self.speed = speed
            self.ext_mask = ext_mask
            self.f_ext = np.ones_like(phi)*float_info.max
            self.extension_velocities()

    def find_frozen(self):
        phi = self.phi
        flag = self.flag

        aborders = np.zeros_like(phi,dtype=bool) # point border
        zeroset = np.logical_and(phi==0.0,flag != MASK)
        aborders[zeroset] = True
        self.d[zeroset] = 0.0

        # cell border
        border_cells = np.zeros_like(phi, dtype=bool)[:-1,:-1,:-1]
        x, y, z = phi.shape

        xmin = 1 if not self.periodic[0] else 0
        ymin = 1 if not self.periodic[1] else 0
        zmin = 1 if not self.periodic[2] else 0
        xmax = x-1 if not self.periodic[0] else x
        ymax = y-1 if not self.periodic[1] else y
        zmax = z-1 if not self.periodic[2] else z

        for i in range(xmin,xmax):
            for j in range(ymin,ymax):
                for k in range(zmin,zmax):
                    for dx in [-1,0,1]:
                        for dy in [-1,0,1]:
                            for dz in [-1,0,1]:
                                ni,nj,nk = wrap(i+dx,j+dy,k+dz,x,y,z,self.periodic)
                                if flag[i,j,k] != MASK and flag[ni,nj,nk] != MASK:
                                    if phi[i,j,k] * phi[ni,nj,nk] < 0:
                                        aborders[i,j,k] = True

        self.aborders = aborders
        self.border_cells = border_cells

    def process_points(self):
        for i in range(self.phi.shape[0]):
            for j in range(self.phi.shape[0]):
                for k in range(self.phi.shape[0]):
                    if self.aborders[i,j,k]:
                        self.process_point(i,j,k)

    def process_point(self,i,j,k):
        # coordinates of this grid point
        x0,y0,z0 = i*self.h[0], j*self.h[1], k*self.h[2]

        cr0 = cross0(self.interp,x0,y0,z0,self.h)
        cr1 = cross1(self.interp,x0,y0,z0,self.h)
        cr2 = cross2(self.interp,x0,y0,z0,self.h)
        fprime = jacobian(self.interp,x0,y0,z0,self.h)
        def eqn(p):
            # the point we want is on the zero level set
            # and perpendicular to the contours of distance from the gp [Chopp 2001, Eqs. 3.2 & 3.3]
            # this splitting is arbitrary
            cr0p,cr1p,cr2p = cr0(p),cr1(p),cr2(p)
            return cr0p*cr0p+cr1p*cr1p,cr2(p), self.interp(p)

        max_attempt = 3
        has_converged = False
        success = False
        n = 0
        while not success and n < max_attempt:
            # symmetric random initial guess
            # this could be improved by looking at where the neighbor with opposite sign is
            dx0,dy0,dz0= self.h*(np.random.rand(3)-0.5)
            sol, info, ierr, mesg = fsolve(eqn, x0=(x0+dx0,y0+dy0,z0+dz0), fprime=fprime, full_output=1)
            #sol, info, ierr, mesg = fsolve(eqn, x0=(x0+dx0,y0+dy0,z0+dz0), full_output=1)
            success = ierr ==1
            (px,py,pz) = sol

#            sol = root(eqn, x0=(x0+dx0,y0+dy0,z0+dz0), jac=fprime, method='lm')
#            sol = root(eqn, x0=(x0+dx0,y0+dy0,z0+dz0), method='lm')
#            success = sol.success
#            (px,py,pz) = sol.x
            n+=1


        if success:
            dx,dy,dz = px-x0,py-y0,pz-z0

#            print("OK", i,j,k,px,py,pz)

            periodic = self.periodic
            h = self.h
            phi = self.phi

            # fsolve's algorithm may cross multiple images,
            # so just use minimum image with periodic boundaries
            Lx,Ly,Lz = h*phi.shape
            if periodic[0]:
                img = round(dx/Lx)
                dx -= img*Lx
            if periodic[1]:
                img = round(dy/Ly)
                dy -= img*Ly
            if periodic[2]:
                img = round(dz/Lz)
                dz -= img*Lz

            # sanity check, the interface shouldn't be further away than 2*h in each direction
            # for boundary points we need to accept points outside [0,1]
            # everything exceeding this tolerance will be handled by linear interpolation
            rough_tol = 0.01*self.h

            if ((-rough_tol[0]-2*h[0] <= dx <= 2*h[0]+rough_tol[0]) \
                and (-rough_tol[1]-2*h[1] <= dy <= 2*h[1]+rough_tol[1]) \
                and (-rough_tol[2]-2*h[2] <= dz <= 2*h[2]+rough_tol[2])) \
                or (not periodic[0] and (i==0 or i==nx-1)) \
                or (not periodic[1] and (j==0 or j==ny-1)) \
                or (not periodic[2] and (k==0 or k==nz-1)):

                dist = np.sqrt(dx**2 + dy**2 + dz**2)
                if self.d[i,j,k] == float_info.max or self.d[i,j,k] > dist:
                    self.d[i,j,k]=dist
                    self.pdict[(i,j,k)] = (px,py,pz)
                return
            print("{} out of bounds".format((dx,dy,dz)))

        print("failed",i,j,k)
        print(sol)
#        print(ierr, mesg, info)

        # fall back to linear interpolation
        self.aborders[i,j,k] = False

    def extension_velocities(self):
        phi = self.phi
        flag = self.flag
        speed = self.speed
        ext_mask = self.ext_mask
        f_ext = self.f_ext

        speed_interp = TriCubicInterp(speed,self.h,self.periodic)
        zeroset = np.logical_and(phi==0.0,flag != MASK)
        if ext_mask is not None:
            zeroset = np.logical_and(zeroset,ext_mask == 0)
        f_ext[zeroset] = speed[zeroset]

        for (i,j,k) in self.pdict:
            if ext_mask is not None and ext_mask[i,j,k]:
                # fall back to linear interpolation
                continue

            # interpolate
            f_ext[i,j,k] = speed_interp(self.pdict[(i,j,k)])

if __name__ == '__main__':
    X,Y,Z = np.meshgrid(np.linspace(0,15,16),
                        np.linspace(0,15,16),
                        np.linspace(0,15,16))

    phi = np.ones_like(X)
    phi[6,6,6] = -1
    init = TriCubicInit(phi)
