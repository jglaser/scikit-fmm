import numpy as np
import pylab as plt
from sys import float_info
from scipy.optimize import fsolve
from .tricubic_interpolation import TriCubicInterp,wrap

class cross_term(object):
    def __init__(self, interp, b0, b1, b2):
        self.b0, self.b1, self.b2 = b0, b1, b2
        self.interp = interp

class cross0(cross_term):
    def __call__(self,p):
        c0,c1,c2 = p

        a = self.interp.get_coeff_point(p)

        b0, b1, b2 = self.b0, self.b1, self.b2
        return -(b1 - c1)*(a[1-1] + 2*a[10-1]*c1**2*c2 + 3*a[11-1]*c1**2*c2**2 + a[13-1]*c1**3 + 2*a[14-1]*c1**3*c2 + 3*a[15-1]*c1**3*c2**2 + a[17-1]*c0 + 2*a[18-1]*c0*c2 + 3*a[19-1]*c0*c2**2 + 2*a[2-1]*c2 + a[21-1]*c0*c1 + 2*a[22-1]*c0*c1*c2 + 3*a[23-1]*c0*c1*c2**2 + a[25-1]*c0*c1**2 + 2*a[26-1]*c0*c1**2*c2 + 3*a[27-1]*c0*c1**2*c2**2 + a[29-1]*c0*c1**3 + 3*a[3-1]*c2**2 + 2*a[30-1]*c0*c1**3*c2 + 3*a[31-1]*c0*c1**3*c2**2 + a[33-1]*c0**2 + 2*a[34-1]*c0**2*c2 + 3*a[35-1]*c0**2*c2**2 + a[37-1]*c0**2*c1 + 2*a[38-1]*c0**2*c1*c2 + 3*a[39-1]*c0**2*c1*c2**2 + a[41-1]*c0**2*c1**2 + 2*a[42-1]*c0**2*c1**2*c2 + 3*a[43-1]*c0**2*c1**2*c2**2 + a[45-1]*c0**2*c1**3 + 2*a[46-1]*c0**2*c1**3*c2 + 3*a[47-1]*c0**2*c1**3*c2**2 + a[49-1]*c0**3 + a[5-1]*c1 + 2*a[50-1]*c0**3*c2 + 3*a[51-1]*c0**3*c2**2 + a[53-1]*c0**3*c1 + 2*a[54-1]*c0**3*c1*c2 + 3*a[55-1]*c0**3*c1*c2**2 + a[57-1]*c0**3*c1**2 + 2*a[58-1]*c0**3*c1**2*c2 + 3*a[59-1]*c0**3*c1**2*c2**2 + 2*a[6-1]*c1*c2 + a[61-1]*c0**3*c1**3 + 2*a[62-1]*c0**3*c1**3*c2 + 3*a[63-1]*c0**3*c1**3*c2**2 + 3*a[7-1]*c1*c2**2 + a[9-1]*c1**2) + (b2 - c2)*(2*a[10-1]*c1*c2**2 + 2*a[11-1]*c1*c2**3 + 3*a[12-1]*c1**2 + 3*a[13-1]*c1**2*c2 + 3*a[14-1]*c1**2*c2**2 + 3*a[15-1]*c1**2*c2**3 + a[20-1]*c0 + a[21-1]*c0*c2 + a[22-1]*c0*c2**2 + a[23-1]*c0*c2**3 + 2*a[24-1]*c0*c1 + 2*a[25-1]*c0*c1*c2 + 2*a[26-1]*c0*c1*c2**2 + 2*a[27-1]*c0*c1*c2**3 + 3*a[28-1]*c0*c1**2 + 3*a[29-1]*c0*c1**2*c2 + 3*a[30-1]*c0*c1**2*c2**2 + 3*a[31-1]*c0*c1**2*c2**3 + a[36-1]*c0**2 + a[37-1]*c0**2*c2 + a[38-1]*c0**2*c2**2 + a[39-1]*c0**2*c2**3 + a[4-1] + 2*a[40-1]*c0**2*c1 + 2*a[41-1]*c0**2*c1*c2 + 2*a[42-1]*c0**2*c1*c2**2 + 2*a[43-1]*c0**2*c1*c2**3 + 3*a[44-1]*c0**2*c1**2 + 3*a[45-1]*c0**2*c1**2*c2 + 3*a[46-1]*c0**2*c1**2*c2**2 + 3*a[47-1]*c0**2*c1**2*c2**3 + a[5-1]*c2 + a[52-1]*c0**3 + a[53-1]*c0**3*c2 + a[54-1]*c0**3*c2**2 + a[55-1]*c0**3*c2**3 + 2*a[56-1]*c0**3*c1 + 2*a[57-1]*c0**3*c1*c2 + 2*a[58-1]*c0**3*c1*c2**2 + 2*a[59-1]*c0**3*c1*c2**3 + a[6-1]*c2**2 + 3*a[60-1]*c0**3*c1**2 + 3*a[61-1]*c0**3*c1**2*c2 + 3*a[62-1]*c0**3*c1**2*c2**2 + 3*a[63-1]*c0**3*c1**2*c2**3 + a[7-1]*c2**3 + 2*a[8-1]*c1 + 2*a[9-1]*c1*c2)

