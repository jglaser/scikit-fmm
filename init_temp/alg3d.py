from sympy import summation, symbols, diff, MatrixSymbol, Matrix
import sympy.printing.python as python
from sympy.abc import x,y,z,i,j,k,l
import re

a = symbols('a:64')

b0, b1, b2 = symbols('b:3')  # the known gridpoint
c0, c1, c2 = symbols('c:3')  # the unknown point on the zero level-set
lower0, lower1, lower2 = symbols('lower:3')  # the coordinates of the (0,0,0) corner of the interpolation cube
h0, h1, h2 = symbols('h:3')  # the grid cell spacing

expr = 0
l = 0

#Lekien Marsden Eq. (10) uses alpha_l = alpha_(1+i+4j+16k) == alpha_ijk
for k in range(4):
    for j in range(4):
        for i in range(4):
            expr += a[l] * x**i * y**j * z**k
            l +=1

print("interpolant expression")
print(expr)

dpdx_c = diff(expr,x).subs(x,c0).subs(y,c1).subs(z,c2)/h0
dpdy_c = diff(expr,y).subs(x,c0).subs(y,c1).subs(z,c2)/h1
dpdz_c = diff(expr,z).subs(x,c0).subs(y,c1).subs(z,c2)/h2

eq0 = expr.subs(x,c0).subs(y,c1).subs(z,c2)

grad_p = Matrix((dpdx_c, dpdy_c, dpdz_c))
eq1 = grad_p.cross(Matrix((b0-c0*h0-lower0,b1-c1*h1-lower1,b2-c2*h2-lower2)))

# eq1 = dpdx_c * (b1-c1) - dpdy_c * (b0-c0)

def to_python(expr):
    return re.sub(r"a(\d+)", r"a[\1]", str(expr))

print()
print(to_python(eq1[0]))
print()
print()
print(to_python(eq1[1]))
print()
print()
print(to_python(eq1[2]))
print()

print("Jacobian matrix")

prod = eq1[0]*eq1[0]+eq1[1]*eq1[1]
df0dx = diff(prod,c0)/h0
df0dy = diff(prod,c1)/h1
df0dz = diff(prod,c2)/h2
df1dx = diff(eq1[2],c0)/h0
df1dy = diff(eq1[2],c1)/h1
df1dz = diff(eq1[2],c2)/h2
df2dx = diff(eq0,c0)/h0
df2dy = diff(eq0,c1)/h1
df2dz = diff(eq0,c2)/h2
jacobian = [[df0dx,df0dy,df0dz],[df1dx,df1dy,df1dz],[df2dx,df2dy,df2dz]]
#jacobian = [[diff(eq1[0],c0)/h0+diff(eq1[1],c0)/h0,diff(eq1[0],c1)/h1+diff(eq1[1],c1)/h1,diff(eq1[0],c2)/h2+diff(eq1[1],c2)/h2],
#            [diff(eq1[2],c0)/h0,diff(eq1[2],c1)/h1,diff(eq1[2],c2)/h2],
#            [diff(eq0,c0)/h0,diff(eq0,c1)/h1,diff(eq0,c2)/h2]]

print('[',end='')
for i in range(3):
    print('[',end='')
    for j in range(3):
        print(to_python(jacobian[i][j]),end='')
        if j != 2:
            print(',',end='')
    print(']',end='')
    if i != 2:
        print(', ',end='')
print(']')

print()
print('Jacobian elements')
print()
print(to_python(df0dx))
print()

print()
print(to_python(df0dy))
print()

print()
print(to_python(df0dz))
print()

print()
print(to_python(df1dx))
print()

print()
print(to_python(df1dy))
print()

print()
print(to_python(df1dz))
print()

print()
print(to_python(df2dx))
print()

print()
print(to_python(df2dy))
print()

print()
print(to_python(df2dz))
print()

