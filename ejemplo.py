import escapy

escapy.MNAf('2_elementos_RLC.cir')

B,l,p = escapy.formula_DDD()
X2 = escapy.resuelve_serie_DDD(B,l,p)
x2 = escapy.simplifica(X2)

A,x,z = escapy.formula_sympy()
X1 = escapy.resuelve_LU(A,x,z)
x1 = escapy.simplifica(X1)