class cross1(cross_term):
    def __call__(self,p):
        c0,c1,c2 = p

        a = self.interp.get_coeff_point(p)

        b0, b1, b2 = self.b0, self.b1, self.b2
        return (b0 - c0)*(a[1-1] + 2*a[10-1]*c1**2*c2 + 3*a[11-1]*c1**2*c2**2 + a[13-1]*c1**3 + 2*a[14-1]*c1**3*c2 + 3*a[15-1]*c1**3*c2**2 + a[17-1]*c0 + 2*a[18-1]*c0*c2 + 3*a[19-1]*c0*c2**2 + 2*a[2-1]*c2 + a[21-1]*c0*c1 + 2*a[22-1]*c0*c1*c2 + 3*a[23-1]*c0*c1*c2**2 + a[25-1]*c0*c1**2 + 2*a[26-1]*c0*c1**2*c2 + 3*a[27-1]*c0*c1**2*c2**2 + a[29-1]*c0*c1**3 + 3*a[3-1]*c2**2 + 2*a[30-1]*c0*c1**3*c2 + 3*a[31-1]*c0*c1**3*c2**2 + a[33-1]*c0**2 + 2*a[34-1]*c0**2*c2 + 3*a[35-1]*c0**2*c2**2 + a[37-1]*c0**2*c1 + 2*a[38-1]*c0**2*c1*c2 + 3*a[39-1]*c0**2*c1*c2**2 + a[41-1]*c0**2*c1**2 + 2*a[42-1]*c0**2*c1**2*c2 + 3*a[43-1]*c0**2*c1**2*c2**2 + a[45-1]*c0**2*c1**3 + 2*a[46-1]*c0**2*c1**3*c2 + 3*a[47-1]*c0**2*c1**3*c2**2 + a[49-1]*c0**3 + a[5-1]*c1 + 2*a[50-1]*c0**3*c2 + 3*a[51-1]*c0**3*c2**2 + a[53-1]*c0**3*c1 + 2*a[54-1]*c0**3*c1*c2 + 3*a[55-1]*c0**3*c1*c2**2 + a[57-1]*c0**3*c1**2 + 2*a[58-1]*c0**3*c1**2*c2 + 3*a[59-1]*c0**3*c1**2*c2**2 + 2*a[6-1]*c1*c2 + a[61-1]*c0**3*c1**3 + 2*a[62-1]*c0**3*c1**3*c2 + 3*a[63-1]*c0**3*c1**3*c2**2 + 3*a[7-1]*c1*c2**2 + a[9-1]*c1**2) - (b2 - c2)*(a[16-1] + a[17-1]*c2 + a[18-1]*c2**2 + a[19-1]*c2**3 + a[20-1]*c1 + a[21-1]*c1*c2 + a[22-1]*c1*c2**2 + a[23-1]*c1*c2**3 + a[24-1]*c1**2 + a[25-1]*c1**2*c2 + a[26-1]*c1**2*c2**2 + a[27-1]*c1**2*c2**3 + a[28-1]*c1**3 + a[29-1]*c1**3*c2 + a[30-1]*c1**3*c2**2 + a[31-1]*c1**3*c2**3 + 2*a[32-1]*c0 + 2*a[33-1]*c0*c2 + 2*a[34-1]*c0*c2**2 + 2*a[35-1]*c0*c2**3 + 2*a[36-1]*c0*c1 + 2*a[37-1]*c0*c1*c2 + 2*a[38-1]*c0*c1*c2**2 + 2*a[39-1]*c0*c1*c2**3 + 2*a[40-1]*c0*c1**2 + 2*a[41-1]*c0*c1**2*c2 + 2*a[42-1]*c0*c1**2*c2**2 + 2*a[43-1]*c0*c1**2*c2**3 + 2*a[44-1]*c0*c1**3 + 2*a[45-1]*c0*c1**3*c2 + 2*a[46-1]*c0*c1**3*c2**2 + 2*a[47-1]*c0*c1**3*c2**3 + 3*a[48-1]*c0**2 + 3*a[49-1]*c0**2*c2 + 3*a[50-1]*c0**2*c2**2 + 3*a[51-1]*c0**2*c2**3 + 3*a[52-1]*c0**2*c1 + 3*a[53-1]*c0**2*c1*c2 + 3*a[54-1]*c0**2*c1*c2**2 + 3*a[55-1]*c0**2*c1*c2**3 + 3*a[56-1]*c0**2*c1**2 + 3*a[57-1]*c0**2*c1**2*c2 + 3*a[58-1]*c0**2*c1**2*c2**2 + 3*a[59-1]*c0**2*c1**2*c2**3 + 3*a[60-1]*c0**2*c1**3 + 3*a[61-1]*c0**2*c1**3*c2 + 3*a[62-1]*c0**2*c1**3*c2**2 + 3*a[63-1]*c0**2*c1**3*c2**3)

