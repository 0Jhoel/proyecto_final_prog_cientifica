import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)

#metodo de donde sale la gráfica con la función
def plot(master_frame,v, m, h, n, t):
    # the figure that will contain the plot
    fig = Figure(figsize = (5, 3), dpi = 100)
    
    #Función super básica que se va a mostrar mientras tanto
    x = [i for i in range(101)]
    y = [i**2 for i in range(101)]

    # se crea el plot
    plot1 = fig.add_subplot(111)
    plot1.plot(x,y)

    # Esto es para agregar el plot a la interfaz
    canvas = FigureCanvasTkAgg(fig, master = master_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas,master_frame)
    toolbar.update()
    canvas.get_tk_widget().pack()

root = tk.Tk()
width = 1020
height = 640
root.geometry(str(width)+"x"+str(height))#dimensiones de la ventana

frame_izquierda = tk.Frame(root, background="#ffffff", height=height)
frame_izquierda.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
root.grid_columnconfigure(0, weight=4)
root.grid_columnconfigure(1, weight=0)

frame_titulo = tk.Frame(frame_izquierda, background="#ffffff", height=height*0.35)

#frames para los parametros
frame_parametros = tk.Frame(frame_izquierda, background="#ffffff", height=height*0.3)#funciona con grid
frame_parametros2 = tk.Frame(frame_izquierda, background="#ffffff", height=height*0.175)#funciona con pack
frame_parametros3 = tk.Frame(frame_izquierda, background="#ffffff", height=height*0.175)#funciona con grid

#se llena el primer frame_parametros
frame_titulo.pack(fill='both')
frame_parametros.pack(fill='both')
frame_parametros2.pack(fill='both')
frame_parametros3.pack(fill='both')

label_v_0 = tk.Label(frame_parametros, text="Vm inicial",font=("Leelawadee UI", 14), background="#ffffff")
v_0 = tk.Entry(frame_parametros)
label_n_0 = tk.Label(frame_parametros, text="n inicial",font=("Leelawadee UI", 14), background="#ffffff")
n_0 = tk.Entry(frame_parametros)
label_m_0 = tk.Label(frame_parametros, text="m inicial",font=("Leelawadee UI", 14), background="#ffffff")
m_0 = tk.Entry(frame_parametros)
label_h_0 = tk.Label(frame_parametros, text="h inicial",font=("Leelawadee UI", 14), background="#ffffff")
h_0 = tk.Entry(frame_parametros)

label_v_0.grid(row = 0, column=0,sticky="nw")
label_n_0.grid(row = 1, column=0,sticky="nw")
label_m_0.grid(row = 2, column=0,sticky="nw")
label_h_0.grid(row = 3, column=0,sticky="nw")
v_0.grid(row = 0, column=1)
n_0.grid(row = 1, column=1)
m_0.grid(row = 2, column=1)
h_0.grid(row = 3, column=1)

#se llena el SEGUNDO frame_parametros
label_t_0 = tk.Label(frame_parametros2, text="Temperatura inicial",font=("Leelawadee UI", 14), background="#ffffff")
t_0 = tk.Entry(frame_parametros2)
label_te_0 = tk.Label(frame_parametros2, text="Tiempo de estimulación",font=("Leelawadee UI", 14), background="#ffffff")
te_0 = tk.Entry(frame_parametros2)
label_t_0.pack(anchor=tk.W)
t_0.pack(anchor=tk.W)
label_te_0.pack(anchor=tk.W)
te_0.pack(anchor=tk.W)

v = tk.IntVar()

cb_fija = tk.Radiobutton(frame_parametros2, text="Fija", variable=v, value=1)
cb_continua = tk.Radiobutton(frame_parametros2, text="Continua", variable=v, value=2)
tk.Label(frame_parametros2, text="Corriente",font=("Leelawadee UI", 14),background="#ffffff").pack(anchor=tk.W)
cb_fija.pack()
cb_continua.pack()

