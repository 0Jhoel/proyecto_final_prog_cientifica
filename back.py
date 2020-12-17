import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt

g_na = 120
gk = 36
gl = 0.3
e_na = 50
e_k = -77
e_l = -54.4

# Beta de la funcion activacion del canal de sodio
def Bm(V):
    return 4 * np.exp(-(V + 65)/10)

# Alfa de la funcion de inactivacion del canal de sodio
def Ah(V):
    return 0.07 * np.exp(-(V + 65)/20)

# Beta de la funcion de inactivacion del canal de sodio
def Bh(V):
    return 1/(1 + np.exp(-(V + 35)/10))

# Alfa de la funcion de la probabilidad de que canal de potacio este abierto
def An(V):
    return 0.01 * (V + 55)/(1 - np.exp(-(V + 55)/10))

# Beta de la funcion de la probabilidad de que canal de potacio este abierto
def Bn(V):
    return 0.125 * np.exp(-(V + 65)/80)

# Alfa de la funcion de activacion del canal de sodio
def Am(V):
    return 0.1 * (V + 40)/(1 + np.exp(-(V + 40)/10))

# Factor de temperatura
def Phi(T):
    return 3 ** ((T-6.3)/10)

# Probabilidad de inactivacion del canal de sodio
def hFun(V,h,phi):
    return phi * (Ah(V) * (1.0 - h) - Bh(V) * h)

# Probabilidad de activacion del canal de sodio
def mFun(V,m,phi):
    return phi * (Am(V) * (1.0 - m) - Bm(V) * m)

# Probabilidad del canal de potacio de estar abierto
def nFun(V,n,phi):
    return phi * (An(V) * (1.0 - n) - Bn(V) * n)

# Funcion de potencial de membrana
def Vm(I,V,n,m,h):
    return I - (gl * (V - e_l) + gk * (n ** 4) * (V - e_k) + g_na * h * (m ** 3) * (V - e_na))

# Metodo Euler Forward
def EulerForward(Vm_0,h_0,m_0,n_0,t,h,phi,I):
    # Se crean los arreglos para guardar los resultados de las iteraciones
    VmEulerFor = np.zeros(len(t))
    hEulerFor = np.zeros(len(t))
    mEulerFor = np.zeros(len(t))
    nEulerFor = np.zeros(len(t))

    # Se agregan los valores iniciales
    VmEulerFor[0] = Vm_0
    hEulerFor[0] = h_0
    mEulerFor[0] = m_0
    nEulerFor[0] = n_0

    for i in range(1,len(t)):
        VmEulerFor[i] = VmEulerFor[i-1] + h * Vm(I[i],VmEulerFor[i-1],nEulerFor[i-1],mEulerFor[i-1],
                                                 hEulerFor[i-1])
        hEulerFor[i] = hEulerFor[i-1] + h * hFun(VmEulerFor[i-1],hEulerFor[i-1],phi)
        mEulerFor[i] = mEulerFor[i-1] + h * mFun(VmEulerFor[i-1],mEulerFor[i-1],phi)
        nEulerFor[i] = nEulerFor[i-1] + h * nFun(VmEulerFor[i-1],nEulerFor[i-1],phi)

    return VmEulerFor

# x : Parametros en la posicion presente
# y1 : Vm anterior
# y2 : h anterior
# y3 : m anterior
# y4 : n anterior
def FEulerBack(x,y1,y2,y3,y4,I,phi,h):
    return[y1 + h * Vm(I,x[0],x[3],x[2],x[1]) - x[0],
           y2 + h * hFun(x[0],x[1],phi) - x[1],
           y3 + h * mFun(x[0],x[2],phi) - x[2],
           y4 + h * nFun(x[0],x[3],phi) - x[3]]

# Metodo Euler Backward
def EulerBackward(Vm_0,h_0,m_0,n_0,t,h,phi,I):
    # Se crean los arreglos para guardar los resultados de las iteraciones
    VmEulerBack = np.zeros(len(t))
    hEulerBack = np.zeros(len(t))
    mEulerBack = np.zeros(len(t))
    nEulerBack = np.zeros(len(t))

    # Se agregan los valores iniciales
    VmEulerBack[0] = Vm_0
    hEulerBack[0] = h_0
    mEulerBack[0] = m_0
    nEulerBack[0] = n_0

    for i in range(1, len(t)):
        SolBack = opt.fsolve(FEulerBack,
                             np.array([VmEulerBack[i-1],hEulerBack[i-1],mEulerBack[i-1],nEulerBack[i-1]]),(VmEulerBack[i - 1], hEulerBack[i - 1], mEulerBack[i - 1], nEulerBack[i - 1], I[i], phi, h),xtol=10**-15)
        VmEulerBack[i] = SolBack[0]
        hEulerBack[i] = SolBack[1]
        mEulerBack[i] = SolBack[2]
        nEulerBack[i] = SolBack[3]

    return VmEulerBack

