import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
import numpy as np
from back import *

#VALORES INICIALES DE LOS PARÁMETROS


hp = 0.01
to1 = 10.0
tf1 = 50.0
to2 = 50.0
tf2 = 100.0
h0 = 0.65
m0 = 0.05
n0 = 0.3
V0 = -65.0
T0 = 6.3
I1 = 50
I2 = 120

#Limpia todos los widgets de un frame, se usa para limpiar el plot
def clearFrame(frame):
    for widget in frame.winfo_children():
       widget.destroy()

# Deshabilita un intervalo cuando se tiene corriente constante
def desInter():
    entr_intervalo_1_0.delete(0, tk.END)
    entr_intervalo_1_1.delete(0, tk.END)
    entr_intensidad_1.delete(0, tk.END)

    entr_intervalo_1_0.configure(state=tk.DISABLED)
    entr_intervalo_1_1.configure(state=tk.DISABLED)
    entr_intensidad_1.configure(state=tk.DISABLED)

    print('borrado')

# Habilita un intervalo cuando se tiene corriente constante
def habInter():
    entr_intervalo_1_0.configure(state=tk.NORMAL)
    entr_intervalo_1_1.configure(state=tk.NORMAL)
    entr_intensidad_1.configure(state=tk.NORMAL)

#Grafica un plot vacio (el inicial)
def plotd(master_frame):
    # Figura que contendrá el plot
    fig = Figure(figsize=(5, 3), dpi=100)

    # se crea el plot
    plot1 = fig.add_subplot(111)
    y = []
    x = []
    plot1.plot(x,y)
    # Esto es para agregar el plot a la interfaz
    canvas = FigureCanvasTkAgg(fig, master=master_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas, master_frame)
    toolbar.update()
    canvas.get_tk_widget().pack()

# metodo de donde sale la gráfica con la función
def plot(master_frame, V, m, h, n, t, I, phi):
    clearFrame(master_frame)
    #la figura que contendrá el the plot
    fig = Figure(figsize=(5, 3), dpi=100)

    # se crea el plot
    plot1 = fig.add_subplot(111)
    lista_metodos = []
    if v_eulerfwd.get():
        lista_metodos.append("Euler Forward")
        y1 = EulerForward(V,h,m,n,t,0.01,phi,I)
        plot1.plot(t,y1)
    if v_eulerback.get():
        lista_metodos.append("Euler Backward")
        y2 = EulerBackward(V,h,m,n,t,0.01,phi,I)
        plot1.plot(t, y2)
    if v_eulermod.get():
        lista_metodos.append("Euler Modificado")
        y3 = EulerMod(V,h,m,n,t,0.01,phi,I)
        plot1.plot(t, y3)
    if v_rk2.get():
        lista_metodos.append("RK2")
        y4 = RK2(V,h,m,n,t,0.01,phi,I)
        plot1.plot(t, y4)
    if v_rk4.get():
        lista_metodos.append("RK4")
        y5 = RK4(V,h,m,n,t,0.01,phi,I)
        plot1.plot(t, y5)
    if v_odeint.get():
        lista_metodos.append("Odeint")
        y6 = funcion_odeint(V,m,h,n, t,phi,I)
        plot1.plot(t, y6)
    plot1.legend(lista_metodos)
    # Esto es para agregar el plot a la interfaz
    canvas = FigureCanvasTkAgg(fig, master=master_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas, master_frame)
    toolbar.update()
    canvas.get_tk_widget().pack()