#Se llena el TERCER frame parametros
entr_intervalo_1_0 = tk.Entry(frame_parametros3)
entr_intervalo_1_0.grid(row=0,column=0)
tk.Label(frame_parametros3,text="-",background="#ffffff").grid(row=0,column=1)
entr_intervalo_1_1 = tk.Entry(frame_parametros3)
entr_intervalo_1_1.grid(row=0,column=2)
tk.Label(frame_parametros3,text="mS",background="#ffffff").grid(row=0,column=3)
entr_intensidad_1 = tk.Entry(frame_parametros3)
entr_intensidad_1.grid(row=0,column=4)

entr_intervalo_2_0 = tk.Entry(frame_parametros3)
entr_intervalo_2_0.grid(row=1,column=0)
tk.Label(frame_parametros3,text="-",background="#ffffff").grid(row=1,column=1)
entr_intervalo_2_1 = tk.Entry(frame_parametros3)
entr_intervalo_2_1.grid(row=1,column=2)
tk.Label(frame_parametros3,text="mS",background="#ffffff").grid(row=1,column=3)
entr_intensidad_2 = tk.Entry(frame_parametros3)
entr_intensidad_2.grid(row=1,column=4)

#Frame del lado derecho
frame_derecha = tk.Frame(root, background="#ffffff", height=height)
frame_derecha.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)

#de aquí para abajo vienen los botones con los métodos de euler
frame_euler_opciones = tk.Frame(frame_derecha, background="#ffffff")
frame_euler_opciones.pack(fill='both')

label = tk.Label(frame_euler_opciones, text="Métodos de Euler",font=("Leelawadee UI", 18), background="#ffffff")
label.pack()

photo = tk.PhotoImage(file = "images/b_euler_mod.png")
b_eulermod = tk.Button(frame_euler_opciones, text ="euler mod",image=photo)
photo1 = tk.PhotoImage(file = "images/b_euler_for.png")
b_eulerback = tk.Button(frame_euler_opciones, text ="euler back",image=photo1)
photo2 = tk.PhotoImage(file = "images/b_euler_back.png")
b_eulerfwd = tk.Button(frame_euler_opciones, text ="euler forward",image=photo2)

label.grid(row=0, column=0, sticky="nw", padx=2, pady=2)
b_eulermod.grid(row=1, column=0, sticky="nw", padx=2, pady=2)
b_eulerback.grid(row=1, column=1, sticky="nw", padx=2, pady=2)
b_eulerfwd.grid(row=1, column=2, sticky="nw", padx=2, pady=2)

#Aquí se crea un frame que contenga la gráfica
frame_grafica = tk.Frame(frame_derecha, background="#ffffff")
frame_grafica.pack(fill='both')
plot(frame_grafica,0,0,0,0,0)

#de aquí para abajo vienen los botones con los métodos de RK y Odeint
frame_rk_opciones = tk.Frame(frame_derecha, background="#ffffff")
frame_rk_opciones.pack(fill='both')

label_rk = tk.Label(frame_rk_opciones, text="Métodos de Runge–Kutta",font=("Leelawadee UI", 18), background="#ffffff")
#label_odeint = tk.Label(frame_rk_opciones, text="Métodos de Odeint",font=("Leelawadee UI", 18), background="#ffffff")
b_rk2 = tk.Button(frame_rk_opciones, text ="Runge–Kutta 2do orden",height = 6,width=26)
b_rk4 = tk.Button(frame_rk_opciones, text ="Runge–Kutta 4to orden",height = 6,width=26)
b_odeint = tk.Button(frame_rk_opciones, text ="ODEINT",height = 6,width=26)

label_rk.grid(row=0, column=0, sticky="nw", padx=2, pady=2)
#label_odeint.grid(row=0, column=1, sticky="nw", padx=2, pady=2)
b_rk2.grid(row=1, column=0, sticky="nw", padx=2, pady=2)
b_rk4.grid(row=1, column=1,  sticky="nw", padx=2, pady=2)
b_odeint.grid(row=1, column=2, sticky="nw", padx=2, pady=2)

root.mainloop()