# x : Parametros en la posicion presente
# y1 : Vm anterior
# y2 : h anterior
# y3 : m anterior
# y4 : n anterior
def FEulerMod(x,y1,y2,y3,y4,I,phi,h):
    return[y1 + (h/2.0) * (Vm(I,y1,y4,y3,y2) + Vm(I,x[0],x[3],x[2],x[1])) - x[0],
           y2 + (h/2.0) * (hFun(y1,y2,phi) + hFun(x[0],x[1],phi)) - x[1],
           y3 + (h/2.0) * (mFun(y1,y3,phi) + mFun(x[0],x[2],phi)) - x[2],
           y4 + (h/2.0) * (nFun(y1,y4,phi) + nFun(x[0],x[3],phi)) - x[3]]

# Metodo Euler Modificado
def EulerMod(Vm_0,h_0,m_0,n_0,t,h,phi,I):
    # Se crean los arreglos para guardar los resultados de las iteraciones
    VmEulerMod = np.zeros(len(t))
    hEulerMod = np.zeros(len(t))
    mEulerMod = np.zeros(len(t))
    nEulerMod = np.zeros(len(t))

    # Se agregan los valores iniciales
    VmEulerMod[0] = Vm_0
    hEulerMod[0] = h_0
    mEulerMod[0] = m_0
    nEulerMod[0] = n_0

    for i in range(1,len(t)):
        SolMod = opt.fsolve(FEulerMod,
                            np.array([VmEulerMod[i-1],hEulerMod[i-1],mEulerMod[i-1],nEulerMod[i-1]]),
                            (VmEulerMod[i-1],hEulerMod[i-1],mEulerMod[i-1],nEulerMod[i-1],I[i],phi,h),
                            xtol=10**-15)
        VmEulerMod[i] = SolMod[0]
        hEulerMod[i] = SolMod[1]
        mEulerMod[i] = SolMod[2]
        nEulerMod[i] = SolMod[3]

    return VmEulerMod

# Metodo Renge-Kutta de 2do orden
def RK2(Vm_0,h_0,m_0,n_0,t,h,phi,I):
    # Se crean los arreglos para guardar los resultados de las iteraciones
    VmRK2 = np.zeros(len(t))
    hRK2 = np.zeros(len(t))
    mRK2 = np.zeros(len(t))
    nRK2 = np.zeros(len(t))

    # Se agregan los valores iniciales
    VmRK2[0] = Vm_0
    hRK2[0] = h_0
    mRK2[0] = m_0
    nRK2[0] = n_0

    for i in range(1,len(t)):
        # Para Vm: k11, k21
        # Para n: k12, k22
        # Para m: k13, k23
        # Para h: k14, k24

        # k1 = F(t_(i - 1), y_(i - 1))
        k11 = Vm(I[i],VmRK2[i - 1],nRK2[i - 1],mRK2[i - 1],hRK2[i - 1])
        k12 = nFun(VmRK2[i - 1],nRK2[i - 1],phi)
        k13 = mFun(VmRK2[i - 1],mRK2[i - 1],phi)
        k14 = hFun(VmRK2[i - 1],hRK2[i - 1],phi)

        # k2 = F(t_(i - 1) + h, y_(i - 1) + hk1)
        k21 = Vm(I[i], VmRK2[i - 1] + h * k11, nRK2[i - 1] + h *k12, mRK2[i - 1] + h * k13, hRK2[i - 1] + h * k14)
        k22 = nFun(VmRK2[i - 1] + h * k11, nRK2[i - 1] + h * k12, phi)
        k23 = mFun(VmRK2[i - 1] + h * k11, mRK2[i - 1] + h * k13, phi)
        k24 = hFun(VmRK2[i - 1] + h * k11, hRK2[i - 1] + h * k14, phi)

        # y_i = y_(i-1) + (h / 2)(k1 + k2)
        VmRK2[i] = VmRK2[i - 1] + (h / 2) * (k11 + k21)
        nRK2[i] = nRK2[i - 1] + (h / 2) * (k12 + k22)
        mRK2[i] = mRK2[i - 1] + (h / 2) * (k13 + k23)
        hRK2[i] = hRK2[i - 1] + (h / 2) * (k14 + k24)

    return VmRK2