# Actualiza los parametros de entrada y llama la funcion para graficar
def pri():
    global hp
    global V0
    global h0
    global n0
    global m0
    global T0
    global I1
    global I2
    global to1
    global tf1
    global to2
    global tf2
    global frame_grafica

    tipo = vc.get()

    if tipo == 1:

        try:
            to2 = float(entr_intervalo_2_0.get())
            tf2 = float(entr_intervalo_2_1.get())
            I2 = float(entr_intensidad_2.get())
            V0 = float(v_0.get())
            m0 = float(m_0.get())
            n0 = float(n_0.get())
            h0 = float(h_0.get())
            T0 = float(t_0.get())

            t = np.arange(to2,tf2+hp,hp)
            I = I2 * np.ones(np.size(t))

            #phi = Phi(T0)
            phi = 1
            plot(frame_grafica, V0,m0,h0,n0,t,I,phi)
        except:
            print('Error en los parametros')
    else:
        try:
            to1 = float(entr_intervalo_1_0.get())
            tf1 = float(entr_intervalo_1_1.get())
            I1 = float(entr_intensidad_1.get())
            to2 = float(entr_intervalo_2_0.get())
            tf2 = float(entr_intervalo_2_1.get())
            I2 = float(entr_intensidad_2.get())
            V0 = float(v_0.get())
            m0 = float(m_0.get())
            n0 = float(n_0.get())
            h0 = float(h_0.get())
            T0 = float(t_0.get())

            t = np.arange(to1, tf2 + hp, hp)
            I = np.zeros(np.size(t))
            r = np.where((t >= to1) & (t <= tf1))
            I[r] = I1
            r = np.where((t >= to2) & (t <= tf2))
            I[r] = I2
            phi = Phi(T0)

            plot(frame_grafica, V0, m0, h0, n0, t, I, phi)

        except:
            print('Error en los parametros')


#ventana
root = tk.Tk()

#método para cerrar ventana
def salir():
    root.destroy()

# Le asigna un tamaño a la ventana inicial
width = 1020
height = 660
root.geometry(str(width) + "x" + str(height))  # dimensiones de la ventana

#Construye el frame de la izquierda (contiene el título y los parámetros)
frame_izquierda = tk.Frame(root, background="#ffffff", height=height)
frame_izquierda.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
root.grid_columnconfigure(0, weight=4)
root.grid_columnconfigure(1, weight=0)


#Pertenece al frame de la izquierda, contiene el título del proyecto y el botón salir
frame_titulo = tk.Frame(frame_izquierda, background="#ffffff", height=height * 0.3)
frame_titulo.pack(fill='both')
#Botón salir
b_salir = tk.Button(frame_titulo,text="Salir",background="#ffffff",borderwidth=1,command=salir)
b_salir.pack(anchor=tk.W)
#Título del proyecto
photo_titulo = tk.PhotoImage(file="images/titulo_general.png")#fuente de la imagen: https://pngtree.com/freepng/neuron-icon-for-your-project_4864040.html
label_titulo = tk.Label(frame_titulo, background="#ffffff", image = photo_titulo)
label_titulo.pack()

#Pertenece al frame de la izquierda, contiene el título 'Parámetros'
frame_parametros_titulo = tk.Frame(frame_izquierda, background="#ffffff", height=height * 0.03)
frame_parametros_titulo.pack(fill='both')
label_rk = tk.Label(frame_parametros_titulo, text="Parámetros", font=("Leelawadee UI", 20), background="#ffffff")
label_rk.pack(anchor=tk.W)

# frames para los parametros
frame_parametros = tk.Frame(frame_izquierda, background="#ffffff", height=height * 0.3)  # funciona con grid
frame_parametros2 = tk.Frame(frame_izquierda, background="#ffffff", height=height * 0.16)  # funciona con pack
frame_parametros3 = tk.Frame(frame_izquierda, background="#ffffff", height=height * 0.1)  # funciona con grid
frame_boton_parametros = tk.Frame(frame_izquierda, background="#ffffff", height=height * 0.11)  # funciona con pack

# se llena el primer frame_parametros
frame_parametros.pack(fill='both')
frame_parametros2.pack(fill='both')
frame_parametros3.pack()
frame_boton_parametros.pack(fill='both')

