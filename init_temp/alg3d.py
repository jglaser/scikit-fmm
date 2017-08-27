from sympy import summation, symbols, diff, MatrixSymbol, Matrix
import sympy.printing.python as python
from sympy.abc import x,y,z,i,j,k,l
import re

a = symbols('a:64')

b0, b1, b2 = symbols('b:3')  # the known gridpoint
c0, c1, c2 = symbols('c:3')  # the unknown point on the zero level-set

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

dpdx_c = diff(expr,x).subs(x,c0).subs(y,c1).subs(z,c2)
dpdy_c = diff(expr,y).subs(x,c0).subs(y,c1).subs(z,c2)
dpdz_c = diff(expr,z).subs(x,c0).subs(y,c1).subs(z,c2)

eq0 = expr.subs(x,c0).subs(y,c1).subs(z,c2)

grad_p = Matrix((dpdx_c, dpdy_c, dpdz_c))
eq1 = grad_p.cross(Matrix((b0-c0,b1-c1,b2-c2)))

# eq1 = dpdx_c * (b1-c1) - dpdy_c * (b0-c0)

def to_python(expr):
    return re.sub(r"a(\d+)", r"a[\1-1]", str(expr))

print()
print(to_python(eq1[0]))
print()
print()
print(to_python(eq1[1]))
print()
print()
print(to_python(eq1[2]))
print()

#print("Jacobian elements")

jacobian = [[diff(eq1[0],c0)+diff(eq1[1],c0),diff(eq1[0],c1)+diff(eq1[1],c1),diff(eq1[0],c2)+diff(eq1[1],c2)],
            [diff(eq1[2],c0),diff(eq1[2],c1),diff(eq1[2],c2)],
            [diff(eq0,c0),diff(eq0,c1),diff(eq0,c2)]]

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