# Metodo Renge-Kutta de 4to orden
def RK4(Vm_0,h_0,m_0,n_0,t,h,phi,I):
    # Se crean los arreglos para guardar los resultados de las iteraciones
    VmRK4 = np.zeros(len(t))
    hRK4 = np.zeros(len(t))
    mRK4 = np.zeros(len(t))
    nRK4 = np.zeros(len(t))

    # Se agregan los valores iniciales
    VmRK4[0] = Vm_0
    hRK4[0] = h_0
    mRK4[0] = m_0
    nRK4[0] = n_0

    for i in range(1, len(t)):
        # Para Vm: k11, k21, k31, k41
        # Para n: k12, k22, k32, k42
        # Para m: k13, k23, k33, k43
        # Para h: k14, k24, k34, k44

        # k1 = F(t_(i-1), y_(i-1))
        k11 = Vm(I[i], VmRK4[i - 1], nRK4[i - 1], mRK4[i - 1], hRK4[i - 1])
        k12 = nFun(VmRK4[i - 1], nRK4[i - 1], phi)
        k13 = mFun(VmRK4[i - 1], mRK4[i - 1], phi)
        k14 = hFun(VmRK4[i - 1], hRK4[i - 1], phi)

        # k2 = F(t_(i - 1) + 0.5h, y_(i - 1) + 0.5k1h)
        k21 = Vm(I[i], VmRK4[i - 1] + 0.5 * h * k11, nRK4[i - 1] + 0.5 * h * k12, mRK4[i - 1] + 0.5 * h * k13,
                 hRK4[i - 1] + 0.5 * h * k14)
        k22 = nFun(VmRK4[i - 1] + 0.5 * h * k11, nRK4[i - 1] + 0.5 * h * k12, phi)
        k23 = mFun(VmRK4[i - 1] + 0.5 * h * k11, mRK4[i - 1] + 0.5 * h * k13, phi)
        k24 = hFun(VmRK4[i - 1] + 0.5 * h * k11, hRK4[i - 1] + 0.5 * h * k14, phi)

        # k3 = F(t_(i - 1) + 0.5h, y_(i - 1) + 0.5k2h)
        k31 = Vm(I[i], VmRK4[i - 1] + 0.5 * h * k21, nRK4[i -1] + 0.5 * h * k22, mRK4[i - 1] + 0.5 * h * k23,
                 hRK4[i - 1] + 0.5 * h * k24)
        k32 = nFun(VmRK4[i - 1] + 0.5 * h * k21, nRK4[i - 1] + 0.5 * h * k22, phi)
        k33 = mFun(VmRK4[i - 1] + 0.5 * h * k21, mRK4[i - 1] + 0.5 * h * k23, phi)
        k34 = hFun(VmRK4[i - 1] + 0.5 * h * k21, hRK4[i - 1] + 0.5 * h * k24, phi)

        # k4 = F(t_(i - 1) + h, y_(i - 1) + k3h)
        k41 = Vm(I[i], VmRK4[i - 1] + h * k31, nRK4[i - 1] + h * k32, mRK4[i - 1] + h * k33, hRK4[i - 1] + h * k34)
        k42 = nFun(VmRK4[i - 1] + h * k31, nRK4[i - 1] + h * k32, phi)
        k43 = mFun(VmRK4[i - 1] + h * k31, mRK4[i - 1] + h * k33, phi)
        k44 = hFun(VmRK4[i - 1] + h * k31, hRK4[i - 1] + h * k34, phi)

        # y_i = y_(i-1)
        VmRK4[i] = VmRK4[i - 1] + (h / 6) * (k11 + 2 * k21 + 2 * k31 + k41)
        nRK4[i] = nRK4[i - 1] + (h / 6) * (k12 + 2 * k22 + 2 * k32 + k42)
        mRK4[i] = mRK4[i - 1] + (h / 6) * (k13 + 2 * k23 + 2 * k33 + k43)
        hRK4[i] = hRK4[i - 1] + (h / 6) * (k14 + 2 * k24 + 2 * k34 + k44)

    return VmRK4

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

# Setup inicial
# Definimos un valor para h
h = 0.01
# Definimos el tiempo inicial
to = 0.0
# Definimos el tiempo final
tf = 40.0
# Creamos un arreglo de tiempo con pasos de h
t = np.arange(to, tf + h, h)
# h inicial
h0 = 0.65
# m inicial
m0 = 0.05
# n inicial
n0 = 0.3
# V inicial
V0 = -65
# Temperatura
T = 6.3
Phi = Phi(T)
# Corriente
I = 120.0 * np.ones(np.size(t))
'''I = np.zeros(np.size(t))
r = np.where((t >= to) & (t <= 50))
I[r] = 120
r = np.where((t >= 50) & (t <= tf))
I[r] = 120'''

# Grafica
plt.figure()
plt.plot(t, EulerForward(V0,h0,m0,n0,t,h,Phi,I), "r")
plt.plot(t, EulerBackward(V0,h0,m0,n0,t,h,Phi,I), "g")
plt.plot(t, EulerMod(V0,h0,m0,n0,t,h,Phi,I), "m")
plt.plot(t, RK2(V0,h0,m0,n0,t,h,Phi,I), "orange")
plt.plot(t, RK4(V0,h0,m0,n0,t,h,Phi,I), "maroon")
plt.xlabel("t", fontsize=15)
plt.ylabel("V", fontsize=15)
plt.legend(["EulerFor","RK2","RK4"], fontsize=12)
plt.legend(["EulerFor","EulerBackRoot","EulerModRoot","RK2","RK4"], fontsize=12)
plt.grid(1)
plt.show()