#Crea los elementos necesarios
label_v_0 = tk.Label(frame_parametros, text="V inicial", font=("Leelawadee UI", 14), background="#ffffff")
v_0 = tk.Entry(frame_parametros)
v_0.insert(0,'-65')
label_n_0 = tk.Label(frame_parametros, text="n inicial", font=("Leelawadee UI", 14), background="#ffffff")
n_0 = tk.Entry(frame_parametros)
n_0.insert(0,'0.3')
label_m_0 = tk.Label(frame_parametros, text="m inicial", font=("Leelawadee UI", 14), background="#ffffff")
m_0 = tk.Entry(frame_parametros)
m_0.insert(0,'0.05')
label_h_0 = tk.Label(frame_parametros, text="h inicial", font=("Leelawadee UI", 14), background="#ffffff")
h_0 = tk.Entry(frame_parametros)
h_0.insert(0,'0.65')

#Le asigna una posición a cada elemento
label_v_0.grid(row=0, column=0, sticky="nw")
label_n_0.grid(row=1, column=0, sticky="nw")
label_m_0.grid(row=2, column=0, sticky="nw")
label_h_0.grid(row=3, column=0, sticky="nw")
v_0.grid(row=0, column=1)
n_0.grid(row=1, column=1)
m_0.grid(row=2, column=1)
h_0.grid(row=3, column=1)

# se llena el SEGUNDO frame_parametros
label_t_0 = tk.Label(frame_parametros2, text="Temperatura inicial", font=("Leelawadee UI", 14), background="#ffffff")
t_0 = tk.Entry(frame_parametros2)
t_0.insert(0,'6.3')
label_t_0.pack(anchor=tk.W)
t_0.pack(anchor=tk.W)

#Variable que contiene el valor q si la corriente es fija y 2 si es continua
vc = tk.IntVar(value=1)

cb_fija = tk.Radiobutton(frame_parametros2, command=desInter, text="Fija", variable=vc, value=1, font=("Leelawadee UI", 12),
                         background="#ffffff")
cb_continua = tk.Radiobutton(frame_parametros2, command=habInter, text="Continua", variable=vc, value=2, font=("Leelawadee UI", 12),
                             background="#ffffff")
tk.Label(frame_parametros2, text="Corriente", font=("Leelawadee UI", 14), background="#ffffff").pack(anchor=tk.W)
cb_fija.pack()
cb_continua.pack()

# Se llena el TERCER frame parametros
entr_intervalo_1_0 = tk.Entry(frame_parametros3, state=tk.DISABLED, width=5)
entr_intervalo_1_0.grid(row=0, column=0)
tk.Label(frame_parametros3, text="-", background="#ffffff").grid(row=0, column=1)
entr_intervalo_1_1 = tk.Entry(frame_parametros3, state=tk.DISABLED, width=5)
entr_intervalo_1_1.grid(row=0, column=2)
tk.Label(frame_parametros3, text="mS", background="#ffffff").grid(row=0, column=3)
entr_intensidad_1 = tk.Entry(frame_parametros3, state=tk.DISABLED, width=5)
entr_intensidad_1.grid(row=0, column=4)

entr_intervalo_2_0 = tk.Entry(frame_parametros3, width=5)
entr_intervalo_2_0.insert(0,'10')
entr_intervalo_2_0.grid(row=1, column=0)
tk.Label(frame_parametros3, text="-", background="#ffffff").grid(row=1, column=1)
entr_intervalo_2_1 = tk.Entry(frame_parametros3, width=5)
entr_intervalo_2_1.insert(0,'100')
entr_intervalo_2_1.grid(row=1, column=2)
tk.Label(frame_parametros3, text="mS", background="#ffffff").grid(row=1, column=3)
entr_intensidad_2 = tk.Entry(frame_parametros3, width=5)
entr_intensidad_2.insert(0,'120')
entr_intensidad_2.grid(row=1, column=4)

