import e2scapy

e2scapy.MNAf('2_elementos_RLC.cir')

B,l,p = e2scapy.formula_DDD()
X2 = e2scapy.resuelve_serie_DDD(B,l,p)
x2 = e2scapy.simplifica(X2)

A,x,z = e2scapy.formula_sympy()
X1 = e2scapy.resuelve_LU(A,x,z)
x1 = e2scapy.simplifica(X1)