class cross2(cross_term):
    def __call__(self,p):
        c0,c1,c2 = p

        a = self.interp.get_coeff_point(p)

        b0, b1, b2 = self.b0, self.b1, self.b2
        return -(b0 - c0)*(2*a[10-1]*c1*c2**2 + 2*a[11-1]*c1*c2**3 + 3*a[12-1]*c1**2 + 3*a[13-1]*c1**2*c2 + 3*a[14-1]*c1**2*c2**2 + 3*a[15-1]*c1**2*c2**3 + a[20-1]*c0 + a[21-1]*c0*c2 + a[22-1]*c0*c2**2 + a[23-1]*c0*c2**3 + 2*a[24-1]*c0*c1 + 2*a[25-1]*c0*c1*c2 + 2*a[26-1]*c0*c1*c2**2 + 2*a[27-1]*c0*c1*c2**3 + 3*a[28-1]*c0*c1**2 + 3*a[29-1]*c0*c1**2*c2 + 3*a[30-1]*c0*c1**2*c2**2 + 3*a[31-1]*c0*c1**2*c2**3 + a[36-1]*c0**2 + a[37-1]*c0**2*c2 + a[38-1]*c0**2*c2**2 + a[39-1]*c0**2*c2**3 + a[4-1] + 2*a[40-1]*c0**2*c1 + 2*a[41-1]*c0**2*c1*c2 + 2*a[42-1]*c0**2*c1*c2**2 + 2*a[43-1]*c0**2*c1*c2**3 + 3*a[44-1]*c0**2*c1**2 + 3*a[45-1]*c0**2*c1**2*c2 + 3*a[46-1]*c0**2*c1**2*c2**2 + 3*a[47-1]*c0**2*c1**2*c2**3 + a[5-1]*c2 + a[52-1]*c0**3 + a[53-1]*c0**3*c2 + a[54-1]*c0**3*c2**2 + a[55-1]*c0**3*c2**3 + 2*a[56-1]*c0**3*c1 + 2*a[57-1]*c0**3*c1*c2 + 2*a[58-1]*c0**3*c1*c2**2 + 2*a[59-1]*c0**3*c1*c2**3 + a[6-1]*c2**2 + 3*a[60-1]*c0**3*c1**2 + 3*a[61-1]*c0**3*c1**2*c2 + 3*a[62-1]*c0**3*c1**2*c2**2 + 3*a[63-1]*c0**3*c1**2*c2**3 + a[7-1]*c2**3 + 2*a[8-1]*c1 + 2*a[9-1]*c1*c2) + (b1 - c1)*(a[16-1] + a[17-1]*c2 + a[18-1]*c2**2 + a[19-1]*c2**3 + a[20-1]*c1 + a[21-1]*c1*c2 + a[22-1]*c1*c2**2 + a[23-1]*c1*c2**3 + a[24-1]*c1**2 + a[25-1]*c1**2*c2 + a[26-1]*c1**2*c2**2 + a[27-1]*c1**2*c2**3 + a[28-1]*c1**3 + a[29-1]*c1**3*c2 + a[30-1]*c1**3*c2**2 + a[31-1]*c1**3*c2**3 + 2*a[32-1]*c0 + 2*a[33-1]*c0*c2 + 2*a[34-1]*c0*c2**2 + 2*a[35-1]*c0*c2**3 + 2*a[36-1]*c0*c1 + 2*a[37-1]*c0*c1*c2 + 2*a[38-1]*c0*c1*c2**2 + 2*a[39-1]*c0*c1*c2**3 + 2*a[40-1]*c0*c1**2 + 2*a[41-1]*c0*c1**2*c2 + 2*a[42-1]*c0*c1**2*c2**2 + 2*a[43-1]*c0*c1**2*c2**3 + 2*a[44-1]*c0*c1**3 + 2*a[45-1]*c0*c1**3*c2 + 2*a[46-1]*c0*c1**3*c2**2 + 2*a[47-1]*c0*c1**3*c2**3 + 3*a[48-1]*c0**2 + 3*a[49-1]*c0**2*c2 + 3*a[50-1]*c0**2*c2**2 + 3*a[51-1]*c0**2*c2**3 + 3*a[52-1]*c0**2*c1 + 3*a[53-1]*c0**2*c1*c2 + 3*a[54-1]*c0**2*c1*c2**2 + 3*a[55-1]*c0**2*c1*c2**3 + 3*a[56-1]*c0**2*c1**2 + 3*a[57-1]*c0**2*c1**2*c2 + 3*a[58-1]*c0**2*c1**2*c2**2 + 3*a[59-1]*c0**2*c1**2*c2**3 + 3*a[60-1]*c0**2*c1**3 + 3*a[61-1]*c0**2*c1**3*c2 + 3*a[62-1]*c0**2*c1**3*c2**2 + 3*a[63-1]*c0**2*c1**3*c2**3)