# botón para actualizar los parámetros
photoP = tk.PhotoImage(file="images/b_parametros.png")
boton_parametros = tk.Button(frame_boton_parametros, text="Actualizar parámetros", image=photoP, command=pri)
boton_parametros.pack()

# Frame del lado derecho
frame_derecha = tk.Frame(root, background="#ffffff", height=height)
frame_derecha.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)

# de aquí para abajo vienen los botones con los métodos de euler
frame_rk_titulo_euler = tk.Frame(frame_derecha, background="#ffffff")
frame_rk_titulo_euler.pack(fill='both')

label_euler = tk.Label(frame_rk_titulo_euler, text="Métodos de Solución (Euler)", font=("Leelawadee UI", 18),
                       background="#ffffff")
label_euler.pack(anchor=tk.W)

frame_euler_opciones = tk.Frame(frame_derecha, background="#ffffff")
frame_euler_opciones.pack(fill='both')

photo = tk.PhotoImage(file="images/b_euler_mod.png")
v_eulermod = tk.IntVar(value=0)
b_eulermod = tk.Checkbutton(frame_euler_opciones,variable = v_eulermod, onvalue = 1, offvalue = 0, image=photo, background="#ffffff")
photo1 = tk.PhotoImage(file="images/b_euler_for.png")
v_eulerback = tk.IntVar(value=0)
b_eulerback = tk.Checkbutton(frame_euler_opciones,variable = v_eulerback, onvalue = 1, offvalue = 0, image=photo1, background="#ffffff")
photo2 = tk.PhotoImage(file="images/b_euler_back.png")
v_eulerfwd = tk.IntVar(value=0)
b_eulerfwd = tk.Checkbutton(frame_euler_opciones,variable = v_eulerfwd, onvalue = 1, offvalue = 0, image=photo2, background="#ffffff")


b_eulermod.grid(row=1, column=0, sticky="nw", padx=2, pady=2)
b_eulerback.grid(row=1, column=1, sticky="nw", padx=2, pady=2)
b_eulerfwd.grid(row=1, column=2, sticky="nw", padx=2, pady=2)

# Aquí se crea un frame que contenga la gráfica
frame_grafica = tk.Frame(frame_derecha, background="#ffffff")
frame_grafica.pack(fill='both')
plotd(frame_grafica)

# de aquí para abajo vienen los botones con los métodos de RK y Odeint
frame_rk_titulo = tk.Frame(frame_derecha, background="#ffffff")
frame_rk_titulo.pack(fill='both')

label_rk = tk.Label(frame_rk_titulo, text="Métodos de Solución (RK u Odeint)", font=("Leelawadee UI", 18), background="#ffffff")
label_rk.pack(anchor=tk.W)

frame_rk_opciones = tk.Frame(frame_derecha, background="#ffffff")
frame_rk_opciones.pack(fill='both')

photo3 = tk.PhotoImage(file="images/b_rk2.png")
v_rk2 = tk.IntVar(value=0)
b_rk2 = tk.Checkbutton(frame_rk_opciones,variable = v_rk2, onvalue = 1, offvalue = 0, bg = "#ffffff", image=photo3)
photo4 = tk.PhotoImage(file="images/b_rk4.png")
v_rk4 = tk.IntVar(value=0)
b_rk4 = tk.Checkbutton(frame_rk_opciones,variable = v_rk4, onvalue = 1, offvalue = 0, bg = "#ffffff", image=photo4)
photo5 = tk.PhotoImage(file="images/b_odeint.png")
v_odeint = tk.IntVar(value=0)
b_odeint = tk.Checkbutton(frame_rk_opciones,variable = v_odeint, onvalue = 1, offvalue = 0, bg = "#ffffff", image=photo5)

b_rk4.grid(row=1, column=0, sticky="w")
b_rk2.grid(row=1, column=1, sticky="w")
b_odeint.grid(row=1, column=2, sticky="w")

root.mainloop()