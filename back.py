import numpy as np
import matplotlib.pyplot as plt

g_na = 120
gk = 36
gl = 0.3
e_na = 50
e_k = -77
e_l = -54.4

def beta_n(v):
    return 0.125*np.exp((v+65)/(-80))

def alfa_n(v):
    return 0.01*(v+55)/(1-np.exp((v+55)/(-10)))

def beta_m(v):
    return 4*np.exp((v+65)/(-18))

def alfa_m(v):
    return 0.1*(v+40)/(1-np.exp((v+40)/(-10)))

def beta_h(v):
    return 1/(1+np.exp((v+35)/(-10)))

def alfa_h(v):
    return 0.07*np.exp((v+65)/(-20))

def phi(temp):
    return 3**((temp-6.3)/10)

def dv(I,v,n,m,h):
    return I - gl*(v-e_l) - gk*(n**4)*(v-e_k)-(g_na*(m**3)*h*(v-e_na))

def dn(temp,v,n):
    return phi(temp)*(alfa_n(v)*(1-n)-beta_n(v)*n)

def dm(temp,v,m):
    return phi(temp)*(alfa_m(v)*(1-m)-beta_m(v)*m)

def dh(temp,v,h):
    return phi(temp)*(alfa_h(v)*(1-h)-beta_h(v)*h)

def funcion(t,vals):
    #dónde va t?
    v = vals[0]
    n = vals[1]
    m = vals[2]
    h = vals[3]
    return np.array([ dv(20,v,n,m,h),
             dn(10,v,n),
             dm(10,v,m),
             dh(10,v,h)])

#Métodos de solución
def iter_RK2(h,fun,v0,n0,m0,h0):

    to = 0.0
    tf = 500.0
    t = np.arange(to, tf + h, h)

    y_rk2 = np.zeros((np.size(t),4))
    y_rk2[0] = np.array([v0,n0,m0,h0])
    #constantes
    c = {'p':1,'q':1 ,'c1':0.5,'c2':0.5}

    for i in range(1,len(t)):
        k1 = fun(t[i - 1], y_rk2[i - 1])
        k2 = fun(t[i - 1] + h*c['p'], y_rk2[i - 1] + k1 * h * c['q'])
        y_rk2[i] = y_rk2[i-1] + h *( c['c1']*k1 + c['c2']*k2)
    return t,y_rk2

def iter_RK4(h,fun,v0,n0,m0,h0):
    to = 0.0
    tf = 500.0
    t = np.arange(to, tf + h, h)

    y_rk4 = np.zeros((np.size(t),4))
    y_rk4[0] = np.array([v0,n0,m0,h0])
    #constantes
    c={'p2' : 0.5, 'p3' : 0.5, 'q21' : 0.5, 'q31' : 0, 'q32' : 0.5, 'p4':1,'q41': 0, 'q42': 0,'q43': 1,'c1' : 1/6,'c2': 1/3,'c3': 1/3,'c4': 1/6}

    for i in range(1,len(t)):
        k1 = fun(t[i - 1], y_rk4[i - 1])
        k2 = fun(t[i - 1] + c['p2']*h, y_rk4[i - 1] + c['q21']* k1 * h)
        k3 = fun(t[i - 1] + c['p3']*h, y_rk4[i - 1] + c['q31']* k1 * h + c['q32']* k2 * h)
        k4 = fun(t[i - 1] + c['p4']*h, y_rk4[i - 1] + c['q41']* k1 * h + c['q42']* k2 * h + c['q43']*k3*h)
        y_rk4[i] = y_rk4[i-1] + h*(c['c1']*k1 + c['c2']*k2 + c['c3']*k3 + c['c4']*k4)
    return t,y_rk4

"""
Esto es para probar
v_0 = -65
m_0 = 0.2
n_0 =0.4
h_0 = 0.6
a = iter_RK2(0.01,funcion,v_0,m_0,n_0,h_0)
print(a[1][:,0])
plt.plot(a[0], a[1][:,0])

plt.xlabel("t")
plt.ylabel("$V(t)$")
plt.show()
"""