class TriCubicInit(object):
    def __init__(self, phi, h=(1,1,1), periodic=(False,False,False)):
        self.phi = phi
        self.interp = TriCubicInterp(phi,h,periodic)
        self.d = np.zeros_like(phi)
        self.pdict = {}
        self.h=h
        self.periodic = periodic
        self.find_frozen()
        self.process_points()

    def find_frozen(self):
        phi = self.phi
        aborders = np.zeros_like(phi,dtype=bool) # point border
        aborders[phi==0.0] = True
        self.d[phi==0.0] = 0.0
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
                    for d in [-1,1]:
                        if phi[i,j,k] * phi[wrap(i+d,j,k,x,y,z,self.periodic)] < 0:
                            aborders[i,j,k] = True
#                            border_cells[i][j][k] = True
                            #border_cells[ii][jj-1][kk] = True
                        elif phi[i,j,k] * phi[wrap(i,j+d,k,x,y,z,self.periodic)] < 0:
                            aborders[i,j,k] = True
#                            border_cells[i][j][k] = True
                            #border_cells[ii-1][jj][kk] = True
                        elif phi[i,j,k] * phi[wrap(i,j,k+d,x,y,z,self.periodic)] < 0:
                            aborders[i,j,k] = True
#                            border_cells[i][j][k] = True
                            #border_cells[ii-1][jj][kk] = True
        self.aborders = aborders
        self.border_cells = border_cells

    def process_points(self):
        for i in range(self.phi.shape[0]):
            for j in range(self.phi.shape[0]):
                for k in range(self.phi.shape[0]):
                    if self.aborders[i,j,k]:
                        self.process_point(i,j,k)

    def process_point(self,i,j,k):
        x0,y0,z0 = i*self.h[0], j*self.h[1], k*self.h[2]
        cr0 = cross0(self.interp,x0,y0,z0)
        cr1 = cross1(self.interp,x0,y0,z0)
        cr2 = cross2(self.interp,x0,y0,z0)
        def eqn(p):
            # the point we want is on the zero level set
            # and perpendicular to the contours of distance from the gp
            return cr0(p) + cr1(p), cr2(p), self.interp(p)
        sol, info, ier, mesg = fsolve(eqn, (i*self.h[0],j*self.h[1],k*self.h[2]), full_output=1)
        if ier==1:
            px,py,pz = sol
            (nx, ny, nz) = self.phi.shape
            print("OK", sol)
            if 0 <= px <= nx*self.h[0] and 0 <= py <= ny*self.h[1] and 0 <= pz <= nz*self.h[2]:
                dist = np.sqrt((px-x0)**2 + (py-y0)**2 + (pz-z0)**2)
                if self.d[i,j,k] > dist:
                    self.d[i,j,k]=dist
                    self.pdict[(i,j,k)] = (px-x0,py-y0,pz-z0)
                return
            else:
                # for boundary points we need to accept points outside [0,1]
                # this could/should be done more cleverly/safely
                # which direction to let sx or sy exceed the interval should be known?
                if ((i==0 or i==nx-1) and not self.periodic[0]) \
                    or ((j==0 or j==ny-1) and not self.periodic[1]) \
                    or ((k == 0 or k==nz-1) and not self.periodic[2]):
                    dist = np.sqrt((px-x0)**2 + (py-y0)**2 + (pz-z0)**2)
                    if self.d[i,j,k] > dist:
                        self.d[i,j,k]=dist
                        self.pdict[(i,j,k)] = (px-x0,py-y0,pz-z0)
                    return

        else:
            print("failed")
            #print(ier, mesg, info)
            # mark as failed to fall back to linear interpolation
            self.aborders[i,j,k] = False

if __name__ == '__main__':
    X,Y,Z = np.meshgrid(np.linspace(0,15,16),
                        np.linspace(0,15,16),
                        np.linspace(0,15,16))

    phi = np.ones_like(X)
    phi[6,6,6] = -1
    init = TriCubicInit(phi)
