from tkinter import *
from tkinter import filedialog
import tkinter as tk
from Main import *

class GUI:
    def __init__(self):
        raiz = tk.Tk()
        frame = Frame(raiz, width=350, height=400)
        raiz.resizable(0, 0)

        # icono
        raiz.iconbitmap(r'./imgs/icon.ico')

        # labels
        label1 = Label(frame, text="Menú del juego", width=100, height=25, font=("", 15), anchor='nw')
        label1.place(x=5, y=5)


        label2 = Label(frame, text="Dimensiones de la patalla", width=100, height=25, font=("", 12), anchor='nw')
        label2.place(x=15, y=50)

        label3 = Label(frame, text="Personalizar tablero:", width=100, height=25, font=("", 12), anchor='nw')
        label3.place(x=15, y=95)

        label4 = Label(frame, text="Dificultad del juego", width=100, height=25, font=("", 12), anchor='nw')
        label4.place(x=15, y=170)

        # combo
        variable = StringVar(raiz)
        variable.set("600 x 400")
        combo = OptionMenu(raiz, variable, "800 x 600", "600 x 400", "400 x 200")
        combo.place(x=240, y=45)


        # botones
        def btn():
            raiz.destroy()
            main(variable.get(), aleatorio, matrizTablero, ancho, alto)

        def personalizar():
            global alto, ancho, variable, aleatorio, matrizTablero
            choosePerso = filedialog.askopenfilename(filetypes=(("Archivos de texto", "*.txt"),))
            if choosePerso != "":
                btnPerso.config(text="☑")
                raiz.update()
                aleatorio = False


                archivo = open(choosePerso, "r")
                tablero = archivo.readline()
                archivo.close()


                alto = math.ceil(len(tablero.split(" "))) * 100
                ancho = math.ceil(len(tablero.split(" ")[0].split(","))) * 100

                matrizTablero = numpy.zeros((alto // 100, ancho // 100))
                j=0
                for x in range(0, alto // 100):
                    matriz = tablero.split(" ")[x]
                    for i in range (0 , len(tablero.split(" ")[0])):
                        if matriz[i] != "[" and matriz[i] != "]" and matriz[i] != ",":
                            matrizTablero[x][j] = float(matriz[i])
                            j += 1
                    j = 0
        btnInicio = Button(frame, text="Inicio", width=20, command=btn)
        btnInicio.place(x=105, y=350)

        btnPerso = Button(frame, text="Seleccionar archivo", width=44,  command=personalizar)
        btnPerso.place(x=15, y=130)

        # radio button
        r1 = Radiobutton(raiz, text="Normal",  value=1)
        r2 = Radiobutton(raiz, text="Dificil",  value=0)
        r1.place(x=240, y=170)
        r2.place(x=240, y=195)

        #dimensiones ventana
        raiz.geometry('{}x{}+{}+{}'.format(350, 400, (raiz.winfo_screenwidth() // 2) - 150, (raiz.winfo_screenheight() // 2) - 200))
        raiz.title("Zelda")
        frame.pack()
        raiz.tk.mainloop()
